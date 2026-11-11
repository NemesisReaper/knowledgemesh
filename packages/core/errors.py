class KnowMeshError(Exception):
    """Base exception for expected KnowMesh domain and service failures."""
    code="knowmesh_error"
    def __init__(self,message: str,*,details=None):
        super().__init__(message)
        self.message=message
        self.details=details or {}

class ValidationError(KnowMeshError): code="validation_error"
class NotFoundError(KnowMeshError): code="not_found"
class ConflictError(KnowMeshError): code="conflict"
class AuthorizationError(KnowMeshError): code="authorization_denied"
class IntegrityError(KnowMeshError): code="integrity_error"
class DependencyUnavailableError(KnowMeshError): code="dependency_unavailable"
