/**
 * 404 Not Found Page Component.
 *
 * Displayed when a route does not match any configured path.
 */

import { Link } from "react-router-dom";
import Button from "../components/common/Button";

export default function NotFoundPage() {
    return (
        <div className="min-h-[80vh] flex items-center justify-center px-4">
            <div className="text-center max-w-md">
                <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
                    <span className="text-5xl font-bold text-gray-300">
                        404
                    </span>
                </div>
                <h1 className="text-2xl font-bold text-gray-900 mb-4">
                    Page Not Found
                </h1>
                <p className="text-gray-600 mb-8">
                    The page you are looking for does not exist or has been
                    moved. Please check the URL or navigate back to the
                    homepage.
                </p>
                <div className="flex justify-center space-x-4">
                    <Link to="/">
                        <Button>Go Home</Button>
                    </Link>
                    <Link to="/verify">
                        <Button variant="secondary">Verify a Job</Button>
                    </Link>
                </div>
            </div>
        </div>
    );
}
