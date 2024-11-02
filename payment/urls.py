"""URLs for Payment App."""

from django.urls import path

from payment.views import (check_out, payment_success, payment_failed,
                           checkout_combine, proceed_to_checkout, user_payment,
                           transaction_success, area_wise_shipping_cost)

app_name = "payment"

urlpatterns = [
    path(
        "paypal_checkout/<int:product_id>/",
        check_out,
        name="checkout",
    ),
    path(
        "payment-success/<int:product_id>/",
        payment_success,
        name="payment_success",
    ),
    path(
        "payment-failed/<int:product_id>/",
        payment_failed,
        name="payment_failed",
    ),
    path(
        "checkout/",
        checkout_combine,
        name = "checkout_all",
        ),
     path(
        "proceed_checkout/",
        proceed_to_checkout,
        name = "proceed_checkout_all",
        ),
    path(
        "method/",
        user_payment,
        name = "user_payment",
        ),
     path(
        "success/",
        transaction_success,
        name = "transaction_success",
        ),
    path(
        "area_shipping_cost/",
        area_wise_shipping_cost,
        name = "area_shipping_cost",
        ),




]
