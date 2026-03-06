<?php include '../includes/admin-header.php'; ?>

<!-- Content Wrapper -->
<div class="min-h-screen bg-[#F9F7F7]">
    
    <!-- Header -->
    <div class="bg-[#112D4E] py-5 px-6 shadow-md">
        <div class="flex items-center justify-between">
            <div>
                <div class="flex flex-col md:flex-row md:items-center gap-2 md:gap-6 mb-1">
                    <h1 class="text-xl md:text-2xl text-white font-normal">
                        Slot Management
                    </h1>
                    <div class="flex items-center gap-2 mt-2 md:mt-0 md:ml-4 overflow-x-auto pb-2 md:pb-0">
                        <a href="<?= BASE_URL ?>/admin/vajebaat-appointments.php" class="whitespace-nowrap px-3 py-1.5 rounded-md text-[#DBE2EF] hover:text-white hover:bg-white/10 text-sm font-medium transition-all flex items-center gap-2">
                            <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                            Appointments
                        </a>
                        <a href="<?= BASE_URL ?>/admin/vajebaat-slots.php" class="whitespace-nowrap px-3 py-1.5 rounded-md bg-[#3F72AF] text-white text-sm font-medium flex items-center gap-2">
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
                    Configure availability and capacity for Vajebaat appointments
                </p>
            </div>
             <div class="flex items-center gap-3 text-[#DBE2EF] text-sm">
                <button
                    id="refresh-btn"
                    onclick="loadDates()"
                    class="px-3 py-1.5 rounded-md bg-white/10 hover:bg-white/20 text-white text-sm font-medium transition-all flex items-center gap-2"
                >
                    <span>Refresh</span>
                </button>
                <button
                    id="add-slot-btn"
                    onclick="openCreateSlotModal()"
                    class="ml-2 px-3 py-1.5 rounded-md bg-green-600 hover:bg-green-700 text-white text-sm font-medium transition-all flex items-center gap-2"
                >
                    <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                    <span>Create Slot</span>
                </button>
            </div>
        </div>
    </div>

    <!-- Main Content -->
    <div class="p-6">
        <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
            
            <!-- Dates Sidebar -->
            <div class="lg:col-span-1 space-y-4">
                <div class="bg-white rounded-xl shadow-sm border border-[#DBE2EF] overflow-hidden">
                    <div class="bg-[#F9FAFB] px-4 py-3 border-b border-[#DBE2EF]">
                        <h3 class="text-xs font-bold text-[#6B7280] uppercase tracking-wider">Appointment Dates</h3>
                    </div>
                    <div id="dates-list" class="divide-y divide-[#DBE2EF] max-h-[60vh] overflow-y-auto custom-scrollbar">
                        <div class="p-4 text-center text-sm text-[#9CA3AF]">Loading dates...</div>
                    </div>
                </div>
            </div>

            <!-- Slots Grid -->
            <div class="lg:col-span-3 space-y-6">
                <!-- Date Header -->
                <div id="selected-date-header" class="bg-white rounded-xl shadow-sm border border-[#DBE2EF] p-6 hidden">
                    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                        <div class="flex items-center gap-4">
                            <div class="w-12 h-12 bg-[#3F72AF]/10 rounded-xl flex items-center justify-center text-[#3F72AF]">
                                <svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                </svg>
                            </div>
                            <div>
                                <h2 id="display-date" class="text-2xl font-bold text-[#112D4E]">...</h2>
                                <p id="display-date-id" class="text-xs text-[#6B7280] font-mono"></p>
                            </div>
                        </div>
                        <div class="flex items-center gap-3">
                            <button id="toggle-date-btn" onclick="toggleDateStatus()" class="px-4 py-2 rounded-lg bg-red-50 text-red-600 border border-red-200 text-sm font-bold transition-all hover:bg-red-100">
                                Disable Date
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Slots -->
                <div id="slots-area" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 hidden">
                    <!-- Slots will be injected here -->
                </div>

                <!-- Empty State -->
                <div id="slots-empty-state" class="bg-white rounded-xl shadow-sm border border-[#DBE2EF] p-12 text-center">
                    <div class="w-16 h-16 bg-[#F9FAFB] rounded-full flex items-center justify-center mx-auto mb-4 text-[#9CA3AF]">
                        <svg class="w-8 h-8" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    </div>
                    <h3 class="text-[#112D4E] font-bold text-lg">No Date Selected</h3>
                    <p class="text-[#6B7280] text-sm">Select an appointment date from the sidebar to manage its slots.</p>
                </div>
            </div>
        </div>
    </div>

</div>

<!-- Booked Users Modal -->
<div id="users-modal-backdrop" class="fixed inset-0 z-[9998] hidden">
    <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" onclick="closeUsersModal()"></div>
    <div class="absolute inset-0 flex items-center justify-center p-4">
        <div class="relative bg-white w-full max-w-2xl rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
            <!-- Header -->
            <div class="bg-[#112D4E] px-6 py-4 flex items-center justify-between shrink-0">
                <div>
                    <h3 id="users-modal-title" class="text-lg font-bold text-white">Booked Appointments</h3>
                    <p id="users-modal-subtitle" class="text-xs text-[#DBE2EF]/70 font-mono"></p>
                </div>
                <button onclick="closeUsersModal()" class="p-1 rounded-lg hover:bg-white/10 text-white/60 hover:text-white transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>
            </div>

            <!-- Table -->
            <div class="overflow-y-auto custom-scrollbar p-0">
                <table class="w-full text-left border-collapse">
                    <thead class="bg-[#F9FAFB] border-b border-[#DBE2EF] sticky top-0">
                        <tr>
                            <th class="px-6 py-3 text-xs font-bold text-[#6B7280] uppercase tracking-wider">ITS</th>
                            <th class="px-6 py-3 text-xs font-bold text-[#6B7280] uppercase tracking-wider">Name</th>
                            <th class="px-6 py-3 text-xs font-bold text-[#6B7280] uppercase tracking-wider">Status</th>
                            <th class="px-6 py-3 text-xs font-bold text-[#6B7280] uppercase tracking-wider">Action</th>
                        </tr>
                    </thead>
                    <tbody id="users-table-body" class="divide-y divide-[#DBE2EF]">
                        <!-- Users will be injected here -->
                    </tbody>
                </table>
            </div>

            <!-- Footer -->
            <div class="px-6 py-4 bg-[#F9FAFB] border-t border-[#DBE2EF] flex justify-end shrink-0">
                <button onclick="closeUsersModal()" class="px-4 py-2 rounded-lg bg-white border border-[#DBE2EF] text-[#112D4E] text-sm font-bold shadow-sm hover:bg-[#F3F4F6] transition-all">Close</button>
            </div>
        </div>
    </div>
</div>

<!-- Create Slot Modal -->
<div id="create-slot-modal-backdrop" class="fixed inset-0 z-[9998] hidden">
    <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" onclick="closeCreateSlotModal()"></div>
    <div class="absolute inset-0 flex items-center justify-center p-4">
        <div class="relative bg-white w-full max-w-md rounded-2xl shadow-2xl overflow-hidden flex flex-col">
            <div class="bg-[#112D4E] px-6 py-4 flex items-center justify-between">
                <h3 class="text-lg font-bold text-white">Create New Time Slot</h3>
                <button onclick="closeCreateSlotModal()" class="p-1 rounded-lg hover:bg-white/10 text-white/60 hover:text-white transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>
            </div>
            <div class="p-6 space-y-4">
                <div>
                    <label class="block text-xs font-bold text-[#6B7280] uppercase mb-2">Target Date</label>
                    <p id="create-slot-date-label" class="text-sm font-bold text-[#112D4E]"></p>
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-bold text-[#6B7280] uppercase mb-2">Start Time</label>
                        <input type="time" id="new-slot-start" class="w-full px-3 py-2 border border-[#DBE2EF] rounded-lg text-sm bg-white outline-none focus:ring-2 focus:ring-[#3F72AF]">
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-[#6B7280] uppercase mb-2">End Time</label>
                        <input type="time" id="new-slot-end" class="w-full px-3 py-2 border border-[#DBE2EF] rounded-lg text-sm bg-white outline-none focus:ring-2 focus:ring-[#3F72AF]">
                    </div>
                </div>
                <div>
                    <label class="block text-xs font-bold text-[#6B7280] uppercase mb-2">Slot Number (Sequence)</label>
                    <input type="number" id="new-slot-number" placeholder="e.g. 1" class="w-full px-3 py-2 border border-[#DBE2EF] rounded-lg text-sm bg-white outline-none focus:ring-2 focus:ring-[#3F72AF]">
                </div>
                <div>
                    <label class="block text-xs font-bold text-[#6B7280] uppercase mb-2">Capacity</label>
                    <input type="number" id="new-slot-capacity" value="10" min="1" class="w-full px-3 py-2 border border-[#DBE2EF] rounded-lg text-sm bg-white outline-none focus:ring-2 focus:ring-[#3F72AF]">
                </div>
            </div>
            <div class="px-6 py-4 bg-[#F9FAFB] border-t border-[#DBE2EF] flex justify-end gap-3">
                <button onclick="closeCreateSlotModal()" class="px-4 py-2 rounded-lg bg-white border border-[#DBE2EF] text-[#112D4E] text-sm font-bold hover:bg-[#F3F4F6] transition-all">Cancel</button>
                <button onclick="submitCreateSlot()" class="px-4 py-2 rounded-lg bg-[#112D4E] text-white text-sm font-bold shadow-md hover:bg-[#1e3d6f] transition-all">Create Slot</button>
            </div>
        </div>
    </div>
</div>

<script src="<?= BASE_URL ?>/assets/js/main.js"></script>
<?php include '../includes/footer.php'; ?>

<script>
    let dates = [];
    let selectedDateId = null;
    let selectedDateInfo = null;
    let slots = [];

    document.addEventListener('DOMContentLoaded', () => {
        if (!localStorage.getItem('access_token')) {
            window.location.href = (window.BASE_URL || '') + '/admin/login.php';
            return;
        }
        loadDates();
    });

    async function loadDates() {
        const list = document.getElementById('dates-list');
        list.innerHTML = '<div class="p-4 text-center text-sm text-[#9CA3AF]">Loading dates...</div>';

        try {
            const response = await apiFetch('/api/vajebaat/dates/', { requireAuth: true });
            if (!response.ok) throw new Error('Failed to load dates');
            dates = await response.json();
            renderDates();
        } catch (err) {
            list.innerHTML = `<div class="p-4 text-center text-sm text-red-500">${err.message}</div>`;
        }
    }

    function renderDates() {
        const list = document.getElementById('dates-list');
        if (dates.length === 0) {
            list.innerHTML = '<div class="p-4 text-center text-sm text-[#9CA3AF]">No dates found.</div>';
            return;
        }

        list.innerHTML = dates.map(d => {
            const activeClass = selectedDateId === d.id ? 'bg-[#3F72AF]/5 border-l-4 border-l-[#3F72AF]' : 'hover:bg-[#F9FAFB]';
            const statusColor = d.is_active ? 'bg-green-500' : 'bg-gray-300';
            const dateObj = new Date(d.date);
            const dateStr = dateObj.toLocaleDateString('en-GB', { day: 'numeric', month: 'short' });
            const dayStr = dateObj.toLocaleDateString('en-GB', { weekday: 'short' });

            return `
                <div class="p-4 cursor-pointer transition-all ${activeClass}" onclick="selectDate(${d.id})">
                    <div class="flex items-center justify-between">
                        <div>
                            <p class="font-bold text-[#112D4E]">${dateStr}</p>
                            <p class="text-xs text-[#6B7280]">${dayStr}</p>
                        </div>
                        <div class="flex items-center gap-2">
                            <span class="text-[10px] font-bold text-[#3F72AF]">${d.slot_count || 0} Slots</span>
                            <div class="w-2 h-2 rounded-full ${statusColor}"></div>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    }

    async function selectDate(id) {
        selectedDateId = id;
        selectedDateInfo = dates.find(d => d.id === id);
        renderDates();

        // Show header
        document.getElementById('display-date').textContent = new Date(selectedDateInfo.date).toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });
        document.getElementById('display-date-id').textContent = `Date ID: ${id}`;
        document.getElementById('selected-date-header').classList.remove('hidden');
        document.getElementById('slots-empty-state').classList.add('hidden');
        document.getElementById('slots-area').classList.remove('hidden');

        // Toggle btn
        const toggleBtn = document.getElementById('toggle-date-btn');
        if (selectedDateInfo.is_active) {
            toggleBtn.textContent = 'Disable Date';
            toggleBtn.className = 'px-4 py-2 rounded-lg bg-red-50 text-red-600 border border-red-200 text-sm font-bold transition-all hover:bg-red-100';
        } else {
            toggleBtn.textContent = 'Enable Date';
            toggleBtn.className = 'px-4 py-2 rounded-lg bg-green-50 text-green-600 border border-green-200 text-sm font-bold transition-all hover:bg-green-100';
        }

        loadSlots();
    }

    async function loadSlots() {
        const area = document.getElementById('slots-area');
        area.innerHTML = '<div class="col-span-full py-12 text-center text-[#9CA3AF]">Loading slots...</div>';

        try {
            const response = await apiFetch(`/api/vajebaat/slots/?date_id=${selectedDateId}`, { requireAuth: true });
            if (!response.ok) throw new Error('Failed to load slots');
            slots = await response.json();
            renderSlots();
        } catch (err) {
            area.innerHTML = `<div class="col-span-full py-12 text-center text-red-500">${err.message}</div>`;
        }
    }

    function renderSlots() {
        const area = document.getElementById('slots-area');
        area.innerHTML = slots.map(s => {
            const count = s.confirmed_count || 0;
            const cap = s.capacity || 10;
            const isFull = count >= cap;
            const pct = Math.round((count / cap) * 100);
            const statusClass = s.is_active ? 'bg-white border-[#DBE2EF]' : 'bg-gray-50 border-gray-200 opacity-75';
            
            return `
                <div class="rounded-xl border shadow-sm p-4 transition-all ${statusClass}">
                    <div class="flex items-center justify-between mb-4">
                        <div class="flex items-center gap-2">
                             <div class="w-8 h-8 rounded-lg bg-[#3F72AF]/10 flex items-center justify-center text-[#3F72AF]">
                                <span class="text-xs font-bold">#${s.slot_number}</span>
                             </div>
                             <span class="font-bold text-[#112D4E] text-sm">${s.start_time.substring(0,5)} – ${s.end_time.substring(0,5)}</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <label class="relative inline-flex items-center cursor-pointer">
                                <input type="checkbox" class="sr-only peer" ${s.is_active ? 'checked' : ''} onchange="toggleSlotActive(${s.id}, this.checked)">
                                <div class="w-9 h-5 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-[#3F72AF]"></div>
                            </label>
                        </div>
                    </div>

                    <div class="space-y-4">
                        <div>
                            <div class="flex items-center justify-between text-xs mb-1.5">
                                <span class="text-[#6B7280] font-medium tracking-tight uppercase">Occupancy</span>
                                <span class="font-bold ${isFull ? 'text-red-500' : 'text-[#112D4E]'}">${count} / ${cap} Booked</span>
                            </div>
                            <div class="w-full h-1.5 bg-gray-100 rounded-full overflow-hidden">
                                <div class="h-full bg-[#112D4E] rounded-full transition-all" style="width: ${pct}%"></div>
                            </div>
                        </div>

                        <div class="grid grid-cols-2 gap-2">
                             <div class="p-2 border border-[#DBE2EF] rounded-lg">
                                <label class="block text-[10px] font-bold text-[#6B7280] uppercase mb-1">Capacity</label>
                                <div class="flex items-center gap-1">
                                    <input type="number" value="${cap}" min="1" max="50" onchange="updateCapacity(${s.id}, this.value)" 
                                           class="w-full bg-transparent font-bold text-[#112D4E] text-sm outline-none focus:text-[#3F72AF]">
                                </div>
                             </div>
                             <button onclick="viewBookings(${s.id}, '${s.start_time.substring(0,5)}–${s.end_time.substring(0,5)}')" 
                                     class="flex flex-col items-center justify-center p-2 border border-[#DBE2EF] rounded-lg hover:border-[#3F72AF] hover:bg-[#3F72AF]/5 transition-all text-[#3F72AF] group">
                                <span class="text-[10px] font-bold uppercase mb-1">View Users</span>
                                <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                </svg>
                             </button>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    }

    async function updateCapacity(slotId, newCapacity) {
        try {
            const response = await apiFetch(`/api/vajebaat/slots/${slotId}/`, {
                method: 'PATCH',
                requireAuth: true,
                body: JSON.stringify({ capacity: parseInt(newCapacity) }),
                headers: { 'Content-Type': 'application/json' }
            });
            if (response.ok) {
                const updated = await response.json();
                const idx = slots.findIndex(s => s.id === slotId);
                if (idx !== -1) {
                    slots[idx].capacity = updated.capacity;
                    renderSlots();
                }
            } else {
                alert('Failed to update capacity');
                loadSlots();
            }
        } catch (err) {
            console.error(err);
        }
    }

    async function toggleSlotActive(slotId, isActive) {
        try {
            const response = await apiFetch(`/api/vajebaat/slots/${slotId}/`, {
                method: 'PATCH',
                requireAuth: true,
                body: JSON.stringify({ is_active: isActive }),
                headers: { 'Content-Type': 'application/json' }
            });
            if (response.ok) {
                const updated = await response.json();
                const idx = slots.findIndex(s => s.id === slotId);
                if (idx !== -1) {
                    slots[idx].is_active = updated.is_active;
                    renderSlots();
                }
            }
        } catch (err) {
            console.error(err);
        }
    }

    async function toggleDateStatus() {
        // Since VajebaatDate is ReadOnly in API, we might need to use Admin or wait for write access.
        // For now, if it's read only, show a message.
        alert('Date activation is managed by system administrators. Only individual slots can be toggled.');
    }

    async function viewBookings(slotId, timeLabel) {
        const modal = document.getElementById('users-modal-backdrop');
        const title = document.getElementById('users-modal-title');
        const subtitle = document.getElementById('users-modal-subtitle');
        const tbody = document.getElementById('users-table-body');

        title.textContent = `Appointments for ${timeLabel}`;
        subtitle.textContent = `Date: ${selectedDateInfo.date} | Slot ID: ${slotId}`;
        tbody.innerHTML = '<tr><td colspan="4" class="px-6 py-12 text-center text-[#9CA3AF]">Loading bookings...</td></tr>';
        
        modal.classList.remove('hidden');
        document.body.classList.add('modal-open');

        try {
            const response = await apiFetch(`/api/vajebaat/slots/${slotId}/users/`, { requireAuth: true });
            if (!response.ok) throw new Error('Failed to load users');
            const bookings = await response.json();

            if (bookings.length === 0) {
                tbody.innerHTML = '<tr><td colspan="4" class="px-6 py-12 text-center text-[#9CA3AF]">No appointments booked in this slot yet.</td></tr>';
                return;
            }

            tbody.innerHTML = bookings.map(b => `
                <tr class="hover:bg-[#F9FAFB] transition-colors">
                    <td class="px-6 py-4 font-mono text-sm text-[#3F72AF]">${b.its_number}</td>
                    <td class="px-6 py-4 font-medium text-[#112D4E]">${b.name}</td>
                    <td class="px-6 py-4">
                        <span class="px-2 py-1 rounded-full text-[10px] font-bold bg-green-100 text-green-700">${b.status}</span>
                    </td>
                    <td class="px-6 py-4">
                        <a href="<?= BASE_URL ?>/admin/vajebaat-appointment-detail.php?id=${b.id}" class="text-[#3F72AF] hover:underline text-xs font-bold">View Details</a>
                    </td>
                </tr>
            `).join('');

        } catch (err) {
            tbody.innerHTML = `<tr><td colspan="4" class="px-6 py-12 text-center text-red-500">${err.message}</td></tr>`;
        }
    }

    function closeUsersModal() {
        document.getElementById('users-modal-backdrop').classList.add('hidden');
        document.body.classList.remove('modal-open');
    }

    function openCreateSlotModal() {
        if (!selectedDateId) {
            alert('Please select a date from the sidebar first.');
            return;
        }
        document.getElementById('create-slot-date-label').textContent = new Date(selectedDateInfo.date).toLocaleDateString();
        document.getElementById('create-slot-modal-backdrop').classList.remove('hidden');
        document.body.classList.add('modal-open');
    }

    function closeCreateSlotModal() {
        document.getElementById('create-slot-modal-backdrop').classList.add('hidden');
        document.body.classList.remove('modal-open');
    }

    async function submitCreateSlot() {
        const start = document.getElementById('new-slot-start').value;
        const end = document.getElementById('new-slot-end').value;
        const num = document.getElementById('new-slot-number').value;
        const cap = document.getElementById('new-slot-capacity').value;

        if (!start || !end || !num) {
            alert('Please fill in all required fields.');
            return;
        }

        try {
            const response = await apiFetch(`/api/vajebaat/slots/`, {
                method: 'POST',
                requireAuth: true,
                body: JSON.stringify({
                    date: selectedDateId,
                    start_time: start,
                    end_time: end,
                    slot_number: parseInt(num),
                    capacity: parseInt(cap)
                }),
                headers: { 'Content-Type': 'application/json' }
            });

            if (response.ok) {
                closeCreateSlotModal();
                loadSlots();
            } else {
                const data = await response.json();
                alert(data.detail || 'Failed to create slot.');
            }
        } catch (err) {
            alert('Network error.');
        }
    }
</script>
