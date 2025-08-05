from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from cars.views import cars_view, new_car_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('carros/', cars_view, name='lista_carros'),
    path('novo_carro/', new_car_view, name='novo_carro'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

