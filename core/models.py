from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from unicodedata import decimal
from pyexpat import model
from email.policy import default
from django.utils.text import slugify
from tinymce.models import HTMLField
from django.urls import reverse


STATUS_CHOICE = (
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

STATUS = (
    ("disabled", "Disabled"),
    ("published", "Published"),
)

ACTIVE_STATUS = (
    ("disabled", "Disabled"),
    ("published", "Published"),
)

COURIER_PARTNER = (
    ("dtdc", "DTDC"),
    ("trackon", "Trackon"),
)

RATING = (
    ("1", "★"),
    ("2", "★★"),
    ("3", "★★★"),
    ("4", "★★★★"),
    ("5", "★★★★★"),
)

COLOR = (
    ("red", "Red"),
    ("black", "Black"),
    ("pink", "Pink"),
    ("blue", "Blue"),
    ("orange", "Orange"),
)

APPROVE = (
    ("approved", "Approved"),
    ("not approved", "Not Approved"),
)

def user_directory_path(instance, filename):
    user_id = instance.user.id if instance.user else 'unknown'
    return 'user_{0}/{1}'.format(user_id, filename)

def product_variant_type_image_upload_path(instance, filename):
    return f'product_variant_type_{instance.product_variant_type.id}/{filename}'



class Main_category(models.Model):
    mid = ShortUUIDField(unique=True, max_length=30, prefix="main_cat", alphabet="abcdefgh12345")
    main_title = models.CharField(max_length=100)
    description = models.CharField(max_length=500, default="N/A")
    meta_description = models.CharField(max_length=100, default="N/A")
    meta_title = models.CharField(max_length=100, default="N/A")
    meta_tag = models.CharField(max_length=100, default="N/A")
    active_status = models.CharField(choices=ACTIVE_STATUS, max_length=10, default="disabled")
    image = models.ImageField(upload_to="category",default="maincategory.jpg")
    banner_image = models.ImageField(upload_to="category",default="maincategorybanner.jpg")

    class Meta:
        verbose_name_plural = "Main Categories"

    def main_category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def main_category_banner_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.banner_image.url))
    
    def main_category_icon_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.icon_img.url))
    
    def get_absolute_url(self):
        return reverse('core:main_category', kwargs={'main_title': str(self.main_title)})
    
    def __str__(self):
        return self.main_title
    
class Category(models.Model):
    cid = ShortUUIDField(unique=True, max_length=30, prefix="cat", alphabet="abcdefgh12345")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    main_category = models.ForeignKey(Main_category, on_delete=models.SET_NULL, null=True)
    cat_title = models.CharField(max_length=100, default="Mobile & Laptop")
    category_slug = models.SlugField(unique=True, max_length=150, blank=True, null=True)
    meta_description = models.CharField(max_length=100)
    meta_title = models.CharField(max_length=100)
    meta_tag = models.CharField(max_length=100)
    home_page_display = models.CharField(choices=APPROVE, max_length=25, default="not approved")
    image = models.ImageField(upload_to=user_directory_path, default="category.jpg")
    home_image = models.ImageField(upload_to=user_directory_path, default="home_img.jpg")
    big_image = models.ImageField(upload_to=user_directory_path, default="bigcategory.jpg")


    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def category_big_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.big_image.url))
    
    def category_home_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.home_image.url))
    
    def save(self, *args, **kwargs):
        if not self.category_slug:
            self.category_slug = slugify(self.cat_title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('core:main_category', kwargs={'category_slug': self.category_slug})
    
    def __str__(self):
        return self.cat_title
    

class Ingredients(models.Model):
    iid = ShortUUIDField(unique=True, max_length=30, prefix="ingred_", alphabet="abcdefgh12345")
    ingredient_title = models.CharField(max_length=100)
    description = models.CharField(max_length=500, default="N/A")
    meta_description = models.CharField(max_length=100, default="N/A")
    meta_title = models.CharField(max_length=100, default="N/A")
    meta_tag = models.CharField(max_length=100, default="N/A")
    active_status = models.CharField(choices=ACTIVE_STATUS, max_length=10, default="published")
    image = models.ImageField(upload_to="category",default="maincategory.jpg")
    banner_image = models.ImageField(upload_to="category",default="maincategorybanner.jpg")

    class Meta:
        verbose_name_plural = "Shop Ingredients"

    def ingredient_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def ingredient_banner_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.banner_image.url))
    
    def __str__(self):
        return self.ingredient_title
    
class Concern(models.Model):
    ccid = ShortUUIDField(unique=True, max_length=30, prefix="concern_", alphabet="abcdefgh12345")
    concern_title = models.CharField(max_length=100)
    product_link = models.CharField(max_length=100, default="N/A")
    active_status = models.CharField(choices=ACTIVE_STATUS, max_length=10, default="published")

    class Meta:
        verbose_name_plural = "Shop By Concern"
    
    def __str__(self):
        return self.concern_title
    

class BannerHome(models.Model):
    bhid = ShortUUIDField(unique=True, max_length=30, prefix="bhid", alphabet="abcdefgh12345")
    banner_title = models.CharField(max_length=100, blank=True)
    active_status = models.CharField(choices=ACTIVE_STATUS, max_length=10, default="disabled")
    order = models.CharField(max_length=10, default="0")
    banner_image = models.ImageField(upload_to="category", default="homebanner.jpg")

    class Meta:
        verbose_name_plural = "Banners and Sliders"
    
    def display_banner_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.banner_image.url))
    
    def __str__(self):
        return self.banner_title
    

class Tags(models.Model):
    pass    
    

class Product(models.Model):
    pid = ShortUUIDField(unique=True, max_length=30, prefix="sub_cat", alphabet="abcdefgh12345")
    main_category = models.ForeignKey(Main_category, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=500, default="Treseme..")
    packing_size = models.CharField(max_length=500, default="Box 100 Pcs")
    form = models.CharField(max_length=500, default="Liquid")
    type = models.CharField(max_length=500, default="Dandruff Control...")
    minimum_order_qty = models.CharField(max_length=500, default="1")
    hsn_code = models.CharField(max_length=100, default="5305")
    gst_rate = models.CharField(max_length=100, default="18%")
    product_slug = models.SlugField(unique=True, max_length=150, blank=True, null=True)
    price = models.DecimalField(max_digits=9999, decimal_places=2, default="1")
    old_price = models.DecimalField(max_digits=9999, decimal_places=2, default="2")
    product_status = models.CharField(choices=STATUS, max_length=10, default="published")
    in_stock = models.BooleanField(default=True)
    summer_sale= models.BooleanField(default=False)
    new_arrival= models.BooleanField(default=False)
    yellow_peel= models.BooleanField(default=False)
    sku = ShortUUIDField(unique=True, max_length=7, prefix="sku", alphabet="12345678900")
    date = models.DateTimeField(auto_now_add=True)
    youtube_link = models.CharField(max_length=12000, default="1")
    youtube_content = models.CharField(max_length=12000, default="100percent free from..")
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg")

    class Meta:
        verbose_name_plural = "Product"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.product_slug:
            self.product_slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:product', kwargs={'product_slug': self.product_slug})
    
    def get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price
    
class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images", default="product.jpg")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Images"

class ProductDescription(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_description = HTMLField(blank=True)
    reasons_to_love = HTMLField(blank=True)
    key_active_ingredients = HTMLField(blank=True)
    safety_warnings = HTMLField(blank=True)
    infusion_of_ingredients = HTMLField(blank=True)
    direction_for_use = HTMLField(blank=True)
    for_your_ease = HTMLField(blank=True)
    more_reasons_to_love = HTMLField(blank=True)

    class Meta:
        verbose_name_plural = "Product Description"

class ProductSeo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    canonical_link = models.CharField(max_length=500, default="N/A")
    meta_description = models.CharField(max_length=500, default="N/A")
    meta_title = models.CharField(max_length=500, default="N/A")
    meta_tag = models.CharField(max_length=500, default="N/A")
    meta_robots = models.CharField(max_length=500, default="N/A")
    og_url = models.CharField(max_length=500, default="N/A")
    og_title = models.CharField(max_length=500, default="N/A")
    og_description = models.CharField(max_length=500, default="N/A")
    og_image = models.CharField(max_length=500, default="N/A")
    twitter_title = models.CharField(max_length=500, default="N/A")
    twitter_description = models.CharField(max_length=500, default="N/A")
    twitter_description = models.CharField(max_length=500, default="N/A")

    class Meta:
        verbose_name_plural = "Product Seo"


class ProductVarient(models.Model):
    pvid = ShortUUIDField(unique=True, max_length=30, prefix="pvid", alphabet="abcdefgh12345") 
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=500, default="Product Varient")
    status = models.BooleanField(default=True)
    sku = ShortUUIDField(unique=True, max_length=50, prefix="sku", alphabet="12345678900")

    class Meta:
        verbose_name_plural = "Product Varient"

    def variant_images(self):
        return ProductVariantTypes.objects.filter(product_variant=self)
    
    def __str__(self):
        return self.title

    def product_varient_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    

class ProductVariantTypes(models.Model):
    product_variant = models.ForeignKey(ProductVarient, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    variant_title = models.CharField(max_length=500, default="Product Varient")
    varient_price = models.DecimalField(max_digits=9999, decimal_places=2, default="1")
    gst_rate = models.CharField(max_length=12, default="5%")
    packaging_size = models.CharField(max_length=100, default="Packaging Size")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.variant_title

    class Meta:
        verbose_name_plural = "Product Variant Types"

class ProductVariantTypeImages(models.Model):
    product_variant_type = models.ForeignKey(ProductVariantTypes, related_name='images', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to=product_variant_type_image_upload_path)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product_variant_type.variant_title}"

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    class Meta:
        verbose_name_plural = "Product Variant Type Images"

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=99999, decimal_places=2, default="1")
    courier_partner = models.CharField(choices=COURIER_PARTNER, max_length=30, default="trackon")
    tracking_id = models.CharField(max_length=100, default="145855..")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")

    class Meta:
        verbose_name_plural = "Cart Orders"

        verbose_name_plural = "Cart Order"


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=99999, decimal_places=2, default="1")
    total = models.DecimalField(max_digits=99999, decimal_places=2, default="1")

    class Meta:
        verbose_name_plural = "Cart Order Items"

    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image.url))   

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "Wishlists"

    def __str__(self):
        return self.product.title


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"


class InternationalShipping(models.Model):
    international_shipping_content = HTMLField()


    class Meta:
        verbose_name_plural = "International Shipping"


class Blogs(models.Model):
    blog_title = models.CharField(max_length=100)
    blog_image = models.ImageField(upload_to="blogs-images", default="blogs.jpg")
    blog_slug = models.SlugField(unique=True, max_length=150, blank=True, null=True) 
    blog_description = HTMLField()   
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Blogs"

class InvoiceNumber(models.Model):
    number = models.IntegerField(default=1)

    def increment(self):
        self.number += 1
        self.save()

    def __str__(self):
        return f'Invoice No: INW2324-{self.number:04d}'
    
class Testimonials(models.Model):
    testimonial_name = models.CharField(max_length=100)
    testimonial_image = models.ImageField(upload_to="blogs-images", default="testimonial.jpg")
    testimonial = HTMLField()   
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Testimonials"