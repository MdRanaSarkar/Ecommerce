"""Models for Products App."""
import os
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from cloudinary.models import CloudinaryField
from products.choices import WARRANTY_CHOICES
from mptt.models import MPTTModel, TreeForeignKey
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from users.models import CustomUser
from django.db.models import Count, Sum, Avg

# for showing this for all models
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



class CategoryTree(MPTTModel, ImageTagMixin):
    status = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    title = models.CharField(max_length=200)
    keywords = models.CharField(max_length=100)
    image = models.ImageField(blank=True, upload_to='category/')
    details = CKEditor5Field('Text', config_name='extends')
    status = models.CharField(max_length=20, choices=status)
    slug = models.SlugField(null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return self.title



class Category(models.Model):
    """Catalog type model for Category."""

    title = models.CharField("Category", max_length=50, unique=True)
    slug = models.SlugField(
        "Slug",
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )
    show_hide = models.BooleanField("Show", default=True)
    image = models.FileField(upload_to='category/', blank=True, null=True, validators=[validate_svg_file])
    created_at = models.DateTimeField("Brand Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Brand Updated at", auto_now=True)
    class Meta:
        ordering = ["title"]
        verbose_name = "category"
        verbose_name_plural = "categories"
        app_label = "products"

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        # Create a slug based on the title
        if not self.slug or self.slug != slugify(self.title):
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Brand(models.Model, ImageTagMixin):
    """Catalog type model for Brand."""

    showcase = (
        ('Anywhere', 'Anywhere'),   # img size
        ('Middle', 'Middle'),  # img size 200 by 200
        ('SubMiddle', 'SubMiddle'),    # img size 300 by 300
        ('Footer', 'Footer'),     # img size 200 by 200
    )

    name = models.CharField("Name", max_length=255, unique=True)
    slug = models.SlugField(
        "Slug",
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )
    show_hide = models.BooleanField("Show/Hide", default=True)

    image = models.ImageField(upload_to='brands', blank=True, null= True)

    showcase_section = models.CharField("Brand Showcase Section", max_length=255, blank=True, choices=showcase, default="Anywhere")

    created_at = models.DateTimeField("Brand Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Brand Updated at", auto_now=True)
    class Meta:
        ordering = ["name"]
        verbose_name = "brand"
        verbose_name_plural = "brands"
        app_label = "products"

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        # Create a slug based on the name
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def img_url(self):
        url = ""
        if self.image:
            url = self.image.url
        return url



class Deal(models.Model, ImageTagMixin):
    """Entity type model for Deals."""

    section_set = (
        ('Hero', 'Hero'),   # img size 1200 by 600
        ('Middle', 'Middle'),  # img size 600 by 200
        ('SubMiddle', 'SubMiddle'),    # img size 300 by 300
        ('Footer', 'Footer'),     # img size 300 by 300
    )

    name = models.CharField("Name", max_length=255, unique=True)
    section_setup = models.CharField("Section Setup", max_length=255, blank=True, choices=section_set, default="Hero")
    slug = models.SlugField(
        "Slug",
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )
    # image = CloudinaryField("Image")
    image = models.ImageField(upload_to='ecom_deal')
    # description = models.TextField("Description", blank=True, null=True)
    description = CKEditor5Field('Text', config_name='extends')
    discount = models.DecimalField(
        "Discount", max_digits=5, decimal_places=2, blank=True, null=True
    )
    start_date = models.DateField("Start Date", blank=True, null=True)
    end_date = models.DateField("End Date", blank=True, null=True)
    status = models.BooleanField("Status", default=True)
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)
    class Meta:
        ordering = ["name"]
        verbose_name = "Deal"
        verbose_name_plural = "deals"
        app_label = "products"

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        # Create a slug based on the name
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)
        super(Deal, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """Method returns the canonical URL for the details of an deal."""
        return reverse("deal_detail", kwargs={"slug": self.slug})

# create model for book writer

class Genre(models.Model):
    title = models.CharField(max_length=255)
    def __str__(self):
        return str(self.title)
class BookAuthor(models.Model, ImageTagMixin):
    name = models.CharField(max_length=200)
    author_type = models.ForeignKey(Genre, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(blank=True,  upload_to='author/')
    bio = CKEditor5Field('Text', config_name='extends')
    website = models.URLField(blank=True)
    slug = models.SlugField(
        "Slug",
        max_length=255,
    )
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def image_url(self):
        img_url = ""
        if self.image:
            img_url = self.image.url
        return img_url

# End book writer section

class Publication(models.Model, ImageTagMixin):
    name = models.CharField(max_length=255)
    address = CKEditor5Field('Text', config_name='extends', blank=True)
    website = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True)
    image = models.ImageField(blank=True,  upload_to='publications/')

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def image_url(self):
        img_url = ""
        if self.image:
            img_url = self.image.url
        return img_url


class Product(models.Model, ImageTagMixin):
    """Entity type model for Products."""
    title = models.CharField("Title", max_length=255, unique=True)
    slug_title = models.CharField("Slugged Title", max_length=255)
    category = models.ForeignKey(
            CategoryTree,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            verbose_name="Category",
        )
      # author related
    author = models.ManyToManyField(
        BookAuthor,
        blank=True,
        related_name='products',
        verbose_name='BookAuthor'
        )
    book_page = models.IntegerField(default=0 , blank= True, null=True)
    edition = models.CharField("Edition", max_length=100, blank= True)
    isbn_code = models.CharField("ISBN", max_length=100, blank= True)

    publication = models.ForeignKey(
        Publication,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name="Publication",
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Brand",
    )

    deal = models.ForeignKey(
        Deal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name="Deal",
    )
    normal_price = models.DecimalField(
        "Price",
        max_digits=10,
        decimal_places=2,
    )
    discount = models.DecimalField(
        "Discount Percentage",
        max_digits=10,
        decimal_places=2,
        default= 0.0
    )

    sale_price = models.DecimalField(
        "Sale Price", max_digits=10, decimal_places=2, null=True, blank=True
    )


    image = models.ImageField(upload_to='products/', max_length=100)

    summery_pdf = models.FileField(upload_to='pdfs/', blank=True, null=True)

    stock = models.PositiveIntegerField("Stock", default=100)

    warranty = models.IntegerField(
        "Warranty", choices=WARRANTY_CHOICES, default="12", blank=True
    )

    # description = models.TextField("Description", blank=True, null=True)
    description = CKEditor5Field('Description', config_name='extends')
    # description =
    specifications =CKEditor5Field('Specifications', config_name='extends')

    seo_keyword = CKEditor5Field('SEO keywords', config_name='extends', blank=True)

    featured = models.BooleanField("featured", default=True)
    show_hide = models.BooleanField("Show/Hide", default=True)

    slug = models.SlugField(
        "Slug",
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)

    class Meta:
        ordering = ["title"]
        verbose_name = "product"
        verbose_name_plural = "products"
        app_label = "products"

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        self.update_sale_price()

        # Create a slug based on the title
        if not self.slug or self.slug != slugify(self.title):
            self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def update_sale_price(self):
        """Method update sale_price based on deal and deal dates."""
        # Check if there is a deal on the product and if it has a discount
        current_date = timezone.now().date()  # Today
        self.sale_price = None
        if self.deal and self.deal.discount is not None:
            if self.deal.start_date and self.deal.end_date:
                # Apply the discount and save the "sale_price"
                if self.deal.start_date <= current_date <= self.deal.end_date:
                    print(self.normal_price)
                    self.sale_price = self.normal_price - self.normal_price*(self.deal.discount / 100)

        if self.discount:
            if  self.sale_price is not None:
                self.sale_price -= self.sale_price*(self.discount/100)
            else:
                self.sale_price = self.normal_price - self.normal_price*(self.discount/100)

    def total_discount(self):
        total_discount_percentage = 0
        current_date = timezone.now().date()  # Today

        # Check if there is a valid deal discount within the date range
        if self.deal and self.deal.discount and self.deal.start_date <= current_date <= self.deal.end_date:
            total_discount_percentage += self.deal.discount
        # Add any additional discount
        if self.discount:
            total_discount_percentage += self.discount
        return int(total_discount_percentage)

        # self.sale_price = self.sale_price - self.discount
        # If no conditions are met, set "None" for the "sale_price"

    def is_new(self):
        """Returns True if the product is new."""
        return self.created_at >= timezone.now() - timezone.timedelta(
            days=1
        ) or self.updated_at >= timezone.now() - timezone.timedelta(days=1)

    def calculate_savings_amount(self):
        """Calculate the amount saved."""
        if self.sale_price:
            return self.normal_price - self.sale_price
        return 0
    def calculate_savings_percentage(self):
        """Calculate the percentage saved."""
        if self.sale_price and self.normal_price > 0:
            savings = (self.normal_price - self.sale_price) / self.normal_price * 100
            return round(savings, 2)  # rounded to 2 decimal places
        return 0
    def book_summery_pdf(self):
        pdf_url = ""
        if self.summery_pdf:
            pdf_url = self.summery_pdf.url
        return pdf_url

    def average_review(self):
        reviews = Comment.objects.filter(
            product=self, comment_status=True).aggregate(average=Avg('rate'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def total_review(self):
        reviews = Comment.objects.filter(
            product=self, comment_status=True).aggregate(count=Count('id'))
        cnt = 0
        if reviews['count'] is not None:
            cnt = (reviews['count'])
        return cnt




@receiver(post_save, sender=Deal)
@receiver(post_delete, sender=Deal)
def product_update_sale_prices(sender, instance, **kwargs):
    """Signal handler to update sale_prices when a Deal is saved or deleted."""
    products = Product.objects.filter(deal=instance)

    # Iterate through the products and update the "sale_price"
    for product in products:
        product.update_sale_price()
        product.save()



class Advertisement(models.Model, ImageTagMixin):
    section_ad = (
        ('Hero', 'Hero'),   # img size 600 by 300
        ('Middle', 'Middle'),  # img size 600 by 200
        ('SubMiddle', 'SubMiddle'),    # img size 300 by 300
        ('Footer', 'Footer'),     # img size 300 by 300
    )
    title = models.CharField(max_length=255)
    section_setup = models.CharField("Advertisement Section Setup", max_length=255, blank=True, choices=section_ad, default="Hero")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='ads/')  # Ensure Pillow is installed
    link = models.URLField(blank=True, null = True) #
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Advertisement"
        verbose_name_plural = "Advertisements"
        ordering = ['-start_date']  # Order by start date, most recent first
    def img_url(self):
        image_url = ""
        if self.image:
            image_url = self.image.url
        return image_url



# product variant sections

class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True)
    def __str__(self):
        return self.name
    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
        else:
            return ""

class Size(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True)
    def __str__(self):
        return self.name


class Variants(models.Model, ImageTagMixin):
    title = models.CharField(max_length=100, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(blank=True, upload_to='product_variant/')
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_url(self):
        img_url = ""
        if self.image:
            img_url = self.image.url
        return img_url


class Comment(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200, blank=True)
    comment = models.CharField(max_length=500, blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=100, blank=True)
    comment_status = models.CharField(max_length=40, choices=STATUS, default='True')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
