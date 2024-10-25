from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from .forms import CustomUserCreationForm
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import CustomUserSerializer
import products.models as productsModels
import products.serializers as productsSerializers
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.parsers import MultiPartParser
from django.contrib.auth.password_validation import validate_password
# Create your views here.


class User_data(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def get(self,request):
        user = CustomUser.objects.get(email = request.user.email)
        serializer = CustomUserSerializer(user)
        data =  { keys:data for keys,data in serializer.data.items() if keys not in ["id","password","groups","is_superuser","last_login","user_permissions"] }  
        return Response({"user": data})
    
    def patch(self,request):
        serializer = CustomUserSerializer(request.user,request.data,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg' : "succesfully updated"})
        else:
            return Response({
                'msg': "Error while updating user information",
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
       

class User_panier(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        panier = productsModels.Panier.objects.get(user = request.user) 
        lignesPanier = productsModels.LignePanier.objects.filter(panier = panier)
        products = []
        for ligne in lignesPanier:
            serializer = productsSerializers.ProductSerializer(productsModels.Product.objects.get(asin=ligne.asin.getAsin()))
            products.append(serializer.data)
            products[-1]["quantity"] = ligne.quantity
        
        return Response({"products" : products})
    
    def patch(self,request):
        panier = productsModels.Panier.objects.get(user = request.user)
        product_data_list = request.data["fieldsToUpdate"].split("/")
        for product_data in product_data_list:
            product_data = product_data.split(";")
            lignePanier = productsModels.LignePanier.objects.get(panier = panier,asin = product_data[0])
            lignePanier.quantity = int(product_data[1])
            lignePanier.save()
        return Response({"msg":"Successfully updated"})

    def delete(self,request):
        panier = productsModels.Panier.objects.get(user = request.user)
        product_asin = request.data["lineToDelete"]
        lignePanier = productsModels.LignePanier.objects.get(panier = panier,asin = product_asin)
        lignePanier.delete()
        return Response({"msg":"Successfully deleted"})
        

    

        

class Register(APIView):

    permission_classes = [permissions.AllowAny]
    
    def post(self,request):
        userInfs = {
            "first_name" : request.data["first_name"],
            "last_name"  : request.data["last_name"],
            "email": request.data["email"],
            "birth_date" : request.data["birth_date"],
            'password1': request.data['password1'],
            'password2': request.data['password2']
        }
        print(userInfs)
        form = CustomUserCreationForm(userInfs)
        if form.is_valid():
            user = form.save()
            refresh = RefreshToken.for_user(user)
           
            return Response({"access": str(refresh.access_token),"refresh" : str(refresh)})
        else:
            messages_list = [msg for key,messages in form.errors.items() for msg in messages]
            return Response({"Error":messages_list},status=status.HTTP_400_BAD_REQUEST)
        
class ChangePassword(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self,request):
        print(request.data)
        if request.user.check_password(request.data["oldPassword"]):
            try:
                validate_password(password = request.data["newPassword"],user = CustomUser)
            except Exception as e:
                Errormessages = list(e.messages)
                return Response({"errors":Errormessages},status=status.HTTP_400_BAD_REQUEST)
            request.user.set_password(request.data["newPassword"])
            request.user.save()
            return Response({"msg":"Votre mot de passe a ete change..."})
        else:
            return Response({"errors":['Le mot de passe fourni ne correspond pas a votre mot de passe actuel!']},status=HTTP_400_BAD_REQUEST)


