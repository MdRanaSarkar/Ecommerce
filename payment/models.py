
from django.db import models
from users.models import CustomUser
from products.models import Product
from django.utils.safestring import mark_safe



class order(models.Model):
    order_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    TASK_STATUS  = [("DRAFT","Draft"),
               ("PENDING","Pending"),
              ("PROCESSING", "processing"),
              ("REJECTED","Rejected"),
              ("CANCELLED","Cancelled"),
              ("DELIVERED","Delivered"),
              ("COMPLETED","Completed")]
    order_status = models.CharField(max_length=30,choices=TASK_STATUS, blank=True, default="PENDING")
    date_created = models.DateTimeField(blank=False,auto_now_add=True)
    date_updated = models.DateTimeField(blank=False,auto_now=True)

    def __str__(self):
        return str(self.order_id)




class order_list(models.Model):
    order_id = models.ForeignKey(order, blank=False,on_delete=models.DO_NOTHING)
    order_item = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    order_quantity = models.IntegerField(blank=False)
    order_price = models.IntegerField(blank=False)
    def __str__(self):
        return str(self.order_item)




class order_note_admin(models.Model):
    order_id = models.ForeignKey(order,blank=False,on_delete=models.DO_NOTHING)
    message = models.CharField(max_length=3000,blank=True)



class invoice(models.Model):
    status = (("NOT_PAID","Not Paid")
              ,("PAID","Paid"),
              ("PENDING_PAY","Pending Payment"),
              ("REJECTED","Rejected"),
              ("FRAUD","Fraud"),
              ("TIMEOUT","Timeout"),
              ("PENDING_CHECK","Pending Check"),)
    invoice_id = models.AutoField(primary_key=True)
    invoice_status = models.CharField(max_length=300, blank=False, choices=status,default="PENDING_PAY")
    order_id = models.ForeignKey(order,null=True, blank=False,on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    """ billing Details -
    Decided to put it here because Most website use it this way """

    name = models.CharField(max_length=100,blank=False)
    gmail = models.EmailField("Email", max_length=255)
    phone_number = models.CharField("Phone Number", max_length=15, blank=False)
    al_phone_number = models.CharField("Phone Number", max_length=15, blank=True)
    country = models.CharField(max_length=100,blank=False, default="bangladesh")
    division = models.CharField(max_length=60, blank=True)
    city = models.CharField(max_length=100,blank=True)
    area = models.CharField(max_length=60,blank=True)
    address = models.CharField(max_length=500, blank=True)
    payment_method = models.CharField(max_length=500, blank=False, default="cash_on_delivery")
    subtotal_price = models.DecimalField(max_digits=20, decimal_places=2, default= 0.00, blank=True)
    shipping_price = models.DecimalField(max_digits=20, decimal_places=2, default= 0.00, blank=True)
    total_price = models.DecimalField(max_digits=20, decimal_places=2, default= 0.00)


    def __str__(self):
        return str(self.invoice_id)


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    order_id = models.OneToOneField(order,null=True, blank=False, on_delete=models.CASCADE)
    invoice_id = models.OneToOneField(invoice,null=True, blank=False, on_delete=models.CASCADE)
    transaction = models.CharField(max_length=500, blank=True)
    transaction_image = models.ImageField(
        upload_to='transac/', blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def image_tag(self):
        return mark_safe('<img src="{}" heights="50" width="40" />'.format(self.transaction_image.url))
    image_tag.short_description = 'Image'

    def img_url(self):
        if self.transaction_image:
            return self.transaction_image.url


class AreaShippingCost(models.Model):
    area_name = models.CharField(max_length=100)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.area_name
