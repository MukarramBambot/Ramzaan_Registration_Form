<?php include 'includes/header.php'; ?>

<!-- Content Wrapper -->
<div id="registration-page" class="min-h-screen bg-[#F9F7F7]">
    <!-- 1) Header Section -->
    <div class="bg-[#112D4E] py-8 px-4 sm:px-6 lg:px-8 text-center sm:text-left">
        <div class="max-w-2xl mx-auto">
            <h1 class="text-3xl text-white font-normal mb-1">
                Azaan & Takhbira Registration - Sherullah Moazzam 1447
            </h1>
            <p class="text-[#DBE2EF] text-lg font-light">
                Saifee Masjid Chennai Only
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
                <p class="text-[#6B7280]">Your intent for Ramadaan Khidmat has been recorded.</p>
                <button id="reset-form-btn" class="mt-8 text-[#3F72AF] hover:underline">
                    Submit another response
                </button>
                <div class="mt-4">
                    <a href="/status.php" class="text-[#112D4E] text-sm hover:underline">Check Allocation Status</a>
                </div>
            </div>

            <!-- Khidmat Practice Section -->
            <section class="khidmat-practice-section bg-white rounded-lg shadow-sm border border-[#DBE2EF] overflow-hidden">
                <div class="h-2 bg-[#3F72AF] w-full"></div>
                <div class="p-6 space-y-4">
                    <h2 class="text-2xl text-[#112D4E] font-normal">🕌 Khidmat Practice Materials</h2>
                    <p class="text-sm text-[#6B7280]">Before submitting your audition for Khidmat, please review and practice using the reference materials below.</p>

                    <ul class="space-y-2">
                        <li class="p-3 border border-[#E6EDF7] rounded flex items-start justify-between">
                            <div>
                                <strong class="text-[#112D4E]">Azaan:</strong>
                                <div class="text-sm text-[#6B7280]">Practice Audio</div>
                            </div>
                            <div>
                                <a href="https://srv1827-files.hstgr.io/b769b84a5cac0666/files/public_html/assets/Pratice%20Files/Azaan.mp3" target="_blank" rel="noopener noreferrer" class="text-[#3F72AF] hover:underline">Watch Practice Audio</a>
                            </div>
                        </li>

                        <li class="p-3 border border-[#E6EDF7] rounded flex items-start justify-between">
                            <div>
                                <strong class="text-[#112D4E]">Takbira:</strong>
                                <div class="text-sm text-[#6B7280]">Practice Audio</div>
                            </div>
                            <div>
                                <a href="/var/www/Ramzaan_Registration_Form/public_html/assets/pratice files/Takbira.mp4" target="_blank" rel="noopener noreferrer" class="text-[#3F72AF] hover:underline">Watch Practice Audio</a>
                            </div>
                        </li>

                        <li class="p-3 border border-[#E6EDF7] rounded flex items-start justify-between">
                            <div>
                                <strong class="text-[#112D4E]">Sanaa:</strong>
                                <div class="text-sm text-[#6B7280]">Practice Reference</div>
                            </div>
                            <div>
                                <a href="https://youtu.be/qwXfSJ4uG-Y?si=b7s8XDt4FJNgrq4D" target="_blank" rel="noopener noreferrer" class="text-[#3F72AF] hover:underline">Watch Reference</a>
                            </div>
                        </li>

                        <li class="p-3 border border-[#E6EDF7] rounded flex items-start justify-between">
                            <div>
                                <strong class="text-[#112D4E]">Yasin (Ruku Wise):</strong>
                                <div class="text-sm text-[#6B7280]">Practice Folder</div>
                            </div>
                            <div>
                                <a href="https://drive.google.com/drive/folders/1uVSCvLv_QBgOjl8DZXjWtYnqaa2HPTRd?usp=drive_link" target="_blank" rel="noopener noreferrer" class="text-[#3F72AF] hover:underline">Open Folder</a>
                            </div>
                        </li>
                    </ul>

                    <div class="mt-2 p-3 rounded border-l-4 border-[#F59E0B] bg-[#FFFBEB]">
                        <div class="text-sm text-[#92400E]">📌 Please ensure you are well prepared before submitting your Khidmat audition. Auditions will be reviewed strictly; please follow the official format.</div>
                    </div>
                </div>
            </section>

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
                            name="full_name"
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
                            name="its_number"
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
                            name="phone_number"
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
                                <input type="checkbox" name="preference" value="Azaan" checked class="w-5 h-5 text-[#3F72AF] border-gray-300 focus:ring-[#3F72AF]">
                                <span class="ml-3 text-[#112D4E]">Azaan</span>
                            </label>
                            <label class="flex items-center p-4 border border-[#DBE2EF] rounded hover:bg-[#F9FAFB] cursor-pointer transition-colors">
                                <input type="checkbox" name="preference" value="Takhbira" class="w-5 h-5 text-[#3F72AF] border-gray-300 focus:ring-[#3F72AF]">
                                <span class="ml-3 text-[#112D4E]">Takbira</span>
                            </label>
                            <label class="flex items-center p-4 border border-[#DBE2EF] rounded hover:bg-[#F9FAFB] cursor-pointer transition-colors">
                                <input type="checkbox" name="preference" value="Sanah" class="w-5 h-5 text-[#3F72AF] border-gray-300 focus:ring-[#3F72AF]">
                                <span class="ml-3 text-[#112D4E]">Sanah</span>
                            </label>
                            <label class="flex items-center p-4 border border-[#DBE2EF] rounded hover:bg-[#F9FAFB] cursor-pointer transition-colors">
                                <input type="checkbox" name="preference" value="Tajweed Quran Tilawat" class="w-5 h-5 text-[#3F72AF] border-gray-300 focus:ring-[#3F72AF]">
                                <span class="ml-3 text-[#112D4E]">Tajweed Quran Masjid Tilawat</span>
                            </label>
                            <label class="flex items-center p-4 border border-[#DBE2EF] rounded hover:bg-[#F9FAFB] cursor-pointer transition-colors">
                                <input type="checkbox" name="preference" value="Dua e Joshan" class="w-5 h-5 text-[#3F72AF] border-gray-300 focus:ring-[#3F72AF]">
                                <span class="ml-3 text-[#112D4E]">Dua e Joshan</span>
                            </label>
                            <label class="flex items-center p-4 border border-[#DBE2EF] rounded hover:bg-[#F9FAFB] cursor-pointer transition-colors">
                                <input type="checkbox" name="preference" value="Yaseen" class="w-5 h-5 text-[#3F72AF] border-gray-300 focus:ring-[#3F72AF]">
                                <span class="ml-3 text-[#112D4E]">Yaseen</span>
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
                            <input type="file" id="fileInput" name="media_files" class="hidden" multiple accept="audio/*">
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
        </div>
    </div>
</div>

<script src="/assets/js/main.js"></script>
<script src="/assets/js/home.js"></script>

<?php include 'includes/footer.php'; ?>
