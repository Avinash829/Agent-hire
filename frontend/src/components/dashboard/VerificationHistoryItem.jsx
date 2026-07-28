/**
 * Verification History Item Component.
 *
 * Displays a single verification history entry in a list.
 */

import Badge from "../common/Badge";
import {
    formatDate,
    formatScore,
    getVerdictColor,
} from "../../utils/formatters";

export default function VerificationHistoryItem({ item, onClick }) {
    const verdictColor = getVerdictColor(item.verdict);

    return (
        <div
            className="bg-white rounded-lg border border-gray-200 p-4 hover:shadow-md transition-shadow cursor-pointer"
            onClick={() => onClick?.(item.verification_id)}
        >
            <div className="flex items-center justify-between mb-2">
                <div className="flex items-center space-x-3">
                    <Badge variant={verdictColor}>
                        {item.verdict?.toUpperCase()}
                    </Badge>
                    <span className="text-sm font-medium text-gray-900">
                        Risk: {formatScore(item.overall_score)}
                    </span>
                </div>
                <span className="text-xs text-gray-400">
                    {formatDate(item.timestamp)}
                </span>
            </div>

            <p className="text-sm text-gray-600 line-clamp-2">
                {item.job_description_preview}
            </p>

            <div className="flex justify-end mt-2">
                <span className="text-xs text-primary-600 font-medium hover:text-primary-700">
                    View Details &rarr;
                </span>
            </div>
        </div>
    );
}
