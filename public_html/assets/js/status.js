/**
 * Status Page Logic (Simplified)
 * Handles searching for registrations and direct Khidmat requests.
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const searchBtn = document.getElementById('search-btn');
    const itsInput = document.getElementById('its-number');
    const resultContainer = document.getElementById('result-container');

    // Event Listeners
    if (itsInput) {
        itsInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') checkStatus();
        });
    }

    // Expose functions globally for inline onclick handlers
    window.checkStatus = checkStatus;
    window.requestCancel = requestCancel;
    window.requestReallocation = requestReallocation;

    /**
     * Core Search Function
     */
    async function checkStatus() {
        const its = itsInput.value.trim();

        if (!its) {
            alert("Please enter your ITS number.");
            return;
        }

        // Loading state
        const originalHTML = searchBtn.innerHTML;
        searchBtn.disabled = true;
        searchBtn.innerHTML = `${ICONS.loader2} <span class="ml-2">Searching...</span>`;

        try {
            const res = await apiFetch(`/api/registrations/search/?its=${encodeURIComponent(its)}`, { requireAuth: false });

            if (!res.ok) {
                if (res.status === 404) {
                    renderError("Registration Not Found", "No record found for this ITS number.");
                } else {
                    throw new Error("Server error occurred");
                }
                return;
            }

            const data = await res.json();
            renderResult(data);

        } catch (err) {
            console.error(err);
            renderError("Connection Error", "Unable to reach the server.");
        } finally {
            searchBtn.disabled = false;
            searchBtn.innerHTML = originalHTML;
            resultContainer.classList.remove('hidden');
            resultContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    /**
     * Action Functions (Direct API Calls)
     */
    async function requestCancel(dutyId) {
        if (!confirm("Are you sure you want to request cancellation for this Khidmat?")) return;
        
        try {
            const res = await apiFetch(`/api/assignments/${dutyId}/cancel/`, {
                method: "POST",
                requireAuth: false
            });

            if (res.ok) {
                alert("Cancellation request submitted successfully.");
                checkStatus(); // Refresh result
            } else {
                const data = await res.json();
                alert(data.error || "Unable to submit request.");
            }
        } catch (err) {
            console.error(err);
            alert("Connection error.");
        }
    }

    async function requestReallocation(dutyId) {
        if (!confirm("Are you sure you want to request reallocation for this Khidmat?")) return;

        try {
            const res = await apiFetch(`/api/assignments/${dutyId}/reallocate/`, {
                method: "POST",
                requireAuth: false
            });

            if (res.ok) {
                alert("Reallocation request submitted successfully.");
                checkStatus(); // Refresh result
            } else {
                const data = await res.json();
                alert(data.error || "Unable to submit request.");
            }
        } catch (err) {
            console.error(err);
            alert("Connection error.");
        }
    }

    /**
     * Rendering Logic
     */
    function renderResult(data) {
        const hasDuties = Array.isArray(data.duties) && data.duties.length > 0;
        const isRejected = data.status === 'REJECTED';

        const statusLabel = isRejected ? 'Rejected' : (hasDuties ? 'Confirmed' : 'Pending Review');
        const colorClass = isRejected ? 'bg-red-100 text-red-700' : (hasDuties ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700');

        const formatDateDMY = (dmy) => {
            try {
                const [dd, mm, yyyy] = dmy.split('/').map(Number);
                const date = new Date(yyyy, mm - 1, dd);
                return date.toLocaleDateString(undefined, { day: 'numeric', month: 'long', year: 'numeric' });
            } catch (e) {
                return dmy;
            }
        };

        let dutyMarkup = '';
        if (hasDuties) {
            dutyMarkup = `
                <div class="space-y-3">
                    ${data.duties.map(d => {
                        const isPending = d.request_status === 'pending';
                        const badgeLabel = d.request_type === 'cancel' ? 'Cancellation Requested' : 'Reallocation Requested';
                        
                        return `
                        <div class="p-3 border rounded-lg bg-white flex flex-col gap-2">
                            <div class="flex items-center justify-between">
                                <div>
                                    <div class="text-sm text-[#6B7280]">Date</div>
                                    <div class="text-[#112D4E] font-bold">${formatDateDMY(d.date)}</div>
                                </div>
                                <div class="text-right">
                                    <div class="text-sm text-[#6B7280]">Duty</div>
                                    <div class="text-[#112D4E] font-bold">${(d.namaaz || '') + (d.type ? ' ' + d.type : '')}</div>
                                </div>
                            </div>
                            ${isPending ? `
                                <div class="mt-2 px-3 py-1.5 bg-amber-50 border border-amber-200 rounded-lg flex items-center gap-2">
                                    <div class="w-2 h-2 rounded-full bg-amber-500 animate-pulse"></div>
                                    <span class="text-amber-800 text-[11px] font-bold uppercase tracking-wider">${badgeLabel}</span>
                                </div>
                            ` : ''}
                        </div>
                        `;
                    }).join('')}
                </div>
            `;
        }

        resultContainer.innerHTML = `
            <div class="bg-white rounded-3xl shadow-xl border border-[#DBE2EF] overflow-hidden animate-zoomIn">
                <div class="bg-[#112D4E] p-6 text-center">
                    <div id="status-badge" class="inline-flex px-3 py-1 rounded-full ${colorClass} text-[10px] font-bold tracking-widest uppercase mb-3">
                        ${statusLabel}
                    </div>
                    <h3 class="text-white text-xl font-bold">${data.full_name}</h3>
                    <p class="text-[#DBE2EF]/60 text-sm font-mono mt-1">${data.its_number}</p>
                </div>

                <div class="p-8 space-y-6">
                    <div class="flex items-center justify-between border-b border-[#F9F7F7] pb-4">
                        <span class="text-[#6B7280] text-sm">Preference</span>
                        <span class="text-[#112D4E] font-bold text-sm tracking-wide uppercase">${data.register_for}</span>
                    </div>

                    ${hasDuties ? `
                        <div class="bg-green-50 rounded-2xl p-4 border border-green-100">
                            <p class="text-green-800 text-sm font-medium">Assignment Confirmed!</p>
                        </div>
                        ${dutyMarkup}
                        
                        ${!data.duties.some(d => d.request_status === 'pending') ? `
                            <div id="action-buttons-container" class="flex flex-col gap-3 mt-6 pt-4 border-t border-[#F9F7F7]">
                                <button onclick="requestCancel(${data.duties[0].id})"
                                    class="w-full px-4 py-3 bg-red-100 text-red-700 hover:bg-red-200 rounded-xl text-sm font-bold transition-colors">
                                    Cancel Khidmat
                                </button>
                                <button onclick="requestReallocation(${data.duties[0].id})"
                                    class="w-full px-4 py-3 bg-amber-100 text-amber-700 hover:bg-amber-200 rounded-xl text-sm font-bold transition-colors">
                                    Request Reallocation
                                </button>
                            </div>
                        ` : `
                            <div class="mt-6 pt-4 border-t border-[#F9F7F7]">
                                <p class="text-[#6B7280] text-xs text-center italic">Your request is being reviewed by the admin.</p>
                            </div>
                        `}
                    ` : (isRejected ? `
                         <div class="bg-red-50 rounded-2xl p-4 border border-red-100">
                            <p class="text-red-800 text-sm font-medium">Your registration has been rejected.</p>
                        </div>
                    ` : `
                        <div class="bg-amber-50 rounded-2xl p-4 border border-amber-100">
                            <p class="text-amber-800 text-sm font-medium">Review in Progress</p>
                        </div>
                    `)}
                </div>
            </div>
        `;
    }

    function renderError(title, msg) {
        resultContainer.innerHTML = `
            <div class="bg-white rounded-3xl shadow-lg border border-red-100 p-8 text-center animate-zoomIn">
                <h3 class="text-[#112D4E] font-bold text-lg">${title}</h3>
                <p class="text-[#6B7280] text-sm mt-1 mb-6">${msg}</p>
                <div class="cursor-pointer text-[#3F72AF] text-sm font-bold hover:underline" onclick="window.location.reload()">Reset Search</div>
            </div>
        `;
    }
});
