

from django.contrib import admin
from django.urls import path, include
from . import views
from .admin import admin_site
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('sellers', views.SellerViewSet, basename='seller')
router.register('categories', views.CategoryViewSet, basename='category')
router.register('products', views.ProductViewSet, basename='product')
router.register('users', views.UserViewSet, basename='user')
router.register('reviews', views.ReviewViewSet, basename='review')

# /seller/ - GET
# /seller/ - POST
# /seller/{seller_id} - GET
# /seller/{seller_id} - PUT
# /seller/{seller_id} - DELETE
# path('admin/', admin.site.urls)
urlpatterns = [
    path('', include(router.urls))

]
