"""Page Object de MiniShop : les tests parlent métier, les localisateurs restent ici."""

from playwright.sync_api import Locator, Page, expect


class ShopPage:
    def __init__(self, page: Page, url: str):
        self.page = page
        self.url = url
        # Seul endroit où apparaissent les localisateurs
        self.coupon_input = page.get_by_label("Code promo")
        self.quote_button = page.get_by_role("button", name="Calculer le total")
        self.order_button = page.get_by_role("button", name="Commander")
        self.summary = page.get_by_test_id("summary")
        self.subtotal = page.get_by_test_id("subtotal")
        self.discount = page.get_by_test_id("discount")
        self.shipping = page.get_by_test_id("shipping")
        self.total_amount = page.get_by_test_id("total")
        self.error = page.get_by_role("alert")
        self.confirmation = page.get_by_test_id("confirmation")

    def open(self) -> "ShopPage":
        self.page.goto(self.url)
        expect(self.page.get_by_test_id("add-mug")).to_be_visible()  # catalogue chargé
        return self

    def add(self, product: str, qty: int = 1) -> None:
        for _ in range(qty):
            self.page.get_by_test_id(f"add-{product}").click()

    def cart_line(self, product: str) -> Locator:
        return self.page.get_by_test_id(f"cart-{product}")

    def apply_coupon(self, code: str) -> None:
        self.coupon_input.fill(code)
        self.quote_button.click()

    def total(self) -> Locator:
        # Localisateur (pas le texte) pour garder l'attente automatique d'expect
        return self.total_amount

    def order(self) -> None:
        self.order_button.click()
