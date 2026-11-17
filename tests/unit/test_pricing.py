"""Tests unitaires des règles de prix — POINT DE DÉPART (Atelier 1).

Complétez ce fichier : objectif >= 90 % de couverture sur minishop/pricing.py.
"""

from decimal import Decimal

import pytest

from minishop.catalog import get_product
from minishop.pricing import coupon_discount, line_total, money, quote, shipping_cost

pytestmark = pytest.mark.unit


def test_money_arrondi_commercial():
    """0.125 s'arrondit à 0.13 (ROUND_HALF_UP), pas 0.12."""
    assert money("0.125") == Decimal("0.13")


def test_line_total_sans_remise():
    assert line_total(Decimal("12.50"), 2) == Decimal("25.00")


def test_quote_panier_vide():
    """Un panier vide coûte 0 € : pas de frais de livraison."""
    q = quote([])
    assert q.total == Decimal("0.00")
    assert q.shipping == Decimal("0.00")


@pytest.mark.parametrize("qty, expected", [(10, Decimal("9.50")), (9, Decimal("9.00"))])
def test_line_total_avec_remise(qty, expected):
    """Remise volume à partir de 10 unités (et pas à 9 !)."""
    unit_price = 1
    assert line_total(Decimal(unit_price), qty) == expected


@pytest.mark.parametrize("qty", [0, -1, 100, "2", True])
def test_quantite_invalide(qty):
    """Quantités invalides -> ValueError."""
    with pytest.raises(ValueError):
        line_total(Decimal("10"), qty)


@pytest.mark.parametrize(
    "coupon, subtotal, expected",
    [
        ("WELCOME10", 15, Decimal(0)),
        ("WELCOME10", 50, Decimal(50 * 0.1)),
        ("FIXED5", 50, Decimal(5)),
        ("FREESHIP", 50, Decimal(0)),
    ],
)
def test_coupon_discount(coupon, subtotal, expected):
    """Coupons WELCOME10 / FIXED5 / FREESHIP (seuils inclus/exclus)."""
    assert coupon_discount(subtotal, coupon) == expected


def test_coupon_inconnu():
    with pytest.raises(ValueError, match="Coupon inconnu"):
        coupon_discount(Decimal(50), "AZOIDJAZIODJA")


@pytest.mark.parametrize(
    "amount, coupon, empty, expected",
    [
        (Decimal(50), "WELCOME10", False, Decimal("0")),
        (Decimal(10), None, False, Decimal("4.90")),
        (Decimal(10), None, True, Decimal("0")),
        (Decimal(10), "FREESHIP", False, Decimal("0")),
    ],
)
def test_shipping_cost(amount, coupon, empty, expected):
    """Livraison offerte à partir de 50 € APRÈS remise."""
    assert shipping_cost(amount, coupon, empty) == expected


@pytest.mark.parametrize("product", ["test", 54, True])
def test_produit_inconnu(product):
    """Produit inconnu -> KeyError."""
    with pytest.raises(KeyError):
        get_product(product)
