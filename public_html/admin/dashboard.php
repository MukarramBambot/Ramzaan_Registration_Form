<?php include '../includes/header.php'; ?>

<!-- Content Wrapper -->
<div class="min-h-screen bg-[#F9F7F7]">
    
    <!-- Header -->
    <div class="bg-[#112D4E] py-5 px-6 shadow-md">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
                <div class="flex flex-col md:flex-row md:items-center gap-2 md:gap-6 mb-1">
                    <h1 class="text-xl md:text-2xl text-white font-normal">
                        Azaan & Takhbira Duty Roster
                    </h1>
                    <div class="flex items-center gap-2 mt-2 md:mt-0 md:ml-4 overflow-x-auto pb-2 md:pb-0">
                        <a href="/admin/dashboard.php" class="whitespace-nowrap px-3 py-1.5 rounded-md bg-[#3F72AF] text-white text-sm font-medium flex items-center gap-2">
                            <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line></svg>
                            Duty Roster
                        </a>
                        <!-- Master Sheet Link (Placeholder for now) -->
                        <a href="/admin/master-sheet.php" class="whitespace-nowrap px-3 py-1.5 rounded-md text-[#DBE2EF] hover:text-white hover:bg-white/10 text-sm font-medium transition-all flex items-center gap-2">
                            <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="8" y1="13" x2="16" y2="13"></line><line x1="8" y1="17" x2="16" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                            Master Sheet
                        </a>
                        <a href="/admin/khidmat-requests.php" class="whitespace-nowrap px-3 py-1.5 rounded-md text-[#DBE2EF] hover:text-white hover:bg-white/10 text-sm font-medium transition-all flex items-center gap-2">
                            <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M22 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
                            Requests
                        </a>
                    </div>
                </div>
                <p class="text-[#DBE2EF] text-sm font-light">
                    Sherullah 1447H – Excel-style Management
                </p>
            </div>
            <div class="flex flex-wrap items-center gap-3 md:gap-4 text-[#DBE2EF] text-xs md:text-sm">
                <div class="flex items-center gap-2 bg-white/5 px-2 py-1 rounded">
                    <svg class="w-3.5 h-3.5" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                    <span id="header-days-count">30 d</span>
                </div>
                <div class="flex items-center gap-2 bg-white/5 px-2 py-1 rounded">
                    <svg class="w-3.5 h-3.5" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
                    <span id="header-locked-count">0 locked</span>
                </div>
                <button
                    onclick="logout()"
                    class="ml-auto md:ml-4 px-3 py-1.5 rounded-md bg-red-500/20 hover:bg-red-500/40 text-white text-xs md:text-sm font-medium transition-all"
                >
                    Logout
                </button>
            </div>
        </div>
    </div>

    <!-- Success Message Banner -->
    <div id="success-banner" class="hidden bg-green-50 border-b-2 border-green-200 px-6 py-3">
        <div class="flex items-center gap-2 text-green-800">
            <svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
            <span class="text-sm font-medium" id="success-message-text"></span>
        </div>
    </div>

    <!-- Main Grid Container -->
    <div class="p-6">
        <div id="loading-state" class="bg-white shadow-lg border border-[#DBE2EF] rounded-lg p-20 flex flex-col items-center justify-center space-y-4">
            <svg class="w-10 h-10 text-[#3F72AF] animate-spin" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-6.219-8.56"></path></svg>
            <p class="text-[#112D4E] font-medium">Loading roster data...</p>
        </div>

        <div id="roster-grid-container" class="hidden bg-white shadow-lg border border-[#DBE2EF] rounded-lg overflow-hidden">
            <div class="overflow-auto max-h-[calc(100vh-220px)]">
                <table class="w-full border-collapse" id="roster-table">
                    <thead>
                        <tr class="bg-[#F9F7F7] border-b-2 border-[#DBE2EF] sticky top-0 z-20" id="roster-header-row">
                            <!-- JS will populate -->
                        </tr>
                    </thead>
                    <tbody id="roster-body">
                        <!-- JS will populate -->
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Summary Stats (Footer of Grid) -->
        <div id="summary-stats" class="hidden mt-4 flex flex-col md:flex-row gap-2 md:gap-4 text-xs md:text-sm">
            <div class="bg-white border border-[#DBE2EF] rounded px-3 py-1.5 md:px-4 md:py-2">
                <span class="text-[#6B7280]">Total Assignments: </span>
                <span class="font-bold text-[#112D4E]" id="stat-total">0</span>
            </div>
            <div class="bg-white border border-[#DBE2EF] rounded px-3 py-1.5 md:px-4 md:py-2">
                <span class="text-[#6B7280]">Locked: </span>
                <span class="font-bold text-[#112D4E]" id="stat-locked">0</span>
            </div>
            <div class="bg-white border border-[#DBE2EF] rounded px-3 py-1.5 md:px-4 md:py-2">
                <span class="text-[#6B7280]">Completion: </span>
                <span class="font-bold text-[#112D4E]" id="stat-completion">0%</span>
            </div>
        </div>
    </div>

</div>

<!-- Details Panel (Hidden by default) -->
<div id="details-panel-container">
    <!-- JS will inject HTML here -->
</div>

<!-- Audition Preview Modal (Hidden by default) -->
<div id="audition-modal-container"></div>

<script src="/assets/js/main.js"></script>
<script src="/assets/js/audition-modal.js"></script>
<script src="/assets/js/dashboard.js"></script>

<script>
    function logout() {
        localStorage.clear();
        window.location.href = '/admin/login.php';
    }
</script>

<?php include '../includes/footer.php'; ?>
