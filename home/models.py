from django.db import models

# Create your models here.

class books(models.Model):
    book_id = models.AutoField #automatic increments id
    book_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to="home/images",default="")
    slug = models.CharField(max_length=1000, default="")
    sellername = models.CharField(max_length=100, default="")
    pickuplocation = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.book_name

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=50000)
    name = models.CharField(max_length=900)
    email = models.CharField(max_length=1101)
    address = models.CharField(max_length=1101)
    city = models.CharField(max_length=1101)
    state = models.CharField(max_length=1101)
    zip_code = models.CharField(max_length=1011)
    phone = models.CharField(max_length=1011, default="")
    def __str__(self):
        return "ORDER ID: "+str(self.order_id) +", from - "+ str(self.state)+ ", city: " +str(self.city)

class TrackUpdate(models.Model):
    order_id = models.CharField(max_length=900,default="")     
    update = models.CharField(max_length=9000,default="")     
    daysleft = models.CharField(max_length=9000,default="")  
    def __str__(self):
        return self.order_id    