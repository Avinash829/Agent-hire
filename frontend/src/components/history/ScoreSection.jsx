/**
 * Score Section Component.
 *
 * Displays the overall risk score, ML score,
 * and Agent score for a verification.
 */

import { formatScore } from "../../utils/formatters";

export default function ScoreSection({ finalScore, mlScore, agentScore }) {
    const scoreCards = [
        {
            title: "Overall Risk Score",
            value: formatScore(finalScore),
            valueClassName: "text-gray-900",
        },
        {
            title: "ML Score",
            value: formatScore(mlScore),
            valueClassName: "text-primary-600",
        },
        {
            title: "Agent Score",
            value: formatScore(agentScore),
            valueClassName: "text-primary-600",
        },
    ];

    return (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            {scoreCards.map((card) => (
                <div
                    key={card.title}
                    className="rounded-lg bg-gray-50 p-5 text-center border border-gray-100"
                >
                    <p className="mb-2 text-sm font-medium text-gray-500">
                        {card.title}
                    </p>

                    <p className={`text-3xl font-bold ${card.valueClassName}`}>
                        {card.value}
                    </p>
                </div>
            ))}
        </div>
    );
}
