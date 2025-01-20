from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from enum import Enum
from decimal import Decimal

class FormatType(str, Enum):
    TEXT = "text"
    HTML = "html"
    JSON = "json"

@dataclass
class PriceDetails:
    """Structure pour stocker les détails du prix"""
    product_name: str
    quantity: int
    unit_price: float
    subtotal: float
    discount_percentage: float
    discount_amount: float
    price_after_discount: float
    state: str
    tax_rate: float
    tax_amount: float
    final_price: float
    calculation_steps: List[str]

class PriceFormatter:
    """Classe pour formater l'affichage des prix"""
    
    @staticmethod
    def format_currency(amount: float) -> str:
        """Formate un montant en devise"""
        return f"{amount:,.2f}€"

    @staticmethod
    def format_percentage(value: float) -> str:
        """Formate un pourcentage"""
        return f"{value:.1f}%"

    def format_text(self, details: PriceDetails) -> str:
        """Formate les détails du prix en texte"""
        lines = [
            "┌─────────────────────────────────────────────────────┐",
            f"│ Détails du prix pour : {details.product_name:<29} │",
            "├─────────────────────────────────────────────────────┤",
            f"│ Quantité : {details.quantity:<39} │",
            f"│ Prix unitaire : {self.format_currency(details.unit_price):<33} │",
            "├─────────────────────────────────────────────────────┤",
            f"│ Sous-total : {self.format_currency(details.subtotal):<35} │",
            "│                                                     │",
            f"│ Remise ({self.format_percentage(details.discount_percentage):<6}) : -{self.format_currency(details.discount_amount):<27} │",
            f"│ Prix après remise : {self.format_currency(details.price_after_discount):<29} │",
            "│                                                     │",
            f"│ Taxe {details.state} ({self.format_percentage(details.tax_rate):<6}) : {self.format_currency(details.tax_amount):<26} │",
            "├─────────────────────────────────────────────────────┤",
            f"│ Prix final : {self.format_currency(details.final_price):<36} │",
            "└─────────────────────────────────────────────────────┘",
            "",
            "Détails du calcul :",
            "----------------"
        ]
        lines.extend(details.calculation_steps)
        return "\n".join(lines)

    def format_html(self, details: PriceDetails) -> str:
        """Formate les détails du prix en HTML"""
        return f"""
        <div class="price-details" style="font-family: Arial, sans-serif; max-width: 600px; margin: 20px auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h2 style="color: #333; margin-bottom: 20px;">Détails du prix pour : {details.product_name}</h2>
            
            <div class="basic-info" style="background: #f9f9f9; padding: 15px; border-radius: 4px; margin-bottom: 20px;">
                <p style="margin: 5px 0;">Quantité : {details.quantity}</p>
                <p style="margin: 5px 0;">Prix unitaire : {self.format_currency(details.unit_price)}</p>
            </div>
            
            <div class="calculations" style="margin-bottom: 20px;">
                <p style="font-size: 1.1em; color: #666;">Sous-total : {self.format_currency(details.subtotal)}</p>
                
                <div class="discount" style="background: #e8f4f8; padding: 10px; border-radius: 4px; margin: 10px 0;">
                    <p style="color: #2980b9; margin: 5px 0;">
                        Remise ({self.format_percentage(details.discount_percentage)}) : 
                        <span style="color: #c0392b;">-{self.format_currency(details.discount_amount)}</span>
                    </p>
                    <p style="margin: 5px 0;">Prix après remise : {self.format_currency(details.price_after_discount)}</p>
                </div>
                
                <div class="tax" style="background: #fdf7e3; padding: 10px; border-radius: 4px; margin: 10px 0;">
                    <p style="color: #d35400; margin: 5px 0;">
                        Taxe {details.state} ({self.format_percentage(details.tax_rate)}) : 
                        {self.format_currency(details.tax_amount)}
                    </p>
                </div>
            </div>
            
            <div class="final-price" style="background: #27ae60; color: white; padding: 15px; border-radius: 4px; text-align: right;">
                <p style="font-size: 1.2em; margin: 0;">Prix final : {self.format_currency(details.final_price)}</p>
            </div>
            
            <div class="calculation-steps" style="margin-top: 20px; padding: 15px; background: #f5f6fa; border-radius: 4px;">
                <h3 style="color: #333; margin-bottom: 10px;">Détails du calcul :</h3>
                <ul style="list-style-type: none; padding: 0; margin: 0;">
                    {chr(10).join(f'<li style="margin: 5px 0; color: #666;">{step}</li>' for step in details.calculation_steps)}
                </ul>
            </div>
        </div>
        """

    def format_json(self, details: PriceDetails) -> Dict[str, Any]:
        """Formate les détails du prix en JSON"""
        return {
            "product": {
                "name": details.product_name,
                "quantity": details.quantity,
                "unit_price": details.unit_price
            },
            "pricing": {
                "subtotal": details.subtotal,
                "discount": {
                    "percentage": details.discount_percentage,
                    "amount": details.discount_amount,
                    "price_after_discount": details.price_after_discount
                },
                "tax": {
                    "state": details.state,
                    "rate": details.tax_rate,
                    "amount": details.tax_amount
                },
                "final_price": details.final_price
            },
            "calculation_steps": details.calculation_steps,
            "formatted_amounts": {
                "unit_price": self.format_currency(details.unit_price),
                "subtotal": self.format_currency(details.subtotal),
                "discount": self.format_currency(details.discount_amount),
                "tax": self.format_currency(details.tax_amount),
                "final_price": self.format_currency(details.final_price)
            }
        }

    def format_price_details(
        self, 
        details: PriceDetails, 
        format_type: FormatType = FormatType.TEXT
    ) -> Any:
        """
        Formate les détails du prix selon le format spécifié
        
        Args:
            details: Les détails du prix à formater
            format_type: Le type de format souhaité (text, html, json)
            
        Returns:
            Les détails formatés dans le format demandé
        """
        format_methods = {
            FormatType.TEXT: self.format_text,
            FormatType.HTML: self.format_html,
            FormatType.JSON: self.format_json
        }
        
        formatter = format_methods.get(format_type)
        if not formatter:
            raise ValueError(f"Format non supporté : {format_type}")
            
        return formatter(details)
