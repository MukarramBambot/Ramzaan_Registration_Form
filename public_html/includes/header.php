<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sherullah 1447H Registration</title>
    
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
                @apply bg-background text-foreground min-h-screen flex flex-col font-sans;
            }
        }
    </style>
</head>
<body>
    <div id="app-root" class="flex flex-col min-h-screen">
        <main class="flex-grow">
