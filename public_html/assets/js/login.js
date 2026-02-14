/**
 * Login JS
 */

document.addEventListener('DOMContentLoaded', () => {
    // Check if already authenticated
    const token = localStorage.getItem('access_token');
    if (token) {
        // Simple check, real verification happens on dashboard load or API call
        window.location.href = '/admin/dashboard.php';
        return;
    }

    const form = document.getElementById('login-form');
    const itsInput = document.getElementById('its');
    const passInput = document.getElementById('pass');
    const togglePassBtn = document.getElementById('toggle-pass-btn');
    const eyeIcon = document.getElementById('eye-icon');
    const eyeOffIcon = document.getElementById('eye-off-icon');
    const loginBtn = document.getElementById('login-btn');
    const errorAlert = document.getElementById('error-alert');

    // Toggle Password Visibility
    togglePassBtn.addEventListener('click', () => {
        const type = passInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passInput.setAttribute('type', type);

        if (type === 'text') {
            eyeIcon.classList.add('hidden');
            eyeOffIcon.classList.remove('hidden');
        } else {
            eyeIcon.classList.remove('hidden');
            eyeOffIcon.classList.add('hidden');
        }
    });

    // Login Handler
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        const itsNumber = itsInput.value;
        const password = passInput.value;

        try {
            // 1) Obtain tokens from SimpleJWT endpoint
            // apiFetch wrapper usually handles auth headers, but here we don't need auth, we are getting it.
            // Using raw fetch or apiFetch with requireAuth: false
            const response = await fetch(`${API_BASE}/api/token/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: itsNumber, password }),
            });

            const tokenData = await response.json();

            if (!response.ok) {
                setError(tokenData.detail || tokenData.error || 'Invalid credentials');
                setLoading(false);
                return;
            }

            const access = tokenData.access;
            const refresh = tokenData.refresh;

            if (!access) {
                setError('No access token returned');
                setLoading(false);
                return;
            }

            // 2) Store tokens
            localStorage.setItem('access_token', access);
            if (refresh) localStorage.setItem('refresh_token', refresh);

            // 3) Fetch current user info
            const meRes = await apiFetch('/api/auth/me/', { method: 'GET', requireAuth: true });
            if (meRes.ok) {
                const meData = await meRes.json();
                localStorage.setItem('user', JSON.stringify(meData));
                window.location.href = '/admin/dashboard.php';
            } else {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                setError('Failed to retrieve user info');
                setLoading(false);
            }

        } catch (err) {
            // console.error(err); // Silenced for production
            setError('Connection error. Please try again.');
            setLoading(false);
        }
    });

    function setLoading(loading) {
        loginBtn.disabled = loading;
        if (loading) {
            loginBtn.innerHTML = `
                ${ICONS.loader2}
                <span class="ml-2">Authenticating...</span>
            `;
        } else {
            loginBtn.innerHTML = 'Sign In';
        }
    }

    function setError(msg) {
        if (msg) {
            errorAlert.textContent = msg;
            errorAlert.classList.remove('hidden');
        } else {
            errorAlert.classList.add('hidden');
            errorAlert.textContent = '';
        }
    }
});
