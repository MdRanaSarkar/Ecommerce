from django.contrib import admin
from payment.models import order, order_note_admin,order_list,invoice, Payment, AreaShippingCost
from django.utils.safestring import mark_safe
# Register your models here.
from django.urls import reverse
from django.utils.html import format_html

admin.site.register(order_note_admin)


# Assuming 'order' is imported from your models

@admin.register(order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'get_client_username', 'get_client_email', 'order_status', 'date_created')
    search_fields = ('order_id', 'client__username', 'client__email')  # Search by order ID, client username, or email
    list_filter = ('order_status', 'date_created')  # Filter by order status
    readonly_fields = ('date_created', 'date_updated')  # Read-only fields for timestamps

    def get_client_username(self, obj):
        return obj.client.username  # Access username from the related CustomUser model
    get_client_username.short_description = 'Client Username'  # Column header in admin

    def get_client_email(self, obj):
        return obj.client.email  # Access email from the related CustomUser model
    get_client_email.short_description = 'Client Email'  # Column header in admin


@admin.register(order_list)
class OrderListAdmin(admin.ModelAdmin):
    list_display = ('get_order_id', 'get_client_username', 'order_item', 'order_quantity', 'order_price')
    search_fields = ('order_id__client__username', 'order_id__order_id')  # Search by client username or order ID
    list_filter = ('order_id__order_status',)  # Filter by order status
    readonly_fields = ('order_price',)  # Set price as read-only

    def get_order_id(self, obj):
        return obj.order_id.order_id  # Access the order ID from the related order
    get_order_id.short_description = 'Order ID'  # Column header in admin

    def get_client_username(self, obj):
        return obj.order_id.client.username  # Access username from the related CustomUser model
    get_client_username.short_description = 'Client Username'  # Column header in admin

    def save_model(self, request, obj, form, change):
        # Additional logic before saving the object can go here
        super().save_model(request, obj, form, change)  # Call the parent class's save method


@admin.register(invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'get_order_id',
        'invoice_id',
        'get_client_username',
        'gmail',
        'total_price',
        'invoice_status',
        'date_created',

    )
    search_fields = ('invoice_id', 'order_id__client__username', 'name', 'gmail')  # Search by invoice ID, client username, or name
    list_filter = ('invoice_status', 'country')  # Filter by invoice status and country
    readonly_fields = (
        'invoice_id',
        'order_id',
        'total_price',
        'date_created',
        'date_updated',
        'name',
        'gmail',
        'phone_number',
        'al_phone_number',
        'country',
        'division',
        'city',
        'area',
        'address',
        'payment_method'
    )# Make these fields read-only

    def get_order_id(self, obj):
        return obj.order_id.order_id  # Access the order ID from the related order
    get_order_id.short_description = 'Order ID'  # Column header in admin

    def get_client_username(self, obj):
        return obj.order_id.client.username  # Access username from the related CustomUser model
    get_client_username.short_description = 'Client Username'  # Column header in admin




@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'payment_id', 'get_client_name', 'invoice_id', 'transaction', 'image_tag', 'date_created')
    search_fields = ('transaction', 'order_id__order_id', 'invoice_id__invoice_number', 'order_id__client__username')  # Search by client name, order ID, invoice ID
    list_filter = ('order_id__order_status', 'invoice_id__invoice_status', 'date_created')  # Filter by order status, invoice status
    readonly_fields = ('image_tag', 'date_created', 'date_updated', 'transaction', 'transaction_image')  # Read-only for image and timestamps
    fields = ('order_id', 'invoice_id', 'transaction', 'transaction_image', 'image_tag', 'date_created', 'date_updated')  # Display fields in form

    def get_client_name(self, obj):
        return obj.order_id.client.username  # Assumes 'username' is used for the client's name
    get_client_name.short_description = 'Client Name'  # Column header in admin

    def image_tag(self, obj):
        if obj.transaction_image:
            return mark_safe(f'<img src="{obj.transaction_image.url}" style="height: 50px; width: 50px;" />')
        return "No Image"

    image_tag.short_description = 'Transaction Image Preview'



@admin.register(AreaShippingCost)
class AreaShippingCostAdmin(admin.ModelAdmin):
    list_display = ('area_name', 'shipping_cost', "date_created")
    list_filter = ('date_created','shipping_cost')

