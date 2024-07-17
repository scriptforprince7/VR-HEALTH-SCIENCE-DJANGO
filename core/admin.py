from django.contrib import admin
from core.models import *
import csv
from django.urls import path
from django.http import HttpResponse
from .forms import ExportCartOrdersForm

class ProductSeoAdmin(admin.StackedInline):
    model = ProductSeo
    extra = 0
    fields = (
        'canonical_link',
        'meta_description',
        'meta_title',
        'meta_tag',
        'meta_robots',
        'og_url',
        'og_title',
        'og_description',
        'og_image',
        'twitter_title',
        'twitter_description',
    )

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages
    extra = 0

class ProductDescriptionAdmin(admin.StackedInline):
    model = ProductDescription
    extra = 0

class ProductVariantTypeImagesAdmin(admin.StackedInline):
    model = ProductVariantTypeImages
    extra = 0

class ProductVariantTypesAdmin(admin.StackedInline):
    model = ProductVariantTypes
    extra = 0  # This allows adding multiple images at once in the admin
    inlines = [ProductVariantTypeImagesAdmin]

class ProductVarientAdmin(admin.StackedInline):
    model = ProductVarient
    extra = 0
    inlines = [ProductVariantTypesAdmin]

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin, ProductVarientAdmin, ProductVariantTypesAdmin, ProductVariantTypeImagesAdmin, ProductDescriptionAdmin]
    list_display = ['main_category','title', 'product_slug', 'packing_size', 'price', 'product_status']
    list_filter = ['main_category', 'category', 'product_status'] 
    search_fields = ['title', 'description'] 

class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ['main_title', 'image', 'description', 'banner_image']  

class IngredientAdmin(admin.ModelAdmin):
    list_display = ['ingredient_title', 'image', 'description', 'banner_image']   

class BannerAdmin(admin.ModelAdmin):
    list_display = ['banner_title', 'active_status', 'order', 'display_banner_image']  

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['main_category', 'cat_title', 'meta_description', 'meta_title', 'meta_tag', 'home_page_display', 'image', 'big_image']
    list_filter = ['main_category']  # Fields to filter by

class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ['paid_status', 'product_status', 'tracking_id']
    list_display = ['user', 'price', 'paid_status', 'order_date', 'tracking_id', 'product_status']
    change_list_template = "core/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export/', self.admin_site.admin_view(self.export_cart_orders_csv), name='export_cart_orders_csv'),
        ]
        return custom_urls + urls
        

    def export_cart_orders_csv(self, request):
        form = ExportCartOrdersForm(request.GET)
        if form.is_valid():
            orders = CartOrder.objects.all()
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            paid_status = form.cleaned_data.get('paid_status')

            if start_date and end_date:
                orders = orders.filter(order_date__range=[start_date, end_date])
            elif start_date:
                orders = orders.filter(order_date__gte=start_date)
            elif end_date:
                orders = orders.filter(order_date__lte=end_date)

            if paid_status:
                orders = orders.filter(paid_status=(paid_status == 'True'))

        else:
            orders = CartOrder.objects.all()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="cart_orders.csv"'
        writer = csv.writer(response)
        writer.writerow(['User', 'Price', 'Courier Partner', 'Tracking ID', 'Paid Status', 'Order Date', 'Product Status'])
        for order in orders.values_list('user__username', 'price', 'courier_partner', 'tracking_id', 'paid_status', 'order_date', 'product_status'):
            writer.writerow(order)

        return response

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item', 'image', 'qty', 'price', 'total']

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating'] 

class wishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'status']   

class InternationalShippingAdmin(admin.ModelAdmin):
    list_display = ['international_shipping_content']     

class BlogsAdmin(admin.ModelAdmin):
    list_display = ['blog_title', 'blog_image', 'blog_description']  

class TestimonialsAdmin(admin.ModelAdmin):
    list_display = ['testimonial_name', 'testimonial', 'testimonial_image']        

admin.site.register(Product, ProductAdmin)
admin.site.register(Main_category, MainCategoryAdmin)
admin.site.register(Ingredients, IngredientAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, wishlistAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(InternationalShipping, InternationalShippingAdmin)
admin.site.register(Blogs, BlogsAdmin)
admin.site.register(Testimonials, TestimonialsAdmin)
admin.site.register(BannerHome, BannerAdmin)

