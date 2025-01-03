"""Views for Home App."""

from django.views.generic import TemplateView, DetailView
from django.shortcuts import render

from home.models import Page
from products.models import (Product, Deal, CategoryTree, Advertisement, Brand, BookAuthor)
from users.forms import ThemePreferenceForm
from django.shortcuts import get_object_or_404

def get_recent_products():
    # Fetch categories for 'book' and 'cloth'
    book_category = get_object_or_404(CategoryTree, title='Books', status='True')
    cloth_category = get_object_or_404(CategoryTree, title='Cloths', status='True')

    # Include child categories of 'book'
    book_categories = list(book_category.children.filter(status='True')) + [book_category]
    book_products = Product.objects.filter(
        category__in=book_categories,
        show_hide=True,
        stock__gte=1
    ).order_by("-updated_at")[:8]

    # Include child categories of 'cloth'
    cloth_categories = list(cloth_category.children.filter(status='True')) + [cloth_category]
    cloth_products = Product.objects.filter(
        category__in=cloth_categories,
        show_hide=True,
        stock__gte=1
    ).order_by("-updated_at")[:4]

    # Combine the two querysets
    recent_products = list(book_products) + list(cloth_products)

    return recent_products


def get_all_products():
    # Fetch categories for 'book' and 'cloth'
    book_category = get_object_or_404(CategoryTree, title='Books', status='True')
    cloth_category = get_object_or_404(CategoryTree, title='Cloths', status='True')

    # Include child categories of 'book'
    book_categories = list(book_category.children.filter(status='True')) + [book_category]
    book_products = Product.objects.filter(
        category__in=book_categories,
        show_hide=True,
        stock__gte=1
    ).order_by("title")[:8]

    # Include child categories of 'cloth'
    cloth_categories = list(cloth_category.children.filter(status='True')) + [cloth_category]
    cloth_products = Product.objects.filter(
        category__in=cloth_categories,
        show_hide=True,
        stock__gte=1
    ).order_by("title")[:4]

    # Combine the two querysets
    all_products = list(book_products) + list(cloth_products)

    return all_products

class IndexTemplateView(TemplateView):
    """View for rendering the site index with multiple contexts."""

    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        # Sends multiple contexts to the templates
        context = super().get_context_data(**kwargs)
        # print(context)

        # Fetch all categories and their titles
        # context["category_titles"] = CategoryTree.objects.values('title', 'slug')
        # Fetch all categories and include their img_url directly
        categories = CategoryTree.objects.all()
        context["categories"] = [
            {"title": category.title, "slug": category.slug, "img_url": category.img_url()}
            for category in categories
        ]

        # All the products (12 prods.)
        context["all_products"] = Product.objects.filter(
            show_hide=True, stock__gte=1
        ).order_by("title")[:12]

        # Recent products (12 prods.)
        context["recent_products"] = Product.objects.filter(
            show_hide=True, stock__gte=1
        ).order_by("-updated_at")[:12]

        # context["all_products"] = get_all_products()
        # context["recent_products"] = get_recent_products()

                # Apple (brand) (6 prods.)
        context["books"] = Product.objects.filter(
            show_hide=True, stock__gte=1, category__title__iexact="books"
        ).order_by("-updated_at")[:12]


        # Apple (brand) (6 prods.)s
        context["apple"] = Product.objects.filter(
            show_hide=True, stock__gte=1, brand__name__iexact="apple"
        ).order_by("-updated_at")[:6]

        # Samsung (brand) (6 prods.)
        context["samsung"] = Product.objects.filter(
            show_hide=True, stock__gte=1, brand__name__iexact="samsung"
        ).order_by("-updated_at")[:6]

        # Computer monitors (category) (6 prods.)
        context["Cloths"] = Product.objects.filter(
            show_hide=True,
            stock__gte=1,
            category__title__iexact="cloths",
        ).order_by("-updated_at")[:12]

        # Deal showing section
        context["deals_products"] = Deal.objects.filter(status=True , section_setup='Hero').order_by('-updated_at')[:10]
        deal_last_two_products = Deal.objects.filter(status=True, section_setup='Middle').order_by('-updated_at')[:3]
        context["deal_last_two_products"] = deal_last_two_products

        # advertising showing section
        context["advertise_data"] = Advertisement.objects.filter(active=True, section_setup="Hero").order_by('-updated_at')[:2]

        context["advertise_middle1"] = Advertisement.objects.filter(active=True, section_setup="Middle").order_by('-start_date')[:1]
        context["advertise_middle2"] = Advertisement.objects.filter(active=True, section_setup="Middle").order_by('-start_date')[1:2]

        context["adv_sub_middle"] = Advertisement.objects.filter(active=True, section_setup="SubMiddle").order_by('-start_date')[:3]

        # Brand showing section
        context["brands_middle"] = Brand.objects.filter(show_hide=True, showcase_section="Middle").order_by('-updated_at')[:2]

        context["brands_all"] = Brand.objects.filter(show_hide=True).order_by('-updated_at')

        context["authors_all"] = BookAuthor.objects.all().order_by('-created_at')

        return context

    def post(self, request, *args, **kwargs):
        """Overrides to handle POST requests."""
        # Handle ThemePreferenceForm submission
        theme_form = ThemePreferenceForm(request.POST)
        if theme_form.is_valid():
            theme_preference = theme_form.cleaned_data["theme_preference"]
            request.session["theme_preference"] = theme_preference

        # Add theme_form to the context
        context = self.get_context_data(**kwargs)
        context["theme_form"] = theme_form

        return render(request, self.template_name, context)


class PageDetailView(DetailView):
    """View to display details of the static pages of the site."""

    model = Page
    template_name = "home/page_detail.html"
    context_object_name = "page"

    def get_object(self, queryset=None):
        # Gets a key from the HTML to be used as a filter in the query
        key = self.kwargs["key"]
        return Page.objects.get(key=key)
