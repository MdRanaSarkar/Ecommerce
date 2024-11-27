"""Models for Cart App."""

from django.db import models
from users.models import CustomUser
from products.models import Product


class Cart(models.Model):
    """Model definition for Cart."""

    user = models.ForeignKey(CustomUser,
                                null=True,          # Allows the cart to exist without a user (session-based)
                                blank=True,
                                on_delete=models.CASCADE)
    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        unique=True         # Ensure each session has one cart
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_updated"]
        verbose_name = "cart"
        verbose_name_plural = "cart"
        app_label = "cart"

    def __str__(self):
        if self.user:
            return f"{self.user.username}"
        return f"{self.session_key}"

    def clear_cart(self):
        self.cart_items.all().delete()


class CartItem(models.Model):
    """Model definition for CartItem."""

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["cart"]
        verbose_name = "cart item"
        verbose_name_plural = "cart items"
        app_label = "cart"

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

    def add_to_cart(self, quantity=1):
        self.quantity += quantity
        self.save()

    def remove_from_cart(self):
        self.delete()

    def subtract_from_cart(self):
        if self.quantity > 1:
            self.quantity -= 1
            self.save()
        else:
            self.remove_from_cart()

    def total_price(self):
        """Calculate the total price for this item."""
        return self.product.normal_price * self.quantity


class Wishlist(models.Model):
    """Model definition for Wishlist."""

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["user"]
        verbose_name = "wishlist"
        verbose_name_plural = "wishlist"
        app_label = "cart"

    def __str__(self):
        total_products = self.products.count()
        return f"{self.user.username} ({total_products} prods)"

    def add_product(self, product):
        self.products.add(product)

    def remove_product(self, product):
        self.products.remove(product)
