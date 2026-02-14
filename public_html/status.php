<?php include 'includes/header.php'; ?>

<div class="min-h-screen p-4 sm:p-10 flex flex-col items-center bg-[#F9F7F7] animate-fadeIn">
    
    <!-- Hero Section -->
    <div class="max-w-2xl w-full text-center mb-10">
        <h1 class="text-3xl sm:text-4xl font-bold text-[#112D4E] mb-3 tracking-tight">Check Registration Status</h1>
        <p class="text-[#3F72AF] text-lg font-medium">Sherullah 1447H • Azaan & Takhbira</p>
    </div>

    <!-- Search Form -->
    <div class="max-w-md w-full bg-white rounded-3xl shadow-xl p-8 border border-[#DBE2EF] mb-8">
        <div class="space-y-6">
            <div>
                <label for="its-number" class="block text-xs font-bold text-[#6B7280] uppercase tracking-wider mb-3 ml-1">Enter your ITS Number</label>
                <div class="relative">
                    <input 
                        type="text" 
                        id="its-number" 
                        placeholder="8-digit ITS number"
                        class="w-full h-14 pl-4 pr-12 bg-[#F9FAFB] border-2 border-[#DBE2EF] rounded-2xl focus:outline-none focus:border-[#3F72AF] focus:ring-4 focus:ring-[#3F72AF]/10 transition-all text-[#112D4E] font-mono text-lg placeholder:font-sans placeholder:text-sm"
                    >
                    <button 
                        type="button"
                        onclick="checkStatus()"
                        class="absolute right-3 top-1/2 -translate-y-1/2 text-[#3F72AF] hover:text-[#112D4E] transition-colors"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                    </button>
                </div>
            </div>
            
            <button 
                id="search-btn"
                type="button"
                onclick="checkStatus()"
                class="w-full h-14 bg-[#112D4E] text-white rounded-2xl font-bold hover:bg-[#3F72AF] transition-all shadow-lg active:scale-[0.98] flex items-center justify-center gap-2 group mt-4"
            >
                <span>Track Status</span>
                <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
            </button>
            
    <!-- Result Placeholder -->
    <div id="result-container" class="max-w-md w-full hidden">
        <!-- Content injected by JS -->
    </div>

</div>

<script src="/assets/js/api.js"></script>
<script src="/assets/js/main.js"></script>
<script src="/assets/js/status.js"></script>

<?php include 'includes/footer.php'; ?>
