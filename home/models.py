"""Models for Home App."""

from django.db import models
from cloudinary.models import CloudinaryField
from django_ckeditor_5.fields import CKEditor5Field
from django.core.exceptions import ValidationError
import os
class Company(models.Model):
    """Model definition for Company."""

    name = models.CharField("Name", max_length=50)
    logo = models.ImageField(upload_to='ecom')
    # logo = CloudinaryField("Logo")
    copy = models.CharField("Copy", max_length=150)
    # description = models.TextField("Description")
    description = CKEditor5Field('Text', config_name='extends')
    email = models.EmailField("Email")
    github = models.URLField("GitHub")
    linkedin = models.URLField("LinkedIn")
    facebook = models.CharField(blank=True, max_length=100)
    facebook_url = models.URLField('Facebook')
    whatsapp = models.CharField(blank=True, max_length=100)
    whatsapp_url = models.URLField('Whatsapp')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "company"
        verbose_name_plural = "company"
        app_label = "home"

    def __str__(self):
        return str(self.name)


class Page(models.Model):
    """Model definition for Page."""

    key = models.CharField("Unique Key", max_length=50, default="pending")
    content = models.TextField("Content", blank=True)
    # image = CloudinaryField("Logo")
    image = models.ImageField(upload_to='ecom_product')
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)

    class Meta:
        ordering = ["key"]
        verbose_name = "page"
        verbose_name_plural = "pages"
        app_label = "home"

    def __str__(self):
        return str(self.key)


class ContactMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),

    )
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=40)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField(max_length=1000, blank=True)
    contact_status = models.CharField(max_length=40, choices=STATUS, default='New')
    ip = models.CharField(max_length=100, blank=True)
    Note = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class FAQ(models.Model):
    STATUS = (
        ("True", "True"),
        ("False", "False")
    )
    order_number = models.IntegerField()
    question = models.CharField(max_length=200)
    answer = models.TextField()
    faq_status = models.CharField(choices=STATUS, max_length=200, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question


class ImageTagMixin:
    IMAGE_TAG_TEMPLATE = '<img src="{}" height="50"/>'
    def image_tag(self):
        """Returns the HTML image tag for the model's image field."""
        if self.image:
            return mark_safe(self.IMAGE_TAG_TEMPLATE.format(self.image.url))
        return ""

def validate_svg_file(file):
    ext = os.path.splitext(file.name)[1].lower()
    if ext != '.svg':
        raise ValidationError("Only SVG files are allowed.")

class SiteICON(models.Model):
    title = models.CharField(max_length=200)
    # Common Icon
    logo_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    cart_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    user_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    wishlist_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    mobile_bar_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])

    # product details
    instock_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    book_hand_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    book_change_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    booklength_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    edition_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    publication_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    isbn_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])

    # cart
    delete_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    view_cart_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])

    # Social Icons
    facebook_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    whatsapp_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    gmail_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    linkedin_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    github_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    chatbot_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    heart_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    payment_done_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])



    # Super Admin Panel
    admin_user_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    admin_total_product_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    admin_total_cat_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    admin_brands_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    admin_processing_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    admin_shipped_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    admin_cancel_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    admin_paid_invoice_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    admin_update_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])

    # Client Admin Panel left section

    admin_dashboard_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    admin_order_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    admin_company_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    admin_pages_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    admin_products_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    admin_category_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    admin_brands_left_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])
    admin_deals_icon = models.FileField(upload_to='icons/', blank=True, null=True, validators=[validate_svg_file])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
