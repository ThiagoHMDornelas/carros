from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from cars.views import cars_view, new_car_view
from accounts.views import register_view, login_view, logout_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('carros/', cars_view, name='lista_carros'),
    path('novo_carro/', new_car_view, name='novo_carro'),
    path('registro/', register_view, name='registro'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='loginout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

