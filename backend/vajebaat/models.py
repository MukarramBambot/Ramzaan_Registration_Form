"""
Models for Vajebaat (Takhmeen) Management.
Completely separate from the registrations app models.
"""

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date, time
from django.core.exceptions import ValidationError


# ============================================================
# VAJEBAAT SCHEDULE CONSTANTS
# ============================================================
MAX_VAJEBAAT_DATE = date(2026, 3, 18)


# ============================================================
# DEFAULT SLOT TIMES — 8 fixed daily slots
# ============================================================
DEFAULT_SLOT_TIMES = [
    (1, time(10, 0), time(10, 15)),
    (2, time(10, 15), time(10, 30)),
    (3, time(10, 30), time(10, 45)),
    (4, time(10, 45), time(11, 0)),
    (5, time(11, 0), time(11, 15)),
    (6, time(11, 15), time(11, 30)),
    (7, time(11, 30), time(11, 45)),
    (8, time(11, 45), time(12, 0)),
]


class VajebaatMember(models.Model):
    """
    Vajebaat member directory.
    Stores member details for Takhmeen form generation.
    """
    its_number = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    mohalla = models.CharField(max_length=255, blank=True, default='')
    file_no = models.CharField(max_length=50, blank=True, default='')
    sector_incharge = models.CharField(max_length=255, blank=True, default='')
    subsector_incharge = models.CharField(max_length=255, blank=True, default='')
    mobile = models.CharField(max_length=20, blank=True, default='')
    email = models.EmailField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Vajebaat Member'
        verbose_name_plural = 'Vajebaat Members'

    def __str__(self):
        return f"{self.name} ({self.its_number})"


class VajebaatForm(models.Model):
    """
    Takhmeen form records.
    Stores submitted Vajebaat amounts for each member.
    """
    its_number = models.CharField(max_length=20, db_index=True)
    name = models.CharField(max_length=255, blank=True, default='')
    mohalla = models.CharField(max_length=255, blank=True, default='')
    file_no = models.CharField(max_length=50, blank=True, default='')
    sector = models.CharField(max_length=255, blank=True, default='')
    sub_sector = models.CharField(max_length=255, blank=True, default='')
    zakat = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    khums = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fitra = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    kaffara = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    meenat_binyan = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    najwa = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Vajebaat Form'
        verbose_name_plural = 'Vajebaat Forms'

    def __str__(self):
        return f"Takhmeen - {self.its_number} ({self.name})"

    def save(self, *args, **kwargs):
        """Auto-calculate total before save."""
        self.total = (
            self.zakat + self.khums + self.fitra +
            self.kaffara + self.meenat_binyan + self.najwa
        )
        super().save(*args, **kwargs)


# ============================================================
# NEW: VajebaatDate — Active appointment dates
# ============================================================
class VajebaatDate(models.Model):
    """
    Represents a date on which Vajebaat appointments can be scheduled.
    Slots are auto-created when a new date is saved.
    """
    date = models.DateField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']
        verbose_name = 'Vajebaat Date'
        verbose_name_plural = 'Vajebaat Dates'

    def __str__(self):
        return str(self.date)

    def clean(self):
        """Restrict dates to the allowed Ramzaan window."""
        if self.date and self.date > MAX_VAJEBAAT_DATE:
            raise ValidationError(
                f"Vajebaat appointments are only allowed until {MAX_VAJEBAAT_DATE}."
            )
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


# ============================================================
# NEW: VajebaatSlot — Time slot within a date
# ============================================================
class VajebaatSlot(models.Model):
    """
    Individual time slot for a given date.
    8 slots per date, each with configurable capacity (default 10).
    """
    date = models.ForeignKey(
        VajebaatDate,
        on_delete=models.CASCADE,
        related_name='slots'
    )
    slot_number = models.PositiveIntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.PositiveIntegerField(default=10)

    class Meta:
        ordering = ['date', 'slot_number']
        unique_together = ('date', 'slot_number')
        verbose_name = 'Vajebaat Slot'
        verbose_name_plural = 'Vajebaat Slots'

    def __str__(self):
        return (
            f"Slot {self.slot_number} | {self.date.date} | "
            f"{self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')}"
        )



# ============================================================
# UPDATED: VajebaatAppointment — Extended with slot FK
# ============================================================
class VajebaatAppointment(models.Model):
    """
    Vajebaat appointment bookings.
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    its_number = models.CharField(max_length=20, db_index=True)
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20, blank=True, default='')
    preferred_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    # NEW fields
    slot = models.ForeignKey(
        VajebaatSlot,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointments'
    )
    confirmed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Vajebaat Appointment'
        verbose_name_plural = 'Vajebaat Appointments'

    def __str__(self):
        return f"Appointment - {self.name} ({self.its_number})"


# ============================================================
# Signal: Auto-create 8 slots when a VajebaatDate is created
# ============================================================
@receiver(post_save, sender=VajebaatDate)
def create_default_slots(sender, instance, created, **kwargs):
    """
    When a new VajebaatDate is created, auto-generate the 8 default time slots.
    """
    if created:
        slots = [
            VajebaatSlot(
                date=instance,
                slot_number=num,
                start_time=start,
                end_time=end,
            )
            for num, start, end in DEFAULT_SLOT_TIMES
        ]
        VajebaatSlot.objects.bulk_create(slots)
