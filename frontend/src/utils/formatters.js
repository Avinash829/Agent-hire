/**
 * Formatting Utility Functions.
 *
 * Provides reusable formatting functions for dates, scores,
 * and other display values.
 */

export function formatScore(score) {
    if (score === null || score === undefined) return "N/A";
    return `${(score * 100).toFixed(0)}%`;
}

export function formatDate(dateString) {
    if (!dateString) return "N/A";

    try {
        const date = new Date(dateString);
        return date.toLocaleDateString("en-US", {
            year: "numeric",
            month: "short",
            day: "numeric",
            hour: "2-digit",
            minute: "2-digit",
        });
    } catch {
        return dateString;
    }
}

export function getVerdictColor(verdict) {
    const colors = {
        legitimate: "success",
        suspicious: "warning",
        fraudulent: "danger",
    };
    return colors[verdict?.toLowerCase()] || "gray";
}

export function truncateText(text, maxLength = 100) {
    if (!text || text.length <= maxLength) return text || "";
    return `${text.substring(0, maxLength)}...`;
}

export function formatConfidence(confidence) {
    if (confidence === null || confidence === undefined) return "N/A";
    return `${(confidence * 100).toFixed(1)}%`;
}
