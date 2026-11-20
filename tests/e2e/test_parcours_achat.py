"""Test E2E Playwright — POINT DE DÉPART (Atelier 8).

Prérequis : application lancée (make run) ; BASE_URL=http://localhost:8000 par défaut.
Lancer :   pytest -m e2e --headed        (pour voir le navigateur)
"""

import re

import pytest
from playwright.sync_api import Page, expect

from tests.e2e.shop_page import ShopPage

pytestmark = pytest.mark.e2e


@pytest.fixture
def shop(page: Page, app_url) -> ShopPage:
    """Ouvre la boutique (catalogue chargé) et retourne le Page Object."""
    return ShopPage(page, app_url).open()


def test_page_accueil(page: Page, app_url):
    page.goto(app_url)
    expect(page).to_have_title(re.compile("MiniShop"))
    expect(page.get_by_test_id("products").locator("li")).to_have_count(5)


def test_parcours_achat_complet(shop: ShopPage):
    # 2 mugs à 12.50 = 25.00 ; WELCOME10 = -2.50 ; livraison 4.90 -> 27.40
    shop.add("mug", qty=2)
    expect(shop.cart_line("mug")).to_contain_text("× 2")

    shop.apply_coupon("WELCOME10")
    expect(shop.subtotal).to_have_text("25.00")
    expect(shop.discount).to_have_text("2.50")
    expect(shop.shipping).to_have_text("4.90")
    expect(shop.total()).to_have_text("27.40")

    shop.order()
    expect(shop.confirmation).to_have_text(re.compile(r"Commande .+ confirmée"))


def test_coupon_invalide_affiche_une_erreur(shop: ShopPage):
    shop.add("mug")
    shop.apply_coupon("PASVALIDE")

    expect(shop.error).to_be_visible()
    expect(shop.error).to_contain_text("Coupon inconnu")
    expect(shop.summary).to_be_hidden()


def test_commander_desactive_tant_que_panier_vide(shop: ShopPage):
    expect(shop.order_button).to_be_disabled()

    shop.add("mug")
    expect(shop.order_button).to_be_enabled()
