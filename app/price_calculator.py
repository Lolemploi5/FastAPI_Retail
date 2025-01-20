from dataclasses import dataclass
from typing import List
from decimal import Decimal
from .tax import TaxCalculator
from .discount import DiscountCalculator
from .exceptions import CalculationError

@dataclass
class PriceBreakdown:
    """Structure pour stocker les détails du calcul de prix"""
    subtotal: float
    discount_percentage: float
    discount_amount: float
    price_after_discount: float
    tax_rate: float
    tax_amount: float
    final_price: float
    tax_description: str
    calculation_steps: List[str]

class PriceCalculator:
    """Calculateur de prix avec remise et taxes"""
    
    def __init__(self):
        self.tax_calculator = TaxCalculator()
        self.discount_calculator = DiscountCalculator()
        self.MAX_QUANTITY = 10000
        self.MAX_UNIT_PRICE = 1000000
        self.MAX_TOTAL = 10000000

    def validate_inputs(self, quantity: int, unit_price: float) -> None:
        """
        Valide les entrées du calculateur
        
        Raises:
            ValueError: Si les entrées sont invalides
        """
        if quantity <= 0:
            raise ValueError("La quantité doit être un nombre positif")
            
        if unit_price <= 0:
            raise ValueError("Le prix unitaire doit être un nombre positif")
            
        if quantity > self.MAX_QUANTITY:
            raise ValueError(f"La quantité ne peut pas dépasser {self.MAX_QUANTITY}")
            
        if unit_price > self.MAX_UNIT_PRICE:
            raise ValueError(f"Le prix unitaire ne peut pas dépasser {self.MAX_UNIT_PRICE}€")
            
        total = quantity * unit_price
        if total > self.MAX_TOTAL:
            raise ValueError(f"Le montant total ne peut pas dépasser 10 millions €")

    def calculate_final_price(
        self,
        quantity: int,
        unit_price: float,
        state: str
    ) -> PriceBreakdown:
        """
        Calcule le prix final avec remise et taxes
        
        Args:
            quantity: Quantité de produits
            unit_price: Prix unitaire
            state: État pour le calcul des taxes
            
        Returns:
            PriceBreakdown contenant tous les détails du calcul
            
        Raises:
            ValueError: Si les entrées sont invalides
            CalculationError: Si une erreur survient pendant le calcul
        """
        try:
            # Validation des entrées
            self.validate_inputs(quantity, unit_price)
            
            # Calcul du sous-total
            subtotal = round(quantity * unit_price, 2)
            
            # Calcul de la remise
            discount_info = self.discount_calculator.calculate_discount(subtotal)
            price_after_discount = discount_info["final_amount"]
            
            # Calcul de la taxe
            tax_info = self.tax_calculator.calculate_tax(price_after_discount, state)
            
            return PriceBreakdown(
                subtotal=subtotal,
                discount_percentage=discount_info["discount_percentage"],
                discount_amount=discount_info["discount_amount"],
                price_after_discount=price_after_discount,
                tax_rate=tax_info["tax_rate"],
                tax_amount=tax_info["tax_amount"],
                final_price=tax_info["final_amount"],
                tax_description=tax_info["tax_description"],
                calculation_steps=tax_info["calculation_details"]
            )
            
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise CalculationError(
                str(e),
                {
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "state": state
                }
            )
