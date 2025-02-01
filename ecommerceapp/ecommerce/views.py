from rest_framework.parsers import MultiPartParser
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from . import serializers
from .models import Seller, Product, Category, User
from .paginators import CategoryPagination
from .serializers import SellerSerializer, CategorySerializer, ProductSerializer, UserSerializer


def index(request):
    return render(request, template_name='index.html', context={
        'name':'Duy Chinh'
    })

class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    # cau truy van
    serializer_class = SellerSerializer
    # List (get) -> xem danh sach
    # Detail -> xem chi tiet
    # list (post) -> them moi'
    # ... (put) -> cap nhat
    # delete -> xoa
    permission_classes = [permissions.IsAuthenticated]
    # isAuthenticated => bat buoc o trang thai User da dang nhap

    @action(methods=['get'], detail=True, url_path='products_by_store')
    def get_products_by_store(self, request, pk):
        products = self.get_object().products.filter(active=True)
        return Response(serializers.ProductSerializer(products, many=True).data)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(active=True)
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination


    # def get_permissions(self):
    #     if self.action == 'list':
    #         return [permissions.AllowAny()]
    #
    #     return [permissions.IsAuthenticated()]

    @action(methods=['get'], url_path='products', detail=True)
    def get_products(self, request, pk):
        products = self.get_object().products.filter(active=True)
        return Response(serializers.ProductSerializer(products, many=True).data)

    # /category/category_id/products

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(active=True)
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.queryset
        kw = self.request.query_params.get("q")
        if kw:
            query = query.filter(product_name__icontains=kw)

        return query

class UserViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]
        
    @action(methods=['get'], detail=False, url_path='current_user')
    def get_current_user(self, request):
        return Response(serializers.UserSerializer(request.user).data)
        
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    @action(methods=['get'], detail=False, url_path='(?P<rating>[0-9]+)/get_products_by_reviews')
    def get_products(self, request, rating=None):
        products = Product.objects.filter(ratings__rating=rating).distinct()
        return Response(serializers.ProductSerializer(products, many=True, context={'request': request}).data)


def welcome(request, year):
    return HttpResponse("HELLO " + str(year))

class TestView(View):
    def get(self, request):
        return HttpResponse("WELCOME TESTING GET")

    def post(self, request):
        pass

# Create your views here.
