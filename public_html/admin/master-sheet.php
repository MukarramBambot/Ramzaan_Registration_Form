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
                        <a href="/admin/khidmat-requests.php" class="px-3 py-1.5 rounded-md text-[#DBE2EF] hover:text-white hover:bg-white/10 text-sm font-medium transition-all flex items-center gap-2">
                             <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M22 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
                            Requests
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
                                    <div id="initial-loader" class="mb-4"></div>
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
        const initialLoader = document.getElementById('initial-loader');
        
        if (refreshIcon) refreshIcon.innerHTML = ICONS.loader2.replace('animate-spin', '').replace('<svg', '<svg class="w-4 h-4"');
        if (syncIcon) syncIcon.innerHTML = ICONS.fileSpreadsheet.replace('<svg', '<svg class="w-4 h-4"');
        if (initialLoader) initialLoader.innerHTML = ICONS.loader2;
        
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
                        ${Array.isArray(reg.preference) ? reg.preference.join(', ') : reg.preference}
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
                    <div class="flex flex-col gap-2 items-end">
                        <button 
                            onclick='viewAuditions(${JSON.stringify(reg.id)})'
                            class="px-3 py-1.5 rounded bg-white border border-[#DBE2EF] text-[#3F72AF] text-xs font-bold hover:bg-[#3F72AF] hover:text-white hover:border-[#3F72AF] transition-all flex items-center gap-1.5 ml-auto w-full justify-center"
                        >
                            ${ICONS.eye.replace('<svg', '<svg class="w-3.5 h-3.5"')}
                            Auditions (${reg.audition_files.length})
                        </button>
                        <button 
                            onclick='requestCorrection(${JSON.stringify(reg.id)}, "${reg.full_name}")'
                            class="px-3 py-1.5 rounded bg-white border border-amber-200 text-amber-600 text-xs font-bold hover:bg-amber-50 hover:border-amber-300 transition-all flex items-center gap-1.5 ml-auto w-full justify-center"
                        >
                            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
                            Correction
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');
    }

    // ... existing helpers ...

    function requestCorrection(regId, fullName) {
        const modalHTML = `
            <div class="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6 animate-fadeIn" id="correction-modal">
                <div class="absolute inset-0 bg-black/60 backdrop-blur-sm transition-opacity" onclick="closeCorrectionModal()"></div>
                
                <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-md flex flex-col animate-zoomIn">
                    <div class="px-6 py-4 border-b border-gray-100 flex items-center justify-between bg-gray-50/50 rounded-t-2xl">
                        <div>
                            <h3 class="text-lg font-bold text-gray-900">Request Correction</h3>
                            <p class="text-sm text-gray-500">For ${fullName}</p>
                        </div>
                        <button onclick="closeCorrectionModal()" class="p-2 text-gray-400 hover:text-gray-600 rounded-full hover:bg-gray-200/50 transition-all">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                        </button>
                    </div>

                    <div class="p-6 space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Field to Correct</label>
                            <select id="correction-field" class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm p-2 border">
                                <option value="audition_files">Audition Files (Re-upload)</option>
                                <option value="full_name">Full Name</option>
                                <option value="its_number">ITS Number</option>
                                <option value="phone_number">Phone Number</option>
                                <option value="email">Email Address</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Message for User</label>
                            <textarea id="correction-msg" rows="3" class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm p-2 border" placeholder="e.g., Please upload a clearer audio file of Azaan."></textarea>
                        </div>
                    </div>

                    <div class="px-6 py-4 border-t border-gray-100 flex justify-end bg-white rounded-b-2xl gap-3">
                        <button onclick="closeCorrectionModal()" class="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg font-medium text-sm transition-all">
                            Cancel
                        </button>
                        <button onclick="submitCorrection(${regId})" class="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-medium text-sm shadow-lg shadow-indigo-200 transition-all">
                            Send Request
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        const container = document.createElement('div');
        container.id = 'correction-modal-wrapper';
        container.innerHTML = modalHTML;
        document.body.appendChild(container);
    }

    function closeCorrectionModal() {
        const el = document.getElementById('correction-modal-wrapper');
        if (el) el.remove();
        
    }

    async function submitCorrection(regId) {
        const field = document.getElementById('correction-field').value;
        const msg = document.getElementById('correction-msg').value;
        
        if (!msg.trim()) {
            alert("Please enter a message for the user.");
            return;
        }

        const btn = document.querySelector('#correction-modal button.bg-indigo-600');
        const originalText = btn.innerHTML;
        btn.innerHTML = 'Sending...';
        btn.disabled = true;

        try {
            const response = await apiFetch('/api/corrections/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    registration: regId,
                    field_name: field,
                    admin_message: msg
                }),
                requireAuth: true
            });

            if (!response.ok) throw new Error((await response.json()).error || 'Failed to send request');
            
            closeCorrectionModal();
            showDialog({
                variant: 'success',
                title: 'Request Sent',
                message: 'Correction link has been generated (Notification pending integration).',
                confirmLabel: 'OK'
            });

        } catch (e) {
            alert(e.message);
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    }

    function getPreferenceClass(pref) {
        // pref may be array or string. Choose class based on presence of key items.
        if (Array.isArray(pref)) {
            if (pref.includes('Azaan') && pref.includes('Takhbira')) return 'bg-purple-100 text-purple-700';
            if (pref.includes('Azaan')) return 'bg-blue-100 text-blue-700';
            if (pref.includes('Takhbira')) return 'bg-indigo-100 text-indigo-700';
            if (pref.includes('Sanah')) return 'bg-teal-100 text-teal-700';
            if (pref.includes('Tajwid Quran Tilawat') || pref.includes('Tajweed Quran Tilawat')) return 'bg-yellow-100 text-yellow-700';
            if (pref.includes('Dua e Joshan')) return 'bg-rose-100 text-rose-700';
            if (pref.includes('Yaseen')) return 'bg-gray-100 text-gray-700';
            return 'bg-gray-100 text-gray-700';
        }
        // legacy string values
        switch(pref) {
            case 'AZAAN': return 'bg-blue-100 text-blue-700';
            case 'TAKHBIRA': return 'bg-indigo-100 text-indigo-700';
            case 'BOTH': return 'bg-purple-100 text-purple-700';
            case 'SANAH': return 'bg-teal-100 text-teal-700';
            case 'TAJWEED QURAN TILAWAT': return 'bg-yellow-100 text-yellow-700';
            case 'DUA E JOSHAN': return 'bg-rose-100 text-rose-700';
            case 'YASEEN': return 'bg-gray-100 text-gray-700';
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

    async function viewAuditions(regId) {
        // 1. Fetch fresh data
        let files = [];
        try {
            const response = await apiFetch(`/api/registrations/${regId}/auditions/`, { requireAuth: true });
            if (!response.ok) throw new Error('Failed to fetch auditions');
            files = await response.json();
        } catch (e) {
            showDialog({ title: 'Error', message: e.message, variant: 'danger' });
            return;
        }

        if (!files || files.length === 0) {
            showDialog({
                title: 'No Files',
                message: 'This user did not upload any audition files.',
                variant: 'info'
            });
            return;
        }

        // 2. Build Modal Content
        const container = document.getElementById('audition-modal-container');
        
        const renderFileList = () => {
            return files.map(file => {
                const isSelected = file.is_selected;
                const borderClass = isSelected ? 'border-green-500 ring-4 ring-green-500/20 bg-green-50' : 'border-gray-200';
                const btnClass = isSelected 
                    ? 'bg-green-600 text-white cursor-default' 
                    : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50';
                const btnText = isSelected ? 'Selected' : 'Select';
                
                // Fix URL
                let url = file.audition_file_path;
                if (url && !url.startsWith('http')) {
                    url = window.API_BASE + (url.startsWith('/') ? '' : '/') + url;
                }

                return `
                    <div class="flex flex-col sm:flex-row gap-4 p-4 rounded-xl border-2 ${borderClass} transition-all mb-4 bg-white shadow-sm relative overflow-hidden">
                        ${isSelected ? '<div class="absolute top-0 right-0 bg-green-500 text-white text-[10px] px-2 py-1 uppercase font-bold tracking-wider rounded-bl-lg">Approved</div>' : ''}
                        
                        <div class="flex-1 min-w-0">
                            <h4 class="font-medium text-gray-900 truncate" title="${file.audition_display_name}">${file.audition_display_name}</h4>
                            <p class="text-xs text-gray-500 mt-1 mb-3">Uploaded: ${new Date(file.uploaded_at).toLocaleString()}</p>
                            
                            <audio controls class="w-full h-10" preload="metadata">
                                <source src="${url}" type="audio/mpeg">
                                Your browser does not support the audio element.
                            </audio>
                        </div>

                        <!--
                        <div class="flex items-center sm:self-center pt-2 sm:pt-0">
                            <button 
                                onclick="selectAudition(${file.id}, ${regId})"
                                class="px-4 py-2 rounded-lg text-sm font-bold transition-all w-full sm:w-auto ${btnClass}"
                                ${isSelected ? 'disabled' : ''}
                            >
                                ${isSelected 
                                    ? `<span class="flex items-center gap-2"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg> Selected</span>` 
                                    : 'Select as Final'}
                            </button>
                        </div>
                        -->
                    </div>
                `;
            }).join('');
        };

        const modalHTML = `
            <div class="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6 animate-fadeIn">
                <div class="absolute inset-0 bg-black/60 backdrop-blur-sm transition-opacity" onclick="closeAuditionModal()"></div>
                
                <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-4xl max-h-[90vh] flex flex-col animate-zoomIn">
                    <!-- Header -->
                    <div class="px-6 py-4 border-b border-gray-100 flex items-center justify-between bg-gray-50/50 rounded-t-2xl">
                        <div>
                            <h3 class="text-lg font-bold text-gray-900">Audition Files</h3>
                            <p class="text-sm text-gray-500">Select one file for the final approved audition.</p>
                        </div>
                        <button onclick="closeAuditionModal()" class="p-2 text-gray-400 hover:text-gray-600 rounded-full hover:bg-gray-200/50 transition-all">
                            ${ICONS.x || '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>'}
                        </button>
                    </div>

                    <!-- List -->
                    <div class="p-6 overflow-y-auto bg-gray-50 custom-scrollbar" id="audition-list-container">
                        ${renderFileList()}
                    </div>

                    <!-- Footer -->
                    <div class="px-6 py-4 border-t border-gray-100 flex justify-end bg-white rounded-b-2xl">
                        <button onclick="closeAuditionModal()" class="px-6 py-2.5 bg-gray-900 text-white rounded-lg hover:bg-gray-800 font-medium text-sm shadow-lg shadow-gray-200 transition-all">
                            Done
                        </button>
                    </div>
                </div>
            </div>
        `;

        container.innerHTML = modalHTML;
        document.body.style.overflow = 'hidden';

        // 3. Define Select Handler Helper
        window.selectAudition = async (fileId, regId) => {
            if (!confirm('Are you sure you want to select this audition? This will unselect any other files for this user.')) return;

            // Show loading overlay or modify button state (simplified here)
            const btn = event.target.closest('button');
            const originalText = btn.innerHTML;
            btn.disabled = true;
            btn.innerHTML = 'Saving...';

            try {
                const response = await apiFetch(`/api/audition-files/${fileId}/select_audition/`, {
                    method: 'PATCH',
                    requireAuth: true
                });

                if (!response.ok) {
                    const data = await response.json();
                    throw new Error(data.error || 'Failed to select audition');
                }

                // Refresh the modal content
                viewAuditions(regId); // Recursively reload to show updated state
                
                // Optional: Refresh background table row if needed, but not strictly required by prompt constraints on stability.
                // loadMasterSheet(); // Doing this might disrupt the view if they are deep in scrolling.

            } catch (err) {
                alert(err.message);
                btn.disabled = false;
                btn.innerHTML = originalText;
            }
        };
    }

    function logout() {
        localStorage.clear();
        window.location.href = '/admin/login.php';
    }
</script>

<?php include '../includes/footer.php'; ?>
