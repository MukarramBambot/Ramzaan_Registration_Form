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

    if (!/^\d{8}$/.test(its)) {
        result.innerHTML = '<div class="bg-white border border-[#FCA5A5] rounded-2xl p-6 text-center">'
            + '<p class="text-red-500 font-semibold">Please enter a valid 8-digit ITS number.</p></div>';
        result.classList.remove('hidden');
        return;
    }

    // Placeholder response — replace with real API call when backend is ready
    // Mock data for demo
    var mockData = {
        "12345678": { date: "15th March 2026", status: "Confirmed", notes: "Please bring your original Takhmeen form." },
        "87654321": { date: "20th March 2026", status: "Pending", notes: "Awaiting sector incharge approval." }
    };

    var data = mockData[its];

    if (data) {
        result.innerHTML = '<div class="bg-white border border-[#DBE2EF] rounded-2xl p-6 shadow">'
            + '<div class="w-12 h-12 bg-green-50 rounded-full flex items-center justify-center mx-auto mb-4">'
            + '<svg class="w-6 h-6 text-green-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" /></svg>'
            + '</div>'
            + '<div class="text-center mb-6">'
            + '<p class="text-[#112D4E] font-bold text-lg">ITS: ' + its + '</p>'
            + '</div>'
            + '<div class="space-y-3 text-sm">'
            + '<div class="flex justify-between py-2 border-b border-gray-50"><span class="text-gray-500">Appointment Date</span><span class="font-bold text-[#112D4E]">' + data.date + '</span></div>'
            + '<div class="flex justify-between py-2 border-b border-gray-50"><span class="text-gray-500">Status</span><span class="font-bold ' + (data.status === 'Confirmed' ? 'text-green-600' : 'text-amber-500') + '">' + data.status + '</span></div>'
            + '<div class="pt-2"><p class="text-gray-500 mb-1 font-medium">Admin Notes:</p><p class="text-[#112D4E] bg-gray-50 p-3 rounded-lg italic">"' + data.notes + '"</p></div>'
            + '</div>'
            + '</div>';
    } else {
        result.innerHTML = '<div class="bg-white border border-[#DBE2EF] rounded-2xl p-6 text-center shadow">'
            + '<div class="w-12 h-12 bg-[#DBE2EF] rounded-full flex items-center justify-center mx-auto mb-4">'
            + '<svg class="w-6 h-6 text-[#3F72AF]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5" /></svg>'
            + '</div>'
            + '<p class="text-[#112D4E] font-semibold text-lg mb-1">ITS: ' + its + '</p>'
            + '<p class="text-[#6B7280] text-sm">No appointment record found. Please book one <a href="' + window.BASE_URL + '/vajebaat/appointment.php" class="text-[#3F72AF] hover:underline">here</a>.</p>'
            + '</div>';
    }
    result.classList.remove('hidden');
}

// Allow Enter key to trigger search
document.getElementById('vaj-its').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') checkVajStatus();
});
</script>

<?php include '../includes/footer.php'; ?>

