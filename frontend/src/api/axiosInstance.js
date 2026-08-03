/**
 * Axios HTTP Client Configuration.
 *
 * Configures axios instance with interceptors for authentication
 * token injection and error handling.
 */

import axios from "axios";
import config from "../config";
import { STORAGE_KEYS, ERROR_MESSAGES } from "../constants";

const axiosInstance = axios.create({
    baseURL: config.api.baseUrl,
    timeout: 240000,
    headers: {
        "Content-Type": "application/json",
    },
});

axiosInstance.interceptors.request.use(
    (requestConfig) => {
        const token = localStorage.getItem(STORAGE_KEYS.authToken);
        if (token) {
            requestConfig.headers.Authorization = `Bearer ${token}`;
        }
        return requestConfig;
    },
    (error) => {
        return Promise.reject(error);
    }
);

axiosInstance.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response) {
            const { status, data } = error.response;

            if (status === 401) {
                localStorage.removeItem(STORAGE_KEYS.authToken);
                localStorage.removeItem(STORAGE_KEYS.userData);
                window.location.href = "/login";
            }

            const serverMessage = data?.error?.message || data?.detail?.message;
            error.customMessage = serverMessage || ERROR_MESSAGES.serverError;
        } else if (error.request) {
            error.customMessage = ERROR_MESSAGES.networkError;
        }

        return Promise.reject(error);
    }
);

export default axiosInstance;
