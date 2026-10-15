"""Base class for business-rule violations raised by the service layer."""


class DomainError(Exception):
    """A business rule violation that maps onto a well-defined API error.

    Concrete subclasses (``NotFoundError``, ``ConflictError`` and friends) are
    introduced alongside the modules that need them, so services can raise
    business intent instead of leaking HTTP concerns into the domain.
    """

    default_message = "A business rule was violated"
    status_code = 400
    error_code = "business_error"

    def __init__(self, message: str | None = None) -> None:
        self.message = message or self.default_message
        super().__init__(self.message)
