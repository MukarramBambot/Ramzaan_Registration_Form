<?php include 'includes/header.php'; ?>

<!-- Home / Landing Page -->
<div class="min-h-screen bg-[#F9F7F7] flex flex-col items-center justify-center px-4 py-16">

    <!-- Portal Header -->
    <div class="text-center mb-12">
        <div class="w-16 h-16 bg-[#DBE2EF] rounded-full flex items-center justify-center mx-auto mb-5">
            <svg class="w-8 h-8 text-[#3F72AF]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 21h16.5M4.5 3h15M5.25 3v18m13.5-18v18M9 6.75h1.5m-1.5 3h1.5m-1.5 3h1.5m3-6H15m-1.5 3H15m-1.5 3H15M9 21v-3.375c0-.621.504-1.125 1.125-1.125h3.75c.621 0 1.125.504 1.125 1.125V21" /></svg>
        </div>
        <h1 class="text-4xl font-semibold text-[#112D4E] mb-2 tracking-tight">Madras Jamaat Portal</h1>
        <p class="text-[#6B7280] text-lg">Saifee Masjid Chennai</p>
    </div>

    <!-- Action Buttons -->
    <div class="w-full max-w-sm space-y-4">

        <!-- Khidmat Registration -->
        <a href="<?= BASE_URL ?>/khidmat/"
           class="flex items-center justify-between w-full px-6 py-5 bg-[#112D4E] text-white rounded-xl shadow-sm hover:bg-[#1e3d6f] active:bg-[#0d2340] transition-all group">
            <div class="flex items-center gap-4">
                <div class="w-10 h-10 bg-white/10 rounded-lg flex items-center justify-center group-hover:bg-white/15 transition-colors">
                    <svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8"><path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125" /></svg>
                </div>
                <div>
                    <div class="font-semibold text-base">Khidmat Registration</div>
                    <div class="text-[#DBE2EF] text-xs mt-0.5">Azaan, Takhbira, Sanaa &amp; more</div>
                </div>
            </div>
            <svg class="w-5 h-5 text-[#DBE2EF] group-hover:translate-x-1 transition-transform" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" /></svg>
        </a>

        <!-- Vajebaat -->
        <a href="<?= BASE_URL ?>/vajebaat/"
           class="flex items-center justify-between w-full px-6 py-5 bg-white border border-[#DBE2EF] text-[#112D4E] rounded-xl shadow-sm hover:border-[#3F72AF] hover:bg-[#F0F4FA] active:bg-[#e8eef8] transition-all group">
            <div class="flex items-center gap-4">
                <div class="w-10 h-10 bg-[#DBE2EF] rounded-lg flex items-center justify-center group-hover:bg-[#c8d4e8] transition-colors">
                    <svg class="w-5 h-5 text-[#3F72AF]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25zM6.75 12h.008v.008H6.75V12zm0 3h.008v.008H6.75V15zm0 3h.008v.008H6.75V18z" /></svg>
                </div>
                <div>
                    <div class="font-semibold text-base">Vajebaat</div>
                    <div class="text-[#6B7280] text-xs mt-0.5">Takhmeen &amp; Appointments</div>
                </div>
            </div>
            <svg class="w-5 h-5 text-[#9CA3AF] group-hover:translate-x-1 transition-transform" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" /></svg>
        </a>

    </div>

    <!-- Footer note -->
    <p class="mt-10 text-xs text-[#9CA3AF]">Sherullah Moazzam 1447H &bull; Saifee Masjid Chennai</p>

</div>

<?php include 'includes/footer.php'; ?>

