<?php include '../includes/header.php'; ?>

<div class="min-h-screen flex flex-col bg-[#F9F7F7] animate-fadeIn">
    <main class="flex-grow flex items-center justify-center px-4 py-12">
        <div class="w-full max-w-md bg-white border border-[#DBE2EF] rounded-2xl shadow-xl overflow-hidden">
            <!-- Header Section -->
            <div class="bg-white p-10 pb-2 text-center">
                <h1 class="text-3xl font-bold text-[#112D4E] tracking-tight">Welcome Back</h1>
                <div class="bg-[#3F72AF]/10 w-20 h-20 rounded-full flex items-center justify-center mx-auto mt-6">
                    <svg class="text-[#3F72AF] w-10 h-10" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
                </div>
                <p class="text-[#112D4E]/60 text-sm mt-3 font-medium">Login to Madras Jamaat Admin Portal</p>
            </div>

            <!-- Form Section -->
            <div class="p-10 pt-6 space-y-6">
                <form id="login-form" class="space-y-4">
                    
                    <div id="error-alert" class="hidden bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
                        <!-- Error Text -->
                    </div>

                    <div class="space-y-2">
                        <label for="its" class="block text-sm font-semibold text-[#112D4E]">
                            ITS Number
                        </label>
                        <div class="relative">
                            <div class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-3-3.87"></path><path d="M4 21v-2a4 4 0 0 1 3-3.87"></path><circle cx="12" cy="7" r="4"></circle></svg>
                            </div>
                            <input
                                id="its"
                                name="its"
                                type="text"
                                required
                                class="w-full bg-[#F9F7F7] border border-[#DBE2EF] focus:border-[#3F72AF] focus:ring-1 focus:ring-[#3F72AF] outline-none h-12 rounded-xl text-lg pl-12 pr-4 transition-all"
                                placeholder="Enter ITS Number"
                                maxlength="8"
                            />
                        </div>
                    </div>

                    <div class="space-y-2">
                        <label for="pass" class="block text-sm font-semibold text-[#112D4E]">
                            Password
                        </label>
                        <div class="relative group">
                            <div class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
                            </div>
                            <input
                                id="pass"
                                name="pass"
                                type="password"
                                required
                                class="w-full bg-[#F9F7F7] border border-[#DBE2EF] focus:border-[#3F72AF] focus:ring-1 focus:ring-[#3F72AF] outline-none h-12 rounded-xl text-lg pl-12 pr-12 transition-all"
                                placeholder="Enter password"
                            />
                            <button
                                type="button"
                                id="toggle-pass-btn"
                                class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
                            >
                                <svg id="eye-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                                <svg id="eye-off-icon" class="hidden" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line></svg>
                            </button>
                        </div>
                    </div>

                    <button
                        type="submit"
                        id="login-btn"
                        class="w-full bg-[#3F72AF] text-white py-4 rounded-xl font-bold hover:bg-[#112D4E] transition-all shadow-lg active:scale-[0.98] flex items-center justify-center mt-6"
                    >
                        Sign In
                    </button>
                </form>
            </div>
        </div>
    </main>
</div>

<script src="/assets/js/main.js"></script>
<script src="/assets/js/login.js"></script>

<?php include '../includes/footer.php'; ?>
