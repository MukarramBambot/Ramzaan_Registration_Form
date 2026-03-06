<?php
// correction.php - Standalone page for user corrections
// Retrieve token from URL
$token = isset($_GET['token']) ? $_GET['token'] : '';

// Defensive handling: if token is missing, show a user-friendly message instead of a blank page or error
if (!$token) {
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Invalid Request</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body class="bg-gray-50 min-h-screen flex items-center justify-center p-4">
    <div class="max-w-md w-full bg-white rounded-xl shadow-lg p-8 text-center">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-amber-100 mb-6">
            <svg class="w-8 h-8 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
            </svg>
        </div>
        <h2 class="text-2xl font-bold text-gray-900 mb-2">Invalid Correction Link</h2>
        <p class="text-gray-600">This link is missing a security token. Please use the original link sent to you via WhatsApp or Email.</p>
    </div>
</body>
</html>
<?php
    exit;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registration Correction - Ramzaan Deployment</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
    </style>
</head>
<body class="bg-gray-50 min-h-screen flex items-center justify-center p-4">

    <div class="max-w-md w-full bg-white rounded-xl shadow-lg p-8" id="loading">
        <div class="flex flex-col items-center justify-center text-center">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4"></div>
            <p class="text-gray-600">Loading correction details...</p>
        </div>
    </div>

    <div class="max-w-md w-full bg-white rounded-xl shadow-lg p-8 hidden" id="error-view">
        <div class="text-center">
            <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-red-100 mb-6">
                <svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                </svg>
            </div>
            <h2 class="text-2xl font-bold text-gray-900 mb-2">Error</h2>
            <p class="text-gray-600" id="error-message">Invalid or expired token.</p>
        </div>
    </div>

    <div class="max-w-md w-full bg-white rounded-xl shadow-lg p-8 hidden" id="success-view">
        <div class="text-center">
            <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-green-100 mb-6">
                <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
            </div>
            <h2 class="text-2xl font-bold text-gray-900 mb-2">Success!</h2>
            <p class="text-gray-600">Your information has been updated successfully.</p>
        </div>
    </div>

    <div class="max-w-md w-full bg-white rounded-xl shadow-lg p-8 hidden" id="form-view">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">Update Your Information</h2>
        
        <div class="bg-blue-50 border-l-4 border-blue-500 p-4 mb-6">
            <div class="flex">
                <div class="flex-shrink-0">
                    <svg class="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
                    </svg>
                </div>
                <div class="ml-3">
                    <p class="text-sm text-blue-700" id="admin-message">
                        Admin Note: Please update this field correctly.
                    </p>
                </div>
            </div>
        </div>

        <form id="correction-form" class="space-y-6">
            <div id="dynamic-field-container">
                <!-- Field will be injected here -->
            </div>

            <button type="submit" 
                class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200">
                Submit Update
            </button>
        </form>
    </div>

    <script>
        const API_BASE_URL = 'https://api.madrasjamaatportal.org/api'; 
        const token = "<?php echo htmlspecialchars($token); ?>";
        let fieldName = '';

        async function fetchDetails() {
            try {
                const response = await fetch(`${API_BASE_URL}/corrections/token/${token}/`);
                if (!response.ok) throw new Error(await response.text());
                
                const data = await response.json();
                renderForm(data);
            } catch (error) {
                showError(error.message || "Failed to load correction details.");
            }
        }

        function renderForm(data) {
            document.getElementById('loading').classList.add('hidden');
            document.getElementById('form-view').classList.remove('hidden');
            
            document.getElementById('admin-message').textContent = data.admin_message || "Please correct the information below.";
            fieldName = data.field_name;
            
            const container = document.getElementById('dynamic-field-container');
            container.innerHTML = '';
            
            const label = document.createElement('label');
            label.className = "block text-sm font-medium text-gray-700 mb-2";
            label.textContent = `Correct Value for: ${formatFieldName(fieldName)}`;
            container.appendChild(label);

            let input;

            if (fieldName === 'audition_files') {
                input = document.createElement('input');
                input.type = 'file';
                input.multiple = true;
                input.accept = 'audio/*,video/*';
                input.className = "flex w-full rounded-md border border-gray-300 border-dashed p-3 text-sm file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100";
            } else {
                input = document.createElement('input');
                input.type = fieldName === 'email' ? 'email' : 'text';
                input.className = "appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm";
                input.placeholder = `Enter correct ${formatFieldName(fieldName)}`;
            }
            
            input.id = 'correction-input';
            container.appendChild(input);
        }

        function formatFieldName(name) {
            return name.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
        }

        function showError(msg) {
            let cleanMsg = msg;
            try {
                const json = JSON.parse(msg);
                if (json.error) cleanMsg = json.error;
            } catch (e) {}

            document.getElementById('loading').classList.add('hidden');
            document.getElementById('form-view').classList.add('hidden');
            document.getElementById('error-view').classList.remove('hidden');
            document.getElementById('error-message').textContent = cleanMsg;
        }

        document.getElementById('correction-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const input = document.getElementById('correction-input');
            const formData = new FormData();
            
            if (fieldName === 'audition_files') {
                if (input.files.length === 0) {
                    alert("Please select at least one file.");
                    return;
                }
                for (let i = 0; i < input.files.length; i++) {
                    formData.append('audition_files', input.files[i]);
                }
            } else {
                if (!input.value.trim()) {
                    alert("Please enter a value.");
                    return;
                }
                formData.append(fieldName, input.value.trim());
            }

            try {
                const response = await fetch(`${API_BASE_URL}/corrections/resolve/${token}/`, {
                    method: 'POST',
                    body: formData
                });
                
                if (!response.ok) throw new Error(await response.text());
                
                document.getElementById('form-view').classList.add('hidden');
                document.getElementById('success-view').classList.remove('hidden');
            } catch (error) {
                alert("Update failed: " + error.message);
            }
        });

        fetchDetails();
    </script>
</body>
</html>
