"""Admin for Cart App."""

from django.contrib import admin

from cart.models import Cart, Wishlist, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin config for Cart model."""
    list_display = ('user', 'date_created')  # Include customer name
    search_fields = ("user",)
    list_filter = ('date_created',)
    list_per_page = 25
    readonly_fields = ("pk",)
    ordering = ("pk",)
    def customer_name(self, obj):
        """Returns the full name of the user."""
        return f"{obj.user.first_name} {obj.user.last_name}"  # Assuming the user model has first_name and last_name fields
    customer_name.short_description = 'Customer Name'  # Custom header for the column




@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Admin config for CartItem model."""
    list_display = ('cart', 'product', 'date_created')
    search_fields = ("cart",)
    list_per_page = 25
    readonly_fields = ("cart", "product", "quantity")
    ordering = ("pk",)

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    """Admin config for Wishlist model."""
    list_display = ('get_product_count', 'user',  'date_created')
    search_fields = ("user",)
    list_per_page = 25
    readonly_fields = ("pk",)
    ordering = ("pk",)
    list_filter = ('date_created',)

    def get_product_count(self, obj):
        """Returns the count of products in the wishlist."""
        return obj.products.count()  # Count the number of products in the wishlist
    get_product_count.short_description = 'Number of Products'
