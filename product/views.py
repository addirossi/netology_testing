from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from product.models import Product, Comment
from product.serializers import ProductSerializer, CommentSerializer


@api_view(['GET'])
def simple_view(request):
    return Response('Hello world!')

#Создание, редактирование и удаление продукта осуществляется администратором
class CreateProductView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]


class ProductsListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class DeleteProductView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

#Комментарий может оставить авторизованный пользователь, изменить и удалить только автор

class CreateCommentView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]