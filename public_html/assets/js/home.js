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

        try {
            const response = await apiFetch('/api/registrations/', {
                method: 'POST',
                body: formData,
                requireAuth: false // Registration is public
            });

            const contentType = response.headers.get("content-type");
            const isJson = contentType && contentType.includes("application/json");

            if (response.ok) {
                // Success
                window.location.href = '/success.php';
                return;
            }

            // Error Handling
            if (isJson) {
                const errorData = await response.json();

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
                        setSubmitting(false);
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
            // console.error('Submission error:', err); // Silenced for production
            const networkMsg = "Network error: Cannot reach the server. Please check your internet connection.";

            showDialog({
                variant: 'danger',
                title: 'Connection Error',
                message: networkMsg,
                confirmLabel: 'Retry Later'
            });
        } finally {
            if (!document.getElementById('success-view').classList.contains('hidden')) {
                // If success, keep loading state off but don't re-enable form
            } else {
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
