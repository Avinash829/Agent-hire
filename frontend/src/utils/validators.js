/**
 * Client-side Validation Utilities.
 *
 * Provides input validation functions for the frontend.
 */

export function validateJobDescription(description) {
    if (!description || !description.trim()) {
        return "Job description is required";
    }
    if (description.trim().length < 20) {
        return "Job description must be at least 20 characters";
    }
    if (description.length > 10000) {
        return "Job description must not exceed 10,000 characters";
    }
    return null;
}

export function validateUrl(url) {
    if (!url || !url.trim()) return null;

    try {
        const parsed = new URL(url);
        if (!["http:", "https:"].includes(parsed.protocol)) {
            return "URL must use http or https scheme";
        }
        return null;
    } catch {
        return "Please enter a valid URL (e.g., https://example.com)";
    }
}
