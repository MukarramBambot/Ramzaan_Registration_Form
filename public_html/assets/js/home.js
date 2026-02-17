/**
 * Home JS - Registration Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('registration-form');
    const fileInput = document.getElementById('fileInput');
    const fileListCtx = document.getElementById('file-list');
    const submitBtn = document.getElementById('submit-btn');
    const successView = document.getElementById('success-view');
    const resetBtn = document.getElementById('reset-form-btn');

    let selectedFiles = [];

    // --- File Handling ---
    fileInput.addEventListener('change', (e) => {
        if (e.target.files) {
            const newFiles = Array.from(e.target.files);
            
            // Validation: Max 6 files
            if (newFiles.length > 6) {
                showDialog({ 
                    variant: 'danger', 
                    title: 'Too Many Files', 
                    message: 'You can only upload a maximum of 6 audition files.', 
                    confirmLabel: 'OK' 
                });
                fileInput.value = ''; // Clear input
                selectedFiles = [];
                renderFiles();
                return;
            }

            // Validation: Max 15MB per file
            const oversizedFiles = newFiles.filter(f => f.size > 15 * 1024 * 1024);
            if (oversizedFiles.length > 0) {
                 const names = oversizedFiles.map(f => f.name).join(', ');
                 showDialog({ 
                    variant: 'danger', 
                    title: 'File Too Large', 
                    message: `The following files exceed the 15MB limit:\n\n${names}`, 
                    confirmLabel: 'OK' 
                });
                fileInput.value = ''; // Clear input
                selectedFiles = [];
                renderFiles();
                return;
            }

            // Append new files (Logic from React was simple setFiles, here we can append or replace)
            // React logic: setFiles(Array.from(e.target.files)) which replaces.
            // Let's implement replacement to match exact React behavior:
            selectedFiles = newFiles;

            renderFiles();
        }
    });

    function renderFiles() {
        fileListCtx.innerHTML = '';
        selectedFiles.forEach(file => {
            const div = document.createElement('div');
            div.className = 'flex items-center text-sm text-[#112D4E] bg-[#F9FAFB] p-2 rounded border border-[#DBE2EF]';
            div.innerHTML = `
                <span class="w-2 h-2 bg-[#3F72AF] rounded-full mr-2"></span>
                ${file.name}
            `;
            fileListCtx.appendChild(div);
        });
    }

    // --- Submit Logic ---
    let isSubmitting = false;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (isSubmitting) return;
        isSubmitting = true;

        const formData = new FormData(form);
        const xhr = new XMLHttpRequest();

        const progressContainer = document.getElementById("uploadProgressContainer");
        const progressBar = document.getElementById("progressBar");
        const percentText = document.getElementById("progressPercent");
        const speedText = document.getElementById("uploadSpeed");
        const timeText = document.getElementById("timeRemaining");
        const submitBtn = document.getElementById("submit-btn");

        // Preference logic
        const prefElems = Array.from(document.querySelectorAll('input[name="preference"]:checked'));
        if (prefElems.length === 0) {
            showDialog({ variant: 'danger', title: 'Validation Error', message: 'Please select at least one option for "Register For".', confirmLabel: 'OK' });
            isSubmitting = false;
            return;
        }
        formData.delete('preference');
        prefElems.forEach(elem => formData.append('preference', elem.value));
        
        // Files logic
        formData.delete('media_files');
        selectedFiles.forEach(file => formData.append('media_files', file));

        progressContainer.style.display = "block";
        submitBtn.disabled = true;
        
        const startTime = Date.now();
        const apiBase = 'https://api.madrasjamaatportal.org';
        xhr.open("POST", `${apiBase}/api/registrations/`, true);

        xhr.upload.onprogress = function(event) {
            if (event.lengthComputable) {
                const percent = Math.round((event.loaded / event.total) * 100);
                progressBar.style.width = percent + "%";
                percentText.innerText = percent + "%";
                const elapsedSeconds = (Date.now() - startTime) / 1000;
                const speed = event.loaded / elapsedSeconds;
                const speedKB = (speed / 1024).toFixed(2);
                speedText.innerText = speedKB + " KB/s";
                const remainingBytes = event.total - event.loaded;
                const remainingSeconds = remainingBytes / speed;
                if (remainingSeconds > 0 && isFinite(remainingSeconds)) {
                    timeText.innerText = Math.ceil(remainingSeconds) + "s remaining";
                }
            }
        };

        xhr.onload = async function() {
            if (xhr.status === 201 || xhr.status === 200) {
                progressBar.style.width = "100%";
                percentText.innerText = "100%";
                timeText.innerText = "Completed";
                submitBtn.innerText = "Submitted";
                window.location.href = '/success.php';
            } else {
                let errorData = {};
                try { errorData = JSON.parse(xhr.responseText); } catch(e) {}
                
                // Handle Duplicate ITS specifically if returned as 400
                if (xhr.status === 400 && errorData.its_number) {
                    const itsMsg = Array.isArray(errorData.its_number) ? errorData.its_number[0] : errorData.its_number;
                    if (itsMsg.toLowerCase().includes('already registered')) {
                         showDialog({ variant: 'info', title: 'Already Registered', message: "You have already registered with this ITS number.", confirmLabel: 'OK' });
                         handleFailureReset();
                         return;
                    }
                }
                
                handleFailureReset(`Submission failed (Error ${xhr.status}).`);
            }
        };

        xhr.onerror = async function() {
            // Recovery polling if connection fails during upload
            const itsNumber = formData.get('its_number');
            const found = await pollRegistrationExists(itsNumber, { attempts: 6, interval: 3000 });
            if (found) {
                window.location.href = '/success.php';
                return;
            }
            handleFailureReset('Network error. Please check your connection.');
        };

        function handleFailureReset(msg) {
            if (msg) showDialog({ variant: 'danger', title: 'Upload Failed', message: msg, confirmLabel: 'OK' });
            progressContainer.style.display = "none";
            progressBar.style.width = "0%";
            submitBtn.disabled = false;
            submitBtn.innerText = "Submit";
            isSubmitting = false;
        }

        xhr.send(formData);
    });

    function setSubmitting(isSubmitting) {
        submitBtn.disabled = isSubmitting;
        if (isSubmitting) {
            submitBtn.innerHTML = `
                ${ICONS.loader2}
                <span class="ml-2">Submitting...</span>
            `;
        } else {
            submitBtn.innerHTML = `Submit`;
        }
    }

    /**
     * Poll the search endpoint to determine whether a registration exists.
     * Returns true as soon as a 200 is returned, false if not found after attempts.
     */
    async function pollRegistrationExists(itsNumber, opts = {}) {
        const attempts = opts.attempts || 10;
        const interval = opts.interval || 2000;

        if (!itsNumber) return false;

        for (let i = 0; i < attempts; i++) {
            try {
                const res = await apiFetch(`/api/registrations/search/?its=${encodeURIComponent(itsNumber)}`, {
                    method: 'GET',
                    requireAuth: false,
                    timeout: 5000
                });

                if (res.status === 200) return true;
                if (res.status === 404) {
                    // Not found yet - wait and retry
                } else {
                    // For other statuses, don't fail immediately; keep polling briefly
                    console.warn('Unexpected status during verification poll:', res.status);
                }
            } catch (e) {
                // Network error for the poll attempt - just log and retry
                console.warn('Verification poll attempt failed:', e);
            }

            // Wait before next attempt
            await new Promise(r => setTimeout(r, interval));
        }

        return false;
    }

    function setSubmitted(success) {
        if (success) {
            form.classList.add('hidden');
            successView.classList.remove('hidden');
        } else {
            form.classList.remove('hidden');
            successView.classList.add('hidden');

            // Reset Form
            form.reset();
            selectedFiles = [];
            renderFiles();
            setSubmitting(false);
        }
    }

    // Reset Handler
    resetBtn.addEventListener('click', () => {
        setSubmitted(false);
    });

});
