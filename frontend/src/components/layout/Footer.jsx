/**
 * Footer Component.
 *
 * Displays the application footer with copyright and links.
 */

export default function Footer() {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="bg-white border-t border-gray-200 mt-auto">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                <div className="flex flex-col sm:flex-row justify-between items-center space-y-4 sm:space-y-0">
                    <div className="text-sm text-gray-500">
                        &copy; {currentYear} Hybrid Fake Job Detection. All
                        rights reserved.
                    </div>
                    <div className="flex space-x-6">
                        <a
                            href="https://github.com"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-sm text-gray-500 hover:text-gray-700 transition-colors"
                        >
                            GitHub
                        </a>
                        <a
                            href="/api/docs"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-sm text-gray-500 hover:text-gray-700 transition-colors"
                        >
                            API Docs
                        </a>
                    </div>
                </div>
            </div>
        </footer>
    );
}
