"""Custom exceptions for Resume Match AI."""


class ResumeMatchError(Exception):
    """Base exception for application errors."""


class InvalidResumeError(ResumeMatchError):
    """Raised when resume text is empty or invalid."""


class InvalidJobDescriptionError(ResumeMatchError):
    """Raised when job description text is empty or invalid."""


class InvalidFileError(ResumeMatchError):
    """Raised when an uploaded file is invalid or unsupported."""


class SkillDictionaryError(ResumeMatchError):
    """Raised when the skill dictionary cannot be loaded."""
