from django.contrib import admin

from .models import Category, Product, Variant

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name',)
    search_fields = ('slug', 'name',)

    fields = ('name', 'slug', 'description',)
    prepopulated_fields = {'slug': ('name',)}


class VariantInline(admin.StackedInline):
    model = Variant
    extra = 0
    min_num = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'enabled',)
    
    fields = ('name', 'slug', 'category', 'description', 'enabled',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [VariantInline]

