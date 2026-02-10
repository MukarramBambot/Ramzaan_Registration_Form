<?php include 'includes/header.php'; ?>

<!-- Content Wrapper -->
<div id="registration-page" class="min-h-screen bg-[#F9F7F7]">
    <!-- 1) Header Section -->
    <div class="bg-[#112D4E] py-8 px-4 sm:px-6 lg:px-8 text-center sm:text-left">
        <div class="max-w-2xl mx-auto">
            <h1 class="text-3xl text-white font-normal mb-1">
                Azaan & Takhbira Registration
            </h1>
            <p class="text-[#DBE2EF] text-lg font-light">
                Submit your intent for Ramadaan duties
            </p>
        </div>
    </div>

    <div class="py-8 px-4 sm:px-6 lg:px-8">
        <div class="max-w-2xl mx-auto space-y-6">

            <!-- Success State (Hidden by default) -->
            <div id="success-view" class="hidden w-full bg-white rounded-lg shadow-sm border border-[#DBE2EF] overflow-hidden text-center p-12">
                <div class="w-16 h-16 bg-[#DBE2EF] rounded-full flex items-center justify-center mx-auto mb-6">
                    <svg class="w-8 h-8 text-[#3F72AF]" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                </div>
                <h2 class="text-3xl text-[#112D4E] mb-2 font-normal">Registration Received</h2>
                <p class="text-[#6B7280]">Your intent for Ramadaan duties has been recorded.</p>
                <button id="reset-form-btn" class="mt-8 text-[#3F72AF] hover:underline">
                    Submit another response
                </button>
                <div class="mt-4">
                    <a href="/status.php" class="text-[#112D4E] text-sm hover:underline">Check Allocation Status</a>
                </div>
            </div>

            <!-- 2) Form Card -->
            <form id="registration-form" class="bg-white rounded-lg shadow-sm border border-[#DBE2EF] overflow-hidden">
                <div class="h-2 bg-[#3F72AF] w-full"></div>

                <div class="p-8 space-y-8">

                    <!-- a) FULL NAME -->
                    <div class="space-y-2">
                        <label for="fullName" class="block text-xs font-bold text-[#6B7280] uppercase tracking-wider">
                            Full Name
                        </label>
                        <input
                            type="text"
                            id="fullName"
                            name="fullName"
                            required
                            class="w-full h-12 px-4 bg-white border border-[#DBE2EF] rounded focus:outline-none focus:border-[#3F72AF] focus:ring-1 focus:ring-[#3F72AF] transition-all text-[#112D4E] placeholder-[#9CA3AF]"
                            placeholder="Enter your full name"
                        />
                    </div>

                    <!-- b) ITS NUMBER -->
                    <div class="space-y-2">
                        <label for="itsNumber" class="block text-xs font-bold text-[#6B7280] uppercase tracking-wider">
                            ITS Number
                        </label>
                        <input
                            type="text"
                            id="itsNumber"
                            name="itsNumber"
                            required
                            class="w-full h-12 px-4 bg-white border border-[#DBE2EF] rounded focus:outline-none focus:border-[#3F72AF] focus:ring-1 focus:ring-[#3F72AF] transition-all text-[#112D4E] placeholder-[#9CA3AF]"
                            placeholder="Enter your ITS number"
                        />
                    </div>

                    <!-- c) EMAIL ADDRESS -->
                    <div class="space-y-2">
                        <label for="email" class="block text-xs font-bold text-[#6B7280] uppercase tracking-wider">
                            Email Address
                        </label>
                        <input
                            type="email"
                            id="email"
                            name="email"
                            required
                            class="w-full h-12 px-4 bg-white border border-[#DBE2EF] rounded focus:outline-none focus:border-[#3F72AF] focus:ring-1 focus:ring-[#3F72AF] transition-all text-[#112D4E] placeholder-[#9CA3AF]"
                            placeholder="Enter your email address"
                        />
                    </div>

                    <!-- New) PHONE NUMBER -->
                    <div class="space-y-2">
                        <label for="phoneNumber" class="block text-xs font-bold text-[#6B7280] uppercase tracking-wider">
                            WhatsApp Number
                        </label>
                        <input
                            type="tel"
                            id="phoneNumber"
                            name="phoneNumber"
                            required
                            class="w-full h-12 px-4 bg-white border border-[#DBE2EF] rounded focus:outline-none focus:border-[#3F72AF] focus:ring-1 focus:ring-[#3F72AF] transition-all text-[#112D4E] placeholder-[#9CA3AF]"
                            placeholder="Enter your WhatsApp number for reminders"
                        />
                    </div>

                    <!-- d) REGISTER FOR -->
                    <div class="space-y-3">
                        <label class="block text-xs font-bold text-[#6B7280] uppercase tracking-wider">
                            Register For <span class="text-red-500">*</span>
                        </label>
                        <div class="space-y-2">
                            <label class="flex items-center p-4 border border-[#DBE2EF] rounded hover:bg-[#F9FAFB] cursor-pointer transition-colors">
                                <input type="radio" name="preference" value="AZAAN" checked class="w-5 h-5 text-[#3F72AF] border-gray-300 focus:ring-[#3F72AF]">
                                <span class="ml-3 text-[#112D4E]">Azaan</span>
                            </label>
                            <label class="flex items-center p-4 border border-[#DBE2EF] rounded hover:bg-[#F9FAFB] cursor-pointer transition-colors">
                                <input type="radio" name="preference" value="TAKHBIRA" class="w-5 h-5 text-[#3F72AF] border-gray-300 focus:ring-[#3F72AF]">
                                <span class="ml-3 text-[#112D4E]">Takhbira</span>
                            </label>
                            <label class="flex items-center p-4 border border-[#DBE2EF] rounded hover:bg-[#F9FAFB] cursor-pointer transition-colors">
                                <input type="radio" name="preference" value="BOTH" class="w-5 h-5 text-[#3F72AF] border-gray-300 focus:ring-[#3F72AF]">
                                <span class="ml-3 text-[#112D4E]">Azaan & Takhbira</span>
                            </label>
                        </div>
                    </div>

                    <!-- e) UPLOAD AUDITION FILES -->
                    <div class="space-y-2">
                        <label class="block text-xs font-bold text-[#6B7280] uppercase tracking-wider">
                            Upload Audition Files <span class="text-red-500">*</span>
                        </label>
                        <p class="text-sm text-[#9CA3AF] mb-2">Audio/Video only. Max 5 files. Max 10MB each.</p>

                        <label class="flex flex-col items-center justify-center w-full h-40 border-2 border-dashed border-[#DBE2EF] rounded-lg hover:bg-[#F9FAFB] cursor-pointer transition-colors group">
                            <div class="flex flex-col items-center justify-center pt-5 pb-6">
                                <div class="w-12 h-12 bg-[#DBE2EF] rounded-full flex items-center justify-center mb-3 group-hover:bg-[#d1d9e8] transition-colors">
                                    <svg class="w-6 h-6 text-[#3F72AF]" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
                                </div>
                                <p class="text-sm text-[#6B7280] font-medium">Click to upload</p>
                            </div>
                            <input type="file" id="fileInput" class="hidden" multiple accept="audio/*,video/*">
                        </label>

                        <div id="file-list" class="grid grid-cols-1 gap-2 mt-2">
                            <!-- JS will populate files here -->
                        </div>
                    </div>

                    <!-- 4) Submit Button -->
                    <div class="pt-4">
                        <button
                            type="submit"
                            id="submit-btn"
                            class="w-full h-14 bg-[#112D4E] text-white font-medium rounded shadow-sm hover:bg-[#2D5A8F] active:bg-[#0E2744] transition-all disabled:opacity-70 disabled:cursor-not-allowed flex items-center justify-center text-lg"
                        >
                            <span>Submit</span>
                        </button>
                        <div class="text-center mt-4">
                            <a href="/status.php" class="text-[#3F72AF] text-sm hover:underline">Already registered? Check status</a>
                        </div>
                    </div>

                </div>
            </form>

            <div class="text-center">
                <p class="text-[#9CA3AF] text-xs">
                    © Sherullah 1447H • Azaan & Takhbira Registration
                </p>
            </div>

        </div>
    </div>
</div>

<script src="/assets/js/main.js"></script>
<script src="/assets/js/home.js"></script>

<?php include 'includes/footer.php'; ?>
