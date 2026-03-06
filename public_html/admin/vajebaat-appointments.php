<?php include '../includes/admin-header.php'; ?>

<!-- Content Wrapper -->
<div class="min-h-screen bg-[#F9F7F7]">
    
    <!-- Header -->
    <div class="bg-[#112D4E] py-5 px-6 shadow-md">
        <div class="flex items-center justify-between">
            <div>
                <div class="flex flex-col md:flex-row md:items-center gap-2 md:gap-6 mb-1">
                    <h1 class="text-xl md:text-2xl text-white font-normal">
                        Vajebaat Appointments
                    </h1>
                    <div class="flex items-center gap-2 mt-2 md:mt-0 md:ml-4 overflow-x-auto pb-2 md:pb-0">
                        <a href="<?= BASE_URL ?>/admin/dashboard.php" class="whitespace-nowrap px-3 py-1.5 rounded-md text-[#DBE2EF] hover:text-white hover:bg-white/10 text-sm font-medium transition-all flex items-center gap-2">
                            <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line></svg>
                            Registration
                        </a>
                        <span class="text-[#DBE2EF]/30 mx-1">|</span>
                        <a href="<?= BASE_URL ?>/admin/vajebaat-appointments.php" class="whitespace-nowrap px-3 py-1.5 rounded-md bg-[#3F72AF] text-white text-sm font-medium flex items-center gap-2">
                            <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                            Appointments
                        </a>
                        <a href="<?= BASE_URL ?>/admin/vajebaat-slots.php" class="whitespace-nowrap px-3 py-1.5 rounded-md text-[#DBE2EF] hover:text-white hover:bg-white/10 text-sm font-medium transition-all flex items-center gap-2">
                            <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                            Slots
                        </a>
                        <a href="<?= BASE_URL ?>/admin/vajebaat-members.php" class="whitespace-nowrap px-3 py-1.5 rounded-md text-[#DBE2EF] hover:text-white hover:bg-white/10 text-sm font-medium transition-all flex items-center gap-2">
                            <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M22 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
                            Members
                        </a>
                    </div>
                </div>
                <p class="text-[#DBE2EF] text-sm font-light">
                    Vajebaat Appointment Management – Sherullah 1447H
                </p>
            </div>
             <div class="flex items-center gap-3 text-[#DBE2EF] text-sm">
                <button
                    id="refresh-btn"
                    onclick="loadAppointments()"
                    class="px-3 py-1.5 rounded-md bg-white/10 hover:bg-white/20 text-white text-sm font-medium transition-all flex items-center gap-2"
                    title="Refresh Data"
                >
                    <span id="refresh-icon"></span>
                    <span>Refresh</span>
                </button>
                <div class="flex items-center gap-2 ml-4">
                    <button onclick="exportData('excel')" class="px-3 py-1.5 rounded-md bg-green-600 hover:bg-green-700 text-white text-xs font-bold transition-all shadow-sm flex items-center gap-2">
                         <svg class="w-3 h-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M7.5 12l4.5 4.5m0 0l4.5-4.5M12 3v13.5" />
                        </svg>
                        Excel
                    </button>
                    <button onclick="exportData('pdf')" class="px-3 py-1.5 rounded-md bg-red-600 hover:bg-red-700 text-white text-xs font-bold transition-all shadow-sm flex items-center gap-2">
                         <svg class="w-3 h-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M7.5 12l4.5 4.5m0 0l4.5-4.5M12 3v13.5" />
                        </svg>
                        PDF
                    </button>
                </div>
                <button
                    onclick="logout()"
                    class="ml-4 px-3 py-1.5 rounded-md bg-red-500/10 hover:bg-red-500/20 text-red-100 text-sm font-medium transition-all"
                >
                    Logout
                </button>
            </div>
        </div>
    </div>

    <!-- Stats Bar -->
    <div id="stats-bar" class="bg-white border-b border-[#DBE2EF] px-6 py-3 hidden">
        <div class="flex flex-wrap gap-6 text-sm">
            <div class="flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-[#3F72AF]"></span>
                <span class="text-[#6B7280]">Total:</span>
                <span id="stat-total" class="font-bold text-[#112D4E]">—</span>
            </div>
            <div class="flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-amber-400"></span>
                <span class="text-[#6B7280]">Pending:</span>
                <span id="stat-pending" class="font-bold text-amber-600">—</span>
            </div>
            <div class="flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-green-400"></span>
                <span class="text-[#6B7280]">Confirmed Today:</span>
                <span id="stat-confirmed" class="font-bold text-green-600">—</span>
            </div>
            <div class="flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-blue-400"></span>
                <span class="text-[#6B7280]">Available Slots Today:</span>
                <span id="stat-available" class="font-bold text-blue-600">—</span>
            </div>
        </div>
    </div>

    <!-- Main Content -->
    <div class="p-6">
        <div class="bg-white rounded-xl shadow-sm border border-[#DBE2EF] overflow-hidden">
            <div class="responsive-table-container custom-scrollbar">
                <table class="w-full text-left border-collapse">
                    <thead class="bg-[#F9FAFB] border-b border-[#DBE2EF]">
                        <tr>
                            <th class="px-6 py-4 text-xs font-bold text-[#6B7280] uppercase tracking-wider">ITS Number</th>
                            <th class="px-6 py-4 text-xs font-bold text-[#6B7280] uppercase tracking-wider">Name</th>
                            <th class="px-6 py-4 text-xs font-bold text-[#6B7280] uppercase tracking-wider">Mobile</th>
                            <th class="px-6 py-4 text-xs font-bold text-[#6B7280] uppercase tracking-wider">Preferred Date</th>
                            <th class="px-6 py-4 text-xs font-bold text-[#6B7280] uppercase tracking-wider">Status</th>
                            <th class="px-6 py-4 text-xs font-bold text-[#6B7280] uppercase tracking-wider">Slot</th>
                            <th class="px-6 py-4 text-xs font-bold text-[#6B7280] uppercase tracking-wider">Actions</th>
                        </tr>
                    </thead>
                    <tbody id="appointments-table-body" class="divide-y divide-[#DBE2EF]">
                        <tr>
                            <td colspan="7" class="px-6 py-12 text-center text-[#9CA3AF]">
                                <div class="flex flex-col items-center">
                                    <div id="initial-loader" class="mb-4"></div>
                                    <p>Loading appointments...</p>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

</div>

<!-- Slot Assignment Modal -->
<div id="slot-modal-backdrop" class="fixed inset-0 z-[9998] hidden">
    <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" onclick="closeSlotModal()"></div>
    <div class="absolute inset-0 flex items-center justify-center p-4">
        <div class="relative bg-white w-full max-w-lg rounded-2xl shadow-2xl overflow-hidden transform transition-all" id="slot-modal-content">
            <!-- Modal Header -->
            <div class="bg-[#112D4E] px-6 py-4 flex items-center justify-between">
                <h3 id="slot-modal-title" class="text-lg font-bold text-white">Assign Appointment Slot</h3>
                <button onclick="closeSlotModal()" class="p-1 rounded-lg hover:bg-white/10 text-white/60 hover:text-white transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>
            </div>

            <!-- User Info -->
            <div class="px-6 py-4 bg-[#F9FAFB] border-b border-[#DBE2EF]">
                <div class="flex items-center gap-3">
                    <div class="bg-[#3F72AF]/10 p-2 rounded-full">
                        <svg class="w-5 h-5 text-[#3F72AF]" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-3-3.87"></path><path d="M4 21v-2a4 4 0 0 1 3-3.87"></path><circle cx="12" cy="7" r="4"></circle></svg>
                    </div>
                    <div>
                        <p id="modal-user-name" class="font-bold text-[#112D4E]"></p>
                        <p id="modal-user-its" class="text-xs text-[#6B7280]"></p>
                    </div>
                </div>
                <p class="text-xs text-[#6B7280] mt-2">Preferred Date: <span id="modal-pref-date" class="font-medium text-[#112D4E]"></span></p>
            </div>

            <!-- Date Selector (Flatpickr Calendar) -->
            <div class="px-6 py-3 border-b border-[#DBE2EF]">
                <label class="block text-xs font-bold text-[#6B7280] uppercase mb-2">Select Date</label>
                <input type="text" id="modal-date-picker" placeholder="Pick an appointment date..." readonly
                       class="w-full px-3 py-2 rounded-lg border border-[#DBE2EF] text-sm text-[#112D4E] focus:ring-2 focus:ring-[#3F72AF] focus:border-transparent outline-none cursor-pointer bg-white" />
            </div>

            <!-- Slot Grid -->
            <div class="px-6 py-4">
                <label class="block text-xs font-bold text-[#6B7280] uppercase mb-3">Available Slots</label>
                <div id="slot-grid" class="grid grid-cols-2 gap-3">
                    <p class="col-span-2 text-center text-[#9CA3AF] text-sm py-4">Select a date first</p>
                </div>
            </div>

            <!-- Modal Footer -->
            <div class="px-6 py-4 bg-[#F9FAFB] border-t border-[#DBE2EF] flex justify-end">
                <button onclick="closeSlotModal()" class="px-4 py-2 rounded-lg border border-gray-200 text-gray-600 text-sm font-medium hover:bg-white transition-all mr-2">
                    Cancel
                </button>
            </div>
        </div>
    </div>
</div>

<!-- Flatpickr CSS & JS -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/flatpickr/dist/themes/airbnb.css">
<script src="https://cdn.jsdelivr.net/npm/flatpickr"></script>

<script src="<?= BASE_URL ?>/assets/js/main.js"></script>
<?php include '../includes/footer.php'; ?>

<script>
    // ============================================================
    // State
    // ============================================================
    let currentAppointmentId = null;
    let currentModalMode = 'assign'; // 'assign' or 'reschedule'
    let datePickerInstance = null;
    let dateIdMap = {};  // { '2026-03-15': 1, '2026-03-16': 2, ... }

    // ============================================================
    // Init
    // ============================================================
    document.addEventListener('DOMContentLoaded', () => {
        const refreshIcon = document.getElementById('refresh-icon');
        const initialLoader = document.getElementById('initial-loader');
        
        if (refreshIcon) refreshIcon.innerHTML = ICONS.loader2.replace('animate-spin', '').replace('<svg', '<svg class="w-4 h-4"');
        if (initialLoader) initialLoader.innerHTML = ICONS.loader2;
        
        // Auth check
        if (!localStorage.getItem('access_token')) {
            window.location.href = (window.BASE_URL || '') + '/admin/login.php';
            return;
        }

        loadAppointments();
        loadDashboardStats();
    });

    // ============================================================
    // Dashboard Stats
    // ============================================================
    async function loadDashboardStats() {
        try {
            const response = await apiFetch('/api/vajebaat/dashboard-stats/', { requireAuth: true });
            if (response.ok) {
                const data = await response.json();
                document.getElementById('stat-total').textContent = data.total_appointments;
                document.getElementById('stat-pending').textContent = data.pending;
                document.getElementById('stat-confirmed').textContent = data.confirmed_today;
                document.getElementById('stat-available').textContent = data.available_slots_today;
                document.getElementById('stats-bar').classList.remove('hidden');
            }
        } catch (err) {
            console.error('Failed to load stats:', err);
        }
    }

    // ============================================================
    // Load Appointments
    // ============================================================
    async function loadAppointments() {
        const tbody = document.getElementById('appointments-table-body');
        const refreshBtn = document.getElementById('refresh-btn');
        const refreshIcon = document.getElementById('refresh-icon');
        const statsBar = document.getElementById('stats-bar');
        
        if (refreshIcon) {
            refreshIcon.innerHTML = ICONS.loader2.replace('<svg', '<svg class="w-4 h-4"');
            refreshBtn.disabled = true;
        }

        try {
            // NOTE: Currently loads all appointments. 
            // Future improvement: Add pagination (?page=1) and search query params.
            const response = await apiFetch('/api/vajebaat/appointments/', {
                requireAuth: true
            });

            if (!response.ok) {
                if (response.status === 401 || response.status === 403) return;
                throw new Error(`Error ${response.status}: Failed to fetch data`);
            }

            const data = await response.json();
            const appointments = data.results || data;
            renderAppointmentsTable(appointments);
            loadDashboardStats();

        } catch (err) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="px-6 py-12 text-center text-red-500">
                        <p class="font-medium">Failed to load appointments</p>
                        <p class="text-xs mt-1">${err.message}</p>
                    </td>
                </tr>
            `;
        } finally {
            if (refreshIcon) {
                refreshIcon.innerHTML = ICONS.loader2.replace('animate-spin', '').replace('<svg', '<svg class="w-4 h-4"');
                refreshBtn.disabled = false;
            }
        }
    }

    // ============================================================
    // Render Table
    // ============================================================
    function renderAppointmentsTable(data) {
        const tbody = document.getElementById('appointments-table-body');
        
        if (!data || data.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="px-6 py-12 text-center text-[#9CA3AF]">
                        No appointments found.
                    </td>
                </tr>
            `;
            return;
        }

        tbody.innerHTML = data.map(apt => {
            const statusBadge = getStatusBadge(apt.status);
            const slotDisplay = apt.slot_info
                ? `<span class="text-xs font-mono text-[#3F72AF]">${apt.slot_info.start_time?.substring(0,5)}–${apt.slot_info.end_time?.substring(0,5)}</span><br><span class="text-[10px] text-[#6B7280]">${apt.slot_info.date_value || ''}</span>`
                : '<span class="text-xs text-[#9CA3AF]">—</span>';
            
            const actionBtns = buildActionButtons(apt);

            return `
                <tr class="hover:bg-[#F9FAFB] transition-colors">
                    <td class="px-6 py-4 text-[#3F72AF] font-mono text-sm">${apt.its_number || ''}</td>
                    <td class="px-6 py-4 text-[#112D4E] font-medium">${apt.name || ''}</td>
                    <td class="px-6 py-4 text-sm text-[#6B7280]">${apt.mobile || ''}</td>
                    <td class="px-6 py-4 text-sm text-[#112D4E]">${apt.preferred_date ? new Date(apt.preferred_date).toLocaleDateString('en-GB') : ''}</td>
                    <td class="px-6 py-4">${statusBadge}</td>
                    <td class="px-6 py-4">${slotDisplay}</td>
                    <td class="px-6 py-4">${actionBtns}</td>
                </tr>
            `;
        }).join('');
    }

    function getStatusBadge(status) {
        const styles = {
            'CONFIRMED': 'bg-green-100 text-green-700',
            'RESCHEDULED': 'bg-amber-100 text-amber-700',
            'PENDING':   'bg-amber-100 text-amber-700',
            'CANCELLED': 'bg-red-100 text-red-700',
            'COMPLETED': 'bg-blue-100 text-blue-700',
        };
        const cls = styles[(status || '').toUpperCase()] || 'bg-gray-100 text-gray-700';
        return `<span class="px-2 py-1 rounded-full text-[10px] font-bold tracking-wider uppercase ${cls}">${status || 'PENDING'}</span>`;
    }

    // ============================================================
    // Action Buttons Builder
    // ============================================================
    function buildActionButtons(apt) {
        const esc = (s) => (s || '').replace(/'/g, "\\'");
        if (apt.status === 'PENDING') {
            return `
                <a href="vajebaat-appointment-detail.php?id=${apt.id}" class="px-3 py-1.5 rounded-lg bg-white border border-[#DBE2EF] hover:bg-gray-50 text-[#112D4E] text-xs font-bold transition-all shadow-sm">View</a>
                <button onclick="openSlotModal(${apt.id}, '${esc(apt.name)}', '${apt.its_number}', '${apt.preferred_date || ''}', 'assign')" class="ml-1 px-3 py-1.5 rounded-lg bg-[#3F72AF] hover:bg-[#2D5A8F] text-white text-xs font-bold transition-all shadow-sm">Assign</button>
                <button onclick="cancelAppointment(${apt.id}, '${esc(apt.name)}')" class="ml-1 px-3 py-1.5 rounded-lg bg-red-50 hover:bg-red-100 text-red-600 text-xs font-bold transition-all border border-red-200">Cancel</button>
            `;
        }
        if (apt.status === 'CONFIRMED' || apt.status === 'RESCHEDULED') {
            return `
                <a href="vajebaat-appointment-detail.php?id=${apt.id}" class="px-3 py-1.5 rounded-lg bg-white border border-[#DBE2EF] hover:bg-gray-50 text-[#112D4E] text-xs font-bold transition-all shadow-sm">View</a>
                <button onclick="openSlotModal(${apt.id}, '${esc(apt.name)}', '${apt.its_number}', '${apt.preferred_date || ''}', 'reschedule')" class="ml-1 px-3 py-1.5 rounded-lg bg-amber-50 hover:bg-amber-100 text-amber-700 text-xs font-bold transition-all border border-amber-200">Reschedule</button>
                <button onclick="cancelAppointment(${apt.id}, '${esc(apt.name)}')" class="ml-1 px-3 py-1.5 rounded-lg bg-red-50 hover:bg-red-100 text-red-600 text-xs font-bold transition-all border border-red-200">Cancel</button>
            `;
        }
        if (apt.status === 'CANCELLED') {
            return `<span class="text-xs text-red-400 font-medium">✕ Cancelled</span>`;
        }
        return '';
    }

    // ============================================================
    // Slot Modal (Flatpickr Calendar)
    // ============================================================
    async function openSlotModal(appointmentId, name, its, prefDate, mode = 'assign') {
        currentAppointmentId = appointmentId;
        currentModalMode = mode;

        // Update modal title
        const title = document.getElementById('slot-modal-title');
        title.textContent = mode === 'reschedule' ? 'Reschedule Appointment Slot' : 'Assign Appointment Slot';

        document.getElementById('modal-user-name').textContent = name;
        document.getElementById('modal-user-its').textContent = `ITS: ${its}`;
        document.getElementById('modal-pref-date').textContent = prefDate
            ? new Date(prefDate).toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' })
            : 'Not specified';

        // Reset picker & grid
        const pickerEl = document.getElementById('modal-date-picker');
        pickerEl.value = '';
        document.getElementById('slot-grid').innerHTML = '<p class="col-span-2 text-center text-[#9CA3AF] text-sm py-4">Pick a date on the calendar</p>';

        // Show modal
        document.getElementById('slot-modal-backdrop').classList.remove('hidden');
        document.body.classList.add('modal-open');

        // Initialize Flatpickr with allowed dates and highlight preferred date
        await initDatePicker(prefDate);
    }

    function closeSlotModal() {
        document.getElementById('slot-modal-backdrop').classList.add('hidden');
        document.body.classList.remove('modal-open');
        currentAppointmentId = null;
        // Destroy picker instance
        if (datePickerInstance) {
            datePickerInstance.destroy();
            datePickerInstance = null;
        }
    }

    async function initDatePicker(prefDate = null) {
        const pickerEl = document.getElementById('modal-date-picker');
        const grid = document.getElementById('slot-grid');

        // Destroy previous instance
        if (datePickerInstance) {
            datePickerInstance.destroy();
            datePickerInstance = null;
        }

        try {
            const response = await apiFetch('/api/vajebaat/dates/', { requireAuth: true });
            if (!response.ok) throw new Error('Failed to load dates');

            const data = await response.json();
            const activeDates = (data.results || data).filter(d => d.is_active);

            if (activeDates.length === 0) {
                pickerEl.placeholder = 'No active dates available';
                grid.innerHTML = '<p class="col-span-2 text-center text-[#9CA3AF] text-sm py-4">No dates configured. Please contact the administrator to add appointment dates.</p>';
                return;
            }

            // Build date→id map and allowed dates list
            dateIdMap = {};
            const today = new Date();
            today.setHours(0, 0, 0, 0);

            const allowedDates = activeDates
                .filter(d => new Date(d.date) >= today)  // no past dates
                .map(d => {
                    dateIdMap[d.date] = d.id;
                    return d.date;  // 'YYYY-MM-DD'
                });

            if (allowedDates.length === 0) {
                pickerEl.placeholder = 'No upcoming dates available';
                grid.innerHTML = '<p class="col-span-2 text-center text-[#9CA3AF] text-sm py-4">All configured dates are in the past.</p>';
                return;
            }

            // Initialize Flatpickr
            datePickerInstance = flatpickr(pickerEl, {
                dateFormat: 'Y-m-d',
                altInput: true,
                altFormat: 'D, j F Y',
                minDate: 'today',
                enable: allowedDates,
                defaultDate: (prefDate && allowedDates.includes(prefDate)) ? prefDate : null,
                disableMobile: true,
                onChange: function(selectedDates, dateStr) {
                    if (dateStr && dateIdMap[dateStr]) {
                        loadSlotsForDate(dateIdMap[dateStr]);
                    } else {
                        grid.innerHTML = '<p class="col-span-2 text-center text-[#9CA3AF] text-sm py-4">Pick a date on the calendar</p>';
                    }
                },
            });

            // Trigger load if defaultDate was set
            if (prefDate && allowedDates.includes(prefDate)) {
                loadSlotsForDate(dateIdMap[prefDate]);
            }

            pickerEl.placeholder = 'Pick an appointment date...';

        } catch (err) {
            pickerEl.placeholder = 'Error loading dates';
            console.error('Date picker init error:', err);
        }
    }

    async function loadSlotsForDate(dateId) {
        const grid = document.getElementById('slot-grid');

        if (!dateId) {
            grid.innerHTML = '<p class="col-span-2 text-center text-[#9CA3AF] text-sm py-4">Pick a date on the calendar</p>';
            return;
        }

        grid.innerHTML = '<p class="col-span-2 text-center text-[#9CA3AF] text-sm py-4">Loading slots...</p>';

        try {
            const response = await apiFetch(`/api/vajebaat/slots/?date_id=${dateId}`, { requireAuth: true });
            if (!response.ok) throw new Error('Failed to load slots');

            const data = await response.json();
            const slotsData = Array.isArray(data) ? data : (data.results || []);

            if (slotsData.length === 0) {
                grid.innerHTML = '<p class="col-span-2 text-center text-[#9CA3AF] text-sm py-4">No slots available</p>';
                return;
            }

            grid.innerHTML = slotsData.map(slot => {
                const count = slot.confirmed_count || 0;
                const cap = slot.capacity || 10;
                const isFull = count >= cap;
                const pct = Math.round((count / cap) * 100);

                const bgColor = isFull
                    ? 'bg-red-50 border-red-200 cursor-not-allowed opacity-60'
                    : 'bg-white border-[#DBE2EF] hover:border-[#3F72AF] hover:shadow-md cursor-pointer';
                
                const barColor = isFull ? 'bg-red-400' : pct > 70 ? 'bg-amber-400' : 'bg-green-400';
                const label = isFull ? 'FULL' : `${count}/${cap}`;

                return `
                    <div class="rounded-xl border-2 p-3 transition-all ${bgColor} ${isFull ? '' : 'active:scale-95'}"
                         ${isFull ? '' : `onclick="confirmSlotAssignment(${slot.id}, '${slot.start_time?.substring(0,5)}–${slot.end_time?.substring(0,5)}', '${label}')"`}>
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-sm font-bold text-[#112D4E]">${slot.start_time?.substring(0,5)} – ${slot.end_time?.substring(0,5)}</span>
                            <span class="text-xs font-bold ${isFull ? 'text-red-500' : 'text-[#3F72AF]'}">${label}</span>
                        </div>
                        <div class="w-full h-1.5 bg-gray-100 rounded-full overflow-hidden">
                            <div class="h-full rounded-full transition-all ${barColor}" style="width: ${pct}%"></div>
                        </div>
                    </div>
                `;
            }).join('');

        } catch (err) {
            grid.innerHTML = `<p class="col-span-2 text-center text-red-500 text-sm py-4">Error: ${err.message}</p>`;
        }
    }

    function confirmSlotAssignment(slotId, timeLabel, occupancy) {
        const isReschedule = currentModalMode === 'reschedule';
        showDialog({
            title: isReschedule ? 'Confirm Reschedule' : 'Confirm Slot Assignment',
            message: isReschedule
                ? `Reschedule this appointment to:\n\n⏰ ${timeLabel}\n📊 Currently: ${occupancy}\n\nThe user will be notified of the change.`
                : `Assign this appointment to slot:\n\n⏰ ${timeLabel}\n📊 Currently: ${occupancy}\n\nThis will confirm the appointment and notify the user.`,
            confirmLabel: isReschedule ? 'Reschedule' : 'Assign & Confirm',
            cancelLabel: 'Cancel',
            variant: 'info',
            onConfirm: () => isReschedule ? rescheduleSlot(slotId) : assignSlot(slotId)
        });
    }

    async function assignSlot(slotId) {
        try {
            const response = await apiFetch(`/api/vajebaat/appointments/${currentAppointmentId}/assign-slot/`, {
                method: 'POST',
                requireAuth: true,
                throwOnError: false, // Handle errors manually below
                body: JSON.stringify({ slot_id: slotId }),
                headers: { 'Content-Type': 'application/json' }
            });

            if (response.ok) {
                closeSlotModal();
                showDialog({ title: 'Slot Assigned', message: 'The appointment has been confirmed and the user will be notified.', confirmLabel: 'OK', cancelLabel: null, variant: 'info' });
                loadAppointments();
            } else {
                const errData = await response.json();
                showDialog({ title: 'Assignment Failed', message: errData.detail || 'Failed to assign slot. The slot may be full.', confirmLabel: 'OK', cancelLabel: null, variant: 'danger' });
            }
        } catch (err) {
            showDialog({ title: 'Error', message: 'Connection error. Please try again.', confirmLabel: 'OK', cancelLabel: null, variant: 'danger' });
        }
    }

    async function rescheduleSlot(slotId) {
        try {
            const response = await apiFetch(`/api/vajebaat/appointments/${currentAppointmentId}/reschedule/`, {
                method: 'PATCH',
                requireAuth: true,
                throwOnError: false, // Handle errors manually below
                body: JSON.stringify({ slot_id: slotId }),
                headers: { 'Content-Type': 'application/json' }
            });

            if (response.ok) {
                closeSlotModal();
                showDialog({ title: 'Rescheduled', message: 'The appointment has been rescheduled and the user will be notified.', confirmLabel: 'OK', cancelLabel: null, variant: 'info' });
                loadAppointments();
            } else {
                const errData = await response.json();
                showDialog({ title: 'Reschedule Failed', message: errData.detail || 'Failed to reschedule. The slot may be full.', confirmLabel: 'OK', cancelLabel: null, variant: 'danger' });
            }
        } catch (err) {
            showDialog({ title: 'Error', message: 'Connection error. Please try again.', confirmLabel: 'OK', cancelLabel: null, variant: 'danger' });
        }
    }

    async function cancelAppointment(appointmentId, name) {
        showDialog({
            title: 'Cancel Appointment',
            message: `Are you sure you want to cancel the appointment for ${name}?\n\nThis action will release the assigned slot and notify the user.`,
            confirmLabel: 'Yes, Cancel',
            cancelLabel: 'Keep',
            variant: 'danger',
            onConfirm: async () => {
                // Find all cancel buttons for this appointment and show loading state
                const btns = document.querySelectorAll(`button[onclick*="cancelAppointment(${appointmentId}"]`);
                btns.forEach(b => {
                    b.disabled = true;
                    b.innerHTML = '<span class="animate-spin inline-block w-3 h-3 border-2 border-white/30 border-t-white rounded-full"></span>';
                });

                try {
                    const response = await apiFetch(`/api/vajebaat/appointments/${appointmentId}/cancel/`, {
                        method: 'PATCH',
                        requireAuth: true,
                        throwOnError: false, // Handle errors manually below
                        headers: { 'Content-Type': 'application/json' }
                    });
                    if (response.ok) {
                        showDialog({ title: 'Cancelled', message: 'The appointment has been cancelled successfully.', confirmLabel: 'OK', cancelLabel: null, variant: 'info' });
                        loadAppointments();
                    } else {
                        const errData = await response.json();
                        showDialog({ title: 'Error', message: errData.detail || 'Failed to cancel appointment.', confirmLabel: 'OK', cancelLabel: null, variant: 'danger' });
                        loadAppointments(); // refresh to reset button state
                    }
                } catch (err) {
                    showDialog({ title: 'Error', message: 'Connection error. Please try again.', confirmLabel: 'OK', cancelLabel: null, variant: 'danger' });
                    loadAppointments(); // refresh to reset button state
                }
            }
        });
    }


    // ============================================================
    // Utility
    // ============================================================
    function logout() {
        localStorage.clear();
        window.location.href = (window.BASE_URL || '') + '/admin/login.php';
    }

    async function exportData(format) {
        // For now, since only CSV is implemented in backend, we redirect to CSV or show alert
        if (format === 'excel' || format === 'pdf') {
            window.location.href = window.API_BASE + '/api/vajebaat/export-csv/?format=' + format;
        } else {
            window.location.href = window.API_BASE + '/api/vajebaat/export-csv/';
        }
    }
</script>
