/**
 * History Header Component.
 *
 * Displays the page heading, back navigation, and verification verdict.
 */

import { Link } from "react-router-dom";
import Badge from "../common/Badge";

export default function HistoryHeader({ verdict, verdictColor }) {
    return (
        <>
            <div className="mb-6">
                <Link
                    to="/history"
                    className="text-sm font-medium text-primary-600 hover:text-primary-700 transition-colors"
                >
                    &larr; Back to History
                </Link>
            </div>

            <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-semibold text-gray-900">
                    Verification Details
                </h2>

                <Badge variant={verdictColor}>{verdict?.toUpperCase()}</Badge>
            </div>
        </>
    );
}
