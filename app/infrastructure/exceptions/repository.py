from infrastructure.exceptions.base import InfrastructureError


class RepositoryError(InfrastructureError): ...


class NotFoundError(RepositoryError): ...


class ConfigIdNotSpecifiedError(RepositoryError): ...
