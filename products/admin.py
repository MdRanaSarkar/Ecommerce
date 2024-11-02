"""Admin for Products App."""

from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from products.models import (
    Product, Deal, Category,
    Brand, CategoryTree, Advertisement,
    Color,Size,Variants,
    Genre, BookAuthor,
    Publication, Comment

    )
from utils.actions import ActionsMixin
from mptt.admin import DraggableMPTTAdmin
import admin_thumbnails
from django.utils.html import format_html


class CategoryTreeAdmin(DraggableMPTTAdmin, ImportExportModelAdmin, ActionsMixin):
    mptt_indent_field = "title"
    #list_display = ('title')
    # list_display = ('tree_actions', 'indented_title',
    #                 'related_products_count', 'related_products_cumulative_count')
    # list_display_links = ('indented_title',)
    #list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',)}

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)

    #     # Add cumulative product count
    #     qs = CategoryTree.objects.add_related_count(
    #         qs,
    #         Product,
    #         'category',
    #         'products_cumulative_count',
    #         cumulative=True)

    #     # Add non cumulative product count
    #     qs = CategoryTree.objects.add_related_count(qs,
    #                                             Product,
    #                                             'category',
    #                                             'products_count',
    #                                             cumulative=False)
    #     return qs

    # def related_products_count(self, instance):
    #     return instance.products_count
    # related_products_count.short_description = 'Related products (for this specific category)'

    # def related_products_cumulative_count(self, instance):
    #     return instance.products_cumulative_count
    # related_products_cumulative_count.short_description = 'Related products (in tree)'


admin.site.register(CategoryTree, CategoryTreeAdmin)



class CategoryResource(resources.ModelResource):

    class Meta:
        model = Category


class BrandResource(resources.ModelResource):

    class Meta:
        model = Brand


class ProductResource(resources.ModelResource):

    class Meta:
        model = Product


class DealResource(resources.ModelResource):

    class Meta:
        model = Deal


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin, ActionsMixin):
    """Admin for Category model."""

    search_fields = ("title",)
    list_display = (
        "title",
        "show_hide",
    )
    list_filter = ("show_hide",)
    list_per_page = 25
    readonly_fields = ("pk", "slug")
    ordering = ("pk",)
    resource_class = CategoryResource


@admin.register(Brand)
class BrandAdmin(ImportExportModelAdmin, ActionsMixin):
    """Admin for Brand model."""

    search_fields = ("name",)
    list_display = ("name",)
    list_filter = ("show_hide",)
    list_per_page = 25
    readonly_fields = ("pk", "slug")
    ordering = ("pk",)
    resource_class = BrandResource


@admin.register(Deal)
class DealAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """Admin for Deal model."""

    search_fields = ("name", "description")
    list_display = ("name", "discount", "start_date", "end_date", "status")
    list_filter = ("status",)
    list_per_page = 25
    readonly_fields = ("pk", "slug")
    ordering = ("pk",)
    resource_class = DealResource


# @admin.register(Product)
# class ProductAdmin(ImportExportModelAdmin, ActionsMixin):
#     """Admin for Product model."""

#     search_fields = ("title",)
#     list_display = ("title", "normal_price", "brand", "updated_at")
#     list_filter = ("show_hide",)
#     list_per_page = 25
#     readonly_fields = ("pk", "slug", "created_at", "updated_at", "sale_price")
#     ordering = ("pk",)
#     resource_class = ProductResource


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, ActionsMixin):
    """Admin for Product model."""

    search_fields = ('title', 'author__name', 'brand__name', 'category__title')
    list_display = ("title", 'image_tag', "normal_price", 'deal',  'discount',
                    'sale_price', 'stock',  "brand", 'display_authors', 'show_hide',"created_at")
    list_filter = ("show_hide", 'author', 'brand', 'category' )
    list_per_page = 25
    readonly_fields = ("pk", "slug", "created_at", "updated_at", "sale_price")
    ordering = ("-updated_at",)
    resource_class = ProductResource

    def get_brand(self, obj):
        """Returns the brand name."""
        return obj.brand.name if obj.brand else "No Brand"
    get_brand.short_description = 'Brand'  # Custom column header

    def display_authors(self, obj):
        return ", ".join(author.name for author in obj.author.all())  # Adjust `author.name` to the correct field

    display_authors.short_description = 'BookAuthor'

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'image_tag', 'start_date', 'end_date', 'created_at')
    list_filter = ('active', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    ordering = ('-start_date',)
    date_hierarchy = 'start_date'



    readonly_fields = ('created_at', 'updated_at')




# for variants section

class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'color_tag']


admin.site.register(Color, ColorAdmin)


class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']


admin.site.register(Size, SizeAdmin)


class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'color', 'size',  'quantity', 'price', 'image_tag']
    list_filter = ('price', 'created_at')
    search_fields = ('title', )
    ordering = ('-created_at',)

admin.site.register(Variants, VariantsAdmin)




# for vbook author section

class GenreAdmin(admin.ModelAdmin):
    list_display = ('title', )
    search_fields = ('title',)

admin.site.register(Genre, GenreAdmin)
class BookAuthorAdmin(admin.ModelAdmin):
    """Admin interface for BookAuthor model."""

    list_display = ('name', 'get_author_type', 'image_tag', 'get_website_link', 'created_at')
    list_filter = ('author_type',)
    search_fields = ('name',)
    ordering = ('-created_at',)
    prepopulated_fields = {'slug': ('name',)}
    # readonly_fields = ("pk", "slug")

    def get_author_type(self, obj):
        """Returns the title of the author type."""
        return obj.author_type.title if obj.author_type else "Not Specified"
    get_author_type.short_description = 'Author Type'  # Custom column header

    def get_website_link(self, obj):
        """Returns a clickable link to the author's website."""
        if obj.website:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.website, obj.website)
        return "No Website"

admin.site.register(BookAuthor, BookAuthorAdmin)



@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('name',  'email', 'image_tag', 'website', 'created_at',)
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'email', 'website')



class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'comment_status', 'created_at', 'updated_at', 'user']
    list_filter = ['comment_status', 'created_at']
    list_per_page = 10


admin.site.register(Comment, CommentAdmin)
