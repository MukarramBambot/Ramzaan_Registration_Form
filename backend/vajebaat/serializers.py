"""
Serializers for Vajebaat API endpoints.
"""

from rest_framework import serializers
from .models import (
    VajebaatMember, VajebaatForm, VajebaatAppointment,
    VajebaatDate, VajebaatSlot,
)


class VajebaatMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = VajebaatMember
        fields = [
            'id', 'its_number', 'name', 'mohalla', 'file_no',
            'sector_incharge', 'subsector_incharge', 'mobile',
            'email', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def validate_its_number(self, value):
        value = value.strip()
        if not value.isdigit():
            raise serializers.ValidationError("ITS number must contain digits only.")
        if len(value) not in (7, 8):
            raise serializers.ValidationError("ITS number must be 7 or 8 digits.")
        return value


class PublicMemberSerializer(serializers.ModelSerializer):
    """Restricted serializer for public by_its endpoint. Masks ITS, omits sensitive fields."""
    its_masked = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = VajebaatMember
        fields = ['its_masked', 'name']

    def get_its_masked(self, obj):
        its = obj.its_number or ''
        if len(its) >= 4:
            return '*' * (len(its) - 4) + its[-4:]
        return its


class VajebaatFormSerializer(serializers.ModelSerializer):
    """
    Serializer for Takhmeen form records.
    `total` is read-only — auto-computed in the model's save().
    `amounts` is a helper dict for the frontend print template.
    """
    amounts = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = VajebaatForm
        fields = [
            'id', 'its_number', 'name', 'mohalla', 'file_no',
            'sector', 'sub_sector',
            'zakat', 'khums', 'fitra', 'kaffara',
            'meenat_binyan', 'najwa', 'total',
            'amounts', 'created_at'
        ]
        read_only_fields = ['id', 'total', 'amounts', 'created_at']

    def get_amounts(self, obj):
        """Maps DB field names to keys used by the frontend print template."""
        return {
            'zakaat':  str(obj.zakat),
            'khums':   str(obj.khums),
            'fitrat':  str(obj.fitra),
            'kaffara': str(obj.kaffara),
            'bunyan':  str(obj.meenat_binyan),
            'najwa':   str(obj.najwa),
            'total':   str(obj.total),
        }

    def validate_its_number(self, value):
        value = value.strip()
        if not value.isdigit():
            raise serializers.ValidationError("ITS number must contain digits only.")
        if len(value) not in (7, 8):
            raise serializers.ValidationError("ITS number must be 7 or 8 digits.")
        return value

    def validate(self, data):
        """Ensure no negative Vajebaat amounts."""
        amount_fields = ['zakat', 'khums', 'fitra', 'kaffara', 'meenat_binyan', 'najwa']
        for field in amount_fields:
            val = data.get(field, 0)
            if val is not None and val < 0:
                raise serializers.ValidationError(
                    {field: "Amount cannot be negative."}
                )
        return data


# ============================================================
# NEW: Date & Slot Serializers
# ============================================================

class VajebaatDateSerializer(serializers.ModelSerializer):
    slot_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = VajebaatDate
        fields = ['id', 'date', 'is_active', 'slot_count', 'created_at']
        read_only_fields = ['id', 'slot_count', 'created_at']


class VajebaatSlotSerializer(serializers.ModelSerializer):
    confirmed_count = serializers.IntegerField(read_only=True)
    is_full = serializers.SerializerMethodField(read_only=True)
    date_value = serializers.DateField(source='date.date', read_only=True)

    class Meta:
        model = VajebaatSlot
        fields = [
            'id', 'date', 'date_value', 'slot_number',
            'start_time', 'end_time', 'capacity',
            'confirmed_count', 'is_full', 'is_active',
        ]
        read_only_fields = ['id', 'confirmed_count', 'is_full', 'date_value']

    def get_is_full(self, obj):
        count = getattr(obj, 'confirmed_count', 0) or 0
        return count >= obj.capacity


class VajebaatSlotBriefSerializer(serializers.ModelSerializer):
    """Minimal slot info embedded in appointment responses."""
    date_value = serializers.DateField(source='date.date', read_only=True)

    class Meta:
        model = VajebaatSlot
        fields = ['id', 'slot_number', 'start_time', 'end_time', 'date_value']


# ============================================================
# UPDATED: Appointment Serializers
# ============================================================

class VajebaatAppointmentSerializer(serializers.ModelSerializer):
    slot_info = VajebaatSlotBriefSerializer(source='slot', read_only=True)

    class Meta:
        model = VajebaatAppointment
        fields = [
            'id', 'its_number', 'member', 'name', 'mobile', 'email',
            'preferred_date', 'remarks', 'status',
            'slot', 'slot_info', 'confirmed_at', 'created_at'
        ]
        read_only_fields = [
            'id', 'member', 'confirmed_at', 'created_at'
        ]

    def validate_its_number(self, value):
        value = value.strip()
        if not value.isdigit():
            raise serializers.ValidationError("ITS number must contain digits only.")
        if len(value) not in (7, 8):
            raise serializers.ValidationError("ITS number must be 7 or 8 digits.")
        return value

    def validate_mobile(self, value):
        value = value.strip()
        if value and not value.lstrip('+').isdigit():
            raise serializers.ValidationError("Enter a valid mobile number.")
        return value


class VajebaatAppointmentStatusSerializer(serializers.Serializer):
    """Serializer for the update_status action."""
    status = serializers.ChoiceField(choices=VajebaatAppointment.STATUS_CHOICES)


class AssignSlotSerializer(serializers.Serializer):
    """Serializer for the assign-slot action."""
    slot_id = serializers.IntegerField()

    def validate_slot_id(self, value):
        try:
            slot = VajebaatSlot.objects.get(pk=value)
        except VajebaatSlot.DoesNotExist:
            raise serializers.ValidationError("Slot does not exist.")
        if not slot.date.is_active:
            raise serializers.ValidationError("This date is no longer active.")
        return value


# ============================================================
# Members Directory Serializer (reads from VajebaatAppointment)
# ============================================================

class MembersDirectorySerializer(serializers.ModelSerializer):
    """
    Flat read-only serializer for the admin members directory.
    Sources data from VajebaatAppointment with optional slot info.
    """
    assigned_date = serializers.SerializerMethodField()
    slot_time = serializers.SerializerMethodField()

    class Meta:
        model = VajebaatAppointment
        fields = [
            'id', 'its_number', 'name', 'mobile',
            'preferred_date', 'status',
            'assigned_date', 'slot_time',
            'confirmed_at', 'created_at',
        ]

    def get_assigned_date(self, obj):
        if obj.slot and obj.slot.date:
            return str(obj.slot.date.date)
        return None

    def get_slot_time(self, obj):
        if obj.slot:
            return (
                f"{obj.slot.start_time.strftime('%H:%M')} – "
                f"{obj.slot.end_time.strftime('%H:%M')}"
            )
        return None
# ============================================================
# Public Status Serializer
# ============================================================

class PublicAppointmentStatusSerializer(serializers.ModelSerializer):
    """
    Restricted read-only serializer for public status checks.
    Masks ITS number and only returns non-sensitive fields.
    """
    its_masked = serializers.SerializerMethodField()
    assigned_date = serializers.DateField(source='slot.date.date', read_only=True)
    slot_time = serializers.SerializerMethodField()

    class Meta:
        model = VajebaatAppointment
        fields = [
            'name', 'its_masked', 'status', 
            'assigned_date', 'slot_time', 'created_at'
        ]
        read_only_fields = ['name', 'its_masked', 'status', 'assigned_date', 'slot_time', 'created_at']

    def get_its_masked(self, obj):
        its = obj.its_number or ''
        if len(its) >= 4:
            return '*' * (len(its) - 4) + its[-4:]
        return its

    def get_slot_time(self, obj):
        if obj.slot:
            return (
                f"{obj.slot.start_time.strftime('%H:%M')} – "
                f"{obj.slot.end_time.strftime('%H:%M')}"
            )
        return None
