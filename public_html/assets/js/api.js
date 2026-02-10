/**
 * Institutional API Client for Madras Jamaat (JS Version)
 * Handles base URL, auth headers, token refresh, and errors.
 */

// ✅ CONFIGURATION: Change this to your production Django API URL
// e.g., 'https://api.yourdomain.com'
window.API_BASE = 'http://localhost:8000';


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

    const url = `${window.API_BASE}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;

    let response = await fetch(url, {
        ...options,
        headers,
    });

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
