/**
 * Dashboard JS - Roster Logic
 */

const DUTY_COLUMNS = [
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
    // 1. Auth Check
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/admin/login.php';
        return;
    }

    // State Variables
    let users = [];
    let assignments = new Map(); // key = "date_duty" (e.g. "14/02/2026_FAJAR_AZAAN") -> { userId, date, duty, locked }
    let dates = generateRamazaanDates();
    let editingCell = null; // { date, duty }
    let detailsPanelData = null; // { user, date, duty, dutyLabel }

    // DOM Elements
    const gridContainer = document.getElementById('roster-grid-container');
    const loadingState = document.getElementById('loading-state');
    const tableHeader = document.getElementById('roster-header-row');
    const tableBody = document.getElementById('roster-body');
    const summaryStats = document.getElementById('summary-stats');
    const statTotal = document.getElementById('stat-total');
    const statLocked = document.getElementById('stat-locked');
    const statCompletion = document.getElementById('stat-completion');
    const detailsContainer = document.getElementById('details-panel-container');
    const successBanner = document.getElementById('success-banner');

    // 2. Initialize
    renderHeader();
    await fetchData();

    // --- Helpers ---

    function generateRamazaanDates() {
        const d = [];
        const start = new Date('2026-02-14');
        for (let i = 0; i < 30; i++) {
            const current = new Date(start);
            current.setDate(start.getDate() + i);
            const day = String(current.getDate()).padStart(2, '0');
            const month = String(current.getMonth() + 1).padStart(2, '0');
            const year = current.getFullYear();
            d.push(`${day}/${month}/${year}`);
        }
        return d;
    }

    function getCellKey(date, duty) {
        return `${date}_${duty}`;
    }

    function getUserById(id) {
        return users.find(u => u.id === String(id));
    }

    // --- Rendering ---

    function renderHeader() {
        let html = `<th class="px-4 py-3 text-left text-xs font-bold text-[#112D4E] uppercase tracking-wider border-r-2 border-[#DBE2EF] bg-[#F9F7F7] sticky left-0 z-30 min-w-[120px]">Date</th>`;
        DUTY_COLUMNS.forEach(col => {
            html += `<th class="px-3 py-3 text-center text-xs font-bold text-[#112D4E] uppercase tracking-wider border-r border-[#DBE2EF] min-w-[160px] bg-[#F9F7F7]">${col.label}</th>`;
        });
        tableHeader.innerHTML = html;
    }

    function renderBody() {
        tableBody.innerHTML = '';

        dates.forEach((date, dateIdx) => {
            const tr = document.createElement('tr');
            tr.className = `border-b border-[#DBE2EF] transition-colors duration-150 ease-out ${dateIdx % 2 === 0 ? 'bg-white' : 'bg-[#F9F7F7]/30'}`;

            // Date Cell
            let html = `<td class="px-4 py-2 text-sm font-medium text-[#112D4E] border-r-2 border-[#DBE2EF] sticky left-0 z-10 bg-inherit transition-colors duration-150 ease-out">${date}</td>`;

            DUTY_COLUMNS.forEach(duty => {
                const key = getCellKey(date, duty.key);
                const assignment = assignments.get(key);
                const user = assignment ? getUserById(assignment.userId) : null;
                const isEditing = editingCell && editingCell.date === date && editingCell.duty === duty.key;

                html += `<td class="px-2 py-1.5 border-r border-[#DBE2EF] relative p-0" id="cell-${key}">`;

                if (isEditing) {
                    html += `
                        <div class="relative">
                            <input 
                                type="text" 
                                class="w-full px-2 py-1.5 text-sm border-2 border-[#3F72AF] rounded focus:outline-none bg-white" 
                                placeholder="Search..."
                                id="input-${key}"
                                autocomplete="off"
                            />
                            <div id="dropdown-${key}" class="absolute top-full left-0 right-0 mt-1 bg-white border border-[#DBE2EF] rounded shadow-lg max-h-48 overflow-y-auto z-50 hidden"></div>
                        </div>
                    `;
                } else {
                    const lockedClass = assignment?.locked ? 'bg-[#DBE2EF]/60 text-[#112D4E] font-medium hover:bg-[#DBE2EF]/80' : 'text-[#6B7280] hover:bg-[#DBE2EF]/30 bg-[#DBE2EF]/10';
                    const content = user ? user.fullName : '–';
                    const lockIcon = assignment?.locked ? `<span class="mr-1">${ICONS.lock.replace('width="24"', 'width="12"').replace('height="24"', 'height="12"').replace('currentColor', '#3F72AF')}</span>` : '';

                    html += `
                        <div 
                            onclick="handleCellClick('${date}', '${duty.key}')" 
                            class="min-h-[36px] px-2 py-1.5 text-sm rounded cursor-pointer transition-all duration-200 ease-out flex items-center gap-2 ${lockedClass}"
                        >
                            ${lockIcon}
                            <span class="flex-1 truncate">${content}</span>
                        </div>
                    `;
                }

                html += `</td>`;
            });

            tr.innerHTML = html;
            tableBody.appendChild(tr);

            // Setup Edit Listeners if needed
            if (editingCell && editingCell.date === date) {
                setupEditListeners(date); // Helper to attach events to inputs
            }
        });

        updateStats();
    }

    function updateStats() {
        statTotal.textContent = assignments.size;

        const lockedCount = Array.from(assignments.values()).filter(a => a.locked).length;
        statLocked.textContent = lockedCount;
        document.getElementById('header-locked-count').textContent = `${lockedCount} locked`;

        const totalSlots = dates.length * DUTY_COLUMNS.length;
        statCompletion.textContent = ((assignments.size / totalSlots) * 100).toFixed(0) + '%';
    }

    function setupEditListeners(rowDate) {
        // We iterate specifically for the columns in editing state
        // Actually, renderBody re-renders everything, so we attach listeners to the Inputs directly
        const key = getCellKey(editingCell.date, editingCell.duty);
        const input = document.getElementById(`input-${key}`);
        const dropdown = document.getElementById(`dropdown-${key}`);

        if (!input || !dropdown) return;

        input.focus();

        // Populate initial dropdown
        populateDropdown(dropdown, users);
        dropdown.classList.remove('hidden');

        input.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            const filtered = users.filter(u => u.fullName.toLowerCase().includes(term) || u.itsNumber.includes(term));
            populateDropdown(dropdown, filtered);
        });

        // Blur handling - tricky with click inside dropdown
        // Using a timeout to allow click to register
        input.addEventListener('blur', () => {
            setTimeout(() => {
                // Check if we are still editing same cell (prevents closing if we just clicked dropdown)
                // Actually, if we click dropdown, blur happens. 
                // We will handle selection via mousedown on dropdown items which fires before blur
                setEditingCell(null);
            }, 200);
        });
    }

    function populateDropdown(container, list) {
        if (list.length === 0) {
            container.innerHTML = `<div class="px-3 py-2 text-sm text-[#6B7280] italic">No users found</div>`;
            return;
        }

        container.innerHTML = list.map(user => `
            <div 
                class="w-full text-left px-3 py-2 text-sm text-[#112D4E] hover:bg-[#DBE2EF] transition-colors border-b border-[#DBE2EF] last:border-b-0 cursor-pointer"
                onmousedown="selectUser('${user.id}')"
            >
                <div class="font-medium">${user.fullName}</div>
                <div class="text-xs text-[#6B7280]">${user.itsNumber}</div>
            </div>
        `).join('');
    }

    // --- Logic ---

    // Exposed global functions for HTML event attributes
    window.handleCellClick = (date, dutyKey) => {
        const key = getCellKey(date, dutyKey);
        const assignment = assignments.get(key);

        if (assignment?.locked) {
            const user = getUserById(assignment.userId);
            if (user) {
                const dutyLabel = DUTY_COLUMNS.find(d => d.key === dutyKey)?.label || '';
                openDetailsPanel(user, date, dutyKey, dutyLabel);
            }
        } else {
            setEditingCell({ date, duty: dutyKey });
        }
    };

    window.selectUser = (userId) => {
        const user = getUserById(userId);
        if (!user || !editingCell) return;

        const { date, duty } = editingCell;
        const dutyLabel = DUTY_COLUMNS.find(d => d.key === duty)?.label || '';

        // Close editing
        // setEditingCell(null) happen in blur, but we want to confirm first.
        // We will process selection now.

        // Confirm Dialog
        showDialog({
            title: 'Confirm Assignment',
            variant: 'info',
            confirmLabel: 'Assign Duty',
            message: `Assign ${user.fullName} to ${dutyLabel} on ${date}?`, // Simplified message compared to React
            onConfirm: () => confirmAssignment(user, date, duty)
        });
    };

    function setEditingCell(cell) {
        editingCell = cell;
        renderBody(); // Re-render to show input or revert
    }

    // --- Data Fetching ---

    async function fetchData() {
        loadingState.classList.remove('hidden');
        gridContainer.classList.add('hidden');

        try {
            // 1. Users
            const usersRes = await apiFetch('/api/registrations/');
            if (!usersRes.ok) throw new Error('Failed to fetch users');
            const userData = await usersRes.json();

            users = userData.map(u => ({
                id: String(u.id),
                fullName: u.full_name,
                itsNumber: u.its_number,
                email: u.email,
                whatsappNumber: u.phone_number,
                registerFor: u.preference,
                auditionFiles: u.audition_files.map(af => ({
                    id: af.id,
                    url: af.audition_file_path.startsWith('http') ? af.audition_file_path : `${window.API_BASE}${af.audition_file_path}`,
                    type: af.audition_file_type,
                    name: af.audition_display_name
                }))
            }));

            // 2. Grid
            const gridRes = await apiFetch('/api/duty-assignments/grid/');
            if (!gridRes.ok) throw new Error('Failed to fetch grid');
            const gridData = await gridRes.json();

            assignments = new Map();
            Object.keys(gridData).forEach(isoDate => {
                // ISO YYYY-MM-DD -> DD/MM/YYYY
                const [y, m, d] = isoDate.split('-');
                const formattedDate = `${d}/${m}/${y}`;

                Object.keys(gridData[isoDate]).forEach(dutyKey => {
                    const cell = gridData[isoDate][dutyKey];
                    assignments.set(getCellKey(formattedDate, dutyKey), {
                        userId: String(cell.user_id || ""),
                        date: formattedDate,
                        duty: dutyKey,
                        locked: cell.locked
                    });
                });
            });

            loadingState.classList.add('hidden');
            gridContainer.classList.remove('hidden');
            summaryStats.classList.remove('hidden');

            renderBody();

        } catch (e) {
            // console.error(e); // Silenced for production
            showDialog({ variant: 'danger', title: 'Error', message: 'Failed to load data. Please refresh.' });
        }
    }

    // --- Actions ---

    async function confirmAssignment(user, date, duty) {
        try {
            const [d, m, y] = date.split('/');
            const isoDate = `${y}-${m}-${d}`;

            const response = await apiFetch('/api/duty-assignments/', {
                method: 'POST',
                body: JSON.stringify({
                    duty_date: isoDate,
                    namaaz_type: duty,
                    assigned_user_id: parseInt(user.id)
                })
            });

            if (!response.ok) {
                const err = await response.json().catch(() => ({}));
                throw new Error(err.error || 'Assignment Failed');
            }

            // Optimistic update
            const key = getCellKey(date, duty);
            assignments.set(key, {
                userId: user.id,
                date: date,
                duty: duty,
                locked: true
            });

            showSuccess(`Duty assigned to ${user.fullName}`);
            renderBody(); // Re-render grid

        } catch (error) {
            showDialog({
                variant: 'danger',
                title: 'Assignment Failed',
                message: error.message
            });
        }
    }

    // --- Details Panel ---

    function openDetailsPanel(user, date, duty, dutyLabel) {
        const panelHTML = `
            <div class="fixed inset-0 bg-white/30 backdrop-blur-sm z-40 animate-fadeIn" onclick="closeDetailsPanel()"></div>
            <div class="fixed top-0 right-0 bottom-0 w-full sm:w-96 bg-white shadow-2xl z-50 overflow-y-auto animate-slideInRight">
                <!-- Header -->
                <div class="bg-[#112D4E] px-6 py-4 flex items-center justify-between sticky top-0">
                    <div>
                        <h2 class="text-lg text-white font-medium">Duty Details</h2>
                        <p class="text-[#DBE2EF] text-sm">${dutyLabel} • ${date}</p>
                    </div>
                    <button onclick="closeDetailsPanel()" class="text-[#DBE2EF] hover:text-white transition-colors">
                        ${ICONS.x}
                    </button>
                </div>

                <!-- Content -->
                <div class="p-6 space-y-6">
                    <!-- User Info -->
                    <div class="space-y-3">
                        <h3 class="text-xs font-bold text-[#6B7280] uppercase tracking-wider">User Information</h3>
                        <div class="bg-[#F9F7F7] rounded-lg p-4 space-y-3">
                            <div><div class="text-xs text-[#6B7280] mb-1">Full Name</div><div class="text-[#112D4E] font-medium">${user.fullName}</div></div>
                            <div><div class="text-xs text-[#6B7280] mb-1">ITS Number</div><div class="text-[#112D4E]">${user.itsNumber}</div></div>
                            <div><div class="text-xs text-[#6B7280] mb-1">Phone</div><div class="text-[#112D4E]">${user.whatsappNumber}</div></div>
                        </div>
                    </div>

                    <!-- Auditions -->
                     <div class="space-y-3">
                        <h3 class="text-xs font-bold text-[#6B7280] uppercase tracking-wider">Audition Files</h3>
                        <div class="space-y-2">
                            ${user.auditionFiles.length ? user.auditionFiles.map(f => `
                                <div class="flex items-center gap-3 p-3 bg-[#F9F7F7] rounded border border-[#DBE2EF]">
                                    <span class="flex-1 text-xs text-[#112D4E] font-medium truncate">${f.name}</span>
                                    <button 
                                        onclick="openAuditionModal({url:'${f.url}', name:'${f.name}', type:'${f.type}'})"
                                        class="p-2 rounded bg-[#3F72AF] text-white hover:bg-[#2D5A8F]"
                                    >
                                        ${ICONS.play.replace('width="24"', 'width="14"').replace('height="24"', 'height="14"')}
                                    </button>
                                </div>
                            `).join('') : '<p class="text-xs text-[#6B7280] italic">No files</p>'}
                        </div>
                    </div>

                    <!-- Unlock -->
                    <div class="pt-4 border-t-2 border-[#DBE2EF]">
                        <button onclick="startUnlock('${date}', '${duty}')" class="w-full flex items-center justify-center gap-2 px-4 py-2.5 border-2 border-amber-500 text-amber-700 rounded-lg hover:bg-amber-50 transition-all font-medium">
                            ${ICONS.unlock} Emergency Unlock
                        </button>
                    </div>
                </div>
            </div>
        `;
        detailsContainer.innerHTML = panelHTML;
        document.body.style.overflow = 'hidden';
    }

    window.closeDetailsPanel = function () {
        detailsContainer.innerHTML = '';
        document.body.style.overflow = 'unset';
    };

    window.startUnlock = function (date, duty) {
        // Show Dialog with Input
        // Inject input into dialog message for reason capture

        const messageHTML = `
            <div class="space-y-4">
                <p class="text-[#112D4E]">This will unlock the assignment. Use only if necessary.</p>
                <div>
                    <label class="block text-xs font-bold text-[#6B7280] uppercase tracking-wider mb-2">Reason</label>
                    <textarea id="unlock-reason" class="w-full px-3 py-2 border border-[#DBE2EF] rounded focus:outline-none focus:border-[#3F72AF]" rows="3"></textarea>
                </div>
            </div>
        `;

        showDialog({
            title: 'Emergency Unlock',
            variant: 'danger',
            confirmLabel: 'Unlock Now',
            message: messageHTML,
            onConfirm: () => {
                const reason = document.getElementById('unlock-reason').value;
                if (!reason) {
                    alert('Reason is required'); // Fallback alert or re-show dialog
                    return;
                }
                performUnlock(date, duty, reason);
            }
        });
    };

    async function performUnlock(date, duty, reason) {
        try {
            // Fetch full list to find Assignment ID (required for unlock endpoint)

            // Let's do that for simplicity:
            const listRes = await apiFetch('/api/duty-assignments/');
            const list = await listRes.json();

            const [d, m, y] = date.split('/');
            const isoDate = `${y}-${m}-${d}`;

            const item = list.find(a => a.duty_date === isoDate && a.namaaz_type === duty);
            if (!item) throw new Error('Assignment not found');

            const res = await apiFetch(`/api/duty-assignments/${item.id}/unlock/`, {
                method: 'POST',
                body: JSON.stringify({ reason })
            });

            if (!res.ok) throw new Error('Unlock Failed');

            // Success
            assignments.delete(getCellKey(date, duty));
            renderBody();
            closeDetailsPanel();
            showSuccess('Unlocked successfully');

        } catch (e) {
            showDialog({ variant: 'danger', title: 'Error', message: e.message });
        }
    }

    function showSuccess(msg) {
        document.getElementById('success-message-text').textContent = msg;
        successBanner.classList.remove('hidden');
        setTimeout(() => successBanner.classList.add('hidden'), 3000);
    }

});
