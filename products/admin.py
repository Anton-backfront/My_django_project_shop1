from django.contrib import admin
from products.models import Product, ProductCategory, Basket, Color, Size, Gallery
from .models import HomepageText
from .forms import ProductForm
from django.utils.safestring import mark_safe
from django.db.models import Sum
from .models import SliderImage


class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery
    extra = 1



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ('name', 'price', 'quantity', 'category', 'display_available_sizes', 'display_available_colors', 'get_photo')
    fields = ('name', 'description', 'price', 'quantity', 'category', 'available_sizes', 'available_colors', 'slug')
    list_display_links = ('name',)
    list_filter = ('name', 'price', 'category')
    ordering = ('category',)
    search_fields = ('name', 'category')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [GalleryInline]

    def get_photo(self, obj):
        if obj.images:
            try:
                return mark_safe(f'<img src="{obj.images.all()[0].image.url}" width="75">')
            except:
                return '-'
        else:
            return '-'

    get_photo.short_description = 'Миниатюра'

    def display_available_sizes(self, obj):
        return ", ".join([str(size) for size in obj.available_sizes.all()])

    def display_available_colors(self, obj):
        return ", ".join([str(color) for color in obj.available_colors.all()])

    display_available_sizes.short_description = 'Available Sizes'
    display_available_colors.short_description = 'Available Colors'




class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 1


# @admin.register(ProductCategory)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description', 'get_products_count')
#
#
#     def get_products_count(self, obj):
#         if obj.products:
#             return str(len(obj.products.all()))
#         else:
#             return '0'
#     get_products_count.short_description = 'Количество товаров'

@admin.register(ProductCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'get_products_count')

    def get_products_count(self, obj):
        total_quantity = obj.products.aggregate(total_quantity=Sum('quantity'))['total_quantity']
        return str(total_quantity) if total_quantity else '0'

    get_products_count.short_description = 'Количество товаров'


@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    list_display = ('get_photo',)

    def get_photo(self, obj):
        if obj.image:
            try:
                return mark_safe(f'<img src="{obj.image.url}" width="75">')
            except:
                return '-'
        else:
            return '-'

    get_photo.short_description = 'Миниатюра'


admin.site.register(HomepageText)
admin.site.register(Color)
admin.site.register(Size)


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('get_photo',)

    def get_photo(self, obj):
        if obj.image:
            try:
                return mark_safe(f'<img src="{obj.image.url}" width="75">')
            except:
                return '-'
        else:
            return '-'

    get_photo.short_description = 'Миниатюра'

