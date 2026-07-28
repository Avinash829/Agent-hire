/**
 * Reusable Input Component.
 *
 * Supports text, textarea, email, and URL input types with labels and error messages.
 */

export default function Input({
    label,
    type = "text",
    value,
    onChange,
    placeholder,
    error,
    required = false,
    disabled = false,
    rows,
    className = "",
}) {
    const inputClasses = [
        "w-full px-4 py-2.5 rounded-lg border transition-colors duration-200",
        "focus:ring-2 focus:border-transparent",
        "placeholder:text-gray-400",
        error
            ? "border-danger-300 focus:ring-danger-500"
            : "border-gray-300 focus:ring-primary-500 focus:border-primary-500",
        disabled && "bg-gray-50 cursor-not-allowed",
        className,
    ].join(" ");

    const inputId = label
        ? label.toLowerCase().replace(/\s+/g, "-")
        : undefined;

    return (
        <div className="space-y-1.5">
            {label && (
                <label
                    htmlFor={inputId}
                    className="block text-sm font-medium text-gray-700"
                >
                    {label}
                    {required && (
                        <span className="text-danger-500 ml-1">*</span>
                    )}
                </label>
            )}
            {type === "textarea" ? (
                <textarea
                    id={inputId}
                    className={inputClasses}
                    value={value}
                    onChange={onChange}
                    placeholder={placeholder}
                    required={required}
                    disabled={disabled}
                    rows={rows || 4}
                />
            ) : (
                <input
                    id={inputId}
                    type={type}
                    className={inputClasses}
                    value={value}
                    onChange={onChange}
                    placeholder={placeholder}
                    required={required}
                    disabled={disabled}
                />
            )}
            {error && <p className="text-sm text-danger-600 mt-1">{error}</p>}
        </div>
    );
}
