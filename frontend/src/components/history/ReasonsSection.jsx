/**
 * Reasons Section Component.
 *
 * Displays the reasons that contributed to the
 * final fraud risk assessment.
 */

export default function ReasonsSection({ reasons = [] }) {
    if (!Array.isArray(reasons) || reasons.length === 0) {
        return null;
    }

    return (
        <div className="mb-8">
            <h3 className="mb-4 text-lg font-semibold text-gray-900">
                Reasons
            </h3>

            <ul className="space-y-3">
                {reasons.map((reason, index) => (
                    <li
                        key={`${index}-${reason}`}
                        className="flex items-start gap-3 rounded-lg border border-gray-200 bg-gray-50 p-4"
                    >
                        <div className="mt-0.5 flex-shrink-0">
                            <svg
                                className="h-5 w-5 text-green-600"
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
                        </div>

                        <p className="text-sm leading-6 text-gray-700">
                            {reason}
                        </p>
                    </li>
                ))}
            </ul>
        </div>
    );
}
