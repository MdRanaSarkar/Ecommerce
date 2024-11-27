"""Views for Cart App."""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from products.models import Product
from cart.models import Cart, Wishlist, CartItem
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.sessions.models import Session

def _cart_session_id(request):
    if not request.session.session_key:
        request.session.create()  # Create a new session if none exists
        request.session.save()
    return request.session.session_key  # Return the session key directly


# Create Cart for user and non user based on session id
def get_cart_with_user_or_session(request):
    """Retrieve or create a cart based on the user or session."""
    if request.user.is_authenticated:
        # Authenticated user: use user-based cart
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        # Anonymous user: use session-based cart
        session_key = _cart_session_id(request)
        cart, _ = Cart.objects.get_or_create(session_key=session_key)

    return cart

def get_wishlist_with_user_or_session(request):
    """Retrieve or create a cart based on the user or session."""
    wishlist  = []
    wishlist_count = 0
    if request.user.is_authenticated:
        # Authenticated user: use user-based cart
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        wishlist_count = wishlist.products.count()
    return wishlist, wishlist_count


def cart(request):
    """Render the cart view and wishlist view."""
    """
    When user is in logged in then use user id
    Otherwise use session id
    """
    cart_items = []
    wishlist = []
    wishlist_count = 0
    cart = get_cart_with_user_or_session(request)
    cart_items = cart.cart_items.all()
    wishlist, wishlist_count = get_wishlist_with_user_or_session(request)

    total_subtotal = sum(
        item.total_price() if callable(item.total_price) else item.total_price
        for item in cart_items
    )

    print(total_subtotal)

    return render(
        request,
        "cart/cart.html",
        {
            "cart_items": cart_items,
            "total_subtotal" : total_subtotal,
            "wishlist": wishlist,
            "wishlist_count": wishlist_count,
        },
    )



def add_prod_cart(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    cart = get_cart_with_user_or_session(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.add_to_cart()
    return redirect("cart:cart")



def remove_prod_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = get_cart_with_user_or_session(request)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.remove_from_cart()
    return redirect("cart:cart")



def subtract_prod_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart_with_user_or_session(request)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    cart_item.subtract_from_cart()
    return redirect("cart:cart")



def clear_cart(request):
    cart = get_cart_with_user_or_session(request)
    cart.clear_cart()
    return redirect("cart:cart")


"""Ajax cart functionalities
"""

def add_to_cart(request):
    session_key = _cart_session_id(request)  # Ensure the session is initialized
    print("Session Key (add_to_cart):", session_key)  # Optional for debugging
    product_id = request.POST.get('product_id')
    if not product_id:
        return JsonResponse({'error': 'Invalid product ID.'}, status=400)
    print("product_id", product_id)
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart_with_user_or_session(request)
    # Check if the item already exists in the cart
    cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.add_to_cart()
    cart_items_count_list = sum(item.quantity for item in cart.cart_items.all())
    return JsonResponse({'message': f'{product.title} added to cart!', "totalCartItems" : cart_items_count_list})


def get_cart(request):
    user = request.user
    # session_key = request.session.session_key
    cart_items = get_cart_with_user_or_session(request)
    print(cart_items)
    return render(request, 'cart/cart_modal.html', {'cart_items': cart_items})




@receiver(user_logged_in)
def transfer_cart_to_user(sender, request, user, **kwargs):
    print("Sending transfer", sender)
    session_key = request.session.session_key  # Get the session key
    print("Transfer Sessions to user", session_key)
    session_cart, _ = Cart.objects.get_or_create(session_key=session_key)

    print("Session Cart", session_cart)
    cart_items = session_cart.cart_items.all()
    print("Session Cart Items", cart_items)

    # Fetch the session-based cart
    session_cart_ = Cart.objects.filter(session_key=session_key).first()
    print("Session Cart New ", session_cart_)
    if session_cart:

        # Retrieve or create the user-based cart
        user_cart, _ = Cart.objects.get_or_create(user=user)
        # Transfer each item from session cart to user cart

        for session_cart_item in session_cart.cart_items.all():
            user_cart_item, _ = CartItem.objects.get_or_create(
                cart=user_cart,
                product=session_cart_item.product
            )
            # Update the quantity
            user_cart_item.quantity += session_cart_item.quantity
            user_cart_item.save()
        # Clear the session-based cart
        session_cart.delete()
        request.session.modified = True  # Mark the session as modified to keep the current session key
        print(f"Session Key After Login: {request.session.session_key}")


# @receiver(user_logged_in)
def transfer_cart_to_user(request, old_session, new_session):
    session_key = request.session.session_key  # Get the session key
    print("Transfer Sessions to user", session_key)
    session_cart, _ = Cart.objects.get_or_create(session_key=old_session)

    print("Session Cart", session_cart)
    cart_items = session_cart.cart_items.all()
    print("Session Cart Items", cart_items)

    # Fetch the session-based cart
    session_cart_ = Cart.objects.filter(session_key=old_session).first()

    print("Session Cart New ", session_cart_)
    if session_cart:

        # Retrieve or create the user-based cart
        user_cart, _ = Cart.objects.get_or_create(user=request.user)
        # Transfer each item from session cart to user cart

        for session_cart_item in session_cart.cart_items.all():
            user_cart_item, _ = CartItem.objects.get_or_create(
                cart=user_cart,
                product=session_cart_item.product
            )
            # Update the quantity
            user_cart_item.quantity += session_cart_item.quantity
            user_cart_item.save()
        # Clear the session-based cart
        session_cart.delete()
        print(f"Session Key After Login: {request.session.session_key}")


# def transfer_session_data(old_session_key, new_session_key):
#     """
#     Transfer data from the old session to the new session if required.
#     """
#     try:
#         old_session = Session.objects.get(session_key=old_session_key)
#         old_data = old_session.get_decoded()

#         new_session = Session.objects.get(session_key=new_session_key)
#         new_data = new_session.get_decoded()

#         # Example: Merging cart items
#         if "cart" in old_data:
#             new_data["cart"] = merge_cart_data(old_data.get("cart", {}), new_data.get("cart", {}))

#         # Save the updated session
#         new_session.session_data = new_data
#         new_session.save()
#     except Session.DoesNotExist:
#         pass  # If session doesn't exist, skip merging

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



