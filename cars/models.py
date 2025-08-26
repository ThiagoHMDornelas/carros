from django.db import models


class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100) 
    def __str__(self):
        return self.name     


class Car(models.Model):
    id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=200) # modelo    
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='brand_car')
    factory_year = models.IntegerField(blank=True, null=True) # ano fabricação
    model_year = models.IntegerField(blank=True, null=True) # modelo ano
    plate = models.CharField(max_length=10, blank=True, null=True) # modelo    
    value = models.FloatField(blank=True, null=True) # valor de venda
    photo = models.ImageField(upload_to='cars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
        
    def __str__(self):
        return self.model    


class CarInventory(models.Model):
    cars_count = models.IntegerField()
    cars_value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] # o sinal - indica que será ordem decrescente

    def __str__(self):
        return f'{self.cars_count} - {self.cars_value}'