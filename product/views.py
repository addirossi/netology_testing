from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import Product, Comment
from .permissions import IsAuthorPermission, IsAuthorOrAdmin
from .serializers import ProductSerializer, CommentSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissions = [IsAuthenticated, IsAdminUser]
        else:
            permissions = []
        return [perm() for perm in permissions]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    #создать коммент может только залогиненный пользователь
    #редактировать может только автор
    #удалить может автор или админ
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated()]
        elif self.action in ['update', 'partial_update']:
            permissions =  [IsAuthorPermission()]
        elif self.action == 'destroy':
            permissions = [IsAuthorOrAdmin()]
        else:
            permissions = []
        return permissions


@api_view(['GET'])
def sample_view(request):
    return Response({'status': 'OK!'})
