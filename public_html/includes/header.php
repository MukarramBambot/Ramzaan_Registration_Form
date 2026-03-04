<?php
require_once __DIR__ . '/config.php';
// Anti-caching headers
header("Cache-Control: no-cache, no-store, must-revalidate"); // HTTP 1.1.
header("Pragma: no-cache"); // HTTP 1.0.
header("Expires: 0"); // Proxies.
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sherullah 1447H Registration</title>
    
    <!-- Expose BASE_URL to JavaScript -->
    <script>window.BASE_URL = '<?= BASE_URL ?>';</script>

    <!-- PWA Metadata -->
    <link rel="manifest" href="<?= BASE_URL ?>/manifest.json">
    <meta name="theme-color" content="#112D4E">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <link rel="apple-touch-icon" href="<?= BASE_URL ?>/assets/icon-192.png">
    <!-- Google Fonts: Geist / Inter (Using Inter as generic replacement for Geist if not available, or loading Geist from CDN if possible) -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap" rel="stylesheet">
    
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
                            accent: "#3291B6",
                        },
                        surface: {
                            DEFAULT: "#FFFFFF",
                            secondary: "#F9FAFB",
                        },
                        text: {
                            primary: "#112D4E",
                            muted: "#6B7280",
                            subtle: "#9CA3AF",
                            inverted: "#FFFFFF",
                        }
                    },
        fontFamily: {
            sans: ['Inter', 'sans-serif'], // Replacing Geist with Inter for simplicity via Google Fonts
        }
    }
            }
        }
    </script>
    
    <style type="text/tailwindcss">
        @layer base {
            body {
                @apply bg-background text-foreground min-h-screen flex flex-col font-sans overflow-y-auto;
            }
            body.modal-open {
                @apply overflow-hidden;
            }
        }
        @layer components {
            .responsive-table-container {
                @apply overflow-x-auto relative;
                -webkit-overflow-scrolling: touch;
            }
            .sticky-col {
                @apply sticky left-0 z-10 bg-inherit border-r;
            }
            .shadow-right {
                box-shadow: 4px 0 6px -2px rgba(0,0,0,0.05);
            }
            /* Custom scrollbar for better mobile UX */
            .custom-scrollbar::-webkit-scrollbar {
                height: 4px;
                width: 4px;
            }
            .custom-scrollbar::-webkit-scrollbar-track {
                @apply bg-gray-100;
            }
            .custom-scrollbar::-webkit-scrollbar-thumb {
                @apply bg-brand-blue/30 rounded-full;
            }

            /* Floating Install Bar Styles */
            .install-bar {
                @apply fixed top-0 left-0 w-full bg-[#112D4E] text-white p-3 flex justify-between items-center z-[9999] shadow-lg transform transition-transform duration-300;
            }
            .install-bar.hidden {
                @apply -translate-y-full flex;
                display: none;
            }
            .install-bar span {
                @apply text-sm font-medium;
            }
            .install-bar .action-btns {
                @apply flex items-center gap-2;
            }
            .install-bar button#installBtn {
                @apply bg-white text-[#112D4E] px-3 py-1 rounded-md text-xs font-bold shadow-sm;
            }
            .install-bar button#closeInstall {
                @apply p-1 rounded-md hover:bg-white/10 text-gray-400;
            }
        }
    </style>
</head>
<body>
    <div id="installBar" class="install-bar hidden">
        <span>Install Jamaat Portal App</span>
        <div class="action-btns">
            <button id="installBtn">Install</button>
            <button id="closeInstall">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
            </button>
        </div>
    </div>

    <div id="app-root" class="flex flex-col min-h-screen">

        <?php
        $current_path = $_SERVER['PHP_SELF'];
        function is_nav_active($pattern) {
            global $current_path;
            if ($pattern === '/') {
                // Home: root index.php only
                $base = BASE_URL;
                return $current_path === $base . '/index.php' || $current_path === $base . '/' || $current_path === $base;
            }
            return strpos($current_path, $pattern) !== false;
        }
        function nav_link($href, $label, $pattern) {
            $is_active = is_nav_active($pattern);
            $active_class = $is_active
                ? 'text-white border-b-2 border-white pb-0.5 font-semibold'
                : 'text-[#DBE2EF] hover:text-white hover:border-b-2 hover:border-[#DBE2EF] pb-0.5 transition-all duration-150';
            echo '<a href="' . $href . '" class="' . $active_class . ' text-sm whitespace-nowrap">' . $label . '</a>';
        }
        function nav_link_mobile($href, $label, $pattern) {
            $is_active = is_nav_active($pattern);
            $active_class = $is_active
                ? 'bg-[#3F72AF] text-white font-semibold'
                : 'text-[#DBE2EF] hover:bg-[#1a3d6b]';
            echo '<a href="' . $href . '" class="' . $active_class . ' block px-4 py-3 rounded-md text-sm transition-colors duration-150">' . $label . '</a>';
        }
        ?>

        <!-- Top Navbar -->
        <nav class="bg-[#112D4E] border-b border-[#1e3d6f] shadow-sm">
            <div class="max-w-4xl mx-auto px-4 sm:px-6 flex items-center justify-between h-12">

                <!-- Brand -->
                <a href="<?= BASE_URL ?>/" class="text-white font-semibold text-sm tracking-wide shrink-0">
                    Madras Jamaat Portal
                </a>

                <!-- Desktop nav links -->
                <div class="hidden sm:flex items-center gap-6">
                    <?php
                    nav_link(BASE_URL . '/', 'Home', '/');
                    nav_link(BASE_URL . '/khidmat/', 'Khidmat Registration', '/khidmat/');
                    nav_link(BASE_URL . '/vajebaat/', 'Vajebaat', '/vajebaat/');
                    ?>
                </div>

                <!-- Mobile hamburger -->
                <button
                    id="nav-hamburger"
                    class="sm:hidden text-[#DBE2EF] hover:text-white p-1.5 rounded focus:outline-none transition-colors"
                    aria-label="Toggle navigation"
                    onclick="(function(){var m=document.getElementById('mobile-nav');m.classList.toggle('hidden');})()"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="3" y1="6" x2="21" y2="6"/>
                        <line x1="3" y1="12" x2="21" y2="12"/>
                        <line x1="3" y1="18" x2="21" y2="18"/>
                    </svg>
                </button>
            </div>

            <!-- Mobile dropdown -->
            <div id="mobile-nav" class="hidden sm:hidden bg-[#0d2340] px-4 py-3 space-y-1 border-t border-[#1e3d6f]">
                <?php
                nav_link_mobile(BASE_URL . '/', 'Home', '/');
                nav_link_mobile(BASE_URL . '/khidmat/', 'Khidmat Registration', '/khidmat/');
                nav_link_mobile(BASE_URL . '/vajebaat/', 'Vajebaat', '/vajebaat/');
                ?>
            </div>
        </nav>

        <main class="flex-grow">


