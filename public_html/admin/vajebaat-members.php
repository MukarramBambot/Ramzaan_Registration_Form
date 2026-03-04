<?php include '../includes/admin-header.php'; ?>

<!-- Content Wrapper -->
<div class="min-h-screen bg-[#F9F7F7]">
    
    <!-- Header -->
    <div class="bg-[#112D4E] py-5 px-6 shadow-md">
        <div class="flex items-center justify-between">
            <div>
                <div class="flex flex-col md:flex-row md:items-center gap-2 md:gap-6 mb-1">
                    <h1 class="text-xl md:text-2xl text-white font-normal">
                        Vajebaat Members
                    </h1>
                    <div class="flex items-center gap-2 mt-2 md:mt-0 md:ml-4 overflow-x-auto pb-2 md:pb-0">
                        <a href="<?= BASE_URL ?>/admin/dashboard.php" class="whitespace-nowrap px-3 py-1.5 rounded-md text-[#DBE2EF] hover:text-white hover:bg-white/10 text-sm font-medium transition-all flex items-center gap-2">
                            <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line></svg>
                            Registration
                        </a>
                        <span class="text-[#DBE2EF]/30 mx-1">|</span>
                        <a href="<?= BASE_URL ?>/admin/vajebaat-appointments.php" class="whitespace-nowrap px-3 py-1.5 rounded-md text-[#DBE2EF] hover:text-white hover:bg-white/10 text-sm font-medium transition-all flex items-center gap-2">
                            <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                            Appointments
                        </a>
                        <a href="<?= BASE_URL ?>/admin/vajebaat-members.php" class="whitespace-nowrap px-3 py-1.5 rounded-md bg-[#3F72AF] text-white text-sm font-medium flex items-center gap-2">
                            <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M22 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
                            Members
                        </a>
                    </div>
                </div>
                <p class="text-[#DBE2EF] text-sm font-light">
                    Vajebaat Master Directory – Sherullah 1447H
                </p>
            </div>
             <div class="flex items-center gap-3 text-[#DBE2EF] text-sm">
                <button
                    id="sync-btn"
                    onclick="syncToSheet()"
                    class="px-3 py-1.5 rounded-md bg-green-500/20 hover:bg-green-500/30 text-green-100 text-sm font-medium transition-all flex items-center gap-2"
                    title="Sync to Google Sheet"
                >
                    <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="8" y1="13" x2="16" y2="13"></line><line x1="8" y1="17" x2="16" y2="17"></line></svg>
                    <span id="sync-label">Sync Sheet</span>
                </button>
                <button
                    onclick="exportCSV()"
                    class="px-3 py-1.5 rounded-md bg-blue-500/20 hover:bg-blue-500/30 text-blue-100 text-sm font-medium transition-all flex items-center gap-2"
                    title="Download CSV"
                >
                    <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                    Export CSV
                </button>
                <button
                    id="refresh-btn"
                    onclick="loadDirectory()"
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

    <!-- Filters Bar -->
    <div class="px-6 pt-4 flex flex-col sm:flex-row gap-3">
        <div class="relative flex-1 max-w-md">
            <div class="absolute left-3 top-1/2 -translate-y-1/2 text-[#6B7280]">
                <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            </div>
            <input 
                type="text" 
                id="search-input" 
                placeholder="Search by ITS, Name, or Mobile..." 
                class="w-full bg-white border border-[#DBE2EF] rounded-lg pl-10 pr-4 py-2.5 text-sm focus:border-[#3F72AF] focus:ring-1 focus:ring-[#3F72AF] outline-none transition-all"
            >
        </div>
        <select 
            id="status-filter" 
            class="bg-white border border-[#DBE2EF] rounded-lg px-4 py-2.5 text-sm text-[#112D4E] focus:border-[#3F72AF] focus:ring-1 focus:ring-[#3F72AF] outline-none transition-all"
        >
            <option value="">All Statuses</option>
            <option value="PENDING">Pending</option>
            <option value="CONFIRMED">Confirmed</option>
            <option value="CANCELLED">Cancelled</option>
            <option value="COMPLETED">Completed</option>
        </select>
    </div>

    <!-- Main Content -->
    <div class="p-6 pt-4">
        <div class="bg-white rounded-xl shadow-sm border border-[#DBE2EF] overflow-hidden">
            <div class="responsive-table-container custom-scrollbar">
                <table class="w-full text-left border-collapse">
                    <thead class="bg-[#F9FAFB] border-b border-[#DBE2EF]">
                        <tr>
                            <th class="px-5 py-4 text-xs font-bold text-[#6B7280] uppercase tracking-wider">ITS</th>
                            <th class="px-5 py-4 text-xs font-bold text-[#6B7280] uppercase tracking-wider">Name</th>
                            <th class="px-5 py-4 text-xs font-bold text-[#6B7280] uppercase tracking-wider">Mobile</th>
                            <th class="px-5 py-4 text-xs font-bold text-[#6B7280] uppercase tracking-wider">Preferred Date</th>
                            <th class="px-5 py-4 text-xs font-bold text-[#6B7280] uppercase tracking-wider">Assigned</th>
                            <th class="px-5 py-4 text-xs font-bold text-[#6B7280] uppercase tracking-wider">Slot Time</th>
                            <th class="px-5 py-4 text-xs font-bold text-[#6B7280] uppercase tracking-wider">Status</th>
                            <th class="px-5 py-4 text-xs font-bold text-[#6B7280] uppercase tracking-wider">Submitted</th>
                        </tr>
                    </thead>
                    <tbody id="directory-body" class="divide-y divide-[#DBE2EF]">
                        <tr>
                            <td colspan="8" class="px-6 py-12 text-center text-[#9CA3AF]">
                                <div class="flex flex-col items-center">
                                    <div id="initial-loader" class="mb-4"></div>
                                    <p>Loading directory...</p>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Pagination -->
            <div id="pagination-bar" class="px-6 py-3 border-t border-[#DBE2EF] flex items-center justify-between text-sm text-[#6B7280] hidden">
                <span id="page-info"></span>
                <div class="flex gap-2">
                    <button id="prev-btn" onclick="changePage(-1)" class="px-3 py-1.5 rounded-lg border border-[#DBE2EF] hover:bg-[#F9FAFB] disabled:opacity-40 disabled:cursor-not-allowed transition-all" disabled>← Previous</button>
                    <button id="next-btn" onclick="changePage(1)" class="px-3 py-1.5 rounded-lg border border-[#DBE2EF] hover:bg-[#F9FAFB] disabled:opacity-40 disabled:cursor-not-allowed transition-all" disabled>Next →</button>
                </div>
            </div>
        </div>
    </div>

</div>

<script src="<?= BASE_URL ?>/assets/js/main.js"></script>
<?php include '../includes/footer.php'; ?>

<script>
    // State
    let currentPage = 1;
    let totalCount = 0;
    let nextUrl = null;
    let prevUrl = null;
    let searchDebounce = null;

    document.addEventListener('DOMContentLoaded', () => {
        const refreshIcon = document.getElementById('refresh-icon');
        const initialLoader = document.getElementById('initial-loader');
        
        if (refreshIcon) refreshIcon.innerHTML = ICONS.loader2.replace('animate-spin', '').replace('<svg', '<svg class="w-4 h-4"');
        if (initialLoader) initialLoader.innerHTML = ICONS.loader2;
        
        if (!localStorage.getItem('access_token')) {
            window.location.href = (window.BASE_URL || '') + '/admin/login.php';
            return;
        }

        // Debounced search
        document.getElementById('search-input').addEventListener('input', () => {
            clearTimeout(searchDebounce);
            searchDebounce = setTimeout(() => { currentPage = 1; loadDirectory(); }, 350);
        });

        // Status filter
        document.getElementById('status-filter').addEventListener('change', () => {
            currentPage = 1;
            loadDirectory();
        });

        loadDirectory();
    });

    async function loadDirectory() {
        const tbody = document.getElementById('directory-body');
        const refreshBtn = document.getElementById('refresh-btn');
        const refreshIcon = document.getElementById('refresh-icon');
        
        if (refreshIcon) {
            refreshIcon.innerHTML = ICONS.loader2.replace('<svg', '<svg class="w-4 h-4"');
            refreshBtn.disabled = true;
        }

        const search = document.getElementById('search-input').value.trim();
        const status = document.getElementById('status-filter').value;

        let params = `?page=${currentPage}`;
        if (search) params += `&search=${encodeURIComponent(search)}`;
        if (status) params += `&status=${status}`;

        try {
            const response = await apiFetch(`/api/vajebaat/members-directory/${params}`, { requireAuth: true });

            if (!response.ok) {
                if (response.status === 401 || response.status === 403) return;
                throw new Error(`Error ${response.status}`);
            }

            const data = await response.json();
            totalCount = data.count || 0;
            nextUrl = data.next;
            prevUrl = data.previous;

            renderTable(data.results || []);
            updatePagination();

        } catch (err) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="8" class="px-6 py-12 text-center text-red-500">
                        <p class="font-medium">Failed to load directory</p>
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

    function renderTable(rows) {
        const tbody = document.getElementById('directory-body');
        
        if (!rows || rows.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="px-6 py-12 text-center text-[#9CA3AF]">No records found.</td></tr>';
            return;
        }

        tbody.innerHTML = rows.map(r => {
            const statusColors = {
                'PENDING':   'bg-amber-100 text-amber-700',
                'CONFIRMED': 'bg-emerald-100 text-emerald-700',
                'CANCELLED': 'bg-red-100 text-red-700',
                'COMPLETED': 'bg-blue-100 text-blue-700',
            };
            const statusClass = statusColors[r.status] || 'bg-gray-100 text-gray-700';

            const prefDate = r.preferred_date ? new Date(r.preferred_date + 'T00:00:00').toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }) : '—';
            const assignDate = r.assigned_date ? new Date(r.assigned_date + 'T00:00:00').toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }) : '—';
            const slotTime = r.slot_time || '—';
            const submitted = r.created_at ? new Date(r.created_at).toLocaleDateString('en-GB', { day: '2-digit', month: 'short' }) + ' ' + new Date(r.created_at).toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' }) : '';

            return `
                <tr class="hover:bg-[#F9FAFB] transition-colors">
                    <td class="px-5 py-3.5 text-[#3F72AF] font-mono text-sm">${r.its_number || ''}</td>
                    <td class="px-5 py-3.5 text-[#112D4E] font-medium text-sm">${r.name || ''}</td>
                    <td class="px-5 py-3.5 text-sm text-[#6B7280]">${r.mobile || ''}</td>
                    <td class="px-5 py-3.5 text-sm text-[#6B7280]">${prefDate}</td>
                    <td class="px-5 py-3.5 text-sm text-[#112D4E] font-medium">${assignDate}</td>
                    <td class="px-5 py-3.5 text-sm text-[#6B7280]">${slotTime}</td>
                    <td class="px-5 py-3.5">
                        <span class="px-2.5 py-1 rounded-full text-xs font-bold ${statusClass}">${r.status}</span>
                    </td>
                    <td class="px-5 py-3.5 text-xs text-[#9CA3AF]">${submitted}</td>
                </tr>
            `;
        }).join('');
    }

    function updatePagination() {
        const bar = document.getElementById('pagination-bar');
        const info = document.getElementById('page-info');
        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');

        if (totalCount <= 50 && currentPage === 1) {
            bar.classList.add('hidden');
            return;
        }

        bar.classList.remove('hidden');
        const pageSize = 50;
        const from = (currentPage - 1) * pageSize + 1;
        const to = Math.min(currentPage * pageSize, totalCount);
        info.textContent = `Showing ${from}–${to} of ${totalCount}`;

        prevBtn.disabled = !prevUrl;
        nextBtn.disabled = !nextUrl;
    }

    function changePage(delta) {
        currentPage += delta;
        if (currentPage < 1) currentPage = 1;
        loadDirectory();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    async function syncToSheet() {
        const btn = document.getElementById('sync-btn');
        const label = document.getElementById('sync-label');
        
        btn.disabled = true;
        label.textContent = 'Syncing...';

        try {
            const response = await apiFetch('/api/vajebaat/sync-sheet/', {
                method: 'POST',
                requireAuth: true,
            });

            const data = await response.json();
            
            if (data.status === 'success') {
                showDialog({
                    variant: 'info',
                    title: 'Sheet Synced',
                    message: `Successfully synced ${data.records_synced} records to Google Sheets (Vajebaat_1447 tab).`,
                    confirmLabel: 'OK',
                    cancelLabel: null,
                });
            } else {
                throw new Error(data.detail || 'Sync failed');
            }
        } catch (err) {
            showDialog({
                variant: 'danger',
                title: 'Sync Failed',
                message: err.message || 'Could not sync to Google Sheets.',
                confirmLabel: 'OK',
                cancelLabel: null,
            });
        } finally {
            btn.disabled = false;
            label.textContent = 'Sync Sheet';
        }
    }

    async function exportCSV() {
        try {
            const token = localStorage.getItem('access_token');
            const resp = await fetch(`${window.API_BASE}/api/vajebaat/export-csv/`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (!resp.ok) throw new Error('Export failed');
            const blob = await resp.blob();
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'vajebaat_members.csv';
            document.body.appendChild(a);
            a.click();
            a.remove();
            URL.revokeObjectURL(url);
        } catch (err) {
            showDialog({
                variant: 'danger',
                title: 'Export Failed',
                message: err.message || 'Could not export CSV.',
                confirmLabel: 'OK',
                cancelLabel: null,
            });
        }
    }

    function logout() {
        localStorage.clear();
        window.location.href = (window.BASE_URL || '') + '/admin/login.php';
    }
</script>
