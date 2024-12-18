"""Views for Cart App."""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from products.models import Product
from cart.models import Cart, Wishlist, CartItem
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

def _cart_id(request):
    cart = request.session.session_key
    if not cart :
        cart = request.session.create()
    return cart



def cart(request):
    """Render the cart view and wishlist view."""
    """
    When user is in logged in then use user id
    Otherwise use session id
    """
    cart_items = []
    wishlist = []
    wishlist_count = 0
    if request.user.is_authenticated:
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        wishlist, created = Wishlist.objects.get_or_create(user=user)
        cart_items = cart.cart_items.all()
        wishlist_count = wishlist.products.count()
    else:
        session_cart = request.session.get("cart", {})
        product_ids = session_cart.keys()
        cart_items = Product.objects.filter(id__in=product_ids)

    return render(
        request,
        "cart/cart.html",
        {
            "cart_items": cart_items,
            "wishlist": wishlist,
            "wishlist_count": wishlist_count,
        },
    )


@login_required
def add_prod_cart(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.add_to_cart()
    return redirect("cart:cart")


@login_required
def remove_prod_cart(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=user)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.remove_from_cart()
    return redirect("cart:cart")


@login_required
def subtract_prod_cart(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=user)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.subtract_from_cart()
    return redirect("cart:cart")


@login_required
def clear_cart(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    cart.clear_cart()
    return redirect("cart:cart")


@login_required
def add_prod_wishlist(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=user)
    wishlist.add_product(product)
    return redirect("cart:cart")


@login_required
def remove_prod_wishlist(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=user)
    wishlist.remove_product(product)
    return redirect("cart:cart")




"""Ajax cart functionalities
"""

def add_to_cart(request):
    user = request.user
    if user.is_authenticated:
        return JsonResponse({'error': 'You need to login to add products to the cart.'}, status=401)

    product_id = request.POST.get('product_id')
    if not product_id:
        return JsonResponse({'error': 'Invalid product ID.'}, status=400)

    product = get_object_or_404(Product, id=product_id)
    # product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.add_to_cart()
    cart_items_count_list = sum(item.quantity for item in cart.cart_items.all())
    # print("cart_item :", cart_items_count_list)
    return JsonResponse({'message': f'{product.title} added to cart!', "totalCartItems" : cart_items_count_list})


def get_cart(request):
    user = request.user
    # session_key = request.session.session_key
    cart_items = Cart.objects.filter(user=user)
    # print(cart_items)
    return render(request, 'cart/cart_modal.html', {'cart_items': cart_items})
