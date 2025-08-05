from django.shortcuts import render, redirect
from cars.models import Car
from cars.forms import CarModelForm


def cars_view(request):
    #cars = Car.objects.all() 
    # o ORM do Django busca as inf. no bando. esse comando internamento o Django faz um select * from Tabela
    #cars = Car.objects.filter(model__contains='p')
    search = request.GET.get('search')
    if search == None:
        cars = Car.objects.all().order_by('model') 
    else:
        cars = Car.objects.filter(model__icontains=search).order_by('model')

    return render(request, 'carros.html', {'cars': cars})


def new_car_view(request):
    if request.method == 'POST':
        new_car_form = CarModelForm(request.POST, request.FILES)
        if new_car_form.is_valid():
            new_car_form.save()
            return redirect('lista_carros')
    else:
        new_car_form = CarModelForm()

    return render(request, 'novo_carro.html', {'new_car_form': new_car_form})