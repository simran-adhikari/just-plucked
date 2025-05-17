from django.db import models
from products.models import Product,Category

class HomepageData(models.Model):
    id=models.BigAutoField(primary_key=True)
    trending=models.ManyToManyField(Product,related_name="homepagedata_trending")
    popular=models.ManyToManyField(Product)

     
class ContactData(models.Model):
    id = models.BigAutoField(primary_key=True)
    fullname = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return f"{self.fullname} - {self.subject}"

