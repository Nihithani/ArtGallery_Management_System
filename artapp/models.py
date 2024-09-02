from django.db import models
from django.utils.html import format_html
from django.contrib.auth.models import User



# Artists
class Artists(models.Model):
    artist_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    about_artist= models.TextField()
    url = models.CharField(max_length=100)
    img= models.ImageField(upload_to='category/')
    add_date = models.DateTimeField( auto_now_add=False, null=True)

    def image_tag(self):
        return format_html('  <img src="/media/{}" style= "width:50%; height:50%" />'.format(self.img))

    def __str__(self) :  # in the filter column in admin panel this function displays the name of the artist to be filtered
        return self.name

#arts
class Arts(models.Model):
    Art_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    aboutArt= models. TextField()
    place=models.CharField(max_length=20,default='hi')
    Artwork_year = models.BigIntegerField(default=00)
    url = models.CharField(max_length=100)
    ArtistName = models.ForeignKey(Artists, on_delete=models.CASCADE)
    img= models.ImageField(upload_to='arts/')
    price = models.IntegerField(default=10)
    type = models.CharField(max_length= 100,default="")
   

    def image_tag(self):
        return format_html('<img src="/media/{}" style= "width:20%; height:20%" />'.format(self.img))

    def __str__(self) :   # in the filter column in admin panel this function displays the title of the artist to be filtered
        return self.title


# cart functionality
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    art = models.ForeignKey(Arts, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.art.title} in cart of {self.cart.user.username}"


#orders functionality
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    art = models.ForeignKey(Arts, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.art.title} in order {self.order.id}"
    

