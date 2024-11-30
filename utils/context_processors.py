"""Context Processors for Utils App."""

from home.models import Company, SiteICON
from products.models import Product, Category, CategoryTree
from cart.models import Cart
from users.forms import ThemePreferenceForm
from cart.views import _cart_session_id

def company(_request):
    """Context processor for company data."""
    company_data = Company.objects.last()
    company_icons =SiteICON.objects.last()
    return {"company": company_data, "company_icons": company_icons}





def user_preferences(request):
    """Context processor to send the theme preference and theme form."""
    theme_preference = request.session.get("theme_preference", "light")
    theme_form = ThemePreferenceForm(
        initial={"theme_preference": theme_preference},
    )
    return {"theme_preference": theme_preference, "theme_form": theme_form}


def products_featured(_request):
    """Context processor return a list of featured products."""
    products_featured_list = Product.objects.filter(
        featured=True, show_hide=True, stock__gte=1
    )[:6]
    return {"products_featured": products_featured_list}


def products_categories(_request):
    """Context processor to provide a list of categories."""
    products_categories_list = Category.objects.filter(show_hide=True)
    return {"products_categories": products_categories_list}

def categories_tree(_request):
    categories_tree = CategoryTree.objects.filter(status=True)
    return {"categories_tree": categories_tree}


def cart_items_count(request):
    """Context processor to add the cart items count to the context."""
    user = request.user
    session_key = _cart_session_id(request)
    if user.is_authenticated:
        # Get the current user"s cart
        cart, created = Cart.objects.get_or_create(user=user)
        cart.session_key = session_key
        cart.save()
        # Calculate the total quantity of items in the cart
        cart_items_count_list = sum(item.quantity for item in cart.cart_items.all())
    else:
        # if not session_key:
        #     request.session.create()
        #     session_key = request.session.session_key
        print("session_key", session_key)
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
        cart_items_count_list = sum(item.quantity for item in cart.cart_items.all())

    return {"cart_items_count": cart_items_count_list}
