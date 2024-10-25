from django.urls import path
from .views import Register,User_data,User_panier,ChangePassword


urlpatterns = [
    path("register/",Register.as_view()),
    path("data/",User_data.as_view()),
    path("panier/",User_panier.as_view()),
    path("changePassword/",ChangePassword.as_view()),
]