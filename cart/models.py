from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse # user to create absolute path
from items.models import Item
# Create your models here.
class Cart(models.Model):
    Item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    # subtotal = models.DecimalField(max_digits=10, decimal_places=2) # total price of add to cart
    completed = models.BooleanField(default=False) # when items are parshase 

    # def save(self, *args, **kwargs): 
    #     # Calculate subtotal before saving
    #     self.subtotal += self.product.price * self.quantity
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.quantity} x {self.Item.name}'
    
    def get_absolute_url(self):
        return reverse("cart:cart_detail")
