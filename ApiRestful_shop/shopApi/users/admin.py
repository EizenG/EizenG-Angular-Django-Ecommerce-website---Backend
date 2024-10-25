from django.contrib import admin
from .models import CustomUser
from products.models import Panier


class PanierInline(admin.StackedInline):
    model = Panier

class CustomUserInline(admin.ModelAdmin):
    inlines = [PanierInline]

admin.site.register(CustomUser, CustomUserInline)
admin.site.register(Panier)