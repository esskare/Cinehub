"""
stores information in the database
"""
from django.db import models #db models

from django.contrib.auth.models import User #authentication
import uuid #generating unique identifiers
 
class BaseModel(models.Model): #models to inherit from
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    timestamp = models.DateField(auto_now_add=True) #creation of timestamp
    updated_at = models.DateField(auto_now_add=True) #for the last timestamp update
     
    class Meta:
        abstract = True
#all of them inherit from the base model
class MovieCategory(BaseModel):
    category_name = models.CharField(max_length=100)
     
class Movie(BaseModel):
    category = models.ForeignKey(MovieCategory, on_delete=models.CASCADE, related_name="pizzas") 
    movie_name = models.CharField(max_length=100)
    price = models.IntegerField(default=100)
    images = models.CharField(max_length=500)
     
class Cart(BaseModel):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="carts")
    is_paid = models.BooleanField(default=False) #indicates whether cart is paid or not
     
class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
