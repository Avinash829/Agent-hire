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
                    <div className="text-sm text-gray-500 flex flex-col sm:flex-row sm:items-center">
                        <span>
                            &copy; {currentYear} Hybrid Fake Job Detection. All
                            rights reserved.
                        </span>
                        <span className="hidden sm:inline mx-2">|</span>
                        <span className="mt-1 sm:mt-0">
                            Developed by{" "}
                            <a
                                href="https://avinashpappala.pages.dev/"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-blue-600 hover:text-blue-800 transition-colors font-medium"
                            >
                                Avinash
                            </a>
                        </span>
                    </div>
                    <div className="flex space-x-6">
                        <a
                            href="https://github.com/Avinash829/Agent-hire"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-sm text-gray-500 hover:text-gray-700 transition-colors"
                        >
                            GitHub
                        </a>
                        <a
                            href="https://www.linkedin.com/in/avinashpappala/"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-sm text-gray-500 hover:text-gray-700 transition-colors"
                        >
                            LinkedIn
                        </a>
                        <a
                            href="https://avinashpappala.pages.dev/"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-sm text-gray-500 hover:text-gray-700 transition-colors"
                        >
                            Portfolio
                        </a>
                    </div>
                </div>
            </div>
        </footer>
    );
}
