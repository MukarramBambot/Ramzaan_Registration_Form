<?php include '../includes/header.php'; ?>

<style>
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
</style>

<div class="min-h-screen bg-[#F9F7F7]">

    <!-- Page Header -->
    <div class="bg-[#112D4E] py-8 px-4 sm:px-6 lg:px-8 text-center sm:text-left">
        <div class="max-w-2xl mx-auto">
            <h1 class="text-3xl text-white font-normal mb-1">Book Appointment</h1>
            <p class="text-[#DBE2EF] text-lg font-light">Vajebaat 1447H &bull; Saifee Masjid Chennai</p>
        </div>
    </div>

    <div class="py-8 px-4 sm:px-6 lg:px-8">
        <div class="max-w-lg mx-auto">

            <!-- Card -->
            <div id="booking-container" class="bg-white rounded-lg shadow-sm border border-[#DBE2EF] overflow-hidden">
                <div class="h-2 bg-[#3F72AF] w-full"></div>
                <div class="p-6 sm:p-8">

                    <form id="appointment-form" onsubmit="handleBooking(event)" class="space-y-5">
                        <div class="space-y-4">
                            <div>
                                <label class="block text-xs font-bold text-[#6B7280] uppercase tracking-wider mb-2">ITS Number <span class="text-red-500">*</span></label>
                                <input type="text" id="apt-its" required class="input-field" placeholder="8-digit ITS number" maxlength="8" inputmode="numeric">
                            </div>

                            <div>
                                <label class="block text-xs font-bold text-[#6B7280] uppercase tracking-wider mb-2">Full Name <span class="text-red-500">*</span></label>
                                <input type="text" id="apt-name" required class="input-field" placeholder="Enter your full name">
                            </div>

                            <div>
                                <label class="block text-xs font-bold text-[#6B7280] uppercase tracking-wider mb-2">Mobile Number <span class="text-red-500">*</span></label>
                                <input type="tel" id="apt-mobile" required class="input-field" placeholder="WhatsApp number">
                            </div>

                            <div>
                                <label class="block text-xs font-bold text-[#6B7280] uppercase tracking-wider mb-2">Preferred Date <span class="text-red-500">*</span></label>
                                <input type="date" id="apt-date" required class="input-field">
                            </div>

                            <div>
                                <label class="block text-xs font-bold text-[#6B7280] uppercase tracking-wider mb-2">Remarks (Optional)</label>
                                <textarea id="apt-remarks" class="input-field h-24 py-3 resize-none" placeholder="Any additional notes..."></textarea>
                            </div>
                        </div>

                        <button type="submit" class="btn-primary mt-4">Confirm Appointment</button>
                    </form>

                </div>
            </div>

            <!-- Success Message (Hidden by default) -->
            <div id="success-view" class="hidden bg-white rounded-lg shadow-sm border border-[#DBE2EF] overflow-hidden">
                <div class="h-2 bg-green-500 w-full"></div>
                <div class="p-8 text-center">
                    <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
                        <svg class="w-8 h-8 text-green-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                        </svg>
                    </div>
                    <h2 class="text-2xl font-bold text-[#112D4E] mb-2">Appointment Booked!</h2>
                    <p class="text-[#6B7280] mb-6">Your appointment has been recorded for year 1447H.</p>
                    
                    <div class="bg-[#F9FAFB] border border-[#DBE2EF] rounded-xl p-5 mb-8 text-left space-y-3">
                        <div class="flex justify-between">
                            <span class="text-sm text-[#6B7280]">Appointment Date</span>
                            <span id="succ-date" class="text-sm font-bold text-[#112D4E]">—</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-sm text-[#6B7280]">Status</span>
                            <span class="text-sm font-bold text-amber-500">Pending</span>
                        </div>
                    </div>

                    <div class="p-4 rounded-lg bg-amber-50 border border-amber-200 text-amber-800 text-sm mb-6">
                        <strong>Important:</strong> Please bring your printed Takhmeen form for your appointment.
                    </div>

                    <a href="<?= BASE_URL ?>/vajebaat/" class="text-[#3F72AF] hover:underline font-medium">Back to Vajebaat Launcher</a>
                </div>
            </div>

            <!-- Back link -->
            <div id="bottom-back" class="text-center mt-6">
                <a href="<?= BASE_URL ?>/vajebaat/" class="text-[#3F72AF] text-sm hover:underline">← Back to Vajebaat</a>
            </div>

        </div>
    </div>
</div>

<script>
    const submitBtn = document.querySelector('[type="submit"]');

    async function handleBooking(e) {
        e.preventDefault();

        const its    = document.getElementById('apt-its').value.trim();
        const name   = document.getElementById('apt-name').value.trim();
        const mobile = document.getElementById('apt-mobile').value.trim();
        const date   = document.getElementById('apt-date').value;
        const remarks = document.getElementById('apt-remarks').value.trim();

        if (!/^\d{7,8}$/.test(its)) {
            alert("Please enter a valid 7 or 8-digit ITS number.");
            return;
        }
        if (!name) { alert("Please enter your full name."); return; }
        if (!mobile) { alert("Please enter your mobile number."); return; }
        if (!date) { alert("Please select a preferred date."); return; }

        // Loading state
        submitBtn.disabled = true;
        submitBtn.textContent = 'Booking…';

        try {
            const response = await fetch(window.API_BASE + '/api/vajebaat/appointments/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    its_number:     its,
                    name:           name,
                    mobile:         mobile,
                    preferred_date: date,
                    remarks:        remarks
                })
            });

            const data = await response.json();

            if (!response.ok) {
                // Extract first error message from DRF response
                const msg = typeof data === 'object'
                    ? Object.values(data).flat().join(' ')
                    : 'Booking failed. Please try again.';
                alert(msg);
                return;
            }

            // Success
            const d = new Date(data.preferred_date);
            document.getElementById('succ-date').textContent = d.toLocaleDateString('en-GB', {
                day: 'numeric', month: 'long', year: 'numeric'
            });

            document.getElementById('booking-container').classList.add('hidden');
            document.getElementById('bottom-back').classList.add('hidden');
            document.getElementById('success-view').classList.remove('hidden');
            window.scrollTo(0, 0);

        } catch (err) {
            alert('Network error. Please check your connection and try again.');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Confirm Appointment';
        }
    }
</script>

<?php include '../includes/footer.php'; ?>
