from django.contrib import admin
from django.urls import reverse_lazy
from django.utils.html import mark_safe

from django_summernote import admin as summernote_admin

from .models import Address, Category, Product, ProductImage, Order, OrderItem


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user__name', 'address_info',)

    search_fields = ('id', 'user__last_name', 'user__first_name',)

    def get_queryset(self, request):
        queryset = super(AddressAdmin, self).get_queryset(request)
        return queryset.select_related('user')

    @admin.display
    def user__name(self, obj):
        return '%s %s' % (obj.user.first_name, obj.user.last_name)

    @admin.display
    def address_info(self, obj):
        return '%s, %s, %s %s' % (obj.street, obj.city, obj.postal_code,
                                  obj.province)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name',)
    search_fields = ('slug', 'name',)

    fields = ('name', 'slug', 'description',)
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    min_num = 1
    extra = 0


@admin.register(Product)
class ProductAdmin(summernote_admin.SummernoteModelAdmin):
    list_display = ('title', 'units_in_stock', 'enabled',)

    fieldsets = ((None, {'fields': ('category', 'title', 'body',)}),
                 ('Stock Information', {'fields': ('stock_keeping_unit',
                                                   'unit_cost',
                                                   'unit_price',
                                                   'units_in_stock',
                                                   'enabled')}),)
    prepopulated_fields = {'stock_keeping_unit': ('title',)}
    inlines = [ProductImageInline, ]
    summernote_fields = ('body',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    min_num = 1
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('placed_by', 'billing_address',
                    'shipping_address', 'status', 'get_total', 'invoice')
    list_filter = ('status',)

    inlines = [OrderItemInline, ]

    def get_queryset(self, request):
        queryset = super(OrderAdmin, self).get_queryset(request)
        return queryset.prefetch_related('orderitem_set')

    @admin.display
    def placed_by(self, obj):
        return obj.placed_by.first_name + ' ' + obj.placed_by.last_name

    @admin.display
    def invoice(self, obj):
        return mark_safe('<a href="/profile/orders/' + str(obj.id)
                         + '/invoice/" target="_blank">PDF</a>')
