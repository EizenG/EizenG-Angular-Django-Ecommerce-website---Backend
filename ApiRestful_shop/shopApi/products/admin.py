from django.contrib import admin
from .models import Product,Commande,LigneCommande,LignePanier

# Register your models here.
admin.site.register(Product)
admin.site.register(Commande)
admin.site.register(LigneCommande)
admin.site.register(LignePanier)
