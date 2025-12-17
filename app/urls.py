from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = [
    path('', include('core.urls')),
    path('user/', include('user.urls')),
    path('caps/', include('cap.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('order.urls')),
    path('payments/', include('payment.urls')),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )