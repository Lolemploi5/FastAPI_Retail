from dataclasses import dataclass
from typing import Dict, Optional, List
from enum import Enum
from .exceptions import InvalidStateError, StateNotSupportedError, CalculationError

class State(str, Enum):
    UT = "UT"  # Utah
    NV = "NV"  # Nevada
    TX = "TX"  # Texas
    AL = "AL"  # Alabama
    CA = "CA"  # California

    @classmethod
    def list_states(cls) -> List[str]:
        """Retourne la liste des états disponibles"""
        return [state.value for state in cls]

    @classmethod
    def is_valid_state(cls, state: str) -> bool:
        """Vérifie si un état est valide"""
        return state in cls._value2member_map_

@dataclass
class TaxRate:
    rate: float
    description: str
    enabled: bool = True  # Indique si le calcul de taxe est activé pour cet état

class TaxCalculator:
    def __init__(self):
        self._initialize_tax_rates()

    def _initialize_tax_rates(self):
        """Initialise les taux de taxe avec leur statut"""
        self.tax_rates: Dict[State, TaxRate] = {
            State.UT: TaxRate(6.85, "Utah Sales Tax", True),
            State.NV: TaxRate(8.00, "Nevada Sales Tax", True),
            State.TX: TaxRate(6.25, "Texas Sales Tax", True),
            State.AL: TaxRate(4.00, "Alabama Sales Tax", True),
            State.CA: TaxRate(8.25, "California Sales Tax", True),
        }

    def validate_state(self, state: str) -> State:
        """
        Valide un état et retourne l'énumération correspondante
        
        Raises:
            InvalidStateError: Si l'état n'existe pas
            StateNotSupportedError: Si l'état existe mais n'est pas supporté
        """
        if not State.is_valid_state(state):
            raise InvalidStateError(state, State.list_states())
        
        state_enum = State(state)
        tax_rate = self.tax_rates.get(state_enum)
        
        if not tax_rate:
            raise StateNotSupportedError(state)
            
        if not tax_rate.enabled:
            raise StateNotSupportedError(
                state, 
                f"Le calcul de taxe pour l'état {state} est temporairement désactivé"
            )
            
        return state_enum

    def get_tax_rate(self, state: State) -> Optional[TaxRate]:
        """Récupère le taux de taxe pour un état donné"""
        return self.tax_rates.get(state)

    def calculate_tax(self, amount: float, state: str) -> dict:
        """
        Calcule la taxe pour un montant et un état donnés
        
        Args:
            amount: Le montant sur lequel appliquer la taxe
            state: Le code de l'état (ex: "CA" pour California)
            
        Returns:
            Dict contenant les détails du calcul
            
        Raises:
            InvalidStateError: Si l'état n'existe pas
            StateNotSupportedError: Si l'état n'est pas supporté
            CalculationError: Si une erreur survient pendant le calcul
        """
        try:
            # Validation de l'état
            state_enum = self.validate_state(state)
            
            # Validation du montant
            if amount < 0:
                raise ValueError("Le montant ne peut pas être négatif")
            
            # Arrondir le montant à 2 décimales
            amount = round(amount, 2)
            
            tax_rate = self.get_tax_rate(state_enum)
            if not tax_rate:
                raise StateNotSupportedError(state)

            # Calcul de la taxe
            tax_amount = round(amount * (tax_rate.rate / 100), 2)
            final_amount = round(amount + tax_amount, 2)

            calculation_details = [
                f"1. Montant de base : {amount}€",
                f"2. État {state} - Taux de taxe : {tax_rate.rate}%",
                f"3. Calcul de la taxe : {amount}€ × {tax_rate.rate}% = {tax_amount}€",
                f"4. Montant final : {amount}€ + {tax_amount}€ = {final_amount}€"
            ]

            return {
                "original_amount": amount,
                "state": state,
                "tax_rate": tax_rate.rate,
                "tax_amount": tax_amount,
                "final_amount": final_amount,
                "tax_description": f"Taxe de vente {state} ({tax_rate.rate}%)",
                "calculation_details": calculation_details
            }
            
        except ValueError as e:
            raise CalculationError(
                str(e),
                {"amount": amount, "state": state}
            )
        except (InvalidStateError, StateNotSupportedError):
            raise
        except Exception as e:
            raise CalculationError(
                "Erreur inattendue lors du calcul de la taxe",
                {"amount": amount, "state": state, "error": str(e)}
            )
