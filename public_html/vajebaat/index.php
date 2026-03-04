<?php include '../includes/header.php'; ?>

<style>
    /* Print-specific styles */
    @media print {
        header, nav, footer, .no-print, #app-root > nav, .bg-[#112D4E].py-8 {
            display: none !important;
        }
        body, #app-root, main {
            background-color: white !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        #takhmeen-form-print {
            display: block !important;
            width: 210mm; /* A4 width */
            padding: 20mm;
            margin: 0 auto;
            color: black !important;
            font-family: 'Inter', sans-serif, "Traditional Arabic", "Adobe Arabic";
        }
        .print-border {
            border: 1px solid black !important;
        }
    }

    #takhmeen-form-print {
        display: none;
    }

    .arabic-text {
        font-family: "Traditional Arabic", "Adobe Arabic", serif;
        font-size: 1.25rem;
        direction: rtl;
        text-align: right;
    }

    .takhmeen-table th, .takhmeen-table td {
        border: 1px solid #000;
        padding: 8px;
    }
</style>

<div class="min-h-screen bg-[#F9F7F7] no-print">

    <!-- Page Header -->
    <div class="bg-[#112D4E] py-8 px-4 sm:px-6 lg:px-8 text-center sm:text-left">
        <div class="max-w-2xl mx-auto">
            <h1 class="text-3xl text-white font-normal mb-1">Vajebaat</h1>
            <p class="text-[#DBE2EF] text-lg font-light">Takhmeen &amp; Appointments &bull; Saifee Masjid Chennai</p>
        </div>
    </div>

    <div class="py-8 px-4 sm:px-6 lg:px-8">
        <div class="max-w-2xl mx-auto space-y-6">

            <!-- Takhmeen Section -->
            <section class="bg-white rounded-lg shadow-sm border border-[#DBE2EF] overflow-hidden">
                <div class="h-2 bg-[#3F72AF] w-full"></div>
                <div class="p-6 space-y-4">
                    <div class="flex items-center gap-3 mb-1">
                        <div class="w-9 h-9 bg-[#DBE2EF] rounded-lg flex items-center justify-center shrink-0">
                            <svg class="w-5 h-5 text-[#3F72AF]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
                            </svg>
                        </div>
                        <div>
                            <h2 class="text-xl text-[#112D4E] font-semibold">Takhmeen</h2>
                            <p class="text-sm text-[#6B7280]">Generate your Vajebaat estimation form</p>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
                        <button
                            type="button"
                            onclick="printTakhmeen('blank')"
                            class="flex items-center justify-center gap-2 px-5 py-3.5 bg-[#112D4E] text-white rounded-lg hover:bg-[#1e3d6f] active:bg-[#0d2340] transition-all font-medium text-sm shadow-sm"
                        >
                            <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
                            </svg>
                            Generate Blank Form
                        </button>
                        <button
                            type="button"
                            onclick="printTakhmeen('prefilled')"
                            class="flex items-center justify-center gap-2 px-5 py-3.5 bg-white border border-[#DBE2EF] text-[#112D4E] rounded-lg hover:border-[#3F72AF] hover:bg-[#F0F4FA] active:bg-[#e8eef8] transition-all font-medium text-sm shadow-sm"
                        >
                            <svg class="w-4 h-4 text-[#3F72AF]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125" />
                            </svg>
                            Generate Pre-filled Form
                        </button>
                    </div>
                </div>
            </section>

            <!-- Appointment Section -->
            <section class="bg-white rounded-lg shadow-sm border border-[#DBE2EF] overflow-hidden">
                <div class="h-2 bg-[#3F72AF] w-full"></div>
                <div class="p-6 space-y-4">
                    <div class="flex items-center gap-3 mb-1">
                        <div class="w-9 h-9 bg-[#DBE2EF] rounded-lg flex items-center justify-center shrink-0">
                            <svg class="w-5 h-5 text-[#3F72AF]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5" />
                            </svg>
                        </div>
                        <div>
                            <h2 class="text-xl text-[#112D4E] font-semibold">Appointment</h2>
                            <p class="text-sm text-[#6B7280]">Book or check your Vajebaat appointment</p>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
                        <a
                            href="<?= BASE_URL ?>/vajebaat/appointment.php"
                            class="flex items-center justify-center gap-2 px-5 py-3.5 bg-[#112D4E] text-white rounded-lg hover:bg-[#1e3d6f] active:bg-[#0d2340] transition-all font-medium text-sm shadow-sm"
                        >
                            <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            Book Appointment
                        </a>
                        <a
                            href="<?= BASE_URL ?>/vajebaat/status.php"
                            class="flex items-center justify-center gap-2 px-5 py-3.5 bg-white border border-[#DBE2EF] text-[#112D4E] rounded-lg hover:border-[#3F72AF] hover:bg-[#F0F4FA] active:bg-[#e8eef8] transition-all font-medium text-sm shadow-sm"
                        >
                            <svg class="w-4 h-4 text-[#3F72AF]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 15.803a7.5 7.5 0 0010.607 10.607z" />
                            </svg>
                            Check Status
                        </a>
                    </div>
                </div>
            </section>

        </div>
    </div>
</div>

<!-- Takhmeen Print Styles -->
<style>
    /* ===== Takhmeen Form (Screen) ===== */
    #takhmeen-form-print {
        display: none; /* Hidden on screen by default; shown via JS before print */
    }

    /* ===== Print-Only Rules ===== */
    @media print {
        /* Hide everything except the Takhmeen form */
        body * {
            visibility: hidden !important;
        }
        #takhmeen-form-print,
        #takhmeen-form-print * {
            visibility: visible !important;
        }
        #takhmeen-form-print {
            display: block !important;
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
        }

        /* A4 page setup */
        @page {
            size: A4 portrait;
            margin: 15mm 18mm 15mm 18mm;
        }

        body {
            margin: 0;
            padding: 0;
            background: white !important;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }
    }

    /* ===== Takhmeen Form Styles ===== */
    #takhmeen-form-print {
        font-family: 'Times New Roman', 'Noto Naskh Arabic', 'Traditional Arabic', Times, serif;
        color: #000;
        font-size: 14px;
        line-height: 1.5;
        max-width: 700px;
        margin: 0 auto;
        padding: 20px 0;
    }

    /* Header block */
    .tkh-header {
        text-align: center;
        margin-bottom: 25px;
        border-bottom: 2px solid #000;
        padding-bottom: 12px;
    }
    .tkh-header h1 {
        font-size: 22px;
        font-weight: bold;
        margin: 0 0 2px 0;
        letter-spacing: 0.5px;
    }
    .tkh-header h2 {
        font-size: 16px;
        font-weight: normal;
        margin: 0;
    }
    .tkh-header .tkh-arabic-title {
        font-size: 26px;
        font-weight: bold;
        margin: 6px 0 4px 0;
        direction: rtl;
    }
    .tkh-header .tkh-year {
        font-size: 18px;
        font-weight: bold;
        margin: 4px 0 0 0;
    }

    /* Member info section */
    .tkh-info-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
        font-size: 14px;
    }
    .tkh-info-table td {
        padding: 5px 4px;
        vertical-align: bottom;
        border: none;
    }
    .tkh-info-table .tkh-label {
        font-weight: bold;
        white-space: nowrap;
        width: 1%;
        padding-right: 6px;
    }
    .tkh-info-table .tkh-value {
        border-bottom: 1px solid #000;
        min-width: 120px;
    }
    .tkh-info-table .tkh-value-wide {
        border-bottom: 1px solid #000;
    }

    /* Vajebaat table */
    .tkh-vajebaat-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 30px;
        font-size: 15px;
    }
    .tkh-vajebaat-table th,
    .tkh-vajebaat-table td {
        border: 1px solid #000;
        padding: 8px 12px;
    }
    .tkh-vajebaat-table thead th {
        background-color: #f5f5f5;
        font-weight: bold;
        text-align: center;
        font-size: 15px;
        padding: 10px 12px;
    }
    .tkh-vajebaat-table tbody td:first-child {
        text-align: right;
        direction: rtl;
        font-size: 18px;
        font-family: 'Noto Naskh Arabic', 'Traditional Arabic', 'Times New Roman', serif;
        padding: 10px 14px;
    }
    .tkh-vajebaat-table tbody td:last-child {
        text-align: center;
        min-height: 30px;
        font-size: 14px;
    }
    .tkh-vajebaat-table tbody tr:last-child {
        font-weight: bold;
        background-color: #fafafa;
    }
    .tkh-vajebaat-table tbody tr:last-child td:first-child {
        font-weight: bold;
    }

    /* Signature section */
    .tkh-signature-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 60px;
        font-size: 13px;
    }
    .tkh-signature-table td {
        text-align: center;
        padding: 0 30px;
        vertical-align: top;
    }
    .tkh-sig-line {
        border-top: 1px solid #000;
        padding-top: 6px;
        width: 160px;
        margin: 0 auto;
        font-weight: bold;
    }
</style>

<!-- Printable Takhmeen Form (hidden on screen, visible only during print) -->
<div id="takhmeen-form-print">

    <!-- ===== HEADER ===== -->
    <div class="tkh-header">
        <h2>Anjuman-e-Burhani, Chennai</h2>
        <div class="tkh-arabic-title">تخمين الواجبات</div>
        <h1>Takhmeen-ul-Vajebaat</h1>
        <div class="tkh-year">Sanah 1447H — Sherullah Moazzam</div>
    </div>

    <!-- ===== MEMBER INFORMATION ===== -->
    <table class="tkh-info-table">
        <tr>
            <td class="tkh-label">S.No:</td>
            <td class="tkh-value"><span id="print-sno">&nbsp;</span></td>
            <td class="tkh-label" style="padding-left: 24px;">Mohalla:</td>
            <td class="tkh-value"><span id="print-mohalla">&nbsp;</span></td>
        </tr>
        <tr>
            <td class="tkh-label">Name:</td>
            <td class="tkh-value-wide" colspan="3"><span id="print-name">&nbsp;</span></td>
        </tr>
        <tr>
            <td class="tkh-label">ITS:</td>
            <td class="tkh-value"><span id="print-its">&nbsp;</span></td>
            <td class="tkh-label" style="padding-left: 24px;">File No:</td>
            <td class="tkh-value"><span id="print-fileno">&nbsp;</span></td>
        </tr>
        <tr>
            <td class="tkh-label">Sector Incharge:</td>
            <td class="tkh-value"><span id="print-sector">&nbsp;</span></td>
            <td class="tkh-label" style="padding-left: 24px;">Sub Sector Incharge:</td>
            <td class="tkh-value"><span id="print-subsector">&nbsp;</span></td>
        </tr>
    </table>

    <!-- ===== VAJEBAAT TABLE ===== -->
    <table class="tkh-vajebaat-table">
        <thead>
            <tr>
                <th style="width: 60%;">Vajebaat</th>
                <th style="width: 40%;">1447</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>زكوة المال</td>
                <td><span class="print-amount" data-key="zakaat"></span></td>
            </tr>
            <tr>
                <td>الخمس</td>
                <td><span class="print-amount" data-key="khums"></span></td>
            </tr>
            <tr>
                <td>فطرة الصيام</td>
                <td><span class="print-amount" data-key="fitrat"></span></td>
            </tr>
            <tr>
                <td>الكفارة</td>
                <td><span class="print-amount" data-key="kaffara"></span></td>
            </tr>
            <tr>
                <td>منة بنيان</td>
                <td><span class="print-amount" data-key="bunyan"></span></td>
            </tr>
            <tr>
                <td>النجوى</td>
                <td><span class="print-amount" data-key="najwa"></span></td>
            </tr>
            <tr>
                <td>جملة عربية</td>
                <td><span class="print-amount" data-key="total"></span></td>
            </tr>
        </tbody>
    </table>

    <!-- ===== SIGNATURE SECTION ===== -->
    <table class="tkh-signature-table">
        <tr>
            <td>
                <div class="tkh-sig-line">Member Signature</div>
            </td>
            <td>
                <div class="tkh-sig-line">Jamaat Seal</div>
            </td>
        </tr>
    </table>

</div>

<script>
    /**
     * printTakhmeen — opens the browser print dialog with the Takhmeen form.
     * @param {'blank'|'prefilled'} mode
     */
    function printTakhmeen(mode) {
        const form = document.getElementById('takhmeen-form-print');

        // Clear all fields first
        resetTakhmeenForm();

        if (mode === 'prefilled') {
            const its = prompt("Enter your 8-digit ITS Number:");
            if (!its || !/^\d{8}$/.test(its)) {
                alert("Please enter a valid 8-digit ITS number.");
                return;
            }

            // Try fetching member data from the backend
            fetchMemberData(its).then(data => {
                if (data) {
                    fillTakhmeenForm(data);
                }
                // Show and print
                form.style.display = 'block';
                window.print();
                form.style.display = 'none';
            }).catch(() => {
                // If fetch fails, just fill ITS and print
                document.getElementById('print-its').textContent = its;
                form.style.display = 'block';
                window.print();
                form.style.display = 'none';
            });
        } else {
            // Blank mode — print immediately
            form.style.display = 'block';
            window.print();
            form.style.display = 'none';
        }
    }

    /**
     * Reset all fields to blank (non-breaking spaces for underline visibility).
     */
    function resetTakhmeenForm() {
        document.getElementById('print-sno').innerHTML = '&nbsp;';
        document.getElementById('print-mohalla').innerHTML = '&nbsp;';
        document.getElementById('print-name').innerHTML = '&nbsp;';
        document.getElementById('print-its').innerHTML = '&nbsp;';
        document.getElementById('print-fileno').innerHTML = '&nbsp;';
        document.getElementById('print-sector').innerHTML = '&nbsp;';
        document.getElementById('print-subsector').innerHTML = '&nbsp;';

        document.querySelectorAll('.print-amount').forEach(el => {
            el.innerHTML = '&nbsp;';
        });
    }

    /**
     * Fill form fields from a data object.
     * @param {Object} data — Expected keys: sno, mohalla, name, its, file_no, sector, sub_sector, amounts
     */
    function fillTakhmeenForm(data) {
        if (data.sno) document.getElementById('print-sno').textContent = data.sno;
        if (data.mohalla) document.getElementById('print-mohalla').textContent = data.mohalla;
        if (data.name) document.getElementById('print-name').textContent = data.name;
        if (data.its) document.getElementById('print-its').textContent = data.its;
        if (data.file_no) document.getElementById('print-fileno').textContent = data.file_no;
        if (data.sector) document.getElementById('print-sector').textContent = data.sector;
        if (data.sub_sector) document.getElementById('print-subsector').textContent = data.sub_sector;

        if (data.amounts && typeof data.amounts === 'object') {
            Object.keys(data.amounts).forEach(key => {
                const el = document.querySelector(`.print-amount[data-key="${key}"]`);
                if (el) el.textContent = data.amounts[key];
            });
        }
    }

    /**
     * Fetch member Takhmeen data from the backend.
     * @param {string} its — 8-digit ITS number
     * @returns {Promise<Object|null>}
     */
    async function fetchMemberData(its) {
        try {
            const url = window.API_BASE + '/api/vajebaat/members/by_its/?its=' + encodeURIComponent(its);
            const response = await fetch(url);
            if (response.ok) {
                const d = await response.json();
                // Map API field names → fillTakhmeenForm keys
                return {
                    its:        d.its_number,
                    name:       d.name,
                    mohalla:    d.mohalla,
                    file_no:    d.file_no,
                    sector:     d.sector_incharge,
                    sub_sector: d.subsector_incharge,
                    amounts:    d.amounts || {}
                };
            }
            // Member not found — just fill ITS
            return { its: its };
        } catch (e) {
            console.warn('Takhmeen API not available, printing with ITS only.');
            return { its: its };
        }
    }
</script>

<?php include '../includes/footer.php'; ?>