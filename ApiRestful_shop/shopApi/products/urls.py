from django.urls import path,include
from . import views
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register("products",views.ProductViews,"products")


urlpatterns = [
    path('',include(router.urls)),
    path('addToCart/',views.AddProductToCart.as_view()),
]