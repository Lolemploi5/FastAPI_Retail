from enum import Enum
from pydantic import BaseModel, Field, PositiveFloat, PositiveInt, validator, model_validator
from typing import Optional
from datetime import datetime
from .tax import State
from decimal import Decimal

class ProductState(str, Enum):
    NEW = "new"
    USED = "used"
    REFURBISHED = "refurbished"
    DAMAGED = "damaged"

class ProductInput(BaseModel):
    name: str = Field(
        ..., 
        min_length=1, 
        max_length=100, 
        description="Nom du produit",
        examples=["Ordinateur portable XPS 13"]
    )
    quantity: PositiveInt = Field(
        ..., 
        description="Quantité en stock",
        examples=[1],
        gt=0,
        le=10000
    )
    unit_price: PositiveFloat = Field(
        ..., 
        description="Prix unitaire",
        examples=[999.99],
        gt=0,
        le=1000000
    )
    state: State = Field(
        ..., 
        description="État pour le calcul des taxes",
        examples=["CA"]
    )
    product_state: ProductState = Field(
        ..., 
        description="État du produit",
        examples=["new"]
    )
    description: Optional[str] = Field(
        None, 
        max_length=500, 
        description="Description du produit",
        examples=["Ordinateur portable dernière génération"]
    )

    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Le nom du produit ne peut pas être vide ou contenir uniquement des espaces")
        return v.strip()

    @validator('unit_price')
    def validate_price(cls, v):
        # Convertir en Decimal pour une précision exacte
        price = Decimal(str(v))
        if price.as_tuple().exponent < -2:
            raise ValueError("Le prix ne peut pas avoir plus de 2 décimales")
        return float(price)

    @model_validator(mode='after')
    def validate_total_amount(self):
        """Valide que le montant total ne dépasse pas les limites raisonnables"""
        total = self.quantity * self.unit_price
        if total > 10000000:  # 10 millions
            raise ValueError(
                "Le montant total (quantité × prix unitaire) ne peut pas dépasser 10 millions"
            )
        return self

class ProductOutput(ProductInput):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    total_price: float = Field(..., description="Prix total brut (quantité × prix unitaire)")
    discount_percentage: float = Field(0, description="Pourcentage de remise appliqué")
    discount_amount: float = Field(0, description="Montant de la remise")
    tax_rate: float = Field(..., description="Taux de taxe appliqué")
    tax_amount: float = Field(..., description="Montant de la taxe")
    final_price: float = Field(..., description="Prix final après remise et taxes")
    tax_description: str = Field("", description="Description de la taxe appliquée")

    @validator('total_price', 'discount_amount', 'tax_amount', 'final_price')
    def validate_amounts(cls, v):
        # Convertir en Decimal pour une précision exacte
        amount = Decimal(str(v))
        if amount.as_tuple().exponent < -2:
            raise ValueError("Les montants ne peuvent pas avoir plus de 2 décimales")
        return float(amount)

    @model_validator(mode='after')
    def validate_calculations(self):
        """Valide que les calculs sont cohérents"""
        # Vérifier que le total brut est correct
        expected_total = self.quantity * self.unit_price
        if abs(self.total_price - expected_total) > 0.01:
            raise ValueError("Le prix total brut ne correspond pas à (quantité × prix unitaire)")

        # Vérifier que le prix final est cohérent
        expected_final = self.total_price - self.discount_amount + self.tax_amount
        if abs(self.final_price - expected_final) > 0.01:
            raise ValueError("Le prix final ne correspond pas au calcul attendu")

        return self
