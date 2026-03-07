<?php include '../includes/admin-header.php'; ?>

<!-- Content Wrapper -->
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri&display=swap');
.font-arabic { font-family: 'Amiri', serif; }
</style>
<div class="min-h-screen bg-[#F9F7F7]">
    
    <!-- Header -->
    <div class="bg-[#112D4E] py-5 px-6 shadow-md print:hidden">
        <div class="flex items-center justify-between">
            <div class="flex items-center gap-4">
                <a href="<?= BASE_URL ?>/admin/vajebaat-appointments.php" class="p-2 rounded-lg bg-white/10 text-white/70 hover:text-white hover:bg-white/20 transition-all">
                    <svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                    </svg>
                </a>
                <div>
                   <h1 class="text-xl md:text-2xl text-white font-normal">
                        Vajebaat Form 1447H
                    </h1>
                    <p id="header-appointment-id" class="text-[#DBE2EF] text-xs font-mono">Loading ID...</p>
                </div>
            </div>
             <div class="flex items-center gap-3 text-[#DBE2EF] text-sm">
                <button onclick="downloadPDF()" class="px-3 py-1.5 rounded-md bg-white/10 hover:bg-white/20 text-white text-xs font-bold transition-all flex items-center gap-2">
                    <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M7.5 12l4.5 4.5m0 0l4.5-4.5M12 3v13.5" />
                    </svg>
                    Download PDF
                </button>
                <button onclick="window.print()" class="px-3 py-1.5 rounded-md bg-white/10 hover:bg-white/20 text-white text-xs font-bold transition-all flex items-center gap-2">
                    Print Form
                </button>
                <button onclick="logout()" class="ml-4 px-3 py-1.5 rounded-md bg-red-500/10 hover:bg-red-500/20 text-red-100 text-sm font-medium transition-all">Logout</button>
            </div>
        </div>
    </div>

    <!-- Layout Grid -->
    <div class="p-6 max-w-[1400px] mx-auto">
        <div id="loading-skeleton" class="animate-pulse space-y-6">
            <div class="h-[200px] bg-white rounded-2xl border border-[#DBE2EF]"></div>
            <div class="h-[400px] bg-white rounded-2xl border border-[#DBE2EF]"></div>
        </div>

        <div id="form-container" class="grid grid-cols-1 lg:grid-cols-12 gap-8 hidden print:block">
            
            <!-- LEFT PANE: Data Entry (40%) -->
            <div class="lg:col-span-5 space-y-6 print:hidden">
                
                <!-- Top Section: Member Details -->
                <div class="bg-white rounded-2xl shadow-sm border border-[#DBE2EF] overflow-hidden">
                    <div class="bg-[#F9FAFB] px-6 py-4 border-b border-[#DBE2EF]">
                        <h3 class="text-xs font-bold text-[#6B7280] uppercase tracking-wider">Demographic Details</h3>
                    </div>
                    <div class="p-6">
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-[10px] font-bold text-[#6B7280] uppercase mb-1">ITS Number</label>
                                <p id="member-its" class="text-sm font-mono text-[#112D4E] font-medium">-</p>
                            </div>
                            <div>
                                <label class="block text-[10px] font-bold text-[#6B7280] uppercase mb-1">Full Name</label>
                                <p id="member-name" class="text-sm text-[#112D4E] font-medium">-</p>
                            </div>
                            <div>
                                <label class="block text-[10px] font-bold text-[#6B7280] uppercase mb-1">File No</label>
                                <p id="member-file" class="text-sm text-[#112D4E] font-medium">-</p>
                            </div>
                            <div>
                                <label class="block text-[10px] font-bold text-[#6B7280] uppercase mb-1">Mobile Number</label>
                                <p id="member-mobile" class="text-sm text-[#112D4E] font-medium">-</p>
                            </div>
                            <div>
                                <label class="block text-[10px] font-bold text-[#6B7280] uppercase mb-1">Sector</label>
                                <p id="member-sector" class="text-xs text-[#112D4E] font-medium">-</p>
                            </div>
                            <div>
                                <label class="block text-[10px] font-bold text-[#6B7280] uppercase mb-1">Sub Sector</label>
                                <p id="member-subsector" class="text-xs text-[#112D4E] font-medium">-</p>
                            </div>
                            <div class="col-span-2">
                                <label class="block text-[10px] font-bold text-[#6B7280] uppercase mb-1">Appointment Slot</label>
                                <p id="member-slot" class="text-sm text-[#3F72AF] font-bold">-</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Bottom Section: Vajebaat Amounts Grid -->
                <div class="bg-white rounded-2xl shadow-sm border border-[#DBE2EF] overflow-hidden">
                    <div class="bg-[#112D4E] px-6 py-4">
                        <h3 class="text-sm font-bold text-white tracking-wider">Data Input</h3>
                    </div>
                    
                    <div class="p-6">
                        <table class="w-full text-left border-collapse">
                            <thead>
                                <tr class="border-b border-[#DBE2EF]">
                                    <th class="py-3 text-xs font-bold text-[#6B7280] uppercase w-7/12">Category</th>
                                    <th class="py-3 text-xs font-bold text-[#6B7280] uppercase w-5/12 text-right pr-2">Amount (₹)</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-[#F3F4F6]">
                                <tr>
                                    <td class="py-3 text-sm font-bold text-[#112D4E]">Zakat al-Mal</td>
                                    <td class="py-2"><input type="number" step="0.01" min="0" id="input-zakat_mal" class="vajebaat-input w-full px-3 py-2 border border-[#DBE2EF] rounded-lg text-sm text-right outline-none focus:ring-2 focus:ring-[#3F72AF]" placeholder="0.00"></td>
                                </tr>
                                <tr>
                                    <td class="py-3 text-sm font-bold text-[#112D4E]">Khums</td>
                                    <td class="py-2"><input type="number" step="0.01" min="0" id="input-khums" class="vajebaat-input w-full px-3 py-2 border border-[#DBE2EF] rounded-lg text-sm text-right outline-none focus:ring-2 focus:ring-[#3F72AF]" placeholder="0.00"></td>
                                </tr>
                                <tr>
                                    <td class="py-3 text-sm font-bold text-[#112D4E]">Nazr Muqam</td>
                                    <td class="py-2"><input type="number" step="0.01" min="0" id="input-nazr_muqam" class="vajebaat-input w-full px-3 py-2 border border-[#DBE2EF] rounded-lg text-sm text-right outline-none focus:ring-2 focus:ring-[#3F72AF]" placeholder="0.00"></td>
                                </tr>
                                <tr>
                                    <td class="py-3 text-sm font-bold text-[#112D4E]">Kaffara</td>
                                    <td class="py-2"><input type="number" step="0.01" min="0" id="input-kaffara" class="vajebaat-input w-full px-3 py-2 border border-[#DBE2EF] rounded-lg text-sm text-right outline-none focus:ring-2 focus:ring-[#3F72AF]" placeholder="0.00"></td>
                                </tr>
                                <tr>
                                    <td class="py-3 text-sm font-bold text-[#112D4E]">Minnat Niyaz</td>
                                    <td class="py-2"><input type="number" step="0.01" min="0" id="input-minnat_niyaz" class="vajebaat-input w-full px-3 py-2 border border-[#DBE2EF] rounded-lg text-sm text-right outline-none focus:ring-2 focus:ring-[#3F72AF]" placeholder="0.00"></td>
                                </tr>
                                <tr>
                                    <td class="py-3 text-sm font-bold text-[#112D4E]">Najwa</td>
                                    <td class="py-2"><input type="number" step="0.01" min="0" id="input-najwa" class="vajebaat-input w-full px-3 py-2 border border-[#DBE2EF] rounded-lg text-sm text-right outline-none focus:ring-2 focus:ring-[#3F72AF]" placeholder="0.00"></td>
                                </tr>
                                <tr>
                                    <td class="py-3 text-sm font-bold text-[#112D4E]">Jamiya</td>
                                    <td class="py-2"><input type="number" step="0.01" min="0" id="input-jamiya" class="vajebaat-input w-full px-3 py-2 border border-[#DBE2EF] rounded-lg text-sm text-right outline-none focus:ring-2 focus:ring-[#3F72AF]" placeholder="0.00"></td>
                                </tr>
                                <!-- Grand Total Row -->
                                <tr class="bg-[#F9FAFB]">
                                    <td class="py-4 text-sm font-bold text-[#112D4E] uppercase">Grand Total</td>
                                    <td class="py-4 text-right pr-4">
                                        <span class="text-xl font-bold text-[#3F72AF]" id="grand-total">₹ 0.00</span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Action Buttons Segment -->
                <div class="flex flex-col gap-3">
                    <button onclick="saveVajebaat()" id="btn-save" class="w-full py-3.5 bg-[#3F72AF] text-white rounded-xl font-bold shadow hover:bg-[#112D4E] transition-all flex justify-center items-center gap-2">
                        <span id="save-text">Save Vajebaat Form</span>
                    </button>
                    <div class="grid grid-cols-2 gap-3">
                        <button onclick="window.print()" class="w-full py-3 rounded-xl border border-gray-300 bg-white text-gray-700 font-bold shadow-sm hover:bg-gray-50 transition-all">Print Selected Preview</button>
                        <button onclick="window.history.back()" class="w-full py-3 rounded-xl border border-gray-300 bg-white text-gray-700 font-bold shadow-sm hover:bg-gray-50 transition-all">Cancel</button>
                    </div>
                </div>

            </div>

            <!-- RIGHT PANE: Live PDF Preview (60%) -->
            <div class="lg:col-span-7 bg-[#E5E7EB] lg:rounded-2xl border border-dashed border-gray-300 flex justify-center items-start lg:p-6 print:col-span-12 print:border-none print:p-0 print:bg-white overflow-x-auto min-h-screen lg:min-h-0">
                
                <!-- A4 Paper Simulator Wrapper -->
                <div class="bg-white shadow-2xl w-[210mm] max-w-full lg:max-w-[700px] aspect-[1/1.414] p-[10mm] md:p-[15mm] text-black print:shadow-none print:scale-100 print:w-full box-border transform origin-top mx-auto">
                    
                    <!-- Title -->
                    <div class="text-center border-b-2 border-black pb-3 mb-6 relative">
                        <h1 class="text-2xl font-bold font-sans">Al Vajebaat 1447</h1>
                    </div>

                    <!-- Member details Header -->
                    <div class="mb-3 font-bold text-sm">Member details:</div>
                    
                    <!-- 2-Column Detail Grid -->
                    <div class="grid grid-cols-2 gap-x-6 gap-y-2 text-[12px] mb-8">
                        <!-- Col 1 -->
                        <div>
                            <div class="flex"><span class="font-bold w-[70px]">Mohalla:</span> <span id="preview-mohalla" class="flex-1 border-b border-dotted border-gray-400"></span></div>
                            <div class="flex mt-3"><span class="font-bold w-[70px]">Name:</span> <span id="preview-name" class="flex-1 border-b border-dotted border-gray-400"></span></div>
                            <div class="flex mt-3"><span class="font-bold w-[70px]">ITS:</span> <span id="preview-its" class="flex-1 border-b border-dotted border-gray-400"></span></div>
                        </div>
                        <!-- Col 2 -->
                        <div>
                            <div class="flex"><span class="font-bold w-[120px]">File No:</span> <span id="preview-file" class="flex-1 border-b border-dotted border-gray-400"></span></div>
                            <div class="flex mt-3"><span class="font-bold w-[120px]">Sector Incharge:</span> <span id="preview-sector" class="flex-1 border-b border-dotted border-gray-400 whitespace-nowrap overflow-hidden text-ellipsis"></span></div>
                            <div class="flex mt-3"><span class="font-bold w-[120px]">Sub Sector Incharge:</span> <span id="preview-subsector" class="flex-1 border-b border-dotted border-gray-400 whitespace-nowrap overflow-hidden text-ellipsis"></span></div>
                        </div>
                    </div>

                    <!-- Separator -->
                    <hr class="border-black mb-6">

                    <!-- Vajebaat Form Structural Table -->
                    <table class="w-full border-collapse border border-black mb-8 text-[14px]">
                        <thead>
                            <tr class="bg-[#112D4E] text-white">
                                <th class="border border-black py-2 px-4 text-left font-bold" style="width: 50%;">Vajebaat</th>
                                <th class="border border-black py-2 px-4 text-center font-bold" style="width: 25%;">1446</th>
                                <th class="border border-black py-2 px-4 text-right font-bold" style="width: 25%;">1447</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td class="border border-black py-2 px-4 font-bold flex items-center justify-between"><div class="font-arabic text-xl mr-2">زكوة المال</div> <div>Zakat al-Mal</div></td>
                                <td class="border border-black py-2 px-4 text-center text-gray-400"></td>
                                <td class="border border-black py-2 px-4 text-right font-mono" id="preview-val-zakat_mal">0.00</td>
                            </tr>
                            <tr>
                                <td class="border border-black py-2 px-4 font-bold flex items-center justify-between"><div class="font-arabic text-xl mr-2">الخمس</div> <div>Khums</div></td>
                                <td class="border border-black py-2 px-4 text-center text-gray-400"></td>
                                <td class="border border-black py-2 px-4 text-right font-mono" id="preview-val-khums">0.00</td>
                            </tr>
                            <tr>
                                <td class="border border-black py-2 px-4 font-bold flex items-center justify-between"><div class="font-arabic text-xl mr-2">نذر المقام</div> <div>Nazr Muqam</div></td>
                                <td class="border border-black py-2 px-4 text-center text-gray-400"></td>
                                <td class="border border-black py-2 px-4 text-right font-mono" id="preview-val-nazr_muqam">0.00</td>
                            </tr>
                            <tr>
                                <td class="border border-black py-2 px-4 font-bold flex items-center justify-between"><div class="font-arabic text-xl mr-2">الكفارة</div> <div>Kaffara</div></td>
                                <td class="border border-black py-2 px-4 text-center text-gray-400"></td>
                                <td class="border border-black py-2 px-4 text-right font-mono" id="preview-val-kaffara">0.00</td>
                            </tr>
                            <tr>
                                <td class="border border-black py-2 px-4 font-bold flex items-center justify-between"><div class="font-arabic text-xl mr-2">منة نياز</div> <div>Minnat Niyaz</div></td>
                                <td class="border border-black py-2 px-4 text-center text-gray-400"></td>
                                <td class="border border-black py-2 px-4 text-right font-mono" id="preview-val-minnat_niyaz">0.00</td>
                            </tr>
                            <tr>
                                <td class="border border-black py-2 px-4 font-bold flex items-center justify-between"><div class="font-arabic text-xl mr-2">النجوى</div> <div>Najwa</div></td>
                                <td class="border border-black py-2 px-4 text-center text-gray-400"></td>
                                <td class="border border-black py-2 px-4 text-right font-mono" id="preview-val-najwa">0.00</td>
                            </tr>
                            <tr>
                                <td class="border border-black py-2 px-4 font-bold flex items-center justify-between"><div class="font-arabic text-xl mr-2">الجامعة</div> <div>Jamiya</div></td>
                                <td class="border border-black py-2 px-4 text-center text-gray-400"></td>
                                <td class="border border-black py-2 px-4 text-right font-mono" id="preview-val-jamiya">0.00</td>
                            </tr>
                            <tr class="bg-gray-100">
                                <td class="border border-black py-3 px-4 font-bold flex items-center justify-between"><div class="font-arabic text-xl mr-2 text-[#112D4E]">جملة روثثيه</div> <div class="uppercase">Grand Total</div></td>
                                <td class="border border-black py-3 px-4 text-center text-gray-400"></td>
                                <td class="border border-black py-3 px-4 text-right font-bold font-mono text-lg" id="preview-val-total">0.00</td>
                            </tr>
                        </tbody>
                    </table>
                    
                    <div class="text-center text-[10px] text-gray-500 italic mt-12">
                        Generated electronically by Sherullah Vajebaat Appointment System
                    </div>
                    
                </div>
            </div>

        </div>
    </div>
</div>

<script src="<?= BASE_URL ?>/assets/js/main.js"></script>
<?php include '../includes/footer.php'; ?>

<script>
    const urlParams = new URLSearchParams(window.location.search);
    const appointmentId = urlParams.get('id');
    let loadedItsId = null;

    document.addEventListener('DOMContentLoaded', () => {
        if (!appointmentId) {
            alert('No appointment ID provided');
            window.location.href = 'vajebaat-appointments.php';
            return;
        }

        document.getElementById('header-appointment-id').textContent = `Appointment #${appointmentId}`;
        
        // Attach event listeners for Live Syncing & Totals Calculation
        document.querySelectorAll('.vajebaat-input').forEach(input => {
            input.addEventListener('input', calculateTotal);
        });

        loadData();
    });

    async function loadData() {
        try {
            const res = await apiFetch(`/api/vajebaat/admin/vajebaat/appointment/${appointmentId}`, { requireAuth: true });
            if (!res.ok) throw new Error('Failed to load data');
            const data = await res.json();
            
            // Map Member Details
            const apt = data.appointment;
            const mem = data.member;
            const vaj = data.vajebaat;
            
            loadedItsId = apt.its;
            
            // 1. Populate Left Pane Header
            document.getElementById('member-its').textContent = apt.its || '-';
            document.getElementById('member-name').textContent = mem.name || '-';
            document.getElementById('member-mobile').textContent = mem.mobile || '-';
            document.getElementById('member-file').textContent = mem.file_no || '-';
            document.getElementById('member-sector').textContent = mem.sector || '-';
            document.getElementById('member-subsector').textContent = mem.sub_sector || '-';
            
            const slotText = apt.date ? `${apt.date} | ${apt.slot || 'No time assigned'}` : 'Pending Assignment';
            document.getElementById('member-slot').textContent = slotText;

            // 2. Populate Right Pane Live Preview Demographics
            document.getElementById('preview-mohalla').textContent = mem.mohalla || mem.sector || 'Mufaddal';
            document.getElementById('preview-name').textContent = mem.name || apt.name || '-';
            document.getElementById('preview-its').textContent = apt.its || '-';
            document.getElementById('preview-file').textContent = mem.file_no || '-';
            document.getElementById('preview-sector').textContent = mem.sector || '-';
            document.getElementById('preview-subsector').textContent = mem.sub_sector || '-';
            
            // 3. Map Vajebaat Data into Inputs
            if (vaj) {
                document.getElementById('input-zakat_mal').value = vaj.zakat_mal || '';
                document.getElementById('input-khums').value = vaj.khums || '';
                document.getElementById('input-nazr_muqam').value = vaj.nazr_muqam || '';
                document.getElementById('input-kaffara').value = vaj.kaffara || '';
                document.getElementById('input-minnat_niyaz').value = vaj.minnat_niyaz || '';
                document.getElementById('input-najwa').value = vaj.najwa || '';
                document.getElementById('input-jamiya').value = vaj.jamiya || '';
            }

            // Sync Preview immediately to reflect populated data
            calculateTotal();

            document.getElementById('loading-skeleton').classList.add('hidden');
            document.getElementById('form-container').classList.remove('hidden');
        } catch (e) {
            alert(e.message);
            console.error(e);
        }
    }

    function calculateTotal() {
        let total = 0;
        const fields = ['zakat_mal', 'khums', 'nazr_muqam', 'kaffara', 'minnat_niyaz', 'najwa', 'jamiya'];
        
        fields.forEach(field => {
            const inputEl = document.getElementById(`input-${field}`);
            if (inputEl) {
                const val = parseFloat(inputEl.value);
                // Accumulate valid numbers into grand total
                if (!isNaN(val)) total += val;
                
                // Live PDF Preview Update logic per cell
                const previewEl = document.getElementById(`preview-val-${field}`);
                if (previewEl) {
                    previewEl.textContent = (!isNaN(val) && val > 0) ? val.toFixed(2) : '0.00';
                }
            }
        });
        
        // Update both the left pane display and the right pane preview display
        document.getElementById('grand-total').textContent = `₹ ${total.toFixed(2)}`;
        
        const previewTotalEl = document.getElementById('preview-val-total');
        if (previewTotalEl) {
            previewTotalEl.textContent = total.toFixed(2);
        }
    }

    async function saveVajebaat() {
        const btn = document.getElementById('btn-save');
        btn.disabled = true;
        const originalText = btn.innerHTML;
        btn.innerHTML = 'Saving...';

        const payload = {
            appointment_id: appointmentId,
            its_id: loadedItsId,
            year: 1447,
            zakat_mal: document.getElementById('input-zakat_mal').value || 0,
            khums: document.getElementById('input-khums').value || 0,
            nazr_muqam: document.getElementById('input-nazr_muqam').value || 0,
            kaffara: document.getElementById('input-kaffara').value || 0,
            minnat_niyaz: document.getElementById('input-minnat_niyaz').value || 0,
            najwa: document.getElementById('input-najwa').value || 0,
            jamiya: document.getElementById('input-jamiya').value || 0,
        };

        try {
            const res = await apiFetch('/api/vajebaat/admin/vajebaat/save', {
                method: 'POST',
                requireAuth: true,
                body: JSON.stringify(payload)
            });

            if (res.ok) {
                showToast('Vajebaat Form successfully saved & securely backed up.', 'success');
            } else {
                const err = await res.json();
                showToast(err.detail || 'Failed to save Vajebaat', 'error');
            }
        } catch (e) {
            showToast('Network error during save', 'error');
        } finally {
            btn.disabled = false;
            btn.innerHTML = originalText;
        }
    }

    function downloadPDF() {
        if (!appointmentId) return;
        const token = localStorage.getItem('access_token');
        if (!token) return;
        
        showToast('Generating PDF receipt...', 'info');
        
        fetch(`${window.BASE_URL}/api/vajebaat/admin/vajebaat/pdf/${appointmentId}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => {
            if(!response.ok) throw new Error('Generation failed');
            return response.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `vajebaat_${loadedItsId}_1447.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        })
        .catch(err => {
            console.error('PDF error', err);
            showToast('Failed to generate secure PDF', 'error');
        });
    }
</script>
