<?php include '../includes/header.php'; ?>

<!-- Content Wrapper -->
<div class="min-h-screen bg-[#F9F7F7]">
    
    <!-- Header -->
    <div class="bg-[#112D4E] py-5 px-6 shadow-md">
        <div class="flex items-center justify-between">
            <div>
                <div class="flex items-center gap-6 mb-1">
                    <h1 class="text-2xl text-white font-normal">
                        Master Sheet
                    </h1>
                    <div class="flex items-center gap-2 ml-4">
                        <a href="/admin/dashboard.php" class="px-3 py-1.5 rounded-md text-[#DBE2EF] hover:text-white hover:bg-white/10 text-sm font-medium transition-all flex items-center gap-2">
                             <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line></svg>
                            Duty Roster
                        </a>
                        <a href="/admin/master-sheet.php" class="px-3 py-1.5 rounded-md bg-[#3F72AF] text-white text-sm font-medium flex items-center gap-2">
                           <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="8" y1="13" x2="16" y2="13"></line><line x1="8" y1="17" x2="16" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                            Master Sheet
                        </a>
                    </div>
                </div>
                <p class="text-[#DBE2EF] text-sm font-light">
                    Sherullah 1447H – Central Database
                </p>
            </div>
             <div class="flex items-center gap-4 text-[#DBE2EF] text-sm">
                <button
                    onclick="logout()"
                    class="ml-4 px-3 py-1.5 rounded-md bg-red-500/20 hover:bg-red-500/40 text-white text-sm font-medium transition-all"
                >
                    Logout
                </button>
            </div>
        </div>
    </div>

    <!-- Main Content -->
    <div class="p-6 flex items-center justify-center min-h-[500px]">
        <div class="text-center">
            <svg class="w-16 h-16 text-[#DBE2EF] mx-auto mb-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="8" y1="13" x2="16" y2="13"></line><line x1="8" y1="17" x2="16" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
            <h2 class="text-xl font-bold text-[#112D4E]">Master Sheet View</h2>
            <p class="text-[#6B7280] mt-2">This module is correctly initialized in the PHP structure.</p>
            <p class="text-[#6B7280] text-sm">(Placeholder as per migration plan)</p>
        </div>
    </div>

</div>

<script>
    function logout() {
        localStorage.clear();
        window.location.href = '/admin/login.php';
    }
</script>

<?php include '../includes/footer.php'; ?>
