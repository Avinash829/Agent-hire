/**
 * Verification Result Card Component.
 *
 * Displays the complete verification result including
 * overall score, breakdown, and evidence from both pipelines.
 */

import Card from "../common/Card";
import Badge from "../common/Badge";
import {
    formatScore,
    formatDate,
    getVerdictColor,
} from "../../utils/formatters";

export default function ResultCard({ result }) {
    if (!result) return null;

    const {
        synthesis,
        ml_result,
        agent_result,
        evidence,
        verification_id,
        timestamp,
    } = result;
    const verdictColor = getVerdictColor(synthesis?.verdict);

    const ScoreBar = ({ label, score, color = "primary" }) => {
        const colorMap = {
            primary: "bg-primary-500",
            success: "bg-success-500",
            warning: "bg-warning-500",
            danger: "bg-danger-500",
        };
        const barColor = colorMap[color] || colorMap.primary;
        return (
            <div className="space-y-1">
                <div className="flex justify-between text-sm">
                    <span className="text-gray-600">{label}</span>
                    <span className="font-medium">{formatScore(score)}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                        className={`${barColor} h-2 rounded-full transition-all`}
                        style={{ width: `${(score || 0) * 100}%` }}
                    />
                </div>
            </div>
        );
    };

    return (
        <Card>
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-gray-900">
                    Verification Result
                </h2>
                <Badge variant={verdictColor}>
                    {synthesis?.verdict?.toUpperCase()}
                </Badge>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-500 mb-1">
                        Overall Risk Score
                    </p>
                    <p className="text-3xl font-bold text-gray-900">
                        {formatScore(synthesis?.overall_score)}
                    </p>
                </div>
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-500 mb-1">
                        ML Pipeline Score
                    </p>
                    <p className="text-3xl font-bold text-primary-600">
                        {formatScore(ml_result?.risk_score)}
                    </p>
                </div>
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-500 mb-1">
                        AI Investigation Score
                    </p>
                    <p className="text-3xl font-bold text-primary-600">
                        {formatScore(agent_result?.agent_risk_score)}
                    </p>
                </div>
            </div>

            <div className="space-y-4 mb-6">
                <ScoreBar
                    label="ML Analysis"
                    score={ml_result?.risk_score}
                    color="primary"
                />
                <ScoreBar
                    label="AI Investigation"
                    score={agent_result?.agent_risk_score}
                    color="primary"
                />
                <ScoreBar
                    label="Overall Confidence"
                    score={synthesis?.overall_confidence}
                    color="success"
                />
            </div>

            {synthesis?.reasons?.length > 0 && (
                <div className="mb-6">
                    <h3 className="text-sm font-semibold text-gray-700 mb-3">
                        Reasons
                    </h3>
                    <ul className="space-y-2">
                        {synthesis.reasons.map((reason, index) => (
                            <li
                                key={index}
                                className="flex items-start space-x-2 text-sm text-gray-600"
                            >
                                <svg
                                    className="w-4 h-4 mt-0.5 text-gray-400 flex-shrink-0"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M9 12l2 2 4-4"
                                    />
                                </svg>
                                <span>{reason}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {synthesis?.recommendations?.length > 0 && (
                <div className="mb-6">
                    <h3 className="text-sm font-semibold text-gray-700 mb-3">
                        Recommendations
                    </h3>
                    <ul className="space-y-2">
                        {synthesis.recommendations.map((rec, index) => (
                            <li
                                key={index}
                                className="flex items-start space-x-2 text-sm text-gray-600"
                            >
                                <svg
                                    className="w-4 h-4 mt-0.5 text-warning-500 flex-shrink-0"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                                    />
                                </svg>
                                <span>{rec}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {agent_result?.gemini_reasoning && (
                <div className="mb-6">
                    <h3 className="text-sm font-semibold text-gray-700 mb-3">
                        AI Analysis
                    </h3>
                    <div className="bg-gray-50 rounded-lg p-4">
                        <p className="text-sm text-gray-600 whitespace-pre-wrap">
                            {agent_result.gemini_reasoning}
                        </p>
                    </div>
                </div>
            )}

            <div className="border-t border-gray-200 pt-4 mt-4">
                <div className="flex justify-between text-xs text-gray-400">
                    <span>ID: {verification_id}</span>
                    <span>{formatDate(timestamp)}</span>
                </div>
            </div>
        </Card>
    );
}
