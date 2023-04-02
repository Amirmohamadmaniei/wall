from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .models import AD, Image
from .serializers import ADSerializer, ImageSerializer, ImageUpdateSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from permissions import IsOwner, IsOwnerImage


class ADListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        ADs = AD.objects.all()
        pagination = PageNumberPagination()
        ADs = pagination.paginate_queryset(queryset=ADs, request=request)
        ser = ADSerializer(instance=ADs, many=True, context={'request': request})
        return Response(ser.data, status=status.HTTP_200_OK)


class ADDetailView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        ad = get_object_or_404(AD, pk=pk)
        ser = ADSerializer(instance=ad, context={'request': request})
        return Response(ser.data, status=status.HTTP_200_OK)


class ADCreateView(APIView):
    def post(self, request):
        ser = ADSerializer(data=request.data, context={'request': request})
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class ADUpdateView(APIView):
    permission_classes = (IsOwner,)

    def put(self, request, pk):
        ad = get_object_or_404(AD, pk=pk)
        self.check_object_permissions(request, ad)

        ser = ADSerializer(instance=ad, data=request.data, partial=True, context={'request': request})
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.data, status=status.HTTP_400_BAD_REQUEST)


class ADDelete(APIView):
    permission_classes = (IsOwner,)

    def delete(self, request, pk):
        ad = get_object_or_404(AD, pk=pk)
        self.check_object_permissions(request, ad)

        ad.delete()
        return Response({'response': 'Deleted'}, status=status.HTTP_200_OK)


class AdSearchView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        q = request.query_params['q']
        ADs = AD.objects.filter(title__icontains=q)

        pagination = PageNumberPagination()
        ADs = pagination.paginate_queryset(queryset=ADs, request=request)

        ser = ADSerializer(instance=ADs, many=True, context={'request': request})
        return Response(ser.data, status=status.HTTP_200_OK)


class ImageUpdateView(APIView):
    permission_classes = (IsOwnerImage,)

    def put(self, request, pk):
        img = get_object_or_404(Image, pk=pk)
        self.check_object_permissions(request, img)

        ser = ImageUpdateSerializer(instance=img, data=request.FILES)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageDeleteView(APIView):
    permission_classes = (IsOwnerImage,)

    def delete(self, request, pk):
        img = get_object_or_404(Image, pk=pk)
        self.check_object_permissions(request, img)

        img.delete()
        return Response({'response': 'Deleted'})
