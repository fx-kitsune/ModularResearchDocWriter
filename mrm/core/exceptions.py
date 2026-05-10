"""Custom exceptions for MRM Toolkit."""

class MRMError(Exception):
    """Base class for all MRM errors."""
    pass

class ToolkitNotFoundError(MRMError):
    """Raised when the bundled toolkit resources cannot be found."""
    pass

class MRMValidationError(MRMError):
    """Raised when validation fails."""
    pass

class MRMAssemblerError(MRMError):
    """Raised when report assembly fails."""
    pass
