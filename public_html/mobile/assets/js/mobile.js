/**
 * Mobile PWA JS - Jamaat Portal
 */

let CURRENT_TAB = 'roster';
let USERS = [];
let ASSIGNMENTS = new Map();
let DATES = generateRamazaanDates();

const DUTY_COLUMNS = [
    { key: 'SANAH', label: 'Sanah' },
    { key: 'TAJWEED', label: 'Tajwid' },
    { key: 'DUA_E_JOSHAN', label: 'Dua e Joshan' },
    { key: 'YASEEN', label: 'Yaseen' },
    { key: 'FAJAR_AZAAN', label: 'Fajar Azaan' },
    { key: 'FAJAR_TAKBIRA', label: 'Fajar Takbira' },
    { key: 'ZOHAR_AZAAN', label: 'Zohar Azaan' },
    { key: 'ZOHAR_TAKBIRA', label: 'Zohar Takbira' },
    { key: 'ASAR_TAKBIRA', label: 'Asar Takbira' },
    { key: 'MAGRIB_AZAAN', label: 'Magrib Azaan' },
    { key: 'MAGRIB_TAKBIRA', label: 'Magrib Takbira' },
    { key: 'ISHAA_TAKBIRA', label: 'Ishaa Takbira' }
];

document.addEventListener('DOMContentLoaded', async () => {
    initUser();
    await loadData();
});

function initUser() {
    const userStr = localStorage.getItem('user');
    if (userStr) {
        const user = JSON.parse(userStr);
        document.getElementById('user-initials').textContent = (user.full_name || user.username || 'U').substring(0, 2).toUpperCase();
    }
}

async function loadData() {
    showSpinner(true);
    try {
        // Fetch Users and Grid in parallel
        const [usersRes, gridRes] = await Promise.all([
            apiFetch('/api/registrations/', { method: 'GET', requireAuth: true }),
            apiFetch('/api/duty-assignments/grid/', { method: 'GET', requireAuth: true })
        ]);

        USERS = await usersRes.json();
        const gridData = await gridRes.json();

        // Convert grid object to Map for easier lookup
        // gridData format: { "DD/MM/YYYY_DUTY_KEY": { userId, ... }, ... }
        ASSIGNMENTS = new Map(Object.entries(gridData));

        renderContent();
    } catch (err) {
        console.error("Failed to load mobile data", err);
        document.getElementById('main-content').innerHTML = `
            <div class="bg-red-50 p-6 rounded-2xl border border-red-100 text-red-800 text-center">
                <p class="font-bold mb-2">Error Loading Data</p>
                <p class="text-sm opacity-80 mb-4">${err.message}</p>
                <button onclick="window.location.reload()" class="bg-red-500 text-white px-4 py-2 rounded-lg text-xs font-bold">Retry</button>
            </div>
        `;
    } finally {
        showSpinner(false);
    }
}

function renderContent() {
    const container = document.getElementById('content-container');
    container.innerHTML = '';
    container.classList.remove('hidden');

    if (CURRENT_TAB === 'roster') {
        renderRoster(container);
    } else {
        container.innerHTML = `
            <div class="py-20 text-center opacity-40">
                <p class="text-sm font-bold uppercase tracking-widest">${CURRENT_TAB} Coming Soon</p>
                <p class="text-xs mt-2">Enhanced mobile views for these sections are being optimized.</p>
            </div>
        `;
    }
}

function renderRoster(container) {
    DATES.forEach(date => {
        const dateCard = document.createElement('div');
        dateCard.className = 'bg-white rounded-2xl shadow-sm border border-[#DBE2EF] overflow-hidden';
        
        // Header with Date
        const [day, month, year] = date.split('/');
        const dateObj = new Date(year, month - 1, day);
        const dayName = dateObj.toLocaleDateString('en-US', { weekday: 'long' });
        const displayDate = dateObj.toLocaleDateString('en-US', { day: 'numeric', month: 'short' });

        dateCard.innerHTML = `
            <div class="bg-[#F9F7F7] px-4 py-3 border-b border-[#DBE2EF] flex justify-between items-center">
                <div>
                    <span class="text-xs font-bold text-[#3F72AF] uppercase tracking-wider">${dayName}</span>
                    <h3 class="text-lg font-bold text-[#112D4E]">${displayDate}</h3>
                </div>
            </div>
            <div class="px-4 py-2 space-y-2" id="duties-${date.replace(/\//g, '')}">
                <!-- Duties cards -->
            </div>
        `;

        container.appendChild(dateCard);
        const dutiesContainer = document.getElementById(`duties-${date.replace(/\//g, '')}`);

        DUTY_COLUMNS.forEach(duty => {
            const key = `${date}_${duty.key}`;
            const assignment = ASSIGNMENTS.get(key);
            const user = assignment ? USERS.find(u => String(u.id) === String(assignment.userId)) : null;

            const dutyItem = document.createElement('div');
            dutyItem.className = `p-3 rounded-xl border flex items-center justify-between gap-3 ${user ? 'bg-[#3F72AF]/5 border-[#3F72AF]/20' : 'bg-white border-[#DBE2EF]/50'}`;
            
            dutyItem.innerHTML = `
                <div class="flex-1 min-w-0">
                    <span class="text-[10px] font-bold text-[#6B7280] uppercase tracking-tighter">${duty.label}</span>
                    <p class="text-sm font-bold text-[#112D4E] truncate">${user ? user.full_name : '<span class="text-gray-300 font-normal">Unassigned</span>'}</p>
                </div>
                ${user ? `<div class="w-2 h-2 rounded-full ${assignment.locked ? 'bg-green-500' : 'bg-yellow-500 shadow-[0_0_8px_rgba(234,179,8,0.5)]'}"></div>` : ''}
            `;
            
            dutiesContainer.appendChild(dutyItem);
        });
    });
}

function generateRamazaanDates() {
    const d = [];
    const start = new Date('2026-02-17');
    const end = new Date('2026-03-18');
    for (let dt = new Date(start); dt <= end; dt.setDate(dt.getDate() + 1)) {
        const day = String(dt.getDate()).padStart(2, '0');
        const month = String(dt.getMonth() + 1).padStart(2, '0');
        const year = dt.getFullYear();
        d.push(`${day}/${month}/${year}`);
    }
    return d;
}

function switchTab(tab) {
    CURRENT_TAB = tab;
    document.querySelectorAll('.nav-item').forEach(el => {
        if (el.dataset.tab === tab) {
            el.classList.add('text-[#3F72AF]');
            el.classList.remove('text-[#6B7280]');
        } else {
            el.classList.remove('text-[#3F72AF]');
            el.classList.add('text-[#6B7280]');
        }
    });
    renderContent();
}

function showSpinner(show) {
    document.getElementById('loading-spinner').classList.toggle('hidden', !show);
}

function showLogoutMenu() {
    if (confirm('Logout from Madras Jamaat Portal?')) {
        localStorage.clear();
        window.location.href = '/admin/login.php';
    }
}
