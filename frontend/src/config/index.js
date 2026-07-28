/**
 * Application Configuration Module.
 *
 * Centralizes access to environment variables and application settings.
 */

const config = {
    api: {
        baseUrl: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
    },

    firebase: {
        apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
        authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
        projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
        storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
        messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
        appId: import.meta.env.VITE_FIREBASE_APP_ID,
        measurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID,
    },

    routes: {
        home: "/",
        login: "/login",
        verify: "/verify",
        dashboard: "/dashboard",
        history: "/history",
    },
};

export default config;
