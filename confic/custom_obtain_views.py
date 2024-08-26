from typing import Dict, Any

from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

from shop import serializers
from shop.serializers import RegisterSerializer, LoginSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
        token_class = RefreshToken

        def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
            data = super().validate(attrs)

            refresh = self.get_token(self.user)

            data['tokens'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }

            data['user'] = {
                'username': self.user.username,
                'message': True
            }

            data.pop('refresh')
            data.pop('access')

            return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



# class RegistrationAPIView(APIView):
#     '''Registers user'''
#     serializer_class = RegisterSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         data = {}
#         if serializer.is_valid(raise_exception=True):
#             user = serializer.save()
#             send_email(serializer.data['email'])
#             data['response'] = "Registration Successful!"
#             refresh = RefreshToken.for_user(user=user)
#             data['refresh'] = str(refresh)
#             data['access'] = str(refresh.access_token)
#
#         return Response(data, status.HTTP_201_CREATED)
# #

# class LoginTokenGenerationAPIView(APIView):
#
#     def post(self, request, *args, **kwargs):
#         serializer = LoginTokenGenerationSerializer(data=request.data)
#         data = {}
#
#         if serializer.is_valid(raise_exception=True):
#
#             email = serializer.data['email']
#             password = serializer.data['password']
#             user_obj = User.objects.get(email=email)
#             try:
#                 if user_obj is not None:
#                     access_token = AccessToken.for_user(user=user_obj)
#                     refresh_token = RefreshToken.for_user(user=user_obj)
#                     data['refresh'] = str(access_token)
#                     data['access'] = str(refresh_token)
#             except Exception as e:
#                 return Response({'message': 'username or password is incorrect'})
#         return Response(data, status.HTTP_200_OK)




class RegisterObtainPairSerializer(RegisterSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)