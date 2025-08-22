from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from cars.views import CarsListView, NewCarCreateView, CarDetailView, CarUpdateView, CarDeleteView
from accounts.views import register_view, login_view, logout_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('carros/', CarsListView.as_view(), name='lista_carros'),
    path('novo_carro/', NewCarCreateView.as_view(), name='novo_carro'),
    path('carro/<int:pk>', CarDetailView.as_view(), name='detalhe_carro'),
    path('carro/<int:pk>/alterar', CarUpdateView.as_view(), name='alterar_carro'),
    path('carro/<int:pk>/deletar', CarDeleteView.as_view(), name='deletar_carro'),
    path('registro/', register_view, name='registro'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

