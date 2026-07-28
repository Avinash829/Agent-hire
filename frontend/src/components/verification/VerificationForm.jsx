/**
 * Verification Form Component.
 *
 * Form for submitting job postings for fraud verification.
 * Includes validation for all input fields.
 */

import { useState } from "react";
import Input from "../common/Input";
import Button from "../common/Button";
import Card from "../common/Card";
import { validateJobDescription, validateUrl } from "../../utils/validators";

export default function VerificationForm({ onSubmit, loading }) {
    const [formData, setFormData] = useState({
        jobDescription: "",
        sourceLink: "",
        applicationLink: "",
    });
    const [errors, setErrors] = useState({});

    const handleChange = (field) => (event) => {
        const { value } = event.target;
        setFormData((prev) => ({ ...prev, [field]: value }));
        if (errors[field]) {
            setErrors((prev) => ({ ...prev, [field]: null }));
        }
    };

    const validate = () => {
        const newErrors = {};

        const descriptionError = validateJobDescription(
            formData.jobDescription
        );
        if (descriptionError) newErrors.jobDescription = descriptionError;

        if (formData.sourceLink) {
            const sourceError = validateUrl(formData.sourceLink);
            if (sourceError) newErrors.sourceLink = sourceError;
        }

        if (formData.applicationLink) {
            const appError = validateUrl(formData.applicationLink);
            if (appError) newErrors.applicationLink = appError;
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        if (validate()) {
            onSubmit(formData);
        }
    };

    return (
        <Card>
            <h2 className="text-xl font-semibold text-gray-900 mb-6">
                Submit Job Posting for Verification
            </h2>

            <form onSubmit={handleSubmit} className="space-y-6">
                <Input
                    label="Job Description"
                    type="textarea"
                    value={formData.jobDescription}
                    onChange={handleChange("jobDescription")}
                    placeholder="Paste the full job posting text here (minimum 20 characters)..."
                    required
                    rows={8}
                    error={errors.jobDescription}
                />

                <Input
                    label="Source Link"
                    type="url"
                    value={formData.sourceLink}
                    onChange={handleChange("sourceLink")}
                    placeholder="https://example.com/job-posting"
                    error={errors.sourceLink}
                />

                <Input
                    label="Application Link"
                    type="url"
                    value={formData.applicationLink}
                    onChange={handleChange("applicationLink")}
                    placeholder="https://example.com/apply"
                    error={errors.applicationLink}
                />

                <div className="flex justify-end">
                    <Button type="submit" loading={loading} size="lg">
                        {loading ? "Analyzing..." : "Verify Job Posting"}
                    </Button>
                </div>
            </form>
        </Card>
    );
}
