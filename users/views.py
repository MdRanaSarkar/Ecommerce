"""Views for Users App."""

from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from users.models import CustomUser
from users.forms import UserLoginForm, UserRegistrationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from payment.models import order,order_list,invoice, Payment
from datetime import datetime
import re
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from cart.models import Cart, Wishlist, CartItem
from django.shortcuts import get_object_or_404

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView, OAuth2CallbackView
from django.contrib.sessions.backends.db import SessionStore
from cart.views import transfer_cart_to_user

class UserLoginView(FormView):
    """View for user login."""

    # template_name = "users/login_form.html"
    template_name = "socialaccount/login.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("home:index")

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(UserLoginView, self).dispatch(
                request,
                *args,
                **kwargs,
            )

    def form_valid(self, form):
        old_session_key = self.request.session.session_key
        print("Old session key", old_session_key)
        login(self.request, form.get_user())
        # Ensure the session key remains the same
        self.request.session.save()
        new_session_key = self.request.session.session_key
        print("New session key", new_session_key)
        # Optional: Transfer session-based data (e.g., cart)
        if old_session_key and old_session_key != new_session_key:
            transfer_cart_to_user(self.request, old_session_key, new_session_key)
        return super(UserLoginView, self).form_valid(form)

    # def form_valid(self, form):
    #     # Save the current session key
    #     original_session_key = self.request.session.session_key
    #     # Log the user in
    #     login(self.request, form.get_user())

    #     # Restore the original session key after login
    #     self.request.session.save()  # Save to ensure session is created
    #     if original_session_key:
    #         self.request.session._session_key = original_session_key
    #         self.request.session.modified = True

    #     return super(UserLoginView, self).form_valid(form)

    def form_invalid(self, form):
        # Pass the form errors to the template so they can be displayed
        return super(UserLoginView, self).form_invalid(form)





class UserRegistrationView(CreateView):
    """View for user registration."""

    model = CustomUser
    form_class = UserRegistrationForm
    template_name = "users/registration_form.html"
    success_url = reverse_lazy("cart:cart")

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

    def form_invalid(self, form):
        # Handle specific validation errors
        # errors = form.errors.as_json()
        email_error = form.errors.get('email')
        username_error = form.errors.get('username')
        password_error = form.errors.get('password2')
        # print(errors)

        # if email_error:
        #     form.errors.pop('email')
        #     form.add_error(None, "A custom user with this Email already exists.")
        if username_error:
            form.errors.pop('username')
            form.errors.pop('email')
            form.add_error(None, "Username already exists. Please choose a different one. ")
        if password_error:
            form.errors.pop('email')
            form.errors.pop('password2')
            form.add_error(None, "Passwords do not match. Please try again.")


        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return self.success_url


class UserPasswordChangeView(PasswordChangeView):
    """View for password change."""

    template_name = "users/password_change_form.html"
    success_url = reverse_lazy("users:password_change-done")


@login_required
def user_logout(request):
    """Closes the current user's session and redirects to homepage."""
    logout(request)
    return HttpResponseRedirect("/")


@login_required(login_url="/login")
def user_dashboard(request):
    user = CustomUser.objects.get(email =request.user.email)
    # user = request.user
    orders = order.objects.all().filter(client = user).order_by('date_created')[:4]
    total_oders = len(order.objects.all().filter(client=user).order_by('date_created'))
    dilevered_orders = len(order.objects.all().filter(client=user,order_status="COMPLETED"))
    print(total_oders)
    print(dilevered_orders)
    registered_on = user.date_joined
    registered_on = datetime.fromisoformat(str(registered_on)).strftime("%d/%m/%Y")
    # last_login = user.last_active
    # last_login = datetime.fromisoformat(str(last_login)).strftime("%d/%m/%Y")
    if request.user.is_authenticated:
        context={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'order_id_list' : orders,
            'total_orders':total_oders,
            'registered_on':registered_on,
            'dilevered_orders':dilevered_orders,
           # 'last_login':last_login,

        }
        return render(request, "users/dashboard.html", context)
    else:
         messages.error(request,"Sorry, You are not logged in. Please Login and try again")
         return redirect("users:login")




@login_required(login_url="/login")
def orders(request):
    if request.user.is_authenticated:
        user = CustomUser.objects.get(email=request.user.email)
        order_id = order.objects.all().filter(client=user).order_by('date_created')
        all_orders = Paginator(order.objects.all().filter(client=user).order_by('-date_created'), 10)
        page = request.GET.get('page')
        try:
            orders = all_orders.page(page)
        except PageNotAnInteger:
            orders = all_orders.page(1)
        except EmptyPage:
            orders=  all_orders.page(all_orders.num_pages)

        context={

            'order_id_list' : orders,
        }
        return render(request,"users/user_order_list.html",context)
    else:
        messages.error("Sorry, you need to be logged in to view your orders")
        return redirect("users:login")

@login_required(login_url="/login")
def view_order(request, order_id):
    if request.user.is_authenticated:
        print("order_id", order_id)
        order_items_list = order_list.objects.all().filter(order_id=order_id)
        invoice_details = invoice.objects.all().filter(order_id=order_id)
        transaction_details = Payment.objects.all().filter(order_id = order_id)

        context={
            "order_id":order_id,
            "order_items_list":order_items_list,
            "invoice_list": invoice_details,
            "transaction_details": transaction_details
        }
        return render(request,"users/user_order_details.html",context=context)
    else:
        return redirect("users:login")


@login_required(login_url="/login")
def view_invoice(request, invoice_id):
    if request.user.is_authenticated:
        invoice_dat = invoice.objects.get(invoice_id=invoice_id)

        context = {

            'invoice':invoice_dat

        }
        return render(request,"view_invoice.html",context=context)
    else:
        return redirect("login")

@login_required(login_url="/login")
def user_wishlist(request):
    user = request.user
    wishlist, created = Wishlist.objects.get_or_create(user=user)
    wishlist_products = wishlist.products.all()
    wishlist_count = wishlist.products.count()
    return render(
        request,
        "users/user_wish_list.html",
        {
            "wishlist": wishlist,
            "wishlist_products": wishlist_products,
            "wishlist_count": wishlist_count,
        },
    )









