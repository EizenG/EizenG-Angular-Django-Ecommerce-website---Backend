from django.db import models
from users.models import CustomUser
from django.core.exceptions import ValidationError

# Create your models here.
def positive_validators(value):
    if value < 0:
        raise ValidationError("Average rating have to be positive number!")

class Product(models.Model):
    asin = models.CharField(max_length=100,verbose_name="ASIN",primary_key=True)
    title = models.CharField(verbose_name="title",max_length=255)
    description = models.TextField(verbose_name="Description")
    price = models.FloatField(verbose_name="price",validators=[positive_validators])
    availability_status = models.BooleanField(verbose_name="avaible",default=True)
    number_of_product_avaible = models.PositiveIntegerField(verbose_name="Number of product avaible")
    image_link = models.CharField(max_length=255,verbose_name="Image link")
    product_category = models.PositiveIntegerField(verbose_name="Category")
    average_rating = models.FloatField(verbose_name="Average rating",validators=[positive_validators])
    total_reviews = models.PositiveIntegerField(verbose_name="Total reviews")
    manufacturer = models.CharField(verbose_name="Manufacturer",null=True,default=" ", max_length=255)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"Product {self.asin}"
    
    def getAsin(self):
        return self.asin


class Panier (models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,unique=True)

    class Meta:

        verbose_name = "Panier"
        verbose_name_plural = "Paniers"
    
    def __str__(self):
        return f"Panier de {self.user.first_name} {self.user.last_name}"

class LignePanier (models.Model):
    asin = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="ASIN")
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    panier = models.ForeignKey(Panier,on_delete=models.CASCADE,verbose_name="Panier")

    class Meta:
        unique_together = (("asin","panier"))

class Commande (models.Model):
    isInProgress = models.BooleanField(default=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

class LigneCommande (models.Model):
    asin = models.CharField(max_length=100,verbose_name="ASIN")
    quantity = models.PositiveIntegerField(verbose_name="ASIN")
    commande = models.ForeignKey(Commande,on_delete=models.CASCADE,verbose_name="Commande")

    class Meta :
        unique_together = (("asin","commande"))
