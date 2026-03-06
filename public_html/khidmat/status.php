<?php include '../includes/header.php'; ?>

<div class="min-h-screen p-4 sm:p-10 flex flex-col items-center bg-[#F9F7F7] animate-fadeIn">
    
    <!-- Hero Section -->
    <div class="max-w-2xl w-full text-center mb-10">
        <h1 class="text-3xl sm:text-4xl font-bold text-[#112D4E] mb-3 tracking-tight">Check Registration Status</h1>
        <p class="text-[#3F72AF] text-lg font-medium">Sherullah 1447H • Azaan &amp; Takhbira</p>
    </div>

    <!-- Search Form -->
    <div class="max-w-md w-full bg-white rounded-3xl shadow-xl p-6 sm:p-8 border border-[#DBE2EF] mb-8">
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
        </div>
    </div>
        
    <!-- Result Placeholder -->
    <div id="result-container" class="max-w-md w-full hidden">
        <!-- Content injected by JS -->
    </div>

</div>

<script src="<?= BASE_URL ?>/assets/js/api.js"></script>
<script src="<?= BASE_URL ?>/assets/js/main.js"></script>
    <style>
        .back-to-form {
            text-align: center;
            margin-top: 32px;
        }
        .btn-back {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 12px 24px;
            background: #112D4E;
            color: #fff;
            border-radius: 12px;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
            transition: all 0.2s ease;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .btn-back:hover {
            background: #1e3a5f;
            transform: translateY(-1px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }
        .btn-back:active {
            transform: translateY(0);
        }
    </style>

    <div class="back-to-form animate-fadeIn animate-delay-300">
        <a href="<?= BASE_URL ?>/khidmat/" class="btn-back">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
            Back to Registration Form
        </a>
    </div>

<script src="<?= BASE_URL ?>/assets/js/status.js"></script>

<?php include '../includes/footer.php'; ?>
