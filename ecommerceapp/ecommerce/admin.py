from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django.contrib.auth.models import Permission
from unicodedata import category
from django.utils.html import mark_safe
from .models import Category, Product, Cart, CartItem, Order, OrderDetail, Seller, Review, Payment, User
from django import forms
# Register your models here.

class CartItemAdminInline(admin.StackedInline):
    model = CartItem
    fk_name = 'cart'

class ProductCategoryInlineAdmin(admin.TabularInline):
    model = Product.categories.through

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'description', 'price', 'stock', 'get_categories']
    search_fields = ['product_name', 'categories__category_name']
    list_filter = ['categories']
    readonly_fields = ['avatar']
    inlines = [ProductCategoryInlineAdmin, ]

    def avatar(self, product):
        print(product.images.name)
        return mark_safe(f"<img src='/static/{product.images.name}' width='200' />")


    def get_categories(self, obj):
        return ','.join([category.category_name for category in obj.categories.all()])
    get_categories.short_description = 'Categories'

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['category_name']
    # inlines = [ProductCategoryInlineAdmin, ]

class ReviewForm(forms.ModelForm):
    review = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Review
        fields = '__all__'

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'review', 'rating', 'product']
    form = ReviewForm

class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemAdminInline, ]


class EcommerceAppAdminSite(admin.AdminSite):
    site_header = 'E-COMMERCE APP'

admin_site = EcommerceAppAdminSite('myecommerceapp')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Seller)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Payment)
admin.site.register(User)
admin.site.register(Permission)

# admin_site.register(Category, CategoryAdmin)
# admin_site.register(Product, ProductAdmin)
# admin_site.register(Cart, CartAdmin)
# admin_site.register(CartItem)
# admin_site.register(Order)
# admin_site.register(OrderDetail)
# admin_site.register(Seller)
# admin_site.register(Review, ReviewAdmin)
# admin_site.register(Payment)
# admin_site.register(User)
