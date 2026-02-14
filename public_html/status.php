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
                    <div class="absolute right-4 top-1/2 -translate-y-1/2 text-[#3F72AF]">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                    </div>
                </div>
            </div>
            
            <button 
                id="search-btn"
                onclick="checkStatus()"
                class="w-full h-14 bg-[#112D4E] text-white rounded-2xl font-bold hover:bg-[#3F72AF] transition-all shadow-lg active:scale-[0.98] flex items-center justify-center gap-2 group"
            >
                <span>Track Status</span>
                <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
            </button>
        </div>
    </div>

    <!-- Result Placeholder -->
    <div id="result-container" class="max-w-md w-full hidden">
        <!-- Content injected by JS -->
    </div>

</div>

<script src="/assets/js/api.js"></script>
<script src="/assets/js/main.js"></script>

<script>
    async function checkStatus() {
        const btn = document.getElementById('search-btn');
        const its = document.getElementById('its-number').value.trim();
        const container = document.getElementById('result-container');

        if (!its) {
            showDialog({ variant: 'info', title: 'Input Required', message: 'Please enter your ITS number to check the status.' });
            return;
        }

        // Loading state
        const originalHTML = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = `<svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> Searching...`;

        try {
            const res = await apiFetch(`/api/registrations/search/?its=${its}`, { requireAuth: false });
            
            if (!res.ok) {
                if (res.status === 404) {
                    renderError("Registration Not Found", "No record found for this ITS number. Please ensure you have registered.");
                } else {
                    throw new Error("Server error occurred");
                }
                return;
            }

            const data = await res.json();
            renderResult(data);

        } catch (err) {
            renderError("Connection Error", "Unable to reach the server. Please try again later.");
        } finally {
            btn.disabled = false;
            btn.innerHTML = originalHTML;
            container.classList.remove('hidden');
            container.scrollIntoView({ behavior: 'smooth' });
        }
    }

    function renderResult(data) {
        const container = document.getElementById('result-container');
        

        const statusLabel = data.status === 'ALLOTTED' ? 'Allotted' : 'Pending Review';
        const colorClass = data.status === 'ALLOTTED' ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700';

        container.innerHTML = `
            <div class="bg-white rounded-3xl shadow-xl border border-[#DBE2EF] overflow-hidden animate-zoomIn">
                <div class="bg-[#112D4E] p-6 text-center">
                    <div class="inline-flex px-3 py-1 rounded-full ${colorClass} text-[10px] font-bold tracking-widest uppercase mb-3">
                        ${statusLabel}
                    </div>
                    <h3 class="text-white text-xl font-bold">${data.full_name}</h3>
                    <p class="text-[#DBE2EF]/60 text-sm font-mono mt-1">${data.its_number}</p>
                </div>
                
                <div class="p-8 space-y-6">
                    <div class="flex items-center justify-between border-b border-[#F9F7F7] pb-4">
                        <span class="text-[#6B7280] text-sm">Preference</span>
                        <span class="text-[#112D4E] font-bold text-sm tracking-wide uppercase">${data.register_for}</span>
                    </div>

                    ${data.status === 'ALLOTTED' ? `
                        <div class="bg-green-50 rounded-2xl p-4 border border-green-100">
                            <p class="text-green-800 text-sm font-medium flex items-center gap-2">
                                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
                                Assignment Confirmed!
                            </p>
                            <p class="text-green-700/70 text-xs mt-1">Please check the official roster or wait for your WhatsApp notification for details.</p>
                        </div>
                    ` : `
                        <div class="bg-amber-50 rounded-2xl p-4 border border-amber-100">
                            <p class="text-amber-800 text-sm font-medium flex items-center gap-2">
                                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                                Review in Progress
                            </p>
                            <p class="text-amber-700/70 text-xs mt-1">Assignments will be finalized soon. You will receive a notification once confirmed.</p>
                        </div>
                    `}
                </div>
            </div>
        `;
    }

    function renderError(title, msg) {
        const container = document.getElementById('result-container');
        container.innerHTML = `
            <div class="bg-white rounded-3xl shadow-lg border border-red-100 p-8 text-center animate-zoomIn">
                <div class="w-16 h-16 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg class="text-red-500 w-8 h-8" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                </div>
                <h3 class="text-[#112D4E] font-bold text-lg">${title}</h3>
                <p class="text-[#6B7280] text-sm mt-1 mb-6">${msg}</p>
                <a href="/" class="text-[#3F72AF] text-sm font-bold hover:underline">Return to registration form</a>
            </div>
        `;
    }
</script>

<?php include 'includes/footer.php'; ?>
