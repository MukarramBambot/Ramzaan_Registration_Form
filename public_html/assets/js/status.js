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
        if (!dutyId) {
            alert("Error: Invalid duty ID.");
            return;
        }

        if (!confirm("Are you sure you want to request cancellation for this Khidmat?")) return;
        
        try {
            const res = await apiFetch(`/api/khidmat-requests/`, {
                method: "POST",
                requireAuth: false,
                body: JSON.stringify({
                    assignment_id: dutyId,
                    request_type: "cancel",
                    reason: "User requested cancellation"
                })
            });

            const data = await res.json();

            if (res.ok) {
                alert(data.message || "Cancellation request submitted successfully.");
                checkStatus(); // Refresh result
            } else {
                alert(data.error || data.message || "Unable to submit request.");
            }
        } catch (err) {
            console.error("Cancellation error:", err);
            alert("Server error: " + err.message);
        }
    }

    async function requestReallocation(dutyId) {
        if (!dutyId) {
            alert("Error: Invalid duty ID.");
            return;
        }

        if (!confirm("Are you sure you want to request reallocation for this Khidmat?")) return;

        try {
            const res = await apiFetch(`/api/khidmat-requests/`, {
                method: "POST",
                requireAuth: false,
                body: JSON.stringify({
                    assignment_id: dutyId,
                    request_type: "reallocate",
                    reason: "User requested reallocation"
                })
            });

            const data = await res.json();

            if (res.ok) {
                alert(data.message || "Reallocation request submitted successfully.");
                checkStatus(); // Refresh result
            } else {
                alert(data.error || data.message || "Unable to submit request.");
            }
        } catch (err) {
            console.error("Reallocation error:", err);
            alert("Server error: " + err.message);
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
                <div class="space-y-4 mt-6 border-t border-[#F9F7F7] pt-6">
                    <h4 class="text-xs font-bold text-[#6B7280] uppercase tracking-widest mb-4">Confirmed Assignments</h4>
                    ${data.duties.map(d => {
                        const isPending = d.request_status === 'pending';
                        const badgeLabel = d.request_type === 'cancel' ? 'Cancellation Requested' : 'Reallocation Requested';
                        
                        return `
                        <div class="p-4 border border-[#DBE2EF] rounded-2xl bg-[#F9FAFB] space-y-4">
                            <div class="flex items-center justify-between">
                                <div>
                                    <div class="text-[10px] text-[#6B7280] uppercase font-bold tracking-tighter">Date</div>
                                    <div class="text-[#112D4E] font-bold">${formatDateDMY(d.date)}</div>
                                </div>
                                <div class="text-right">
                                    <div class="text-[10px] text-[#6B7280] uppercase font-bold tracking-tighter">Duty</div>
                                    <div class="text-[#112D4E] font-bold text-sm leading-tight">${(d.namaaz || '') + (d.type ? ' ' + d.type : '')}</div>
                                    ${d.reporting_time ? `<div class="text-[11px] text-[#3F72AF] font-bold mt-1 bg-blue-50 px-2 py-0.5 rounded-md inline-block">Reporting: ${d.reporting_time}</div>` : ''}
                                </div>
                            </div>

                            ${isPending ? `
                                <div class="px-3 py-2 bg-amber-50 border border-amber-200 rounded-xl flex items-center gap-2">
                                    <div class="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse"></div>
                                    <span class="text-amber-800 text-[10px] font-bold uppercase tracking-wider">${badgeLabel}</span>
                                </div>
                            ` : `
                                <div class="flex gap-2">
                                    <button onclick="requestCancel(${d.id})"
                                        class="flex-1 px-3 py-2 bg-red-100 text-red-700 hover:bg-red-200 rounded-xl text-[11px] font-bold transition-colors">
                                        Cancel
                                    </button>
                                    <button onclick="requestReallocation(${d.id})"
                                        class="flex-1 px-3 py-2 bg-amber-100 text-amber-700 hover:bg-amber-200 rounded-xl text-[11px] font-bold transition-colors">
                                        Reallocate
                                    </button>
                                </div>
                            `}
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
