from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
import products.models as productsModels
from django.utils.translation import gettext_lazy as _


# Create your models here.

class CustomUserManager (BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Users must have an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        panier = productsModels.Panier(user = user)
        panier.save()
        print(panier)
        print(user)
        return user
    def create_superuser(self,email,password,**extra_fields):
        user = self.create_user(email,password,**extra_fields)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class CustomUser (AbstractBaseUser, PermissionsMixin):

    is_staff = models.BooleanField(_("Is staff"),default=False)
    email = models.EmailField(verbose_name=_("Email"),unique = True)
    secondEmail = models.EmailField(verbose_name=_("Secondary email"),null=True,blank=True,unique=True)
    first_name = models.CharField(verbose_name=_("Fisrt name"),null= False,blank=False,max_length=50)
    last_name = models.CharField(verbose_name=_("Last name"),null= False,blank=False,max_length=50)
    birth_date = models.DateField(verbose_name=_("Birth date"))
    tel = models.CharField(verbose_name=_("Phone number"),max_length=9,null = True,unique=True)
    country = models.CharField(verbose_name=_("Country"),max_length=20, null=True)
    region = models.CharField(verbose_name=_("Region"),max_length=20,null=True)
    zipCode = models.IntegerField(verbose_name=_("Zip code"),null=True)
    username = models.CharField(verbose_name=_("User name"),max_length=10,null = True,unique = True)
    address = models.CharField(verbose_name = _("Address"), max_length= 255,null = True)
    profileImage = models.ImageField(null=True,blank=True,upload_to="user/profileImages")
    date_joined = models.DateTimeField(auto_now_add= True)


    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name","last_name","birth_date"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        get_latest_by = "date_joined"

    
    def __str__(self) -> str:
        return self.last_name + " " + self.first_name
