"""Models for Home App."""

from django.db import models
from cloudinary.models import CloudinaryField
from django_ckeditor_5.fields import CKEditor5Field

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
