/**
 * Recommendations Section Component.
 *
 * Displays recommendations generated from the
 * fraud verification analysis.
 */

export default function RecommendationsSection({ recommendations = [] }) {
    if (!Array.isArray(recommendations) || recommendations.length === 0) {
        return null;
    }

    return (
        <div className="mb-8">
            <h3 className="mb-4 text-lg font-semibold text-gray-900">
                Recommendations
            </h3>

            <ul className="space-y-3">
                {recommendations.map((recommendation, index) => (
                    <li
                        key={`${index}-${recommendation}`}
                        className="flex items-start gap-3 rounded-lg border border-yellow-200 bg-yellow-50 p-4"
                    >
                        <div className="mt-0.5 flex-shrink-0">
                            <svg
                                className="h-5 w-5 text-yellow-600"
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
                        </div>

                        <p className="text-sm leading-6 text-gray-700">
                            {recommendation}
                        </p>
                    </li>
                ))}
            </ul>
        </div>
    );
}
