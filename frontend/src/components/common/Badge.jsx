/**
 * Reusable Badge Component.
 *
 * Displays status or category labels with color coding.
 */

export default function Badge({ children, variant = "gray", className = "" }) {
    const variants = {
        success: "bg-success-100 text-success-800",
        warning: "bg-warning-100 text-warning-800",
        danger: "bg-danger-100 text-danger-800",
        info: "bg-blue-100 text-blue-800",
        gray: "bg-gray-100 text-gray-800",
    };

    const classes = [
        "inline-flex items-center px-3 py-1 rounded-full text-sm font-medium",
        variants[variant] || variants.gray,
        className,
    ].join(" ");

    return <span className={classes}>{children}</span>;
}
