/**
 * Metadata Section Component.
 *
 * Displays verification metadata including
 * the verification ID and creation timestamp.
 */

import { formatDate } from "../../utils/formatters";

export default function MetadataSection({ id, timestamp }) {
    return (
        <div className="mt-8 border-t border-gray-200 pt-4">
            <div className="flex flex-col gap-2 text-xs text-gray-500 md:flex-row md:items-center md:justify-between">
                <div>
                    <span className="font-medium text-gray-700">
                        Verification ID:
                    </span>{" "}
                    <span className="break-all">{id}</span>
                </div>

                <div>
                    <span className="font-medium text-gray-700">
                        Verified On:
                    </span>{" "}
                    {formatDate(timestamp)}
                </div>
            </div>
        </div>
    );
}
