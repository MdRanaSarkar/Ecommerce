"""Views for Payment App."""

import uuid
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect
from paypal.standard.forms import PayPalPaymentsForm
from products.models import Product

from cart.models import Cart, CartItem
from cart.views import _cart_session_id
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import authenticate
from django.contrib import auth , messages
from payment.models import order,order_list,invoice, Payment, AreaShippingCost
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


@login_required
def check_out(request, product_id):
    """View for the integration with PayPal."""
    product = Product.objects.get(id=product_id)
    host = request.get_host()

    # Use sale_price if defined, otherwise use normal_price
    current_price = product.sale_price if product.sale_price is not None else product.normal_price

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': current_price,
        'item_name': product.title,
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('payment:payment_success', kwargs = {'product_id': product.id})}",
        'cancel_url': f"http://{host}{reverse('payment:payment_failed', kwargs = {'product_id': product.id})}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
    context = {
        "product": product,
        "paypal": paypal_payment
    }

    return render(request, "payment/checkout.html", context)


@login_required
def payment_success(request, product_id):
    """View sends the product as context if the payment was successful."""
    product = Product.objects.get(id=product_id)
    return render(
        request, "payment/payment_success.html", {"product": product}
    )


@login_required
def payment_failed(request, product_id):
    """View sends the product as context if the payment failed."""
    product = Product.objects.get(id=product_id)
    return render(
        request, 'payment/payment_failed.html', {'product': product}
    )


@login_required
def checkout_combine(request,total=0, total_price=0, quantity=0, cart_items=None):
    tax = 0.00
    handing = 0.00
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(cart__user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_session_id(request))
            cart_items = CartItem.objects.filter(cart=cart)
        print(cart_items)
        for cart_item in cart_items:
            # print(cart_item.product.sale_price)
            total_price += cart_item.total_price()
            quantity += cart_item.quantity

        total = total_price + 10

    except ObjectDoesNotExist:
        pass # just ignore


    tax = round(((2 * total_price)/100), 2)
    grand_total = total_price + tax
    handing = 15.00
    total = float(grand_total) + handing

    context = {
        'total_price': total_price,
        'quantity': quantity,
        'cart_items':cart_items,
        'handing': handing,
        'vat' : tax,
        'order_total': total,
    }
    return render(request, 'payment/checkout_all_carts.html', context)




special_char_list = r"!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
email_special_char_list = r"!\"#$%&'()*+,/:;<=>?@[\]^`{|}~"

def num_checker(string):
        return any(i.isdigit() for i in string)

def special_char_checker(string):
    for i in string:
        if i in special_char_list:
            return True
    return False

def email_special_char_checker(string):
    if "@" in string:
        email = string.split("@", "")
        for i in email[0]:
            if i in email_special_char_list:
                return True
        return False
    else:
        return True



@login_required(login_url="/users/login")
def proceed_to_checkout(request):
    if request.POST:
        req_user = request.user
        if req_user.is_authenticated:
            client = request.user
            user_order_id = order.objects.create(
                client=client
            )
            # order_save.save()


            # print("Order Save Done !")
            # print("user order id :", user_order_id)
            # working on order_list
            # session = request.session.session_key
            cart = Cart.objects.get(user_id=req_user.id)
            cart_items_list = CartItem.objects.all().filter(cart=cart)
            # print(cart_items_list)
            total = 0

            for item in cart_items_list:

                order_item= Product.objects.get(title=item.product)
                price = order_item.normal_price
                quantity = item.quantity
                # print("Price", price, quantity)
                total += price*quantity

                order_list_save = order_list.objects.create(
                    order_id=user_order_id,
                    order_item=order_item,
                    order_price=price,
                    order_quantity=quantity
                )
                order_list_save.save()
                order_item.stock -= item.quantity
                order_item.save()


            # working on invoice

            # total_price =  request.POST['todalCheckoutPrice']

            user_name = request.POST['user_name']
            user_gmail = request.POST['user_gmail']
            phone_number = request.POST['phone_number']
            al_phone_number = request.POST.get('al_phone_number', '')  # Optional field
            country = request.POST['country']
            city = request.POST.get('city', '')
            thana_area = request.POST.get('areaThana', '')
            address = request.POST.get('addressFullData', '')
            payment_method = request.POST.get('delivery-method', '')
            division = request.POST.get('division', '')

            subtotal = total

            shipping_cost = request.POST.get('final_shipping_cost', '')
            total_vat = request.POST.get('productTotalVat', '')

            shipping_cost = float(shipping_cost)
            total_vat = float(total_vat)
            print("total_vat", total_vat)
            print("shipping_cost", shipping_cost)

            total_checkout_amount = float(subtotal) + shipping_cost + total_vat

            # print("total_vat", total_vat)
            # print("shipping_cost", shipping_cost)
            # print(total_checkout_amount)



            new_invoice =  invoice.objects.create(
                order_id=user_order_id,
                name =user_name,
                gmail=user_gmail,
                phone_number = phone_number,
                al_phone_number = al_phone_number,
                country=country,
                division= division,
                city= city,
                area = thana_area,
                address= address,
                payment_method = payment_method,
                subtotal_price= subtotal,
                shipping_price = shipping_cost,
                total_price=  total_checkout_amount,
            )
            # updating order
            # order_status_update = order.objects.filter(order_id=order_save.order_id).update(order_status="PROCESSING")
            # removing cart
            invoice_id = new_invoice.invoice_id
            # print("Invoce ID", invoice_id)
            for item in cart_items_list:
                stocks_now = Product.objects.get(title=item.product)
                # decreasing stock
                stocks_now.stocks = stocks_now.stock- item.quantity
                stocks_now.save()

            # Delete Card Item
            cart.delete()
            # print("cart")
            new_order_id = user_order_id.order_id
            # print("Final order ID", user_order_id.order_id)
            # messages.success(request,"Your order has been successfully received.")
            total_amount_str = str(total_checkout_amount)
            if payment_method == "cash_on_delivery":
                request.session['payment_method'] = payment_method

                # default payment add so that from admin easily checked
                Payment.objects.create(
                    order_id= user_order_id,
                    invoice_id=new_invoice,
                    transaction= "cash_on_delivery",  # Only assign if not empty
                    transaction_image= None  # Only assign if not empty
                )

                return redirect("payment:transaction_success")
            else:
                request.session['payment_method'] = payment_method
                request.session['payment_amount'] = total_amount_str
                request.session['new_order_id'] = new_order_id
                request.session['new_invoice_id'] = invoice_id
                return redirect("payment:user_payment")
        else:
            return redirect("users:login")


@login_required(login_url="/users/login")
def user_payment(request):
    if request.method == 'POST':
        # Retrieve transaction details from the POST request
        transactions_idx = request.POST.get('payment_transactions', '').strip()
        transactions_img = request.FILES.get('transaction_img', None)
        # print("transactions-img", transactions_img)

        # Retrieve order ID and invoice ID from the session
        product_order_id = request.session.get('new_order_id')
        invoice_id = request.session.get('new_invoice_id')  # Assuming this is the correct key

        # Check if at least one of the fields has a value
        if not (transactions_idx or transactions_img):
            messages.warning(request, "At least one of the fields must be provided.")
            return redirect("payment:user_payment")

        # print(f"Order id {product_order_id} Invoice ID {invoice_id}" )

        order_instance = get_object_or_404(order, pk=product_order_id)
        payment_instance = get_object_or_404(invoice, pk=invoice_id)
        # Create a new Payment transaction
        new_transaction = Payment.objects.create(
            order_id= order_instance,
            invoice_id=payment_instance,
            transaction=transactions_idx if transactions_idx else None,  # Only assign if not empty
            transaction_image=transactions_img if transactions_img else None  # Only assign if not empty
        )

        # Redirect to the transaction success page
        return redirect("payment:transaction_success")

    payment_method = request.session.get('payment_method')
    payment_total_amount = request.session.get('payment_amount')
    context = {
               "payment_method" : payment_method,
               "payment_total_amount": payment_total_amount
        }
    return render(request, "payment/payment_method.html", context)


@login_required
def transaction_success(request):
    """View sends the product as context if the payment was successful."""
    payment_method = request.session.get('payment_method')
    context = {
        "payment_method" : payment_method
        }
    return render(
        request, "payment/transaction_success.html", context
    )



def area_wise_shipping_cost(request):
    # Fetch all areas and prices
    area_shipping = AreaShippingCost.objects.all().values('area_name', 'shipping_cost')
    return JsonResponse(list(area_shipping), safe=False)

