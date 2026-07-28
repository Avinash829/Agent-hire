/**
 * Score Card Component.
 *
 * Displays a metric with label, value, and optional color coding.
 */

import Badge from "../common/Badge";

export default function ScoreCard({ label, score, verdict, loading = false }) {
    if (loading) {
        return (
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 animate-pulse">
                <div className="h-4 bg-gray-200 rounded w-1/2 mb-4" />
                <div className="h-8 bg-gray-200 rounded w-1/3 mb-2" />
                <div className="h-4 bg-gray-200 rounded w-1/4" />
            </div>
        );
    }

    const getVerdictVariant = (v) => {
        const map = {
            legitimate: "success",
            suspicious: "warning",
            fraudulent: "danger",
        };
        return map[v?.toLowerCase()] || "gray";
    };

    const formatScoreValue = (s) => {
        if (s === null || s === undefined) return "N/A";
        return `${(s * 100).toFixed(0)}%`;
    };

    return (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <p className="text-sm font-medium text-gray-500 mb-2">{label}</p>
            <p className="text-3xl font-bold text-gray-900 mb-2">
                {formatScoreValue(score)}
            </p>
            {verdict && (
                <Badge variant={getVerdictVariant(verdict)}>{verdict}</Badge>
            )}
        </div>
    );
}
