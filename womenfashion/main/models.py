from django.db import models

# Create your models here.
from django.db import models



class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)  # For SEO-friendly URLs

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # E.g., 9999.99
    available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField()  # Number of items in stock
    image = models.ImageField(upload_to='products/')  # Requires Pillow library
  

    def __str__(self):
        return self.name

# Variations for size and color
class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variations")
    size = models.CharField(max_length=20)  # E.g., XS, S, M, L, XL
    color = models.CharField(max_length=50)  # E.g., Red, Blue, Black
    additional_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Price difference for variations

    def __str__(self):
        return f"{self.product.name}"
    
class Offers(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    offer_per = models.PositiveIntegerField()
    
    def __str__(self):
        return self.product.name
    
class Userprofile(models.Model):
    name= models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Profile(models.Model):
    user = models.ForeignKey(Userprofile,on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=False)
    email = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=150, null=False)
  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.name}'

class Profilepic(models.Model):
    user = models.ForeignKey(Userprofile,on_delete=models.CASCADE)
    propic = models.ImageField(upload_to='images/profilepic')
    resume = models.FileField(upload_to='files/resume')
    def __str__(self) -> str:
        return f'{self.user.name}'
    
class Usercart(models.Model):
    user = models.ForeignKey(Userprofile,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    no_of_item = models.IntegerField(default=1)
    size = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    individual_price = models.IntegerField()
    total_price = models.IntegerField()

    def __str__(self):
        return self.user.name

class Product_images(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to='products/')  # Requires Pillow library
    image2 = models.ImageField(upload_to='products/')  # Requires Pillow library
    image3 = models.ImageField(upload_to='products/')  # Requires Pillow library

    def __str__(self):
        return self.product.name
    
class Wish_list(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(Userprofile,on_delete=models.CASCADE)

    def __str__ (self):
        return self.product.name
    
class Orderitems(models.Model):
    user = models.ForeignKey(Userprofile,on_delete=models.CASCADE)
    first_name= models.CharField(max_length=100)
    middile_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.TextField()
    pin = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    mobile = models.CharField(max_length=11)
    message  = models.TextField()
    modes = (
        ('Pay_On_Delivery','Pay_On_Delivery'),
        ('Online_Payment','Online_Payment'),
    )
    payment_mode = models.CharField(max_length=100,choices=modes)
    orderstatus = (
        ('Pending','Pending'),
        ('Out for shipping','Out for shipping'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled')
    )
    status = models.CharField(max_length=150,choices=orderstatus, default='pending')
    ordered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name
    
    
class Reviews(models.Model):
    user = models.ForeignKey(Userprofile,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    message = models.TextField()
    rating = models.IntegerField(choices=[(i, int(i)) for i in range(1, 6)])     
    
    def __str__(self):
        return self.user.name
    
class History(models.Model):
    user = models.ForeignKey(Userprofile,on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')
    no_of_item = models.IntegerField()
    size = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    individual_price = models.CharField(max_length=100)
    total_price = models.CharField(max_length=100)
    payment_mode = models.CharField(max_length=100)
    orderstatus = (
        ('Pending','Pending'),
        ('Out for shipping','Out for shipping'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled')
    )
    status = models.CharField(max_length=150,choices=orderstatus, default='pending')
    ordered_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.name