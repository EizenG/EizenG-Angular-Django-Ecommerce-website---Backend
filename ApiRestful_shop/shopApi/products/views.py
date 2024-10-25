from django.http import JsonResponse
from django.core.paginator import Paginator
from rest_framework import viewsets,views,authentication,permissions,status
from rest_framework.response import Response
from .serializers import ProductSerializer
from .models import Product,LignePanier,Panier
from math import fabs
from rest_framework.views import APIView


class ProductViews(viewsets.ViewSet):

    
    def list(self, request):
        category = request.GET.get("category")
        if category:
            category = int(category)
            if category not in range(1,12):
                return JsonResponse({"Errormessage": f"This category code {category} is invalid."},status = 400)
            queryset = Product.objects.filter(product_category = category)
            serializer = ProductSerializer(queryset, many=True)
            pagination = Paginator(serializer.data,15)
            page = request.GET.get("page")
            if page:
                page = int(page)
                if page not in range(1,pagination.num_pages + 1):
                    return JsonResponse({"Errormessage": f"This category {category} has not page {page},invalid request!"},status = 400)
                dict_response = {
                "category" : category,
                "page" : page,
                "num_pages" : pagination.num_pages,
                "products": pagination.page(page).object_list,
                }

                return Response(dict_response,status=200)
            else:
                dict_response = {
                    "category" : category,
                    "page" : 1,
                    "num_pages" : pagination.num_pages,
                    "products": pagination.page(1).object_list,
                    }
                return Response(dict_response,status=200) 
        else:
            page = request.GET.get("page")
            queryset = Product.objects.all()
            serializer = ProductSerializer(queryset, many=True)
            pagination = Paginator(serializer.data,15)
            if page :
                page = int(page)
                if page not in range(1,pagination.num_pages + 1):
                    return JsonResponse({"Errormessage": f"This page {page} is invalid, for category all products!"},status = 400)
                dict_response = {
                "category" : 0,
                "page" : page,
                "num_pages" : pagination.num_pages,
                "products": pagination.page(page).object_list,
                }
                return Response(dict_response,status=200)
            else:
                dict_response = {
                "category" : 0,
                "page" : 1,
                "num_pages" : pagination.num_pages,
                "products": pagination.page(1).object_list,
                }
                return Response(dict_response,status=200)
            
    def retrieve(self,request,pk):
        try:
            queryset = Product.objects.get(asin = pk)
        except Exception as e:
            return JsonResponse({"Errormessage": f"Product with asin {pk} does not exist"})
        serializer = ProductSerializer(queryset)
        return Response(serializer.data,status=200)


class AddProductToCart(views.APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        
        panier = Panier.objects.get(user = request.user)
        if Product.objects.filter(asin = request.data['asin']).exists():
            product = Product.objects.get(asin = request.data['asin'])
            if LignePanier.objects.filter(asin = product,panier = panier).exists():
                lignePanier = LignePanier.objects.get(asin = product,panier = panier)
                lignePanier.quantity = fabs(request.data["quantity"])
                lignePanier.save()
                return Response({"success":"Product quantity has been sucessfully update."},status=status.HTTP_200_OK)
            else:
                lignePanier = LignePanier(asin = product,quantity = request.data["quantity"],panier = panier)
                lignePanier.save()
                return Response({"success":"Product has been sucessfully add to the cart."},status=status.HTTP_200_OK)
        else:
            return Response({"error":"Product with this asin doesn't exist!"},status=status.HTTP_404_NOT_FOUND)
    
