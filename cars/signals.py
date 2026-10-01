from django.db.models.signals import pre_save, post_save, post_delete
from django.db.models import Sum
from django.dispatch import receiver

from cars.models import Car, CarInventory


def car_inventory_update():
    count = Car.objects.all().count()
    value = Car.objects.aggregate(total_value=Sum('value'))['total_value']

    CarInventory.objects.create(cars_count=count, cars_value=value or 0)


@receiver(pre_save, sender=Car)
def car_pre_save(sender, instance, **kwargs):
    if not instance.bio:
        instance.bio = 'Descrição deste carro ainda não foi informada!'


@receiver(post_save, sender=Car)
def car_post_save(sender, instance, **kwargs):
    car_inventory_update()


@receiver(post_delete, sender=Car)
def car_post_delete(sender, instance, **kwargs):
    car_inventory_update()
