"""URLs for the core app."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Django URLs
    path("admin/", admin.site.urls),
    # App URLs
    path("", include("home.urls")),
    path("users/", include("users.urls")),
    path("products/", include("products.urls")),
    path("cart/", include("cart.urls")),
    path("management/", include("management.urls")),
    path("payment/", include("payment.urls")),
    # Third party URLs
    path("paypal/", include("paypal.standard.ipn.urls")),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('accounts/', include('allauth.urls')),  # allauth URLs for authentication
    path('logout', LogoutView.as_view()),
    # path('social-auth/', include('social_django.urls', namespace='social')),
     # path('social/', include('social_django.urls', namespace='social')),
  # new
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )


# Custom attributes for admin
admin.site.site_header = "RS_ECOM"
admin.site.site_title = "New RS_ECOM"
admin.site.index_title = "Admin"
