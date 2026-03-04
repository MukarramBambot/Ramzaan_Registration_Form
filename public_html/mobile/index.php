<?php
// mobile/index.php
require_once __DIR__ . '/../includes/config.php';
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Jamaat Portal Mobile</title>
    
    <script>window.BASE_URL = '<?= BASE_URL ?>';</script>

    <!-- PWA Metadata -->
    <link rel="manifest" href="<?= BASE_URL ?>/mobile/manifest.json">
    <meta name="theme-color" content="#112D4E">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    
    <!-- Tailwind CSS (CDN) -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        background: "#F9F7F7",
                        foreground: "#112D4E",
                        brand: {
                            blue: "#3F72AF",
                            dark: "#112D4E",
                            light: "#DBE2EF",
                        }
                    }
                }
            }
        }
    </script>

    <link rel="stylesheet" href="<?= BASE_URL ?>/mobile/assets/css/mobile.css">
    
    <script>
        // Auth check - reuse existing JWT auth
        if (!localStorage.getItem('access_token')) {
            window.location.href = (window.BASE_URL || '') + '/admin/login.php';
        }
    </script>
</head>
<body class="bg-[#F9F7F7] text-[#112D4E] min-h-screen pb-20">

    <div id="app" class="flex flex-col min-h-screen">
        <!-- Header -->
        <header class="bg-[#112D4E] text-white px-6 py-4 sticky top-0 z-40 shadow-md">
            <div class="flex items-center justify-between">
                <h1 class="text-xl font-bold">Jamaat Portal</h1>
                <div id="user-initials" class="w-8 h-8 rounded-full bg-[#3F72AF] flex items-center justify-center text-xs font-bold">--</div>
            </div>
        </header>

        <!-- Main Content -->
        <main id="main-content" class="flex-grow p-4">
            <div id="loading-spinner" class="flex flex-col items-center justify-center py-20 space-y-4">
                <div class="w-10 h-10 border-4 border-[#3F72AF] border-t-transparent rounded-full animate-spin"></div>
                <p class="text-sm font-medium opacity-60">Loading your schedule...</p>
            </div>
            
            <div id="content-container" class="hidden space-y-4">
                <!-- Cards will be injected here -->
            </div>
        </main>

        <!-- Bottom Navigation -->
        <nav class="fixed bottom-0 left-0 right-0 bg-white border-t border-[#DBE2EF] px-6 py-3 flex justify-around items-center z-50 pb-safe">
            <button onclick="switchTab('roster')" class="nav-item flex flex-col items-center gap-1 text-[#3F72AF]" data-tab="roster">
                <svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>
                <span class="text-[10px] font-bold uppercase">Roster</span>
            </button>
            <button onclick="switchTab('requests')" class="nav-item flex flex-col items-center gap-1 text-[#6B7280]" data-tab="requests">
                <svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                <span class="text-[10px] font-bold uppercase">Requests</span>
            </button>
            <button onclick="switchTab('master')" class="nav-item flex flex-col items-center gap-1 text-[#6B7280]" data-tab="master">
                <svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="8" y1="13" x2="16" y2="13"/><line x1="8" y1="17" x2="16" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
                <span class="text-[10px] font-bold uppercase">Master</span>
            </button>
            <button onclick="showLogoutMenu()" class="flex flex-col items-center gap-1 text-[#6B7280]">
                <svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
                <span class="text-[10px] font-bold uppercase">Exit</span>
            </button>
        </nav>
    </div>

    <!-- App Scripts -->
    <script src="<?= BASE_URL ?>/assets/js/api.js"></script>
    <script src="<?= BASE_URL ?>/mobile/assets/js/mobile.js"></script>
    <script>
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register((window.BASE_URL || '') + '/mobile/service-worker.js');
        }
    </script>
</body>
</html>
