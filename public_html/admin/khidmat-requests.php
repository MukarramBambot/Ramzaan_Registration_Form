<?php include '../includes/admin-header.php'; ?>

<!-- Content Wrapper -->
<div class="min-h-screen bg-[#F9F7F7]">
    
    <!-- Header -->
    <div class="bg-[#112D4E] py-5 px-6 shadow-md">
        <div class="flex items-center justify-between">
            <div>
                <div class="flex items-center gap-6 mb-1">
                    <h1 class="text-2xl text-white font-normal">
                        Khidmat Requests
                    </h1>
                    <div class="flex items-center gap-2 ml-4">
                        <a href="<?= BASE_URL ?>/admin/dashboard.php" class="px-3 py-1.5 rounded-md text-[#DBE2EF] hover:text-white hover:bg-white/10 text-sm font-medium transition-all flex items-center gap-2">
                             <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line></svg>
                            Duty Roster
                        </a>
                        <a href="<?= BASE_URL ?>/admin/master-sheet.php" class="px-3 py-1.5 rounded-md text-[#DBE2EF] hover:text-white hover:bg-white/10 text-sm font-medium transition-all flex items-center gap-2">
                           <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="8" y1="13" x2="16" y2="13"></line><line x1="8" y1="17" x2="16" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                            Master Sheet
                        </a>
                        <a href="<?= BASE_URL ?>/admin/khidmat-requests.php" class="px-3 py-1.5 rounded-md bg-[#3F72AF] text-white text-sm font-medium flex items-center gap-2">
                            <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M22 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
                            Requests
                        </a>
                        <span class="text-[#DBE2EF]/30 mx-1">|</span>
                        <a href="<?= BASE_URL ?>/admin/vajebaat-appointments.php" class="whitespace-nowrap px-3 py-1.5 rounded-md text-[#DBE2EF] hover:text-white hover:bg-white/10 text-sm font-medium transition-all flex items-center gap-2">
                            <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                            Vajebaat
                        </a>
                    </div>
                </div>
                <p class="text-[#DBE2EF] text-sm font-light">
                    Manage User Cancellation & Reallocation Requests
                </p>
            </div>
             <div class="flex items-center gap-3 text-[#DBE2EF] text-sm">
                <button
                    id="refresh-btn"
                    onclick="loadRequests()"
                    class="px-3 py-1.5 rounded-md bg-white/10 hover:bg-white/20 text-white text-sm font-medium transition-all flex items-center gap-2"
                    title="Refresh Data"
                >
                    <span id="refresh-icon"></span>
                    <span>Refresh</span>
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
            <div class="responsive-table-container custom-scrollbar">
                <table class="w-full text-left border-collapse">
                    <thead class="bg-[#F9FAFB] border-b border-[#DBE2EF]">
                        <tr>
                            <th class="px-6 py-4 text-xs font-bold text-[#6B7280] uppercase tracking-wider">User Info</th>
                            <th class="px-6 py-4 text-xs font-bold text-[#6B7280] uppercase tracking-wider">Current Duty</th>
                            <th class="px-6 py-4 text-xs font-bold text-[#6B7280] uppercase tracking-wider">Request Type</th>
                            <th class="px-6 py-4 text-xs font-bold text-[#6B7280] uppercase tracking-wider">Submitted</th>
                            <th class="px-6 py-4 text-xs font-bold text-[#6B7280] uppercase tracking-wider text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody id="requests-table-body" class="divide-y divide-[#DBE2EF]">
                        <!-- Data will be loaded here -->
                        <tr>
                            <td colspan="5" class="px-6 py-12 text-center text-[#9CA3AF]">
                                <div class="flex flex-col items-center">
                                    <div id="initial-loader" class="mb-4"></div>
                                    <p>Loading requests...</p>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    <!-- Reallocation Modal -->
    <div id="reallocation-modal" class="fixed inset-0 z-[100] hidden bg-slate-900/60 backdrop-blur-sm animate-fadeIn">
        <div class="flex items-center justify-center min-h-screen p-4">
            <div class="bg-white rounded-3xl shadow-2xl max-w-md w-full overflow-hidden animate-slideUp">
                <div class="bg-[#112D4E] p-6 text-white">
                    <h3 class="text-xl font-bold">Approve Reallocation Request</h3>
                    <p class="text-blue-100 text-sm mt-1">Move user to a different duty date</p>
                </div>
                
                <div class="p-8 space-y-6">
                    <div>
                        <label class="block text-xs font-bold text-[#6B7280] uppercase tracking-wider mb-2">Current Duty Date</label>
                        <div id="current-date-display" class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-slate-500 font-medium">
                            --
                        </div>
                    </div>

                    <div>
                        <label for="new-duty-date" class="block text-xs font-bold text-[#6B7280] uppercase tracking-wider mb-2">Select New Duty Date</label>
                        <input 
                            type="date" 
                            id="new-duty-date"
                            class="w-full px-4 py-3 bg-white border-2 border-[#DBE2EF] rounded-xl focus:outline-none focus:border-[#3F72AF] transition-all text-[#112D4E] font-medium"
                            required
                        >
                    </div>

                    <div class="pt-2 flex gap-3">
                        <button 
                            onclick="closeReallocationModal()"
                            class="flex-1 px-6 py-3 border-2 border-slate-200 text-slate-600 rounded-xl font-bold hover:bg-slate-50 transition-all"
                        >
                            Cancel
                        </button>
                        <button 
                            id="confirm-reallocation-btn"
                            onclick="submitReallocation()"
                            class="flex-1 px-6 py-3 bg-[#3F72AF] text-white rounded-xl font-bold hover:bg-[#112D4E] shadow-lg shadow-blue-500/20 transition-all active:scale-[0.98]"
                        >
                            Confirm & Update
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>

</div>


<script src="<?= BASE_URL ?>/assets/js/main.js"></script>
<?php include '../includes/footer.php'; ?>

<script>
    document.addEventListener('DOMContentLoaded', () => {
        // Initialize icons
        const refreshIcon = document.getElementById('refresh-icon');
        const initialLoader = document.getElementById('initial-loader');
        
        if (refreshIcon) refreshIcon.innerHTML = ICONS.loader2.replace('animate-spin', '').replace('<svg', '<svg class="w-4 h-4"');
        if (initialLoader) initialLoader.innerHTML = ICONS.loader2;
        
        loadRequests();
    });

    async function loadRequests() {
        const tbody = document.getElementById('requests-table-body');
        const refreshBtn = document.getElementById('refresh-btn');
        const refreshIcon = document.getElementById('refresh-icon');
        
        if (refreshIcon) {
            refreshIcon.innerHTML = ICONS.loader2.replace('<svg', '<svg class="w-4 h-4"');
            refreshBtn.disabled = true;
        }

        try {
            const response = await apiFetch('/api/khidmat-requests/?status=pending', {
                requireAuth: true
            });

            if (!response.ok) {
                if (response.status === 401 || response.status === 403) return;
                throw new Error(`Error ${response.status}: Failed to fetch data`);
            }


            const data = await response.json();
            const requests = data.results || [];  // Extract results from paginated response
            renderTable(requests);

        } catch (err) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="5" class="px-6 py-12 text-center text-red-500">
                        <p class="font-medium">Failed to load requests</p>
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

    function renderTable(requests) {
        const tbody = document.getElementById('requests-table-body');
        
        if (requests.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="5" class="px-6 py-12 text-center text-[#9CA3AF]">
                        <p>No pending requests found.</p>
                    </td>
                </tr>
            `;
            return;
        }

        tbody.innerHTML = requests.map(req => {
            const user = req.user_details;
            const duty = req.assignment_details;
            const type = req.request_type_display;
            const typeClass = req.request_type === 'cancel' ? 'bg-red-50 text-red-700' : 'bg-amber-50 text-amber-700';

            return `
                <tr id="req-row-${req.id}" 
                    data-type="${req.request_type}" 
                    data-date="${duty.date}" 
                    class="hover:bg-[#F9FAFB] transition-colors"
                >
                    <td class="px-6 py-4">
                        <div class="text-sm font-bold text-[#112D4E]">${user.full_name}</div>
                        <div class="text-[11px] font-mono text-[#6B7280]">${user.its_number}</div>
                        <div class="text-[11px] text-[#3F72AF] mt-0.5">${user.phone_number}</div>
                    </td>
                    <td class="px-6 py-4">
                        <div class="text-xs text-[#112D4E] font-medium">${duty.date}</div>
                        <div class="text-[10px] text-[#6B7280] uppercase tracking-wider">${duty.namaaz}</div>
                    </td>
                    <td class="px-6 py-4">
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-tight ${typeClass}">
                            ${type}
                        </span>
                    </td>
                    <td class="px-6 py-4 text-xs text-[#6B7280]">
                        ${new Date(req.created_at).toLocaleDateString()}
                        <div class="text-[10px] opacity-60">${new Date(req.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
                    </td>
                    <td class="px-6 py-4 text-right">
                        <div class="flex items-center justify-end gap-2">
                            <button 
                                onclick="handleAction(${req.id}, 'approve')"
                                class="p-2 bg-green-50 text-green-600 hover:bg-green-600 hover:text-white rounded-lg transition-all"
                                title="Approve Request"
                            >
                                <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                            </button>
                            <button 
                                onclick="handleAction(${req.id}, 'reject')"
                                class="p-2 bg-red-50 text-red-600 hover:bg-red-600 hover:text-white rounded-lg transition-all"
                                title="Reject Request"
                            >
                                <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                            </button>
                        </div>
                    </td>
                </tr>
            `;
        }).join('');
    }

    let activeRequestId = null;

    async function handleAction(requestId, action) {
        const row = document.getElementById(`req-row-${requestId}`);
        const originalBg = row.style.backgroundColor;
        const requestType = row.dataset.type;

        // Special handling for reallocation approval
        if (action === 'approve' && requestType === 'reallocate') {
            const currentDate = row.dataset.date;
            openReallocationModal(requestId, currentDate);
            return;
        }
        
        showDialog({
            variant: action === 'approve' ? 'info' : 'danger',
            title: `${action.charAt(0).toUpperCase() + action.slice(1)} Request?`,
            message: `Are you sure you want to ${action} this request? This action is irreversible.`,
            confirmLabel: `Yes, ${action}`,
            onConfirm: () => executeAction(requestId, action)
        });
    }

    async function executeAction(requestId, action, payload = {}) {
        const row = document.getElementById(`req-row-${requestId}`);
        if (!row) return;

        const originalBg = row.style.backgroundColor;
        
        try {
            row.style.opacity = '0.5';
            row.classList.add('pointer-events-none');

            const response = await apiFetch(`/api/khidmat-requests/${requestId}/${action}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload),
                requireAuth: true
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || `Failed to ${action} request`);
            }

            // Success animation and removal
            row.style.backgroundColor = action === 'approve' ? '#ecfdf5' : '#fef2f2';
            setTimeout(() => {
                row.style.transform = 'translateX(20px)';
                row.style.opacity = '0';
                setTimeout(() => {
                    loadRequests(); // Reload to refresh list
                }, 300);
            }, 500);

        } catch (err) {
            row.style.opacity = '1';
            row.style.backgroundColor = originalBg;
            row.classList.remove('pointer-events-none');
            
            showDialog({
                variant: 'danger',
                title: 'Action Failed',
                message: err.message,
                confirmLabel: 'Close'
            });
        }
    }

    function openReallocationModal(requestId, currentDate) {
        activeRequestId = requestId;
        document.getElementById('current-date-display').innerText = currentDate;
        document.getElementById('new-duty-date').value = '';
        document.getElementById('reallocation-modal').classList.remove('hidden');
    }

    function closeReallocationModal() {
        document.getElementById('reallocation-modal').classList.add('hidden');
        activeRequestId = null;
    }

    async function submitReallocation() {
        const newDate = document.getElementById('new-duty-date').value;
        if (!newDate) {
            showDialog({
                variant: 'danger',
                title: 'Date Required',
                message: 'Please select a new duty date to proceed with reallocation.',
                confirmLabel: 'OK'
            });
            return;
        }

        const btn = document.getElementById('confirm-reallocation-btn');
        const originalText = btn.innerText;
        btn.innerText = 'Updating...';
        btn.disabled = true;

        try {
            await executeAction(activeRequestId, 'approve', { new_date: newDate });
            closeReallocationModal();
        } catch (err) {
            // Error handled in executeAction
        } finally {
            btn.innerText = originalText;
            btn.disabled = false;
        }
    }

    async function logout() {
        localStorage.removeItem('token');
        window.location.href = window.BASE_URL + '/admin/login.php';
    }
</script>
