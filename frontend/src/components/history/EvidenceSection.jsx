/**
 * Evidence Section Component.
 *
 * Displays the collected evidence from the
 * verification process.
 */

import EvidenceList from "../dashboard/EvidenceList";

export default function EvidenceSection({ evidence }) {
    return (
        <div className="mb-8">
            <h3 className="mb-4 text-lg font-semibold text-gray-900">
                Evidence
            </h3>

            <EvidenceList evidence={evidence || {}} />
        </div>
    );
}
