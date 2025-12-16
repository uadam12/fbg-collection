from typing import Dict, List
from django.http import HttpRequest
from cap.models import Cap

cap_cat_qs = Cap.objects.select_related("category")

class Cart:
    SESSION_KEY = "cart"

    def __init__(self, request: HttpRequest):
        self.session = request.session
        self.cart: Dict[str, int] = self.session.get(self.SESSION_KEY, {})
        self._items: List[dict] | None = None

        # Ensure cart exists in session
        self.session[self.SESSION_KEY] = self.cart

    # --------------------
    # Core operations
    # --------------------
    def add(self, cap_id: int | str, quantity: int = 1) -> None:
        cap_id = str(cap_id)
        self.cart[cap_id] = max(1, quantity)
        self._invalidate()
        self._save()

    def remove(self, cap_id: int | str) -> None:
        cap_id = str(cap_id)
        if cap_id in self.cart:
            del self.cart[cap_id]
            self._invalidate()
            self._save()

    def toggle(self, cap_id: int | str) -> None:
        cap_id = str(cap_id)
        if cap_id in self.cart:
            self.remove(cap_id)
        else:
            self.add(cap_id)

    def increase(self, cap_id: int | str, step: int = 1) -> None:
        cap_id = str(cap_id)
        self.cart[cap_id] = self.cart.get(cap_id, 0) + max(1, step)
        self._invalidate()
        self._save()

    def decrease(self, cap_id: int | str, step: int = 1) -> None:
        cap_id = str(cap_id)
        if cap_id not in self.cart:
            return

        new_qty = self.cart[cap_id] - max(1, step)
        if new_qty > 0:
            self.cart[cap_id] = new_qty

        self._invalidate()
        self._save()

    def clear(self) -> None:
        self.cart.clear()
        self._invalidate()
        self._save()

    # --------------------
    # Derived data
    # --------------------
    def get_item(self, cap: Cap) -> dict:
        return {
            "cap": cap,
            "quantity": (qty := self.cart[str(cap.id)]),
            "unit_price": cap.price,
            "amount": cap.price * qty,
        }

    def _build_items(self) -> None:
        cap_ids = self.cart.keys()
        caps = cap_cat_qs.filter(id__in=cap_ids)
        self._items = [self.get_item(cap) for cap in caps]

    @property
    def items(self) -> List[dict]:
        if self._items is None:
            self._build_items()
        return self._items

    @property
    def items_count(self) -> int:
        return len(self.cart)

    @property
    def total_amount(self) -> int:
        return sum(item["amount"] for item in self.items)

    # --------------------
    # Internals
    # --------------------
    def _invalidate(self) -> None:
        self._items = None

    def _save(self) -> None:
        self.session[self.SESSION_KEY] = self.cart
        self.session.modified = True
