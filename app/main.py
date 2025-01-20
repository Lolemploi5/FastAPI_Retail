from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional, List, Dict, Any
from .models import ProductInput, ProductOutput
from .price_calculator import PriceCalculator
from .exceptions import CalculationError, InvalidStateError, StateNotSupportedError
from datetime import datetime

app = FastAPI(
    title="FastAPI Retail",
    description="API de gestion des prix pour le retail",
    version="1.0.0"
)

price_calculator = PriceCalculator()

@app.exception_handler(CalculationError)
async def calculation_error_handler(request, exc: CalculationError):
    return JSONResponse(
        status_code=400,
        content={
            "error": "Erreur de calcul",
            "message": str(exc),
            "details": exc.details
        }
    )

@app.exception_handler(InvalidStateError)
async def invalid_state_error_handler(request, exc: InvalidStateError):
    return JSONResponse(
        status_code=400,
        content={
            "error": "État invalide",
            "message": str(exc)
        }
    )

@app.exception_handler(StateNotSupportedError)
async def state_not_supported_error_handler(request, exc: StateNotSupportedError):
    return JSONResponse(
        status_code=400,
        content={
            "error": "État non supporté",
            "message": str(exc)
        }
    )

@app.post("/products/", response_model=ProductOutput)
async def create_product(product: ProductInput):
    return ProductOutput(
        **product.model_dump(),
        id=1,
        created_at=datetime.now()
    )

@app.post("/calculate-total/")
async def calculate_total(
    quantity: int = Query(..., gt=0, description="Quantité de produits"),
    unit_price: float = Query(..., gt=0, description="Prix unitaire"),
    state: str = Query(..., min_length=2, max_length=2, description="Code de l'état (ex: CA)")
) -> Dict[str, Any]:
    try:
        result = price_calculator.calculate_final_price(
            quantity=quantity,
            unit_price=unit_price,
            state=state
        )
        
        return {
            "subtotal": result.subtotal,
            "discount_percentage": result.discount_percentage,
            "discount_amount": result.discount_amount,
            "price_after_discount": result.price_after_discount,
            "tax_rate": result.tax_rate,
            "tax_amount": result.tax_amount,
            "final_price": result.final_price,
            "calculation_details": result.calculation_steps
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
