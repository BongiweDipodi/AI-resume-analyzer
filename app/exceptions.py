"""Application-specific exception classes."""

from __future__ import annotations


class InvalidFileError(Exception):
    """Raised when uploaded or parsed file content is invalid."""


class InvalidJobDescriptionError(ValueError):
    """Raised when a job description is missing or invalid."""


class InvalidResumeError(ValueError):
    """Raised when a resume text is missing or invalid."""


class SkillDictionaryError(Exception):
    """Raised when the skill dictionary fails to load or is invalid."""
"""Custom exceptions for Resume Match AI."""


class ResumeMatchError(Exception):
    """Base exception for application errors."""

