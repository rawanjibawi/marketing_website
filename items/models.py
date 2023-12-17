from django.db import models
from django.contrib.auth.models import User

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True) # we add db_index=True since we will use category name for search
    
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE) # if category is deleted all items inside the category is deleted as well
    name = models.CharField(max_length=200)
    # TextField allow multi line text field
    description = models.TextField(blank=True, null = True) # this allow the user not to put description
    price = models.FloatField()
    image = models.ImageField(upload_to='item_images', blank=True, null = True) # upload_to specify where in the server images should be saved (server will create a folder item_image)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='items', on_delete = models.CASCADE) # if user get deleted delete the items as well
    created_at = models.DateTimeField(auto_now_add=True)# will automatically be added when user add the item
    
    def __str__(self):
        return self.name
    

class CartItem(models.Model):
    Item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
