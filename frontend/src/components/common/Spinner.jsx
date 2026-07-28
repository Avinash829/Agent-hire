/**
 * Loading Spinner Component.
 *
 * Displays a centered loading spinner with optional message.
 */

export default function Spinner({ message = "Loading...", size = "md" }) {
    const sizes = {
        sm: "h-6 w-6",
        md: "h-10 w-10",
        lg: "h-16 w-16",
    };

    const spinnerSize = sizes[size] || sizes.md;

    return (
        <div className="flex flex-col items-center justify-center py-12">
            <svg
                className={`animate-spin text-primary-600 ${spinnerSize}`}
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
            {message && <p className="mt-4 text-sm text-gray-500">{message}</p>}
        </div>
    );
}
