from dataclasses import dataclass
from typing import List

@dataclass
class DiscountRule:
    min_amount: float
    discount_percentage: float
    description: str

class DiscountCalculator:
    def __init__(self):
        self.discount_rules: List[DiscountRule] = [
            DiscountRule(100, 5, "5% de remise pour les achats de plus de 100€"),
            DiscountRule(500, 10, "10% de remise pour les achats de plus de 500€"),
            DiscountRule(1000, 15, "15% de remise pour les achats de plus de 1000€"),
            DiscountRule(5000, 20, "20% de remise pour les achats de plus de 5000€")
        ]

    def get_applicable_discount(self, total_amount: float) -> DiscountRule:
        """Retourne la règle de remise la plus avantageuse pour un montant donné"""
        applicable_rules = [rule for rule in self.discount_rules 
                          if total_amount >= rule.min_amount]
        return max(applicable_rules, key=lambda x: x.discount_percentage) if applicable_rules else None

    def calculate_discount(self, total_amount: float) -> dict:
        """Calcule la remise applicable pour un montant donné"""
        discount_rule = self.get_applicable_discount(total_amount)
        
        if not discount_rule:
            return {
                "original_amount": total_amount,
                "discount_percentage": 0,
                "discount_amount": 0,
                "final_amount": total_amount,
                "discount_description": "Aucune remise applicable"
            }

        discount_amount = total_amount * (discount_rule.discount_percentage / 100)
        final_amount = total_amount - discount_amount

        return {
            "original_amount": total_amount,
            "discount_percentage": discount_rule.discount_percentage,
            "discount_amount": round(discount_amount, 2),
            "final_amount": round(final_amount, 2),
            "discount_description": discount_rule.description
        }
