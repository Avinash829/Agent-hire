/**
 * Reusable Button Component.
 *
 * Supports multiple variants, sizes, loading state, and icon support.
 */

export default function Button({
    children,
    variant = "primary",
    size = "md",
    loading = false,
    disabled = false,
    className = "",
    type = "button",
    onClick,
    icon: Icon,
}) {
    const baseStyles =
        "inline-flex items-center justify-center font-medium rounded-lg transition-colors duration-200 focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed";

    const variants = {
        primary:
            "bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500",
        secondary:
            "bg-white text-gray-700 border border-gray-300 hover:bg-gray-50 focus:ring-primary-500",
        danger: "bg-danger-600 text-white hover:bg-danger-700 focus:ring-danger-500",
        ghost: "text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:ring-gray-500",
    };

    const sizes = {
        sm: "px-3 py-1.5 text-sm",
        md: "px-6 py-2.5 text-sm",
        lg: "px-8 py-3 text-base",
    };

    const classes = [
        baseStyles,
        variants[variant] || variants.primary,
        sizes[size] || sizes.md,
        className,
    ].join(" ");

    return (
        <button
            type={type}
            className={classes}
            disabled={disabled || loading}
            onClick={onClick}
        >
            {loading && (
                <svg
                    className="animate-spin -ml-1 mr-2 h-4 w-4"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                >
                    <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                    />
                    <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                    />
                </svg>
            )}
            {Icon && !loading && <Icon className="w-5 h-5 mr-2" />}
            {children}
        </button>
    );
}
