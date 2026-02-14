/**
 * Main JS - UI Components and Helpers
 */

// --- Icons (SVG Strings) ---
const ICONS = {
    check: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>`,
    alertTriangle: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>`,
    info: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>`,
    x: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>`,
    loader2: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="animate-spin"><path d="M21 12a9 9 0 1 1-6.219-8.56"></path></svg>`,
    upload: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>`,
    // Admin Icons
    shield: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>`,
    lock: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>`,
    unlock: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 9.9-1"></path></svg>`,
    user: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-3-3.87"></path><path d="M4 21v-2a4 4 0 0 1 3-3.87"></path><circle cx="12" cy="7" r="4"></circle></svg>`,
    eye: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>`,
    eyeOff: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line></svg>`,
    calendar: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>`,
    layout: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line></svg>`,
    fileSpreadsheet: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="8" y1="13" x2="16" y2="13"></line><line x1="8" y1="17" x2="16" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>`,
    video: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="23 7 16 12 23 17 23 7"></polygon><rect x="1" y="5" width="15" height="14" rx="2" ry="2"></rect></svg>`,
    play: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>`,
    pause: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>`

};

// --- Scroll Lock Manager ---
const ScrollLockManager = {
    locks: 0,
    lock() {
        this.locks++;
        if (this.locks === 1) {
            document.body.style.overflow = 'hidden';
        }
    },
    unlock() {
        if (this.locks > 0) {
            this.locks--;
            if (this.locks === 0) {
                document.body.style.overflow = '';
            }
        }
    }
};

// --- Dialog System ---

function createDialogHTML(config) {
    const {
        title,
        message,
        confirmLabel = 'Confirm',
        cancelLabel = 'Cancel',
        variant = 'default'
    } = config;

    let styles = {
        icon: ICONS.alertTriangle,
        iconClass: 'text-blue-500',
        buttonClass: 'bg-[#3F72AF] hover:bg-[#2D5A8F] text-white',
        bgClass: 'bg-blue-50'
    };

    if (variant === 'danger') {
        styles = {
            icon: ICONS.alertTriangle,
            iconClass: 'text-red-500',
            buttonClass: 'bg-blue-600 hover:bg-blue-700 text-white',
            bgClass: 'bg-blue-50'
        };
    } else if (variant === 'info') {
        styles = {
            icon: ICONS.info,
            iconClass: 'text-blue-500',
            buttonClass: 'bg-[#3F72AF] hover:bg-[#2D5A8F] text-white',
            bgClass: 'bg-blue-50'
        };
    }

    // Parse icon string into DOM element if needed, but for template literal we just insert string
    // Note: The icon strings are raw SVG HTML

    // Inject icon color class
    const iconHTML = styles.icon.replace('<svg', `<svg class="${styles.iconClass}"`);

    return `
        <div id="confirm-dialog-backdrop" class="fixed inset-0 z-[9999] flex items-center justify-center p-4 sm:p-6 transition-opacity duration-200 opacity-0">
            <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" onclick="closeDialog()"></div>
            
            <div class="relative bg-white w-full max-w-md rounded-2xl shadow-2xl overflow-hidden transform transition-all duration-200 scale-95 opacity-0" id="confirm-dialog-content">
                <div class="p-6 pb-2 flex items-start gap-4">
                    <div class="p-3 rounded-xl ${styles.bgClass} shrink-0">
                        ${iconHTML}
                    </div>
                    <div class="flex-1 min-w-0 pt-1">
                        <h3 class="text-xl font-bold text-[#112D4E] tracking-tight truncate">${title}</h3>
                    </div>
                    <button onclick="closeDialog()" class="p-1 rounded-lg hover:bg-gray-100 text-gray-400 transition-colors">
                        ${ICONS.x}
                    </button>
                </div>

                <div class="px-6 py-4">
                    <div class="text-gray-600 leading-relaxed text-sm whitespace-pre-wrap">${message}</div>
                </div>

                <div class="px-6 py-6 bg-gray-50 flex flex-col-reverse sm:flex-row sm:justify-end gap-3 mt-2">
                    ${cancelLabel ? `<button onclick="window.currentDialogCancel?.(); closeDialog()" class="px-5 py-2.5 rounded-xl border border-gray-200 text-gray-600 font-bold text-sm hover:bg-white hover:border-gray-300 transition-all active:scale-95">${cancelLabel}</button>` : ''}
                    <button onclick="window.currentDialogConfirm?.(); closeDialog()" class="px-5 py-2.5 rounded-xl font-bold text-sm shadow-md transition-all active:scale-95 ${styles.buttonClass}">
                        ${confirmLabel}
                    </button>
                </div>
            </div>
        </div>
    `;
}

window.showDialog = function (config) {
    // Remove existing dialog if any
    const existing = document.getElementById('confirm-dialog-container');
    if (existing) existing.remove();

    // Create container
    const container = document.createElement('div');
    container.id = 'confirm-dialog-container';
    container.innerHTML = createDialogHTML(config);
    document.body.appendChild(container);

    // Bind callbacks
    window.currentDialogConfirm = () => {
        if (config.onConfirm) config.onConfirm();
    };
    window.currentDialogCancel = () => {
        if (config.onCancel) config.onCancel();
    };

    // Animation: fade in
    // Force reflow
    container.offsetHeight;

    const backdrop = document.getElementById('confirm-dialog-backdrop');
    const content = document.getElementById('confirm-dialog-content');

    if (backdrop) backdrop.classList.remove('opacity-0');
    if (content) {
        content.classList.remove('scale-95', 'opacity-0');
        content.classList.add('scale-100', 'opacity-100');
    }

    // Scroll lock
    ScrollLockManager.lock();
};

window.closeDialog = function () {
    const backdrop = document.getElementById('confirm-dialog-backdrop');
    const content = document.getElementById('confirm-dialog-content');

    if (backdrop) backdrop.classList.add('opacity-0');
    if (content) {
        content.classList.add('scale-95', 'opacity-0');
        content.classList.remove('scale-100', 'opacity-100');
    }

    setTimeout(() => {
        const container = document.getElementById('confirm-dialog-container');
        if (container) container.remove();
        ScrollLockManager.unlock();
    }, 200);
};

// Handle Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        window.closeDialog();
    }
});
