/**
 * API Endpoint Functions.
 *
 * Provides typed functions for all backend API interactions.
 * Each function encapsulates the request to a specific endpoint.
 */

import axiosInstance from "./axiosInstance";
import { API_ENDPOINTS } from "../constants";

export async function verifyAuthToken() {
    const response = await axiosInstance.post(API_ENDPOINTS.verifyToken);
    return response.data;
}

export async function getUserProfile() {
    const response = await axiosInstance.get(API_ENDPOINTS.userProfile);
    return response.data;
}

export async function verifyJobPosting({
    jobDescription,
    sourceLink,
    applicationLink,
}) {
    const response = await axiosInstance.post(API_ENDPOINTS.verifyJob, {
        job_description: jobDescription,
        source_link: sourceLink,
        application_link: applicationLink,
    });
    return response.data;
}

export async function getVerificationHistory(page = 1, limit = 20) {
    const response = await axiosInstance.get(
        API_ENDPOINTS.verificationHistory,
        {
            params: { page, limit },
        }
    );
    return response.data;
}

export async function getVerificationDetail(verificationId) {
    const response = await axiosInstance.get(
        `${API_ENDPOINTS.verificationHistory}${verificationId}`
    );
    return response.data;
}
