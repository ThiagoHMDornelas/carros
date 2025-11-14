#from django.shortcuts import render, redirect
#from django.views import View
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
    
# def cars_view(request):
#     #cars = Car.objects.all() 
#     # o ORM do Django busca as inf. no banco. esse comando internamente o Django faz um select * from Tabela
#     #cars = Car.objects.filter(model__contains='p')
#     search = request.GET.get('search')
#     if search == None:
#         cars = Car.objects.all().order_by('model') 
#     else:
#         cars = Car.objects.filter(model__icontains=search).order_by('model')

#     return render(request, 'carros.html', {'cars': cars})

# class CarsView(View):
#     def get(self, request):
#         #cars = Car.objects.all() 
#         # o ORM do Django busca as inf. no bando. esse comando internamente o Django faz um select * from Tabela
#         #cars = Car.objects.filter(model__contains='p')
#         search = request.GET.get('search')
#         if search == None:
#             cars = Car.objects.all().order_by('model') 
#         else:
#             cars = Car.objects.filter(model__icontains=search).order_by('model')

#         return render(request, 'carros.html', {'cars': cars})    



class CarDetailView(DetailView):
    template_name = 'carros_detalhe.html'
    model = Car 

# def new_car_view(request):
#     if request.method == 'POST':
#         new_car_form = CarModelForm(request.POST, request.FILES)
#         if new_car_form.is_valid():
#             new_car_form.save()
#             return redirect('lista_carros')
#     else:
#         new_car_form = CarModelForm()

#     return render(request, 'novo_carro.html', {'new_car_form': new_car_form})

# class NewCarView(View):

#     def get(self, request):
#         new_car_form = CarModelForm()
#         return render(request, 'novo_carro.html', {'new_car_form': new_car_form})

#     def post(self, request):
#         new_car_form = CarModelForm(request.POST, request.FILES)
#         if new_car_form.is_valid():
#             new_car_form.save()
#             return redirect('lista_carros')
        
#         return render(request, 'novo_carro.html', {'new_car_form': new_car_form})    
    

@method_decorator(login_required(login_url='login'), name='dispatch')
class NewCarCreateView(CreateView):
    model = Car
    form_class = CarModelForm
    template_name = 'novo_carro.html'
    success_url = '/carros/'

# aula 068 - Em relação ao problema encontrado pelo professor, uma outra solução é sobreescrever o método que passa essas informações para nosso template.

# ```
# def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["new_car_form"] = context["form"]
#         return context
# ```

# Nesse mesmo método podemos também adicionar mais váriaveis pra utilizar no template também:

# ```
# def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     context['titulo'] = 'Criar Novo Produto'
#     context['categorias'] = Categoria.objects.all()
#     return context


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
