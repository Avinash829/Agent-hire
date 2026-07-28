/**
 * Evidence List Component.
 *
 * Displays structured evidence from the investigation in a readable format.
 */

export default function EvidenceList({ evidence }) {
    if (!evidence) return null;

    const sections = [];

    if (evidence.whois) {
        sections.push({
            title: "Domain Registration",
            icon: "globe",
            items: [
                {
                    label: "Domain Age",
                    value: evidence.whois.domain_age_days
                        ? `${evidence.whois.domain_age_days} days`
                        : "Unknown",
                },
                {
                    label: "Registrar",
                    value: evidence.whois.registrar || "Unknown",
                },
                {
                    label: "Suspicious",
                    value: evidence.whois.is_suspiciously_young
                        ? "Yes - Recently registered"
                        : "No",
                },
            ],
        });
    }

    if (evidence.website) {
        sections.push({
            title: "Website Analysis",
            icon: "browser",
            items: [
                {
                    label: "Career Page Found",
                    value: evidence.website.has_career_page ? "Yes" : "No",
                },
                {
                    label: "Page Title",
                    value: evidence.website.page_title || "N/A",
                },
                {
                    label: "Status",
                    value: evidence.website.status_code
                        ? `HTTP ${evidence.website.status_code}`
                        : "Unknown",
                },
            ],
        });
    }

    if (evidence.online_reputation) {
        sections.push({
            title: "Online Reputation",
            icon: "chat",
            items: [
                {
                    label: "Relevant Sources",
                    value: evidence.online_reputation.mentions_count || 0,
                },
                {
                    label: "Reported Scam Indicators",
                    value: evidence.online_reputation.scam_mentions || 0,
                },
                {
                    label: "Overall Reputation",
                    value: evidence.online_reputation.sentiment || "Neutral",
                },
            ],
        });
    }

    if (sections.length === 0) return null;

    return (
        <div className="space-y-4">
            <h3 className="text-sm font-semibold text-gray-700">
                Investigation Evidence
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {sections.map((section) => (
                    <div
                        key={section.title}
                        className="bg-gray-50 rounded-lg p-4"
                    >
                        <h4 className="text-sm font-medium text-gray-700 mb-3">
                            {section.title}
                        </h4>
                        <dl className="space-y-2">
                            {section.items.map((item) => (
                                <div
                                    key={item.label}
                                    className="flex justify-between"
                                >
                                    <dt className="text-xs text-gray-500">
                                        {item.label}
                                    </dt>
                                    <dd className="text-xs font-medium text-gray-900">
                                        {item.value}
                                    </dd>
                                </div>
                            ))}
                        </dl>
                    </div>
                ))}
            </div>
        </div>
    );
}
