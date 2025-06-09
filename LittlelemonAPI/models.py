from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class MenuItem(models.Model):
    title = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()

    def __str__(self):
        return self.title
    
    def clean(self):
        if self.inventory < 0:
            raise ValidationError("Inventory cannot be negative.")
        if self.price < 0:
            raise ValidationError("Price cannot be negative.")
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    items = models.ManyToManyField('MenuItem')
    created_at = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders') 

    def __str__(self):
        return f"Order #{self.id} by {self.customer_name}"
