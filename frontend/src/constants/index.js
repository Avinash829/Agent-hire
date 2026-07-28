/**
 * Application Constants.
 *
 * Defines shared constants used across the frontend application.
 */

export const RISK_THRESHOLDS = {
    legitimate: { max: 0.3, color: "success", label: "Legitimate" },
    suspicious: { min: 0.3, max: 0.65, color: "warning", label: "Suspicious" },
    fraudulent: { min: 0.65, color: "danger", label: "Fraudulent" },
};

export const VERDICT_COLORS = {
    legitimate: "success",
    suspicious: "warning",
    fraudulent: "danger",
};

export const API_ENDPOINTS = {
    verifyToken: "/api/v1/auth/verify",
    userProfile: "/api/v1/auth/profile",
    verifyJob: "/api/v1/verify/",
    verificationHistory: "/api/v1/history/",
};

export const STORAGE_KEYS = {
    authToken: "auth_token",
    userData: "user_data",
};

export const APP_NAME = "Hybrid Fake Job Detection";

export const ERROR_MESSAGES = {
    networkError: "Network error. Please check your connection.",
    authenticationError: "Authentication failed. Please login again.",
    validationError: "Please check your input and try again.",
    serverError: "Server error. Please try again later.",
    unauthorized: "You are not authorized to perform this action.",
};
