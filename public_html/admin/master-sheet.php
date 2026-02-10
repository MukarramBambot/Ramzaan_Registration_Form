<?php include '../includes/header.php'; ?>

<!-- Content Wrapper -->
<div class="min-h-screen bg-[#F9F7F7]">
    
    <!-- Header -->
    <div class="bg-[#112D4E] py-5 px-6 shadow-md">
        <div class="flex items-center justify-between">
            <div>
                <div class="flex items-center gap-6 mb-1">
                    <h1 class="text-2xl text-white font-normal">
                        Master Sheet
                    </h1>
                    <div class="flex items-center gap-2 ml-4">
                        <a href="/admin/dashboard.php" class="px-3 py-1.5 rounded-md text-[#DBE2EF] hover:text-white hover:bg-white/10 text-sm font-medium transition-all flex items-center gap-2">
                             <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line></svg>
                            Duty Roster
                        </a>
                        <a href="/admin/master-sheet.php" class="px-3 py-1.5 rounded-md bg-[#3F72AF] text-white text-sm font-medium flex items-center gap-2">
                           <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="8" y1="13" x2="16" y2="13"></line><line x1="8" y1="17" x2="16" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                            Master Sheet
                        </a>
                    </div>
                </div>
                <p class="text-[#DBE2EF] text-sm font-light">
                    Sherullah 1447H – Central Database
                </p>
            </div>
             <div class="flex items-center gap-3 text-[#DBE2EF] text-sm">
                <button
                    id="refresh-btn"
                    onclick="loadMasterSheet()"
                    class="px-3 py-1.5 rounded-md bg-white/10 hover:bg-white/20 text-white text-sm font-medium transition-all flex items-center gap-2"
                    title="Refresh Data"
                >
                    <span id="refresh-icon"></span>
                    <span>Refresh</span>
                </button>
                <button
                    id="sync-btn"
                    onclick="syncToSheets()"
                    class="px-3 py-1.5 rounded-md bg-green-500/10 hover:bg-green-500/20 border border-green-500/20 text-green-400 text-sm font-medium transition-all flex items-center gap-2"
                    title="Sync to Google Sheets"
                >
                    <span id="sync-icon"></span>
                    <span>Sync to Google Sheet</span>
                </button>
                <button
                    onclick="logout()"
                    
                    class="ml-4 px-3 py-1.5 rounded-md bg-red-500/10 hover:bg-red-500/20 text-red-100 text-sm font-medium transition-all"
                >
                    Logout
                </button>
            </div>
        </div>
    </div>

    <!-- Main Content -->
    <div class="p-6">
        <div class="bg-white rounded-xl shadow-sm border border-[#DBE2EF] overflow-hidden">
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead class="bg-[#F9FAFB] border-b border-[#DBE2EF]">
                        <tr>
                            <th class="px-6 py-4 text-xs font-bold text-[#6B7280] uppercase tracking-wider">Full Name</th>
                            <th class="px-6 py-4 text-xs font-bold text-[#6B7280] uppercase tracking-wider">ITS Number</th>
                            <th class="px-6 py-4 text-xs font-bold text-[#6B7280] uppercase tracking-wider">Contact</th>
                            <th class="px-6 py-4 text-xs font-bold text-[#6B7280] uppercase tracking-wider">Preference</th>
                            <th class="px-6 py-4 text-xs font-bold text-[#6B7280] uppercase tracking-wider">Status</th>
                            <th class="px-6 py-4 text-xs font-bold text-[#6B7280] uppercase tracking-wider">Registered</th>
                            <th class="px-6 py-4 text-xs font-bold text-[#6B7280] uppercase tracking-wider text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody id="master-sheet-body" class="divide-y divide-[#DBE2EF]">
                        <!-- Data will be loaded here -->
                        <tr>
                            <td colspan="7" class="px-6 py-12 text-center text-[#9CA3AF]">
                                <div class="flex flex-col items-center">
                                    <div class="animate-spin mb-4">${ICONS.loader2}</div>
                                    <p>Loading registrations...</p>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

</div>

<!-- Audition Modal Container -->
<div id="audition-modal-container"></div>

<script src="/assets/js/api.js"></script>
<script src="/assets/js/main.js"></script>
<script src="/assets/js/audition-modal.js"></script>

<script>
    document.addEventListener('DOMContentLoaded', () => {
        // Initialize icons
        const refreshIcon = document.getElementById('refresh-icon');
        const syncIcon = document.getElementById('sync-icon');
        
        if (refreshIcon) refreshIcon.innerHTML = ICONS.loader2.replace('animate-spin', '').replace('<svg', '<svg class="w-4 h-4"');
        if (syncIcon) syncIcon.innerHTML = ICONS.fileSpreadsheet.replace('<svg', '<svg class="w-4 h-4"');
        
        loadMasterSheet();
    });

    async function loadMasterSheet() {
        const tbody = document.getElementById('master-sheet-body');
        const refreshBtn = document.getElementById('refresh-btn');
        const refreshIcon = document.getElementById('refresh-icon');
        
        // Show loading state on button
        if (refreshIcon) {
            refreshIcon.innerHTML = ICONS.loader2.replace('<svg', '<svg class="w-4 h-4"');
            refreshBtn.disabled = true;
        }

        try {
            const response = await apiFetch('/api/registrations/', {
                requireAuth: true
            });

            if (!response.ok) {
                if (response.status === 401 || response.status === 403) return; // Handled by apiFetch
                throw new Error(`Error ${response.status}: Failed to fetch data`);
            }

            const registrations = await response.json();
            renderTable(registrations);

        } catch (err) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="px-6 py-12 text-center text-red-500">
                        <p class="font-medium">Failed to load data</p>
                        <p class="text-xs mt-1">${err.message}</p>
                    </td>
                </tr>
            `;
        } finally {
            if (refreshIcon) {
                refreshIcon.innerHTML = ICONS.loader2.replace('animate-spin', '').replace('<svg', '<svg class="w-4 h-4"');
                refreshBtn.disabled = false;
            }
        }
    }

    async function syncToSheets() {
        const syncBtn = document.getElementById('sync-btn');
        const syncIcon = document.getElementById('sync-icon');
        const originalIcon = syncIcon.innerHTML;

        // Confirm action
        showDialog({
            variant: 'info',
            title: 'Sync to Google Sheets',
            message: 'This will overwite the existing Google Sheet with the current database records. Proceed?',
            confirmLabel: 'Yes, Sync',
            onConfirm: async () => {
                try {
                    // Loading state
                    syncBtn.disabled = true;
                    syncIcon.innerHTML = ICONS.loader2.replace('<svg', '<svg class="w-4 h-4"');
                    
                    const response = await apiFetch('/api/registrations/sync_to_sheets/', {
                        method: 'POST',
                        requireAuth: true
                    });

                    const data = await response.json();

                    if (!response.ok) {
                        throw new Error(data.error || 'Failed to sync to Google Sheets');
                    }

                    showDialog({
                        variant: 'success',
                        title: 'Sync Successful',
                        message: data.message || 'All records have been pushed to Google Sheets.',
                        confirmLabel: 'Close'
                    });

                } catch (err) {
                    showDialog({
                        variant: 'danger',
                        title: 'Sync Failed',
                        message: err.message,
                        confirmLabel: 'Retry'
                    });
                } finally {
                    syncBtn.disabled = false;
                    syncIcon.innerHTML = originalIcon;
                }
            }
        });
    }

    function renderTable(data) {
        const tbody = document.getElementById('master-sheet-body');
        
        if (!data || data.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="px-6 py-12 text-center text-[#9CA3AF]">
                        No registrations found.
                    </td>
                </tr>
            `;
            return;
        }

        tbody.innerHTML = data.map(reg => `
            <tr class="hover:bg-[#F9FAFB] transition-colors group">
                <td class="px-6 py-4 text-[#112D4E] font-medium">${reg.full_name}</td>
                <td class="px-6 py-4 text-[#3F72AF] font-mono text-sm">${reg.its_number}</td>
                <td class="px-6 py-4">
                    <div class="text-sm text-[#112D4E]">${reg.email}</div>
                    <div class="text-xs text-[#6B7280]">${reg.phone_number}</div>
                </td>
                <td class="px-6 py-4">
                    <span class="px-2 py-1 rounded-full text-[10px] font-bold tracking-wider uppercase ${getPreferenceClass(reg.preference)}">
                        ${reg.preference}
                    </span>
                </td>
                <td class="px-6 py-4">
                    <span class="px-2 py-1 rounded-full text-[10px] font-bold tracking-wider uppercase ${getStatusClass(reg.status)}">
                        ${reg.status}
                    </span>
                </td>
                <td class="px-6 py-4 text-[#6B7280] text-xs">
                    ${new Date(reg.created_at).toLocaleDateString('en-GB')}
                </td>
                <td class="px-6 py-4 text-right">
                    <button 
                        onclick='viewAuditions(${JSON.stringify(reg.audition_files)})'
                        class="px-3 py-1.5 rounded bg-white border border-[#DBE2EF] text-[#3F72AF] text-xs font-bold hover:bg-[#3F72AF] hover:text-white hover:border-[#3F72AF] transition-all flex items-center gap-1.5 ml-auto"
                    >
                        ${ICONS.eye.replace('<svg', '<svg class="w-3.5 h-3.5"')}
                        Auditions (${reg.audition_files.length})
                    </button>
                </td>
            </tr>
        `).join('');
    }

    function getPreferenceClass(pref) {
        switch(pref) {
            case 'AZAAN': return 'bg-blue-100 text-blue-700';
            case 'TAKHBIRA': return 'bg-indigo-100 text-indigo-700';
            case 'BOTH': return 'bg-purple-100 text-purple-700';
            default: return 'bg-gray-100 text-gray-700';
        }
    }

    function getStatusClass(status) {
        switch(status) {
            case 'PENDING': return 'bg-amber-100 text-amber-700';
            case 'ALLOTTED': return 'bg-green-100 text-green-700';
            default: return 'bg-gray-100 text-gray-700';
        }
    }

    function viewAuditions(files) {
        if (!files || files.length === 0) {
            showDialog({
                title: 'No Files',
                message: 'This user did not upload any audition files.',
                variant: 'info'
            });
            return;
        }

        // Just open the first file for now, or we could extend the modal to handle a list
        // However audition-modal.js openAuditionModal takes a single file object: { url, name, type }
        // Let's open the first one and show a choice if multiple (or just use the first for now to keep it simple as a starting point)
        const file = {
            url: files[0].audition_file_path || files[0].url,
            name: files[0].audition_display_name || files[0].name || 'Audition 1',
            type: files[0].audition_file_type || files[0].type || 'audio'
        };

        // Fix URL if it's relative
        if (file.url && !file.url.startsWith('http')) {
            file.url = window.API_BASE + (file.url.startsWith('/') ? '' : '/') + file.url;
        }

        openAuditionModal(file);
    }

    function logout() {
        localStorage.clear();
        window.location.href = '/admin/login.php';
    }
</script>

<?php include '../includes/footer.php'; ?>
