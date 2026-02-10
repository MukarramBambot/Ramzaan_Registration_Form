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
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (submitBtn.disabled) return;

        // Set Loading State
        setSubmitting(true);

        const formData = new FormData(form);

        // Append files
        selectedFiles.forEach(file => {
            formData.append('audition_files', file);
        });

        // Preference is radio, auto handled by FormData

        let isRedirecting = false;

        try {
            // Use a sensible client timeout for uploads; if the connection is interrupted
            // we'll fall back to a verification poll so users are not left in limbo.
            const response = await apiFetch('/api/registrations/', {
                method: 'POST',
                body: formData,
                requireAuth: false, // Registration is public
                timeout: 20000 // 20s
            });

            // CRITICAL: Successfully created (201) or OK (200) - Short-circuit to success page
            if (response.status === 200 || response.status === 201) {
                console.log('Registration success:', response.status);
                isRedirecting = true;
                window.location.href = '/success.php';
                return; // Exit immediately, redirection is in progress
            }

            const contentType = response.headers.get("content-type");
            const isJson = contentType && contentType.includes("application/json");

            // Error Handling
            if (isJson) {
                let errorData;
                try {
                    errorData = await response.json();
                } catch (e) {
                    errorData = { detail: "An unexpected error occurred and the server response could not be parsed." };
                }

                // Handle Duplicate ITS
                if (response.status === 400 && errorData.its_number) {
                    const itsMsg = Array.isArray(errorData.its_number) ? errorData.its_number[0] : errorData.its_number;
                    if (itsMsg.toLowerCase().includes('already exists')) {
                        showDialog({
                            variant: 'info',
                            title: 'Already Registered',
                            message: "You have already registered for Sherullah 1447H with this ITS number.",
                            confirmLabel: 'OK'
                        });
                        return;
                    }
                }

                // Generic Errors
                const errorMessages = Object.entries(errorData)
                    .map(([key, value]) => `${key.replace('_', ' ')}: ${Array.isArray(value) ? value[0] : value}`)
                    .join('\n');

                showDialog({
                    variant: 'danger',
                    title: 'Validation Error',
                    message: errorMessages || `Submission failed (Error ${response.status}). Please check your input.`,
                    confirmLabel: 'Fix Errors'
                });

            } else {
                const fallbackMsg = response.status >= 500
                    ? "Our server is currently experiencing issues. Please try again or check the status page later."
                    : `An unexpected error occurred (Status ${response.status}). Please try again later.`;

                showDialog({
                    variant: 'danger',
                    title: 'Registration Failed',
                    message: fallbackMsg,
                    confirmLabel: 'OK'
                });
            }

        } catch (err) {
            console.error('Submission technical error:', err);
                // --- DISTRIBUTED CONSISTENCY RECOVERY ---
                // Use a short polling loop to verify whether the registration actually made
                // it into the database despite the network/connection error. This avoids
                // false failures while preventing double-submits.
                const itsNumber = formData.get('its_number');
                console.log(`Checking if registration exists for ITS: ${itsNumber} after connection error...`);

                const found = await pollRegistrationExists(itsNumber, { attempts: 12, interval: 2000 });

                if (found) {
                    console.log('Recovery Success: Registration found in database despite connection error.');
                    isRedirecting = true;
                    window.location.href = '/success.php';
                    return;
                }

                // If not found after polling, inform user and re-enable the form.
                const networkMsg = err && err.isTimeout
                    ? 'Submission timed out. The server may be busy. We checked for your registration but did not find it.'
                    : 'Network error: Cannot reach the server. Please check your internet connection.';

                showDialog({
                    variant: 'danger',
                    title: 'Connection Error',
                    message: networkMsg,
                    confirmLabel: 'Retry Later'
                });
        } finally {
            // ONLY reset submitting state if we are NOT redirecting.
            // This prevents the button from "flicking" back to active while the next page is loading.
            if (!isRedirecting) {
                setSubmitting(false);
            }
        }
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
