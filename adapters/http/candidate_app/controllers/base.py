from abc import ABC, abstractmethod

from fastapi import HTTPException

from core.exceptions import EntityNotFoundException, ValidationException, DomainException


class BaseControllerInterface(ABC):
    """Interfaz base para controladores"""

    @abstractmethod
    def handle_exception(self, exception: Exception) -> None:
        """Maneja excepciones del dominio y las convierte en HTTP exceptions"""
        pass


class BaseController(BaseControllerInterface):
    """Implementación base de controlador con manejo de excepciones"""

    def handle_exception(self, exception: Exception) -> None:
        """Maneja excepciones del dominio y las convierte en HTTP exceptions"""
        if isinstance(exception, EntityNotFoundException):
            raise HTTPException(status_code=404, detail=str(exception))
        elif isinstance(exception, ValidationException):
            raise HTTPException(status_code=400, detail=str(exception))
        elif isinstance(exception, DomainException):
            raise HTTPException(status_code=500, detail=str(exception))
        else:
            raise HTTPException(status_code=500, detail="Internal server error")
