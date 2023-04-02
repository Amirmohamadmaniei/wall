from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, UserChangePasswordSerializer, UserRegisterSerializer
from rest_framework import status
from permissions import NotAuthenticated, IsOwner
from ad.serializers import ADSerializer
from ad.models import AD


class RegisterUserView(APIView):
    permission_classes = (NotAuthenticated,)

    def post(self, request):
        ser = UserRegisterSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    def get(self, request):
        ser = UserSerializer(instance=request.user)
        return Response(ser.data, status=status.HTTP_200_OK)


class ProfileUpdateView(APIView):
    def put(self, request):
        ser = UserSerializer(instance=request.user, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    def put(self, request):
        ser = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        if ser.is_valid():
            request.user.set_password(ser.validated_data['password1'])
            request.user.save()
            return Response({'response': 'password changed'}, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class UserADView(APIView):
    permission_classes = (IsOwner,)

    def get(self, request):
        ADs = AD.objects.filter(user=request.user)
        ser = ADSerializer(instance=ADs, many=True, context={'request': request})
        return Response(ser.data, status=status.HTTP_200_OK)
