<?php include '../includes/admin-header.php'; ?>

<!-- Content Wrapper -->
<div class="min-h-screen bg-[#F9F7F7]">
    
    <!-- Header -->
    <div class="bg-[#112D4E] py-5 px-6 shadow-md">
        <div class="flex items-center justify-between">
            <div class="flex items-center gap-4">
                <a href="<?= BASE_URL ?>/admin/vajebaat-appointments.php" class="p-2 rounded-lg bg-white/10 text-white/70 hover:text-white hover:bg-white/20 transition-all">
                    <svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                    </svg>
                </a>
                <div>
                   <h1 class="text-xl md:text-2xl text-white font-normal">
                        Appointment Details
                    </h1>
                    <p id="header-appointment-id" class="text-[#DBE2EF] text-xs font-mono">Loading ID...</p>
                </div>
            </div>
             <div class="flex items-center gap-3 text-[#DBE2EF] text-sm">
                <button onclick="exportDetail('pdf')" class="px-3 py-1.5 rounded-md bg-white/10 hover:bg-white/20 text-white text-xs font-bold transition-all flex items-center gap-2">
                    <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M7.5 12l4.5 4.5m0 0l4.5-4.5M12 3v13.5" />
                    </svg>
                    Download Form
                </button>
                <button onclick="exportDetail('excel')" class="px-3 py-1.5 rounded-md bg-white/10 hover:bg-white/20 text-white text-xs font-bold transition-all flex items-center gap-2">
                    Export
                </button>
                <button onclick="logout()" class="ml-4 px-3 py-1.5 rounded-md bg-red-500/10 hover:bg-red-500/20 text-red-100 text-sm font-medium transition-all">Logout</button>
            </div>
        </div>
    </div>

    <!-- Layout Grid -->
    <div class="p-6">
        <div id="loading-skeleton" class="animate-pulse space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="h-[500px] bg-white rounded-2xl border border-[#DBE2EF]"></div>
                <div class="h-[500px] bg-white rounded-2xl border border-[#DBE2EF]"></div>
            </div>
        </div>

        <div id="detail-container" class="grid grid-cols-1 lg:grid-cols-2 gap-6 hidden">
            
            <!-- Left Side: User Info Form -->
            <div class="space-y-6">
                <div class="bg-white rounded-2xl shadow-sm border border-[#DBE2EF] overflow-hidden">
                    <div class="bg-[#F9FAFB] px-6 py-4 border-b border-[#DBE2EF]">
                        <h3 class="text-xs font-bold text-[#6B7280] uppercase tracking-wider">User Information</h3>
                    </div>
                    <div class="p-6 space-y-4">
                        <div class="grid grid-cols-2 gap-4">
                             <div>
                                <label class="block text-[10px] font-bold text-[#6B7280] uppercase mb-1">ITS Number</label>
                                <input type="text" id="edit-its" class="w-full px-3 py-2 border border-[#DBE2EF] rounded-lg text-sm font-mono text-[#112D4E] outline-none focus:ring-2 focus:ring-[#3F72AF]">
                             </div>
                             <div>
                                <label class="block text-[10px] font-bold text-[#6B7280] uppercase mb-1">Full Name</label>
                                <input type="text" id="edit-name" class="w-full px-3 py-2 border border-[#DBE2EF] rounded-lg text-sm text-[#112D4E] outline-none focus:ring-2 focus:ring-[#3F72AF]">
                             </div>
                        </div>
                        <div class="grid grid-cols-2 gap-4">
                             <div>
                                <label class="block text-[10px] font-bold text-[#6B7280] uppercase mb-1">Mobile</label>
                                <input type="text" id="edit-mobile" class="w-full px-3 py-2 border border-[#DBE2EF] rounded-lg text-sm text-[#112D4E] outline-none focus:ring-2 focus:ring-[#3F72AF]">
                             </div>
                             <div>
                                <label class="block text-[10px] font-bold text-[#6B7280] uppercase mb-1">Email</label>
                                <input type="email" id="edit-email" class="w-full px-3 py-2 border border-[#DBE2EF] rounded-lg text-sm text-[#112D4E] outline-none focus:ring-2 focus:ring-[#3F72AF]">
                             </div>
                        </div>
                        <hr class="border-[#DBE2EF]">
                        <div class="grid grid-cols-2 gap-4">
                             <div>
                                <label class="block text-[10px] font-bold text-[#6B7280] uppercase mb-1">Preferred Date</label>
                                <input type="date" id="edit-pref-date" class="w-full px-3 py-2 border border-[#DBE2EF] rounded-lg text-sm text-[#112D4E] outline-none focus:ring-2 focus:ring-[#3F72AF]">
                             </div>
                             <div>
                                <label class="block text-[10px] font-bold text-[#6B7280] uppercase mb-1">Created At</label>
                                <p id="val-created" class="text-xs text-[#6B7280] py-2">...</p>
                             </div>
                        </div>
                        <div>
                            <label class="block text-[10px] font-bold text-[#6B7280] uppercase mb-1">Remarks</label>
                            <textarea id="edit-remarks" rows="3" class="w-full px-3 py-2 border border-[#DBE2EF] rounded-lg text-sm text-[#112D4E] outline-none focus:ring-2 focus:ring-[#3F72AF] resize-none"></textarea>
                        </div>
                        <div class="pt-4 flex justify-end">
                             <button onclick="saveAppointment()" class="px-6 py-2.5 bg-[#112D4E] text-white rounded-xl font-bold text-sm shadow-md hover:bg-[#3F72AF] transition-all flex items-center gap-2">
                                <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                                </svg>
                                Save Changes
                             </button>
                        </div>
                    </div>
                </div>

                <!-- Current Assignment -->
                <div id="current-slot-info" class="bg-blue-50/50 rounded-2xl border border-blue-100 p-6 hidden">
                    <div class="flex items-center gap-4">
                         <div class="w-12 h-12 bg-[#3F72AF] rounded-xl flex items-center justify-center text-white shadow-lg">
                            <svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                         </div>
                         <div class="flex-grow">
                             <div class="flex items-center justify-between mb-1">
                                 <h4 class="text-xs font-bold text-[#3F72AF] uppercase tracking-widest">Confirmed Slot</h4>
                                 <span id="badge-status" class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-[#3F72AF] text-white">CONFIRMED</span>
                             </div>
                             <p id="val-confirmed-slot" class="text-lg font-bold text-[#112D4E]">Loading...</p>
                             <p id="val-confirmed-date" class="text-sm text-[#6B7280]">Loading...</p>
                         </div>
                    </div>
                </div>
            </div>

            <!-- Right Side: Admin Controls -->
            <div class="space-y-6">
                <!-- Status Control -->
                <div class="bg-white rounded-2xl shadow-sm border border-[#DBE2EF] overflow-hidden">
                    <div class="bg-[#F9FAFB] px-6 py-4 border-b border-[#DBE2EF]">
                        <h3 class="text-xs font-bold text-[#6B7280] uppercase tracking-wider">Appointment Lifecycle</h3>
                    </div>
                    <div class="p-6 space-y-6">
                        <div id="assign-area" class="space-y-6">
                             <div class="space-y-3">
                                <label class="block text-xs font-bold text-[#6B7280] uppercase tracking-wider">Assign / Reschedule Slot</label>
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                                    <input type="text" id="slot-date-picker" placeholder="Select Date" class="w-full h-12 px-4 rounded-xl border border-[#DBE2EF] outline-none focus:ring-2 focus:ring-[#3F72AF] text-sm">
                                    <button onclick="loadSlotsForDate()" class="h-12 bg-[#3F72AF] text-white rounded-xl font-bold text-sm shadow-md hover:bg-[#112D4E] transition-all">Check Slots</button>
                                </div>
                             </div>

                             <div id="slot-grid" class="grid grid-cols-2 gap-2 max-h-[300px] overflow-y-auto custom-scrollbar p-1">
                                <!-- Slots injected here -->
                                <p class="col-span-full text-center py-8 text-sm text-[#9CA3AF]">Pick a date to see available slots</p>
                             </div>
                        </div>

                        <hr class="border-[#DBE2EF]">

                        <div class="flex flex-wrap gap-3">
                             <button id="btn-complete" onclick="updateAptStatus('COMPLETED')" class="grow px-4 py-3 rounded-xl bg-green-500 text-white font-bold text-sm shadow-md hover:bg-green-600 transition-all active:scale-95 disabled:opacity-50">Mark Completed</button>
                             <button id="btn-cancel" onclick="updateAptStatus('CANCELLED')" class="grow px-4 py-3 rounded-xl bg-red-50 text-red-600 border border-red-200 font-bold text-sm hover:bg-red-100 transition-all active:scale-95 disabled:opacity-50">Cancel Booking</button>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </div>

</div>

<!-- Flatpickr CSS & JS -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css">
<script src="https://cdn.jsdelivr.net/npm/flatpickr"></script>

<script src="<?= BASE_URL ?>/assets/js/main.js"></script>
<?php include '../includes/footer.php'; ?>

<script>
    const appointmentId = new URLSearchParams(window.location.search).get('id');
    let appointment = null;
    let picker = null;

    document.addEventListener('DOMContentLoaded', () => {
        if (!localStorage.getItem('access_token')) {
            window.location.href = (window.BASE_URL || '') + '/admin/login.php';
            return;
        }
        if (!appointmentId) {
            window.location.href = (window.BASE_URL || '') + '/admin/vajebaat-appointments.php';
            return;
        }

        picker = flatpickr("#slot-date-picker", {
            dateFormat: "Y-m-d",
            minDate: "today",
            altInput: true,
            altFormat: "F j, Y",
            onChange: loadSlotsForDate
        });

        loadAppointmentDetail();
    });

    async function loadAppointmentDetail() {
        try {
            const response = await apiFetch(`/api/vajebaat/appointments/${appointmentId}/`, { requireAuth: true });
            if (!response.ok) throw new Error('Appointment not found');
            appointment = await response.json();
            renderAppointmentDetail();
        } catch (err) {
            alert(err.message);
            window.location.href = (window.BASE_URL || '') + '/admin/vajebaat-appointments.php';
        }
    }

    function renderAppointmentDetail() {
        document.getElementById('header-appointment-id').textContent = `ID: ${appointment.id} | Status: ${appointment.status}`;
        
        document.getElementById('edit-its').value = appointment.its_number || '';
        document.getElementById('edit-name').value = appointment.name || '';
        document.getElementById('edit-mobile').value = appointment.mobile || '';
        document.getElementById('edit-email').value = appointment.email || '';
        document.getElementById('edit-pref-date').value = appointment.preferred_date || '';
        document.getElementById('edit-remarks').value = appointment.remarks || '';
        
        document.getElementById('val-created').textContent = new Date(appointment.created_at).toLocaleString();

        const currentSlotInfo = document.getElementById('current-slot-info');
        if (appointment.slot_info) {
            currentSlotInfo.classList.remove('hidden');
            document.getElementById('val-confirmed-slot').textContent = `${appointment.slot_info.start_time.substring(0,5)} – ${appointment.slot_info.end_time.substring(0,5)}`;
            document.getElementById('val-confirmed-date').textContent = new Date(appointment.slot_info.date_value).toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });
            
            const badge = document.getElementById('badge-status');
            badge.textContent = appointment.status;
            if (appointment.status === 'RESCHEDULED') badge.className = 'px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-500 text-white';
            else if (appointment.status === 'COMPLETED') badge.className = 'px-2 py-0.5 rounded-full text-[10px] font-bold bg-blue-500 text-white';
            else if (appointment.status === 'CANCELLED') badge.className = 'px-2 py-0.5 rounded-full text-[10px] font-bold bg-red-500 text-white';
            else badge.className = 'px-2 py-0.5 rounded-full text-[10px] font-bold bg-[#3F72AF] text-white';
        } else {
            currentSlotInfo.classList.add('hidden');
        }

        // Action buttons
        document.getElementById('btn-complete').disabled = (appointment.status === 'COMPLETED' || appointment.status === 'CANCELLED');
        document.getElementById('btn-cancel').disabled = (appointment.status === 'CANCELLED');

        document.getElementById('loading-skeleton').classList.add('hidden');
        document.getElementById('detail-container').classList.remove('hidden');
    }

    async function loadSlotsForDate() {
        const date = document.getElementById('slot-date-picker').value;
        const grid = document.getElementById('slot-grid');
        if (!date) return;

        grid.innerHTML = '<div class="col-span-full py-8 text-center text-sm text-[#6B7280]">Searching slots...</div>';

        try {
            // Find the date ID first? No, we filter slots by date string via backend if we add support, 
            // but currently slots API takes date_id. Let's find date_id from dates list.
            const datesResp = await apiFetch('/api/vajebaat/dates/', { requireAuth: true });
            const dates = await datesResp.json();
            const dateObj = dates.find(d => d.date === date);
            
            if (!dateObj) {
                grid.innerHTML = '<div class="col-span-full py-8 text-center text-sm text-red-500">This date is not configured for Vajebaat.</div>';
                return;
            }

            const slotsResp = await apiFetch(`/api/vajebaat/slots/?date_id=${dateObj.id}`, { requireAuth: true });
            const slots = await slotsResp.json();

            if (slots.length === 0) {
                grid.innerHTML = '<div class="col-span-full py-8 text-center text-sm text-red-500">No slots configured for this date.</div>';
                return;
            }

            grid.innerHTML = slots.map(s => {
                const count = s.confirmed_count || 0;
                const cap = s.capacity || 10;
                const isFull = count >= cap;
                const isCurrent = appointment.slot === s.id;
                
                const btnClass = isCurrent 
                    ? 'border-2 border-[#112D4E] bg-[#112D4E]/5 text-[#112D4E]' 
                    : isFull 
                        ? 'border border-red-200 bg-red-50 text-red-500 opacity-60 cursor-not-allowed' 
                        : 'border border-[#DBE2EF] hover:border-[#3F72AF] text-[#112D4E]';

                return `
                    <button ${isFull || isCurrent ? 'disabled' : ''} onclick="assignSlot(${s.id})" 
                            class="p-3 rounded-xl transition-all flex flex-col items-center gap-1 ${btnClass}">
                        <span class="text-xs font-bold font-mono">${s.start_time.substring(0,5)}–${s.end_time.substring(0,5)}</span>
                        <span class="text-[10px] uppercase font-bold tracking-tighter opacity-70">${count}/${cap} Occupied</span>
                        ${isCurrent ? '<span class="text-[8px] font-bold uppercase mt-1">Current</span>' : ''}
                    </button>
                `;
            }).join('');

        } catch (err) {
            grid.innerHTML = `<div class="col-span-full py-8 text-center text-sm text-red-500">${err.message}</div>`;
        }
    }

    async function assignSlot(slotId) {
        if (!confirm('Assign this slot to the user?')) return;
        
        const endpoint = appointment.slot ? 'reschedule' : 'assign-slot';
        const method = appointment.slot ? 'PATCH' : 'POST';

        try {
            const response = await apiFetch(`/api/vajebaat/appointments/${appointmentId}/${endpoint}/`, {
                method: method,
                requireAuth: true,
                body: JSON.stringify({ slot_id: slotId }),
                headers: { 'Content-Type': 'application/json' }
            });
            if (response.ok) {
                alert('Slot assigned successfully!');
                loadAppointmentDetail();
                loadSlotsForDate();
            } else {
                const error = await response.json();
                alert(error.detail || 'Failed to assign slot.');
            }
        } catch (err) {
            alert('Error connecting to server.');
        }
    }

    async function updateAptStatus(status) {
        if (!confirm(`Are you sure you want to mark this as ${status}?`)) return;

        try {
            const endpoint = status === 'CANCELLED' ? 'cancel' : 'update_status';
            const response = await apiFetch(`/api/vajebaat/appointments/${appointmentId}/${endpoint}/`, {
                method: 'PATCH',
                requireAuth: true,
                body: JSON.stringify({ status: status }),
                headers: { 'Content-Type': 'application/json' }
            });
            if (response.ok) {
                loadAppointmentDetail();
            } else {
                alert('Failed to update status.');
            }
        } catch (err) {
            alert('Error connecting to server.');
        }
    }

    async function saveAppointment() {
        const payload = {
            its_number: document.getElementById('edit-its').value,
            name: document.getElementById('edit-name').value,
            mobile: document.getElementById('edit-mobile').value,
            email: document.getElementById('edit-email').value,
            preferred_date: document.getElementById('edit-pref-date').value,
            remarks: document.getElementById('edit-remarks').value
        };

        try {
            const response = await apiFetch(`/api/vajebaat/appointments/${appointmentId}/`, {
                method: 'PATCH',
                requireAuth: true,
                body: JSON.stringify(payload),
                headers: { 'Content-Type': 'application/json' }
            });

            if (response.ok) {
                alert('Changes saved successfully!');
                loadAppointmentDetail();
            } else {
                alert('Failed to save changes.');
            }
        } catch (err) {
            alert('Error connecting to server.');
        }
    }

    function exportDetail(format) {
        if (format === 'pdf') {
            window.location.href = window.API_BASE + `/api/vajebaat/appointments/${appointmentId}/export-pdf/`;
        } else {
            // excel - uses existing csv export with filter
            window.location.href = window.API_BASE + `/api/vajebaat/export-csv/?id=${appointmentId}`;
        }
    }

    function logout() {
        localStorage.clear();
        window.location.href = (window.BASE_URL || '') + '/admin/login.php';
    }
</script>
