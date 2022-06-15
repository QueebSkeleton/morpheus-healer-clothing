from django.contrib import admin

from .models import Category, Product, ProductImage, Order, OrderItem

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name',)
    search_fields = ('slug', 'name',)

    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    min_num = 1
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'units_in_stock', 'enabled',)
    
    prepopulated_fields = {'stock_keeping_unit': ('title',)}
    inlines = [ProductImageInline,]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    min_num = 1
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('placed_by', 'billing_address', 'shipping_address', 'status', 'get_total')
    list_filter = ('status',)

    inlines = [OrderItemInline,]

    def get_queryset(self, request):
        queryset = super(OrderAdmin, self).get_queryset(request)
        return queryset.prefetch_related('orderitem_set')

    @admin.display
    def placed_by(self, obj):
        return obj.placed_by.first_name + ' ' + obj.placed_by.last_name
