from fastapi import HTTPException
from typing import Optional, Dict, Any

class RetailException(HTTPException):
    """Exception de base pour l'application retail"""
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str,
        additional_info: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "error_code": error_code,
                "message": detail,
                "additional_info": additional_info or {}
            }
        )

class InvalidStateError(RetailException):
    """Exception levée quand un état invalide est fourni"""
    def __init__(self, state: str, valid_states: list):
        super().__init__(
            status_code=400,
            error_code="INVALID_STATE",
            detail=f"L'état '{state}' n'est pas valide",
            additional_info={
                "provided_state": state,
                "valid_states": valid_states,
                "suggestion": "Veuillez utiliser un des états valides listés"
            }
        )

class StateNotSupportedError(RetailException):
    """Exception levée quand un état n'est pas encore supporté"""
    def __init__(self, state: str):
        super().__init__(
            status_code=400,
            error_code="STATE_NOT_SUPPORTED",
            detail=f"L'état '{state}' n'est pas encore supporté pour les calculs de taxe",
            additional_info={
                "state": state,
                "suggestion": "Contactez le support pour ajouter le support de cet état"
            }
        )

class CalculationError(RetailException):
    """Exception levée lors d'une erreur de calcul"""
    def __init__(self, detail: str, calculation_data: Dict[str, Any]):
        super().__init__(
            status_code=500,
            error_code="CALCULATION_ERROR",
            detail=f"Erreur lors du calcul : {detail}",
            additional_info={
                "calculation_data": calculation_data,
                "suggestion": "Veuillez vérifier les données d'entrée"
            }
        )

class ProductNotFoundError(RetailException):
    """Exception levée quand un produit n'est pas trouvé"""
    def __init__(self, product_id: int):
        super().__init__(
            status_code=404,
            error_code="PRODUCT_NOT_FOUND",
            detail=f"Le produit avec l'ID {product_id} n'existe pas",
            additional_info={
                "product_id": product_id,
                "suggestion": "Vérifiez l'ID du produit"
            }
        )
