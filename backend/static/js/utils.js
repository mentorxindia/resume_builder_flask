const utils = {
    getToken: function() {
        return localStorage.getItem('token');
    },

    isAuthenticated: function() {
        return this.getToken() !== null;
    },

    fetchWithAuth: async function(url, options = {}) {
        const token = this.getToken();
        if (!token) {
            throw new Error('No token found');
        }

        const headers = {
            ...options.headers,
            'Authorization': `Bearer ${token}`,
        };

        const response = await fetch(url, { ...options, headers });
        if (!response.ok) {
            throw new Error('Request failed');
        }
        return response.json();
    }
};
