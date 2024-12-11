"""Admin for Home App."""

from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from home.models import Company, Page, SiteICON

class CompanyResource(resources.ModelResource):

    class Meta:
        model = Company


class PageResource(resources.ModelResource):

    class Meta:
        model = Page


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Admin for Company model."""

    list_display = ("name",)
    readonly_fields = ("pk",)
    resource_class = CompanyResource


@admin.register(Page)
class PageAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """Admin for Page model."""
    search_fields = ("key",)
    list_display = ("key", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 25
    readonly_fields = ("pk",)
    ordering = ("pk",)
    resource_class = PageResource



@admin.register(SiteICON)
class SiteICONAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('General Information', {
            'fields': ('title',)
        }),
        ('Common Icons', {
            'fields': ('logo_icon', 'cart_icon', 'user_icon', 'wishlist_icon', 'mobile_bar_icon')
        }),
        ('Product Details Icons', {
            'fields': ('instock_icon', 'book_hand_icon', 'book_change_icon', 'booklength_icon',
                       'edition_icon', 'publication_icon', 'isbn_icon')
        }),
        ('Cart Icons', {
            'fields': ('delete_icon', 'view_cart_icon')
        }),
        ('Social Icons', {
            'fields': ('facebook_icon', 'whatsapp_icon', 'gmail_icon', 'linkedin_icon',
                       'github_icon', 'chatbot_icon', 'heart_icon', 'payment_done_icon')
        }),
        ('Super Admin Panel Icons', {
            'fields': ('admin_user_icon', 'admin_total_product_icon', 'admin_total_cat_icon',
                       'admin_brands_icon', 'admin_processing_icon', 'admin_shipped_icon',
                       'admin_cancel_icon', 'admin_paid_invoice_icon', 'admin_update_icon')
        }),
        ('Client Admin Panel Left Section Icons', {
            'fields': ('admin_dashboard_icon', 'admin_order_icon', 'admin_company_icon',
                       'admin_pages_icon', 'admin_products_icon', 'admin_category_icon',
                       'admin_brands_left_icon', 'admin_deals_icon')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_queryset(self, request):
        """Optimized queryset to reduce database load."""
        qs = super().get_queryset(request)
        return qs.only('title', 'created_at', 'updated_at')
