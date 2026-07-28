/**
 * Reusable Card Component.
 *
 * Provides consistent card styling for content containers.
 */

export default function Card({ children, className = "", padding = true }) {
    const classes = [
        "bg-white rounded-xl shadow-sm border border-gray-200",
        padding && "p-6",
        className,
    ]
        .filter(Boolean)
        .join(" ");

    return <div className={classes}>{children}</div>;
}
