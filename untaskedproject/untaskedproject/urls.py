from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/auth/login/', permanent=False)),
    path('admin/', admin.site.urls),
    path('auth/', include('apps.users.urls')),
    path('untasked/', include('apps.untaskedapp.urls')),
]
