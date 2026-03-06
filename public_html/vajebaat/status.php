<?php include '../includes/header.php'; ?>

<div class="min-h-screen p-4 sm:p-10 flex flex-col items-center bg-[#F9F7F7]">

    <!-- Hero Section -->
    <div class="max-w-2xl w-full text-center mb-10">
        <h1 class="text-3xl sm:text-4xl font-bold text-[#112D4E] mb-3 tracking-tight">Appointment Status</h1>
        <p class="text-[#3F72AF] text-lg font-medium">Vajebaat &bull; Saifee Masjid Chennai</p>
    </div>

    <!-- Search Card -->
    <div class="max-w-md w-full bg-white rounded-3xl shadow-xl p-6 sm:p-8 border border-[#DBE2EF] mb-8">
        <div class="space-y-6">
            <div>
                <label for="vaj-its" class="block text-xs font-bold text-[#6B7280] uppercase tracking-wider mb-3 ml-1">Enter your ITS Number</label>
                <div class="relative">
                    <input
                        type="text"
                        id="vaj-its"
                        placeholder="8-digit ITS number"
                        maxlength="8"
                        inputmode="numeric"
                        class="w-full h-14 pl-4 pr-12 bg-[#F9FAFB] border-2 border-[#DBE2EF] rounded-2xl focus:outline-none focus:border-[#3F72AF] focus:ring-4 focus:ring-[#3F72AF]/10 transition-all text-[#112D4E] font-mono text-lg placeholder:font-sans placeholder:text-sm"
                    >
                    <button
                        type="button"
                        onclick="checkVajStatus()"
                        class="absolute right-3 top-1/2 -translate-y-1/2 text-[#3F72AF] hover:text-[#112D4E] transition-colors"
                        aria-label="Search"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="11" cy="11" r="8"></circle>
                            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                        </svg>
                    </button>
                </div>
            </div>

            <button
                id="vaj-search-btn"
                type="button"
                onclick="checkVajStatus()"
                class="w-full h-14 bg-[#112D4E] text-white rounded-2xl font-bold hover:bg-[#3F72AF] transition-all shadow-lg active:scale-[0.98] flex items-center justify-center gap-2 group"
            >
                <span>Check Status</span>
                <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="5" y1="12" x2="19" y2="12"></line>
                    <polyline points="12 5 19 12 12 19"></polyline>
                </svg>
            </button>
        </div>
    </div>

    <!-- Result Section -->
    <div id="vaj-result" class="max-w-md w-full hidden">
        <!-- content injected by JS -->
    </div>

    <!-- Back link -->
    <div class="mt-6">
        <a href="<?= BASE_URL ?>/vajebaat/" class="inline-flex items-center gap-2 px-5 py-3 bg-[#112D4E] text-white rounded-xl text-sm font-semibold hover:bg-[#1e3a5f] transition-all shadow">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
            Back to Vajebaat
        </a>
    </div>

</div>

<script>
function checkVajStatus() {
    var its = document.getElementById('vaj-its').value.trim();
    var result = document.getElementById('vaj-result');
    var btn = document.getElementById('vaj-search-btn');

    if (!/^\d{8}$/.test(its)) {
        result.innerHTML = '<div class="bg-white border border-[#FCA5A5] rounded-2xl p-6 text-center shadow-sm">'
            + '<p class="text-red-500 font-semibold">Please enter a valid 8-digit ITS number.</p></div>';
        result.classList.remove('hidden');
        return;
    }

    // Loading State
    btn.disabled = true;
    btn.innerHTML = '<span>Checking...</span>';
    result.classList.add('opacity-50');

    console.log("[Status] Checking status for ITS:", its);
    var apiUrl = window.API_BASE + '/api/vajebaat/appointments/check_status/?its=' + its;
    console.log("[Status] API URL:", apiUrl);

    fetch(apiUrl)
        .then(response => {
            if (response.status === 404) {
                throw new Error('NOT_FOUND');
            }
            if (!response.ok) {
                throw new Error('API_ERROR');
            }
            return response.json();
        })
        .then(data => {
            console.log("[Status] API Response:", data);
            
            // Format status color and label
            var statusClass = 'text-amber-500';
            var statusLabel = data.status;
            if (data.status === 'CONFIRMED') statusClass = 'text-green-600';
            if (data.status === 'CANCELLED') statusClass = 'text-red-500';
            if (data.status === 'COMPLETED') statusClass = 'text-blue-600';

            var dateVal = data.assigned_date || 'Not yet assigned';
            var slotVal = data.slot_time || 'TBD';

            result.innerHTML = '<div class="bg-white border border-[#DBE2EF] rounded-3xl p-6 sm:p-8 shadow-xl animate-in fade-in slide-in-from-bottom-4 duration-500">'
                + '<div class="w-16 h-16 bg-blue-50 rounded-full flex items-center justify-center mx-auto mb-6">'
                + '<svg class="w-8 h-8 text-[#3F72AF]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>'
                + '</div>'
                + '<div class="text-center mb-8">'
                + '<h3 class="text-[#112D4E] font-bold text-xl mb-1">' + data.name + '</h3>'
                + '<p class="text-[#3F72AF] font-mono font-medium tracking-widest text-sm">' + data.its_masked + '</p>'
                + '</div>'
                + '<div class="space-y-4">'
                + '<div class="p-4 bg-[#F9FAFB] rounded-2xl flex justify-between items-center"><span class="text-xs font-bold text-[#6B7280] uppercase tracking-tighter">Status</span><span class="font-bold ' + statusClass + '">' + statusLabel + '</span></div>'
                + '<div class="p-4 bg-[#F9FAFB] rounded-2xl flex justify-between items-center"><span class="text-xs font-bold text-[#6B7280] uppercase tracking-tighter">Date</span><span class="font-bold text-[#112D4E]">' + dateVal + '</span></div>'
                + '<div class="p-4 bg-[#F9FAFB] rounded-2xl flex justify-between items-center"><span class="text-xs font-bold text-[#6B7280] uppercase tracking-tighter">Slot</span><span class="font-bold text-[#112D4E]">' + slotVal + '</span></div>'
                + '</div>'
                + '</div>';
        })
        .catch(error => {
            console.error("[Status] Error:", error);
            if (error.message === 'NOT_FOUND') {
                result.innerHTML = '<div class="bg-white border border-[#DBE2EF] rounded-3xl p-8 text-center shadow-xl animate-in fade-in duration-300">'
                    + '<div class="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-6">'
                    + '<svg class="w-8 h-8 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9.172 9.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>'
                    + '</div>'
                    + '<p class="text-[#112D4E] font-bold text-xl mb-2">Not Found</p>'
                    + '<p class="text-[#6B7280] text-sm leading-relaxed mb-6">No appointment record found for ITS <span class="font-mono font-bold">' + its + '</span>. Please ensure the number is correct or book an appointment.</p>'
                    + '<a href="' + window.BASE_URL + '/vajebaat/" class="inline-flex items-center gap-2 text-[#3F72AF] font-bold hover:underline">Book Appointment →</a>'
                    + '</div>';
            } else {
                result.innerHTML = '<div class="bg-white border border-red-100 rounded-3xl p-8 text-center shadow-xl">'
                    + '<p class="text-red-600 font-bold mb-2">Connection Error</p>'
                    + '<p class="text-gray-500 text-sm">Unable to reach the server. Please try again later.</p>'
                    + '</div>';
            }
        })
        .finally(() => {
            btn.disabled = false;
            btn.innerHTML = '<span>Check Status</span>' + 
                '<svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>';
            result.classList.remove('opacity-50');
            result.classList.remove('hidden');
        });
}

// Allow Enter key to trigger search
document.getElementById('vaj-its').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') checkVajStatus();
});
</script>

<?php include '../includes/footer.php'; ?>

