"""URLs for Users App."""

from django.urls import path
from django.contrib.auth.views import PasswordResetDoneView

from users.views import (
    UserLoginView,
    UserRegistrationView,
    PasswordChangeView,
    user_logout,
    user_dashboard,
    orders,
    view_order,
    user_wishlist,

)

app_name = "users"

urlpatterns = [
    path(
        "login/",
        UserLoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        user_logout,
        name="logout",
    ),
    path(
        "registration/",
        UserRegistrationView.as_view(),
        name="registration",
    ),
    path(
        "password-change/",
        PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password-change/done",
        PasswordResetDoneView.as_view(),
        name="password_change_done",
    ),
     path(
        "dashboard/",
        user_dashboard,
        name="user_dashboard",
    ),
    path(
        "orders/",
        orders,
        name="user_order",
    ),
     path(
        "view_order/<int:order_id>",
        view_order,
        name="view_order",
    ),
    path(
        "wishlist",
        user_wishlist,
        name="user_wishlist",
    ),


]
