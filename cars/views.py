from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from cars.models import Car
from cars.forms import CarModelForm


class CarsListView(ListView):
    model = Car
    template_name = 'carros.html'
    context_object_name = 'cars'

    def get_queryset(self):
        cars = super().get_queryset().order_by('model')
        search = self.request.GET.get('search')
        if search:
            cars = cars.filter(model__icontains=search)

        return cars


class CarDetailView(DetailView):
    template_name = 'carros_detalhe.html'
    model = Car


@method_decorator(login_required(login_url='login'), name='dispatch')
class NewCarCreateView(CreateView):
    model = Car
    form_class = CarModelForm
    template_name = 'novo_carro.html'
    success_url = '/carros/'


@method_decorator(login_required(login_url='login'), name='dispatch')
class CarUpdateView(UpdateView):
    model = Car
    form_class = CarModelForm
    template_name = 'carros_alterar.html'

    def get_success_url(self):
        return reverse_lazy('detalhe_carro', kwargs={'pk': self.object.pk})


@method_decorator(login_required(login_url='login'), name='dispatch')
class CarDeleteView(DeleteView):
    model = Car
    template_name = 'carros_deletar.html'
    success_url = '/carros/'
