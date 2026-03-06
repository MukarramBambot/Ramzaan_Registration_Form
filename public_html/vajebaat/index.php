<?php include '../includes/header.php'; ?>

<style>
    /* Print-specific styles - Keep for potential future use or clean if strictly "Remove Takhmeen" */
    @media print {
        header, nav, footer, .no-print, #app-root > nav, .bg-[#112D4E].py-8 {
            display: none !important;
        }
        body, #app-root, main {
            background-color: white !important;
            padding: 0 !important;
            margin: 0 !important;
        }
    }

    .input-field {
        width: 100%; height: 3rem;
        padding: 0 1rem;
        background: #fff;
        border: 1px solid #DBE2EF;
        border-radius: 0.375rem;
        color: #112D4E;
        font-size: 1rem;
        transition: border-color 0.15s, box-shadow 0.15s;
    }
    .input-field:focus { outline: none; border-color: #3F72AF; box-shadow: 0 0 0 3px rgba(63,114,175,0.12); }
    
    .btn-primary {
        width: 100%; height: 3.25rem;
        background: #112D4E; color: #fff;
        font-weight: 600; font-size: 0.95rem;
        border-radius: 0.5rem; border: none; cursor: pointer;
        transition: background 0.15s;
    }
    .btn-primary:hover { background: #1e3d6f; }
    .btn-primary:active { background: #0d2340; }
    .btn-primary:disabled { background: #9CA3AF; cursor: not-allowed; }

    /* Slot radio button styles */
    .slot-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
        gap: 0.75rem;
    }
    .slot-option input { display: none; }
    .slot-label {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.75rem;
        border: 1px solid #DBE2EF;
        border-radius: 0.5rem;
        cursor: pointer;
        font-size: 0.875rem;
        transition: all 0.2s;
        background: white;
    }
    .slot-option input:checked + .slot-label {
        background: #112D4E;
        color: white;
        border-color: #112D4E;
    }
    .slot-option input:disabled + .slot-label {
        opacity: 0.5;
        cursor: not-allowed;
        background: #F9FAFB;
    }
</style>

<div class="min-h-screen bg-[#F9F7F7] no-print">

    <!-- Page Header -->
    <div class="bg-[#112D4E] py-8 px-4 sm:px-6 lg:px-8 text-center sm:text-left">
        <div class="max-w-2xl mx-auto">
            <h1 class="text-3xl text-white font-normal mb-1">Vajebaat</h1>
            <p class="text-[#DBE2EF] text-lg font-light">Appointment Booking &bull; Saifee Masjid Chennai</p>
        </div>
    </div>

    <div class="py-8 px-4 sm:px-6 lg:px-8">
        <div class="max-w-2xl mx-auto space-y-6">

            <!-- Appointment Booking Form -->
            <section id="booking-section" class="bg-white rounded-lg shadow-sm border border-[#DBE2EF] overflow-hidden">
                <div class="h-2 bg-[#3F72AF] w-full"></div>
                <div class="p-6 sm:p-8 space-y-6">
                    <div class="flex items-center gap-3 mb-1">
                        <div class="w-9 h-9 bg-[#DBE2EF] rounded-lg flex items-center justify-center shrink-0">
                            <svg class="w-5 h-5 text-[#3F72AF]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5" />
                            </svg>
                        </div>
                        <div>
                            <h2 class="text-xl text-[#112D4E] font-semibold">Book Appointment</h2>
                            <p class="text-sm text-[#6B7280]">Select a date and time to book your Vajebaat appointment</p>
                        </div>
                    </div>

                    <form id="appointment-form" onsubmit="handleBooking(event)" class="space-y-5">
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div>
                                <label class="block text-xs font-bold text-[#6B7280] uppercase tracking-wider mb-2">ITS Number <span class="text-red-500">*</span></label>
                                <input type="text" id="apt-its" required class="input-field" placeholder="8-digit ITS number" maxlength="8" inputmode="numeric">
                            </div>

                            <div>
                                <label class="block text-xs font-bold text-[#6B7280] uppercase tracking-wider mb-2">Full Name <span class="text-red-500">*</span></label>
                                <input type="text" id="apt-name" required class="input-field" placeholder="Enter your full name">
                            </div>
                        </div>

                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div>
                                <label class="block text-xs font-bold text-[#6B7280] uppercase tracking-wider mb-2">Mobile Number <span class="text-red-500">*</span></label>
                                <input type="tel" id="apt-mobile" required class="input-field" placeholder="WhatsApp number">
                            </div>

                            <div>
                                <label class="block text-xs font-bold text-[#6B7280] uppercase tracking-wider mb-2">Email Address <span class="text-red-500">*</span></label>
                                <input type="email" id="apt-email" required class="input-field" placeholder="yourname@example.com">
                            </div>
                        </div>

                        <div>
                            <label class="block text-xs font-bold text-[#6B7280] uppercase tracking-wider mb-2">Select Date <span class="text-red-500">*</span></label>
                            <input type="date" id="apt-date" required class="input-field" onchange="fetchSlots()">
                        </div>

                        <div id="slots-container" class="hidden">
                            <label class="block text-xs font-bold text-[#6B7280] uppercase tracking-wider mb-3">Available Time Slot <span class="text-red-500">*</span></label>
                            <div id="slots-grid" class="slot-grid">
                                <!-- Slots will be loaded here -->
                            </div>
                        </div>

                        <div>
                            <label class="block text-xs font-bold text-[#6B7280] uppercase tracking-wider mb-2">Remarks (Optional)</label>
                            <textarea id="apt-remarks" class="input-field h-24 py-3 resize-none" placeholder="Any additional notes..."></textarea>
                        </div>

                        <div class="pt-2">
                            <button type="submit" id="submit-btn" class="btn-primary">Book Appointment</button>
                        </div>

                        <div class="text-center pt-2">
                            <a href="<?= BASE_URL ?>/vajebaat/status.php" class="text-sm text-[#3F72AF] hover:underline">Already booked? Check Status</a>
                        </div>
                    </form>
                </div>
            </section>

            <!-- Success Message (Hidden by default) -->
            <section id="success-view" class="hidden bg-white rounded-lg shadow-sm border border-[#DBE2EF] overflow-hidden">
                <div class="h-2 bg-green-500 w-full"></div>
                <div class="p-8 text-center">
                    <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
                        <svg class="w-8 h-8 text-green-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                        </svg>
                    </div>
                    <h2 class="text-2xl font-bold text-[#112D4E] mb-2">Appointment Booked!</h2>
                    <p class="text-[#6B7280] mb-6">Your appointment has been successfully recorded.</p>
                    
                    <div class="bg-[#F9FAFB] border border-[#DBE2EF] rounded-xl p-5 mb-8 text-left space-y-3">
                        <div class="flex justify-between">
                            <span class="text-sm text-[#6B7280]">Appointment Date</span>
                            <span id="success-date" class="text-sm font-bold text-[#112D4E]">...</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-sm text-[#6B7280]">Time Slot</span>
                            <span id="success-slot" class="text-sm font-bold text-[#112D4E]">...</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-sm text-[#6B7280]">Status</span>
                            <span class="text-sm font-bold text-amber-500">Confirmed</span>
                        </div>
                    </div>

                    <a href="<?= BASE_URL ?>/vajebaat/" class="inline-block px-6 py-2.5 bg-[#112D4E] text-white rounded-lg hover:bg-[#1e3d6f] transition-all font-medium text-sm">Book Another Appointment</a>
                </div>
            </section>

        </div>
    </div>
</div>

<script>
    async function fetchSlots() {
        const dateInput = document.getElementById('apt-date');
        const date = dateInput.value;
        const slotsContainer = document.getElementById('slots-container');
        const slotsGrid = document.getElementById('slots-grid');

        if (!date) return;

        slotsGrid.innerHTML = '<div class="col-span-full py-4 text-center text-sm text-[#6B7280]">Loading slots...</div>';
        slotsContainer.classList.remove('hidden');

        try {
            const response = await fetch(window.API_BASE + `/api/vajebaat/available-slots/?date=${date}`);
            const data = await response.json();

            if (!response.ok) throw new Error('Failed to fetch slots');

            const availableSlots = data.filter(slot => slot.available);

            if (availableSlots.length === 0) {
                slotsGrid.innerHTML = '<div class="col-span-full py-4 text-center text-sm text-red-500">No available slots for this date. Please pick another date.</div>';
            } else {
                slotsGrid.innerHTML = availableSlots.map((slot, index) => `
                    <div class="slot-option">
                        <input type="radio" name="slot" id="slot-${slot.id}" value="${slot.id}" data-label="${slot.slot}" required>
                        <label for="slot-${slot.id}" class="slot-label">${slot.slot}</label>
                    </div>
                `).join('');
            }
        } catch (err) {
            slotsGrid.innerHTML = '<div class="col-span-full py-4 text-center text-sm text-red-500">Error loading slots. Please try again.</div>';
        }
    }

    async function handleBooking(e) {
        e.preventDefault();
        const submitBtn = document.getElementById('submit-btn');
        
        const its = document.getElementById('apt-its').value.trim();
        const name = document.getElementById('apt-name').value.trim();
        const mobile = document.getElementById('apt-mobile').value.trim();
        const email = document.getElementById('apt-email').value.trim();
        const date = document.getElementById('apt-date').value;
        const remarks = document.getElementById('apt-remarks').value.trim();
        const slotEl = document.querySelector('input[name="slot"]:checked');

        if (!slotEl) {
            alert("Please select a time slot.");
            return;
        }
        const slotId = slotEl.value;
        const slotLabel = slotEl.dataset.label;

        if (!/^\d{8}$/.test(its)) {
            alert("Please enter a valid 8-digit ITS number.");
            return;
        }

        submitBtn.disabled = true;
        submitBtn.textContent = 'Booking...';

        try {
            const response = await fetch(window.API_BASE + '/api/vajebaat/appointments/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    its: its,
                    name: name,
                    mobile: mobile,
                    email: email,
                    date: date,
                    slot_id: slotId,
                    remarks: remarks
                })
            });

            const data = await response.json();

            if (!response.ok) {
                const msg = typeof data === 'object'
                    ? Object.values(data).flat().join(' ')
                    : 'Booking failed. Please try again.';
                alert(msg);
                return;
            }

            // Success
            document.getElementById('success-date').textContent = new Date(date).toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });
            document.getElementById('success-slot').textContent = slotLabel;

            document.getElementById('booking-section').classList.add('hidden');
            document.getElementById('success-view').classList.remove('hidden');
            window.scrollTo(0, 0);

        } catch (err) {
            alert('Network error. Please check your connection and try again.');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Book Appointment';
        }
    }
</script>

<?php include '../includes/footer.php'; ?>