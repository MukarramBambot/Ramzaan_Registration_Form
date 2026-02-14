/**
 * Institutional API Client for Madras Jamaat (JS Version)
 * Handles base URL, auth headers, token refresh, and errors.
 */

// ✅ CONFIGURATION: Change this to your production Django API URL
// e.g., 'https://api.yourdomain.com'
window.API_BASE = 'https://api.madrasjamaatportal.org';


// Helper to get tokens
function getAccessToken() {
    return localStorage.getItem('access_token');
}

function getRefreshToken() {
    return localStorage.getItem('refresh_token');
}

/**
 * Refresh JWT access token using refresh token
 */
async function refreshAccessToken() {
    const refresh = getRefreshToken();
    if (!refresh) return null;

    try {
        const res = await fetch(`${window.API_BASE}/api/token/refresh/`, { // Corrected endpoint for SimpleJWT usually
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh }),
        });

        if (!res.ok) return null;

        const data = await res.json();
        localStorage.setItem('access_token', data.access);
        return data.access;
    } catch (e) {
        console.error("Token refresh failed", e);
        return null;
    }
}

/**
 * Main API fetch wrapper
 * @param {string} endpoint 
 * @param {object} options 
 */
async function apiFetch(endpoint, options = {}) {
    // Default requireAuth to true unless specified
    const requireAuth = options.requireAuth !== false;

    // Optional timeout in milliseconds. If set to >0, the request will be aborted
    // after the timeout and a timeout error will be thrown with `isTimeout=true`.
    const timeout = options.timeout || 0;
    if (options.timeout) delete options.timeout;

    // Prepare headers
    const headers = new Headers(options.headers || {});

    // Content-Type default
    if (
        options.body &&
        !headers.has('Content-Type') &&
        !(options.body instanceof FormData)
    ) {
        headers.set('Content-Type', 'application/json');
    }

    // Auth header
    if (requireAuth) {
        const token = getAccessToken();
        if (token) {
            headers.set('Authorization', `Bearer ${token}`);
        }
    }

    let url = `${window.API_BASE}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;

    // Add cache-buster to GET requests
    if (!options.method || options.method === 'GET') {
        const sep = url.includes('?') ? '&' : '?';
        url += `${sep}v=${Date.now()}`;
    }

    // Use AbortController to support timeouts
    const controller = new AbortController();
    const signal = controller.signal;
    const fetchOptions = {
        ...options,
        headers,
        signal,
    };

    let timeoutId = null;
    if (timeout > 0) {
        timeoutId = setTimeout(() => controller.abort(), timeout);
    }

    let response;
    try {
        response = await fetch(url, fetchOptions);
    } catch (err) {
        // Normalize AbortError as a timeout for callers
        if (err.name === 'AbortError') {
            const toErr = new Error('Request timed out');
            toErr.isTimeout = true;
            throw toErr;
        }
        throw err;
    } finally {
        if (timeoutId) clearTimeout(timeoutId);
    }

    // Auto-refresh on 401
    if (response.status === 401 && requireAuth) {
        const newToken = await refreshAccessToken();

        if (!newToken) {
            localStorage.clear();
            window.location.href = '/admin/login.php';
            throw new Error('Session Expired');
        }

        headers.set('Authorization', `Bearer ${newToken}`);

        response = await fetch(url, {
            ...options,
            headers,
        });
    }

    // Handle 403 Forbidden
    if (response.status === 403 && requireAuth) {
        showDialog({
            variant: 'danger',
            title: 'Permission Denied',
            message: 'You do not have permission to perform this action. Your account may lack administrative privileges.'
        });
    }

    return response;
}
