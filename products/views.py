"""Views for Products App."""

from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q

from products.models import Product, Brand, Deal, Category, CategoryTree, Comment
from products.forms import CategoriesForm, FiltersForm, ReviewForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

def check_product_category(product):
    category_data = product.category
    # Define a set of slugs to check for
    category_flags = {
        'books': 'is_book_category',
        'cloths': 'is_cloths_category',
        'electronics': 'is_electronics_category'
    }
    # Initialize the result dictionary with all categories set to False
    result = {key: False for key in category_flags.values()}

    # Check if the category or top parent category matches any of the known slugs
    if category_data.slug in category_flags:
        result[category_flags[category_data.slug]] = True
    else:
        # Use MPTT get_root() to directly get the top parent category
        top_parent_category = category_data.get_root()
        if top_parent_category.slug in category_flags:
            result[category_flags[top_parent_category.slug]] = True

    return result['is_book_category'], result['is_electronics_category'], result['is_cloths_category']



class CategoryListView(ListView):
    """Display the complete list of all products, active and in stock."""

    model = Product
    template_name = "products/category_list.html"
    context_object_name = "categories"
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = CategoryTree.objects.all()
        context["categories_all"] = [
            {"title": category.title, "slug": category.slug, "img_url": category.img_url()}
            for category in categories
        ]
        return context

class ProductListView(ListView):
    """Display the complete list of all products, active and in stock."""

    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(show_hide=True, stock__gte=1)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "All Products"
        return context


class ProductDetailView(DetailView):
    """Display the details of a specific product."""

    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"
    pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        # Get the default context data
        context = super().get_context_data(**kwargs)
        # Calculate the price difference
        product = context['product']
        context['price_savings'] = product.calculate_savings_amount
        context['product_saving_percentages'] = product.calculate_savings_percentage
        # all reviews and comments
        context['all_reviews_comment'] = Comment.objects.filter(product=product, comment_status='True')

        # Check if the product's category is related to books
        is_book_cat, is_electronics_cat, is_cloth_cat = check_product_category(product)
        context['is_book_category'] = is_book_cat
        context['is_electronics_cat'] = is_electronics_cat
        context['is_cloth_cat'] = is_cloth_cat

        return context

    def post(self, request, *args, **kwargs):
        """Handle the review submission."""
        self.object = self.get_object()
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = self.object
            review.user = request.user  # Associate the review with the logged-in user
            review.save()
            # print("Saved...")
            return redirect('products:detail', pk=self.object.pk)
        # If the form is invalid, render the same page with error messages
        return self.get(request, *args, **kwargs)


class FiltersListView(ListView):
    """Display a list of products filtered by categories."""

    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(show_hide=True, stock__gte=1)
        form = FiltersForm(self.request.GET)

        if form.is_valid():
            category = form.cleaned_data["category"]
            brand = form.cleaned_data["brand"]
            deal = form.cleaned_data["deal"]
            min_price = form.cleaned_data["min_price"]
            max_price = form.cleaned_data["max_price"]

            if category:
                # print("Category:", category)
                queryset = queryset.filter(category=category)
            if brand:
                queryset = queryset.filter(brand=brand)
            if deal:
                queryset = queryset.filter(deal=deal)
            if min_price:
                queryset = queryset.filter(normal_price__gte=min_price)
            if max_price:
                queryset = queryset.filter(normal_price__lte=max_price)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = FiltersForm()
        context["deals"] = Deal.objects.all()
        context["title"] = "Categories"
        return context


class DealListView(ListView):
    """View to display a list of deals."""

    model = Deal
    template_name = "products/deal_list.html"
    context_object_name = "deals"


class DealDetailView(DetailView):
    """View to display in detail all the products of an offer."""

    model = Deal
    template_name = "products/deal_detail.html"
    context_object_name = "deal"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the products as context
        context["products"] = self.object.products.all()
        return context


class RecentProductsListView(ListView):
    """Display a list of recent products."""

    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(show_hide=True, stock__gte=1)
        queryset = queryset.order_by("-updated_at", "title")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Recent Products"
        return context


class CategoryFilterListView(ListView):
    """Display a list of all products from a category."""
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 12
    ordering = ["title"]

    def get_queryset(self):
        category_slug = self.kwargs["category_slug"]
        category_data = CategoryTree.objects.get(slug=category_slug)
        # queryset = Product.objects.filter(category__slug=category_slug, show_hide=True, stock__gte=1)
        # queryset = Product.objects.filter(Q(category=category_data) | Q(category__parent=category_data),
        #                                   show_hide=True,
        #                                   stock__gte=1)

        self.descendant_categories = category_data.get_descendants(include_self=True)

        queryset = Product.objects.filter(
                category__in=self.descendant_categories,
                show_hide=True,
                stock__gte=1
            )
        # check the selected category is related to books category or not

        if category_data.slug == 'books':
            self.is_book_category = True
        else:
            try:
                books_parent_category = CategoryTree.objects.get(slug="books")
                self.is_book_category = category_data.is_descendant_of(books_parent_category)
            except CategoryTree.DoesNotExist:
                self.is_book_category = False

        # call forms
        form = CategoriesForm(self.request.GET)

        # print("request data ", self.request.GET)

        if form.is_valid():
            # print("form...")
            category = form.cleaned_data["category"]
            brand = form.cleaned_data["brand"]
            deal = form.cleaned_data["deal"]
            min_price = form.cleaned_data["min_price"]
            max_price = form.cleaned_data["max_price"]

            # print("Category", category)
            if category:
                # print("Category", category)
                queryset = queryset.filter(category=category)
            if brand:
                queryset = queryset.filter(brand=brand)
            if deal:
                # print("Deal", deal)
                queryset = queryset.filter(deal=deal)
            if min_price:
                queryset = queryset.filter(normal_price__gte=min_price)
            if max_price:
                queryset = queryset.filter(normal_price__lte=max_price)
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book_category"] = self.is_book_category
        # print("Descendant Category",  self.descendant_categories)
        context["form"] = CategoriesForm(descendant_categories = self.descendant_categories)
        category = CategoryTree.objects.get(slug=self.kwargs["category_slug"])
        context["category"] = category
        context["title"] = f"{category.title}"
        return context


class BrandFilterListView(ListView):
    """Display a list of all products from a brand."""

    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 12
    ordering = ["title"]

    def get_queryset(self):
        brand_slug = self.kwargs["brand_slug"]
        return Product.objects.filter(
            brand__slug=brand_slug, show_hide=True, stock__gte=1
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand = Brand.objects.get(slug=self.kwargs["brand_slug"])
        context["brand"] = brand
        context["title"] = f"{brand.name}"
        return context


def product_search(request):
    """Search bar, filtering by product title and brand."""
    queryset = request.GET.get("search")
    # print("Searched QuerySet", queryset)
    products = Product.objects.filter(show_hide=True, stock__gte=1)

    # Search filter
    if queryset:
        products = Product.objects.filter(
            Q(title__icontains=queryset) | Q(brand__name__icontains=queryset)
        ).distinct()

    results = products.count()
    paginator = Paginator(products, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "products/product_list.html",
        {
            "products": products,
            "title": queryset,
            "results": results,
            "page_obj": page_obj,
        },
    )


def product_search_(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('query', '').strip()  # Get the search query
        # print(query)
        if query:
            # print("Query :", query )
            products = Product.objects.filter(Q(title__icontains=query) | Q(brand__name__icontains=query)).distinct()[:5]
            # print("product data ", products)
            #product_list = list(products.values('id', 'title', 'normal_price', 'image'))  # Convert queryset to a list of dictionaries
            product_list = [
                {
                    'id': product.id,
                    'title': product.title,
                    'normal_price': product.normal_price,
                    'sale_price': product.sale_price,
                    'image_url': product.image.url if product.image else ''
                }
                for product in products
            ]
            return JsonResponse(product_list, safe=False)  # Return JSON response
        return JsonResponse([], safe=False)  # Return empty list if not AJAX or no query



# get book summaries pdf and show in modal
def get_book_summary(request, book_id):
    book = get_object_or_404(Product, id=book_id)
    # print("book Id ", book.id)
    pdf_url = book.summery_pdf.url  # Assuming the PDF file is saved in the model
    return JsonResponse({'pdf_url': pdf_url})
