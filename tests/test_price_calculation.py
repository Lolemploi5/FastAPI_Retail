import pytest
from decimal import Decimal
from app.price_calculator import PriceCalculator
from app.models import ProductInput
from app.tax import State

class TestPriceCalculation:
    """Tests pour le calcul du prix brut"""

    @pytest.fixture
    def calculator(self):
        """Fixture pour le calculateur de prix"""
        return PriceCalculator()

    @pytest.mark.parametrize("quantity, unit_price, expected_total", [
        (1, 100.00, 100.00),
        (2, 99.99, 199.98),
        (5, 10.00, 50.00),
        (10, 1.99, 19.90),
        (100, 0.50, 50.00),
    ])
    def test_basic_price_calculation(self, calculator, quantity, unit_price, expected_total):
        """Test le calcul de base du prix brut"""
        result = calculator.calculate_final_price(
            quantity=quantity,
            unit_price=unit_price,
            state="CA"
        )
        assert abs(result.subtotal - expected_total) < 0.01, \
            f"Le prix brut calculé {result.subtotal} ne correspond pas au résultat attendu {expected_total}"

    def test_zero_quantity(self, calculator):
        """Test avec une quantité de zéro"""
        with pytest.raises(ValueError) as exc_info:
            calculator.calculate_final_price(
                quantity=0,
                unit_price=100.00,
                state="CA"
            )
        assert "positif" in str(exc_info.value).lower()

    def test_negative_quantity(self, calculator):
        """Test avec une quantité négative"""
        with pytest.raises(ValueError) as exc_info:
            calculator.calculate_final_price(
                quantity=-1,
                unit_price=100.00,
                state="CA"
            )
        assert "positif" in str(exc_info.value).lower()

    def test_zero_price(self, calculator):
        """Test avec un prix unitaire de zéro"""
        with pytest.raises(ValueError) as exc_info:
            calculator.calculate_final_price(
                quantity=1,
                unit_price=0,
                state="CA"
            )
        assert "positif" in str(exc_info.value).lower()

    def test_negative_price(self, calculator):
        """Test avec un prix unitaire négatif"""
        with pytest.raises(ValueError) as exc_info:
            calculator.calculate_final_price(
                quantity=1,
                unit_price=-10.00,
                state="CA"
            )
        assert "positif" in str(exc_info.value).lower()

    def test_large_numbers(self, calculator):
        """Test avec de grands nombres"""
        result = calculator.calculate_final_price(
            quantity=999,
            unit_price=9999.99,
            state="CA"
        )
        expected = 999 * 9999.99
        assert abs(result.subtotal - expected) < 0.01, \
            f"Le calcul avec de grands nombres a échoué. Attendu: {expected}, Obtenu: {result.subtotal}"

    def test_precision(self, calculator):
        """Test la précision des calculs avec des nombres décimaux"""
        test_cases = [
            (3, 1.99, 5.97),
            (7, 3.33, 23.31),
            (2, 4.999, 10.00),  # Devrait être arrondi à 10.00
        ]
        
        for quantity, price, expected in test_cases:
            result = calculator.calculate_final_price(
                quantity=quantity,
                unit_price=price,
                state="CA"
            )
            assert abs(result.subtotal - expected) < 0.01, \
                f"Erreur de précision. Attendu: {expected}, Obtenu: {result.subtotal}"

    def test_max_values(self, calculator):
        """Test les valeurs maximales autorisées"""
        # Test avec le montant maximum autorisé
        result = calculator.calculate_final_price(
            quantity=100,
            unit_price=99999.99,
            state="CA"
        )
        assert result.subtotal <= 10000000, "Le montant total dépasse la limite maximale"

        # Test avec un montant qui dépasse la limite
        with pytest.raises(ValueError) as exc_info:
            calculator.calculate_final_price(
                quantity=1000,
                unit_price=99999.99,
                state="CA"
            )
        assert "10 millions" in str(exc_info.value)
