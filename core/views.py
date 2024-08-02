from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from core.models import *
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import Http404
import os
import requests
from django.db.models import Case, When, Value, IntegerField
from django.views.generic import View
import razorpay
from django.db import transaction
from datetime import datetime 
import csv
from decimal import Decimal, ROUND_HALF_UP
import re
from django.http import QueryDict
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags    
from num2words import num2words
from bs4 import BeautifulSoup
from indian_pincode_details import get_pincode_details
import indiapins
import json
import pdfkit
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from xhtml2pdf import pisa
from io import BytesIO
from django.contrib.auth.models import User
from instamojo_wrapper import Instamojo
from core.forms import *
from django.http import HttpResponseBadRequest
from decimal import Decimal, ROUND_HALF_UP

api = Instamojo(api_key=settings.API_KEY,
                auth_token=settings.AUTH_TOKEN, endpoint='https://www.instamojo.com/api/1.1/')


def index(request):
    categories = Category.objects.filter(home_page_display='approved')
    home_banner = BannerHome.objects.filter(active_status='published').order_by('order')
    new_arrival = Product.objects.filter(new_arrival=True, product_status='published')
    yellow_peel = Product.objects.filter(yellow_peel=True)
    summer_sale = Product.objects.filter(summer_sale=True)
    testimonials = Testimonials.objects.all()

    new_arrival_main_categories = Main_category.objects.filter(product__in=new_arrival).distinct()

    # Fetching product variants and variant types for products in summer sale
    product_variants = ProductVarient.objects.filter(product__in=summer_sale)
    product_variant_types = ProductVariantTypes.objects.filter(product_variant__product__in=summer_sale)

    for product in new_arrival:
    # Calculate the default price including GST and round off to two decimal places
        product.gst_inclusive_price = product.price
        product.variant_price = None
        product.first_variant_type_title = None
        product.first_variant_type_id = None


         # Iterate over products in new arrival to determine prices
    for product in yellow_peel:
    # Check if the product has variants
        product_has_variants = product.productvarient_set.exists()

        if product_has_variants:
        # Get the first variant
            first_variant = product.productvarient_set.first()
            first_variant_type = first_variant.productvarianttypes_set.first()

            product.first_variant_type_title = first_variant_type.variant_title if first_variant_type else None
            product.first_variant_type_id = first_variant_type.id if first_variant_type else None

            # Calculate default price without GST
            price_wo_gst = first_variant_type.varient_price if first_variant_type else product.price
            # Fetching GST rate
            gst_rate = first_variant_type.gst_rate if first_variant_type else product.gst_rate
            # Calculate default price including GST
            base_price = first_variant_type.varient_price if first_variant_type else product.price
            # Calculate GST amount
            gst_amount = base_price * Decimal(gst_rate.strip('%')) / 100
        # Calculate total price including GST and round off to two decimal places
            product.gst_inclusive_price = round(base_price + gst_amount, 2)
        # Include original variant price in the context
            product.variant_price = price_wo_gst
        else:
        # Use the existing price for the product if it doesn't have variants
            product.gst_inclusive_price = product.price * (1 + Decimal(product.gst_rate.strip('%')) / 100)
            product.variant_price = None
            product.first_variant_type_title = None
            product.first_variant_type_id = None


    context = {
        "category": categories,
        "new_arrival": new_arrival,
        "yellow_peel": yellow_peel,
        "summer_sale": summer_sale,
        "home_banner": home_banner,
        # "product": product,
        "new_arrival_main_categories":new_arrival_main_categories,
        "product_variants": product_variants,
        "product_variant_types": product_variant_types,
        "testimonials": testimonials,
    }

    return render(request, 'core/index.html', context)


def main_category(request, category_slug):
    categories = Category.objects.get(category_slug=category_slug)
    products = Product.objects.filter(category=categories, product_status='published')
    product_images = ProductImages.objects.filter(product__in=products)

    product_variants = ProductVarient.objects.filter(product__in=products)
    variant_types = ProductVariantTypes.objects.filter(product_variant__in=product_variants)

    prices = products.values_list('price', flat=True)
    min_price = min(prices) if prices else 0
    max_price = max(prices) if prices else 0

    min_price_filter = float(request.GET.get('min_price', min_price))
    max_price_filter = float(request.GET.get('max_price', max_price))

    if min_price_filter and max_price_filter:
        products = products.filter(price__range=(min_price_filter, max_price_filter))

    gst_rate = None

    for product in products:
        product_has_variants = product.productvarient_set.exists()

        if product_has_variants:
            first_variant = product.productvarient_set.first()
            first_variant_type = first_variant.productvarianttypes_set.first() if first_variant.productvarianttypes_set.exists() else None

            product.first_variant_type_title = first_variant_type.variant_title if first_variant_type else None
            product.first_variant_type_id = first_variant_type.id if first_variant_type else None
            
            price_wo_gst = first_variant_type.varient_price if first_variant_type else product.price
            gst_rate = first_variant_type.gst_rate if first_variant_type else product.gst_rate
            base_price = first_variant_type.varient_price if first_variant_type else product.price
            gst_amount = base_price * Decimal(gst_rate.strip('%')) / 100
            product.gst_inclusive_price = round(base_price + gst_amount, 2)
            product.variant_price = price_wo_gst
        else:
            product.gst_inclusive_price = product.price * (1 + Decimal(product.gst_rate.strip('%')) / 100)
            gst_rate = product.gst_rate
            product.variant_price = None
            product.first_variant_type_title = None
            product.first_variant_type_id = None

    context = {
        "categories": categories,
        "products": products,
        "product_images": product_images,
        "min_price": min_price,
        "max_price": max_price,
        "min_price_filter": min_price_filter,
        "max_price_filter": max_price_filter,
        "product_variants": product_variants,
        "variant_types": variant_types,
        "gst_rate": gst_rate,
    }

    return render(request, "core/main_category.html", context)




def expert_series(request):
    main_categories = Main_category.objects.filter(mid="main_cat5323f35gfd54af15aba54g")
    products = Product.objects.filter(main_category__in=main_categories)
    product_images = ProductImages.objects.filter(product__in=products)

    product_variants = ProductVarient.objects.filter(product__in=products)
    variant_types = ProductVariantTypes.objects.filter(product_variant__in=product_variants)

    prices = products.values_list('price', flat=True)
    min_price = min(prices) if prices else 0
    max_price = max(prices) if prices else 0

    price_range = request.GET.get('price_range')
    if price_range:
        min_price, max_price = map(float, price_range.split(','))
        products = products.filter(price__range=(min_price, max_price))

    gst_rate = None  # Initialize gst_rate here

    # Fetching variant details for products
    for product in products:
        # Check if the product has variants
        product_has_variants = product.productvarient_set.exists()

        if product_has_variants:
            # Get the first variant
            first_variant = product.productvarient_set.first()
            first_variant_type = first_variant.productvarianttypes_set.first() if first_variant.productvarianttypes_set.exists() else None

            product.first_variant_type_title = first_variant_type.variant_title if first_variant_type else None
            product.first_variant_type_id = first_variant_type.id if first_variant_type else None  # Add this line
            
            # Calculate default price without GST
            price_wo_gst = first_variant_type.varient_price if first_variant_type else product.price
            # Fetching GST rate
            gst_rate = first_variant_type.gst_rate if first_variant_type else product.gst_rate
            # Calculate default price including GST
            base_price = first_variant_type.varient_price if first_variant_type else product.price
            # Calculate GST amount
            gst_amount = base_price * Decimal(gst_rate.strip('%')) / 100
            # Calculate total price including GST and round off to two decimal places
            product.gst_inclusive_price = round(base_price + gst_amount, 2)
            # Include original variant price in the context
            product.variant_price = price_wo_gst
        else:
            # Use the existing GST-inclusive price for the product
            product.gst_inclusive_price = product.price * (1 + Decimal(product.gst_rate.strip('%')) / 100)
            gst_rate = product.gst_rate
            # If the product doesn't have variants, set variant_price to None
            product.variant_price = None
            product.first_variant_type_title = None  # Add this line
            product.first_variant_type_id = None  # Add this line

    context = {
        "main_categories":main_categories,
        "products": products,
        "product_images": product_images,
        "min_price": min_price,
        "max_price": max_price,
        "product_variants": product_variants,
        "variant_types": variant_types,
        "gst_rate": gst_rate,  # Include gst_rate in the context
    }

    return render(request, "core/expert-series.html", context)



from django.http import JsonResponse

def fetch_pin_details(request):
    if request.method == 'GET':
        zipcode = request.GET.get('zipcode')
        print('Zipcode received:', zipcode)
        
        pin_details_list = indiapins.matching(zipcode)
        print('Pin details fetched:', pin_details_list)
        
        if pin_details_list:
            # Format all pin details to be sent in the response
            response_data = [
                {
                    'Name': pin_details.get('Name'),
                    'Region': pin_details.get('Region'),
                    'District': pin_details.get('District'),
                    'Division': pin_details.get('Division'),
                    'Block': pin_details.get('Block'),
                    'Circle': pin_details.get('Circle'),
                    'State': pin_details.get('State')
                }
                for pin_details in pin_details_list
            ]
            response = {
                'success': True,
                'data': response_data
            }
            print('Response:', response)  # Check if the response is correctly formatted
            return JsonResponse(response)
        else:
            return JsonResponse({'success': False, 'error': 'Pincode details not found'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


def checkout(request):
    return render(request, "core/checkout.html")

def payment_failed_view(request):
    return render(request, "core/confirmation-failed.html")


def add_to_cart(request):
    # Ensure all required parameters are present
    required_params = ['id', 'title', 'qty', 'price', 'image', 'sku', 'price_wo_gst', 'gst_applied', 'gst_rate']
    for param in required_params:
        if param not in request.GET:
            return JsonResponse({"error": f"Missing parameter: {param}"}, status=400)
    
    product_id = request.GET.get('id')
    variant_id = request.GET.get('variant_id', '')  # Optional parameter
    unique_key = f"{product_id}_{variant_id}"  # Create a unique key

    try:
        qty = request.GET['qty']  # Ensure qty is an integer
        price = request.GET['price']  # Ensure price is a float
        price_wo_gst = request.GET['price_wo_gst']  # Ensure price_wo_gst is a float
        gst_applied = request.GET['gst_applied']  # Ensure price_wo_gst is a float
        gst_rate = request.GET['gst_rate']  # Ensure gst_rate is a float
    except ValueError:
        return JsonResponse({"error": "Invalid numeric value"}, status=400)

    cart_product = {
        'product_id': product_id,
        'variant_id': variant_id,
        'title': request.GET.get('title'),
        'qty': qty,
        'price': price,
        'image': request.GET.get('image'),
        'sku': request.GET.get('sku'),
        'price_wo_gst': price_wo_gst,
        'gst_applied':gst_applied,
        'gst_rate': gst_rate,
    }

    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        # Check if the product with the same unique key is already in the cart
        if unique_key in cart_data:
            return JsonResponse({"already_in_cart": True})
        
        cart_data[unique_key] = cart_product
    else:
        cart_data = {unique_key: cart_product}

    request.session['cart_data_obj'] = cart_data

    return JsonResponse({
        "data": request.session['cart_data_obj'], 
        'totalcartitems': len(request.session['cart_data_obj']), 
        "already_in_cart": False
    })

def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])


        cart_total_amount_shipping = cart_total_amount

        return render(request, "core/cart.html", {
            "cart_data": request.session['cart_data_obj'], 
            'totalcartitems': len(request.session['cart_data_obj']), 
            'cart_total_amount': cart_total_amount,
            'cart_total_amount_shipping': cart_total_amount_shipping
        })
    else:
        messages.warning(request, "Your cart is empty")
        return redirect("/")



def search_view(request):
    query = request.GET.get("q")

    products = Product.objects.filter(title__icontains=query, product_status='published').order_by("-date")
    related_main_categories = Main_category.objects.filter(product__in=products).distinct()
    product_images = ProductImages.objects.filter(product__in=products)
    
    total_products_count = Product.objects.count()
    if total_products_count == 0:
        percentage = 0
    else:
        percentage = (products.count() / total_products_count) * 100

    context = {
        "products": products,
        "query": query,
        "related_main_categories": related_main_categories,
        "percentage": percentage, 
        "product_images": product_images,
    }

    return render(request, "core/search.html", context)

def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    refresh_page = request.GET.get('refresh_page', False)

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
           cart_data = request.session['cart_data_obj']
           del request.session['cart_data_obj'][product_id]
           request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = {
        "cart_data": request.session['cart_data_obj'],
        'totalcartitems': len(request.session['cart_data_obj']),
        'cart_total_amount': cart_total_amount,
        'refresh_page': refresh_page,  # Include refresh_page flag in context
    }

    rendered_html = render_to_string("core/cart.html", context)
    
    # Return JSON response with rendered HTML and refresh_page flag
    return JsonResponse({"data": rendered_html, 'totalcartitems': len(request.session['cart_data_obj']), 'refresh_page': refresh_page})      


def update_cart(request):
    product_id = str(request.GET.get('id'))
    product_qty = int(request.GET.get('qty'))
    refresh_page = request.GET.get('refresh_page', False)
    
    if 'cart_data_obj' not in request.session:
        request.session['cart_data_obj'] = {}

    cart_data = request.session['cart_data_obj']
    
    if product_id in cart_data:
        cart_data[product_id]['qty'] = product_qty
        request.session['cart_data_obj'] = cart_data
        request.session.modified = True

    cart_total_amount = 0
    for p_id, item in cart_data.items():
        cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("core/cart.html", {
        "cart_data": cart_data, 
        'totalcartitems': len(cart_data), 
        'cart_total_amount': cart_total_amount
    })
    
    return JsonResponse({
        "data": context, 
        'totalcartitems': len(cart_data), 
        'refresh_page': refresh_page
    })


def payment_failed_view(request):
    return render(request, "core/confirmation.html")

def payment_success_view(request):
    return render(request, "core/payment_confirm.html")

def about(request):
    return render(request, "core/about-us.html")

def privacypolicy(request):
    return render(request, "core/privacy-policy.html")

def main_categoryy(request, main_title):
    main_categoryy = Main_category.objects.get(main_title=main_title)
    product = Product.objects.filter(main_category=main_categoryy)

    prices = product.values_list('price', flat=True)
    min_price = min(prices) if prices else 0
    max_price = max(prices) if prices else 0

    min_price_filter = float(request.GET.get('min_price', min_price))
    max_price_filter = float(request.GET.get('max_price', max_price))

    if min_price_filter and max_price_filter:
        products = product.filter(price__range=(min_price_filter, max_price_filter))

    context = {
        "main_categoryy": main_categoryy,
        "product": product,
        "min_price": min_price,
        "max_price": max_price,
        "min_price_filter": min_price_filter,
        "max_price_filter": max_price_filter,
    }

    return render(request, "core/main_categoryy.html", context)

def tnc(request):
    return render(request, "core/tnc.html")

def contact(request):
    return render(request, "core/contact_us.html")

def private_label(request):
    return render(request, "core/private_label.html")

def career(request):
    return render(request, "core/career.html")

def product(request):
    return render(request, "core/product.html")

def write_to_ceo(request):
    return render(request, "core/write-to-ceo.html")

def cart(request):
    return render(request, "core/cart.html")

def blogs(request):
    blogs = Blogs.objects.all()
    for blog in blogs:
        # Parsing HTML and extracting text
        soup = BeautifulSoup(blog.blog_description, "html.parser")
        description_text = soup.get_text(separator='\n')
        # Splitting the text into lines and selecting the first two lines
        description_lines = description_text.split('\n')
        blog.short_description = '\n'.join(description_lines[:2])

    context = {
        "blogs": blogs,
    }

    return render(request, "core/blog.html", context)

def blog_details(request, blog_slug):
    blog_detail = Blogs.objects.get(blog_slug=blog_slug)

    context = {
        "blog_detail": blog_detail,
    }

    return render(request, "core/blog-details.html", context)

def checkout_view(request):
    total_shipping_rate_with_gst = Decimal('0')
    cart_total_amount_shipping = Decimal('0')
    cart_total_amount = Decimal('0')
    shipping_rate = Decimal('0')
    price_wo_gst_total = Decimal('0')
    total_gst = Decimal('0')  # Initialize total_gst as Decimal

    if 'cart_data_obj' not in request.session or not request.session['cart_data_obj']:
        messages.info(request, 'Please shop first before checkout')
        return redirect('/cart')

    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        zipcode = request.POST.get('zipcode')  # Fixed: Should match the name used in the form
        pin_details = request.POST.get('pin_details')
        city = request.POST.get('city')
        district = request.POST.get('district')
        division = request.POST.get('division')
        state = request.POST.get('state')
        billing_address = request.POST.get('billingaddress')
        shipping_address = request.POST.get('shippingaddress')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        company_name = request.POST.get('companyname')
        gst_number = request.POST.get('gstnumber')
        have_gst = request.POST.get('have-gst')  # For the checkbox

        # Calculate shipping charge based on number of products
        if 'cart_data_obj' in request.session:
            cart_data = request.session['cart_data_obj']
            num_products = len(cart_data)
            if num_products == 1:
                shipping_rate = Decimal('0')
            elif num_products > 1:
                shipping_rate = Decimal('0') * num_products

            gst_amount = shipping_rate * Decimal('0.18')
            total_shipping_rate_with_gst = shipping_rate + gst_amount

            # Calculate total amount including shipping
            for unique_key, item in cart_data.items():
                qty = Decimal(item['qty'])
                price = Decimal(item['price'])
                price_wo_gst = Decimal(item.get('price_wo_gst', price))
                gst_applied = Decimal(item['gst_applied'])  # Extract the gst_applied

                cart_total_amount += qty * price
                price_wo_gst_total += qty * price_wo_gst
                total_gst += gst_applied  # Sum up the gst_applied

            cart_total_amount_shipping = cart_total_amount + total_shipping_rate_with_gst

        total_amount = Decimal('0')
        user_zipcode = zipcode  # Get user's zipcode from the form

          # Store the form data in the session
        request.session['checkout_data'] = {
            'firstname': first_name,
            'lastname': last_name,
            'zipcode': zipcode,
            'city': city,
            'district': district,
            'division': division,
            'state': state,
            'billingaddress': billing_address,
            'shippingaddress': shipping_address,
            'phone': phone,
            'email': email,
            'companyname': company_name,
            'gstnumber': gst_number,
            'have_gst': have_gst,
            'price_wo_gst_total': float(price_wo_gst_total),
            'total_gst': float(total_gst),
            'cart_total_amount_shipping': float(cart_total_amount_shipping),
        }

        with open('new_delhi_zipcodes.json', 'r') as f:
            maharashtra_zipcodes = json.load(f)

        # Check if user's zipcode is in Maharashtra
        if user_zipcode in maharashtra_zipcodes:
            cgst_factor = Decimal('0.025')  # CGST rate for Maharashtra (2.5%)
            sgst_factor = Decimal('0.025')  # SGST rate for Maharashtra (2.5%)
            igst_factor = Decimal('0')      # IGST will be 0%
        else:
            cgst_factor = Decimal('0.09')   # CGST rate for other states (9%)
            sgst_factor = Decimal('0.09')   # SGST rate for other states (9%)
            igst_factor = Decimal('1')      # IGST will be 100%

        if 'cart_data_obj' in request.session:
            # Calculate total amount, price without GST, and total GST
            for unique_key, item in cart_data.items():
                qty = Decimal(item['qty'])
                price = Decimal(item['price'])
                price_wo_gst = Decimal(item.get('price_wo_gst', price))

                total_amount += qty * price
                price_wo_gst_total += qty * price_wo_gst
                item_gst = (price - price_wo_gst) * qty  # Calculate GST for this item

                # Calculate CGST and SGST for each product based on the user's zipcode
                cgst = item_gst * cgst_factor
                sgst = item_gst * sgst_factor
                igst = item_gst * igst_factor

                total_gst += item_gst  # Add item's GST to total GST

                # Do whatever you want with CGST, SGST, and IGST here

        for unique_key, item in cart_data.items():
            # Retrieve the correct product ID from the item data
            product_id = item['product_id']

            # Ensure the product exists in the database
            try:
                product = Product.objects.get(pid=product_id)
            except Product.DoesNotExist:
                messages.error(request, f"Product with ID {product_id} does not exist.")
                return redirect('/cart')  # Redirect the user to the cart page
            
        if 'cart_data_obj' in request.session:
            try:
                response = api.payment_request_create(
                    amount=str(cart_total_amount_shipping),  # Use cart_total_amount_shipping here
                    purpose='Order Processing',
                    buyer_name=f'{first_name} {last_name}',
                    email=email,
                    phone=phone,
                    redirect_url='https://vrhealthscience.com/payment-invoice/'
                )
                payment_url = response['payment_request']['longurl']
                return redirect(payment_url)
            except Exception as e:
                messages.error(request, f"Payment initiation failed: {str(e)}")
                return HttpResponseBadRequest("Error processing payment request")

        context = {
            "price_wo_gst_total": price_wo_gst_total,
            "total_gst": total_gst,
            "user_zipcode": user_zipcode,
            "maharashtra_zipcodes": maharashtra_zipcodes,
            "shipping_rate": total_shipping_rate_with_gst,
            'cart_total_amount_shipping': cart_total_amount_shipping
        }

        return render(request, "core/checkout.html", {
            'cart_data': request.session.get('cart_data_obj', {}),
            'totalcartitems': len(request.session.get('cart_data_obj', {})),
            'cart_total_amount': cart_total_amount,
            **context
        })

    else:
        if 'cart_data_obj' in request.session:
            cart_data = request.session['cart_data_obj']
            cart_total_amount = Decimal('0')  # Initialize cart_total_amount

            for unique_key, item in cart_data.items():
                qty = Decimal(item['qty'])
                price = Decimal(item['price'])
                price_wo_gst = Decimal(item.get('price_wo_gst', price))
                gst_applied = Decimal(item['gst_applied'])  # Extract the gst_applied

                cart_total_amount += qty * price
                price_wo_gst_total += qty * price_wo_gst
                total_gst += gst_applied  # Sum up the gst_applied

            num_products = len(cart_data)
            if num_products == 1:
                shipping_rate = Decimal('0')
            elif num_products > 1:
                shipping_rate = Decimal('0') * num_products

            gst_amount = shipping_rate * Decimal('0.18')
            total_shipping_rate_with_gst = shipping_rate + gst_amount
            cart_total_amount_shipping = cart_total_amount + total_shipping_rate_with_gst

        context = {
            "price_wo_gst_total": price_wo_gst_total,
            "total_gst": total_gst,
            'cart_total_amount_shipping': cart_total_amount_shipping,
            'cart_data': request.session.get('cart_data_obj', {}),
            'totalcartitems': len(request.session.get('cart_data_obj', {})),
            'cart_total_amount': cart_total_amount
        }

        return render(request, "core/checkout.html", context)

def invoice(request):
    return render(request, "core/payment_invoice.html")

def payment_invoice(request):

    if 'checkout_data' not in request.session:
        return HttpResponseBadRequest("No checkout data found in session.")

    checkout_data = request.session.pop('checkout_data')

    # Extract data from session
    first_name = checkout_data.get('firstname')
    last_name = checkout_data.get('lastname')
    zipcode = checkout_data.get('zipcode')
    pin_details = request.POST.get('pin_details')
    city = checkout_data.get('city')
    district = checkout_data.get('district')
    division = checkout_data.get('division')
    state = checkout_data.get('state')
    billing_address = checkout_data.get('billingaddress')
    shipping_address = checkout_data.get('shippingaddress')
    phone = checkout_data.get('phone')
    email = checkout_data.get('email')
    company_name = checkout_data.get('companyname')
    gst_number = checkout_data.get('gstnumber')
    have_gst = checkout_data.get('have_gst')
    price_wo_gst_total = Decimal(checkout_data.get('price_wo_gst_total'))
    total_gst = Decimal(checkout_data.get('total_gst'))
    cart_total_amount_shipping = Decimal(checkout_data.get('cart_total_amount_shipping'))
    cart_total_amount = 0
    total_amount = 0
    price_wo_gst_total = 0
    total_gst = 0

    current_datetime = datetime.now()

    with open('new_delhi_zipcodes.json', 'r') as f:
        maharashtra_zipcodes = json.load(f)

    print('payment', maharashtra_zipcodes)

    if 'cart_data_obj' in request.session:
        # Initialize dictionaries to store CGST, SGST, and IGST amounts for each product
        cgst_amounts = {}
        sgst_amounts = {}
        igst_amounts = {}
        gst_amounts = {}
        gst_amounts_combined = {}  # Dictionary to store aggregated GST amounts

        # Calculate total amount, price without GST, and total GST
        for p_id, item in request.session['cart_data_obj'].items():
            total_amount += int(item['qty']) * Decimal(item['price'])
            price_wo_gst_total += int(item['qty']) * Decimal(item.get('price_wo_gst', item['price']))
            price_wo_gst_final = int(item['qty']) * Decimal(item.get('price_wo_gst', item['price']))
            item_gst = (Decimal(item['price']) - Decimal(item.get('price_wo_gst', item['price']))) * int(
                item['qty'])  # Calculate GST for this item

            # Calculate GST rates
            if price_wo_gst_final != 0:
                gst_rates_final = (item_gst / price_wo_gst_final) * 100
            else:
                gst_rates_final = Decimal('0')

            item['gst_rates_final'] = gst_rates_final

            # Divide the GST amount by 2 to get CGST and SGST separately
            if zipcode in maharashtra_zipcodes:
                # For Maharashtra zip codes, calculate CGST and SGST separately
                igst_amount = Decimal('0')  # IGST will be 0
                gst_rates_final = gst_rates_final / Decimal(2)
            else:
                # For non-Maharashtra zip codes, IGST will be double of CGST
                igst_amount = item_gst
                gst_rates_final = gst_rates_final

            # Aggregate GST amounts based on GST rates
            if gst_rates_final in gst_amounts:
                gst_amounts[gst_rates_final] += item_gst
            else:
                gst_amounts[gst_rates_final] = item_gst

            total_gst += item_gst

        # Print CGST Amounts
        print("CGST Amounts:")
        for gst_rate, total_gst_amount in gst_amounts.items():
            cgst_amount = total_gst_amount / Decimal(2)
            print(f"CGST Amount: {cgst_amount}, GST Rate: {gst_rate}")

        # Print SGST Amounts
        print("\nSGST Amounts:")
        for gst_rate, total_gst_amount in gst_amounts.items():
            sgst_amount = total_gst_amount / Decimal(2)
            print(f"SGST Amount: {sgst_amount}, GST Rate: {gst_rate}")

        print("\nIGST Amounts:")
        for gst_rate, total_gst_amount in gst_amounts.items():
            igst_amount = total_gst_amount
            print(f"IGST Amount: {igst_amount}, GST Rate: {gst_rate}")

        print("GST Amounts:")
        print(gst_amounts)

        for gst_rate, total_gst_amount in gst_amounts.items():
            cgst_amount = total_gst_amount / Decimal(2)
            sgst_amount = total_gst_amount / Decimal(2)
            gst_amounts_combined[gst_rate] = {'cgst': cgst_amount, 'sgst': sgst_amount}

        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

            order = CartOrder.objects.create(
                user=request.user if request.user.is_authenticated else None,
                price=item['price'],
                firstname=first_name,
                lastname=last_name,
                zipcode=zipcode,
                order_date=current_datetime,
                pin_details=pin_details,
                city=city,
                district=district,
                division=division,
                state=state,
                billingaddress=billing_address,
                shippingaddress=shipping_address,
                phone=phone,
                email=email,
                companyname=company_name if have_gst else '',
                gstnumber=gst_number if have_gst else '',
                price_wo_gst_total=price_wo_gst_total,
            )

            cart_order_products = CartOrderItems.objects.create(
                order=order,
                invoice_no="order_id-" + str(order.id),
                product_status=item.get('product_status', ''),
                item=item.get('title', ''),  # Ensure this matches the field in your model
                image=item.get('image', ''),
                qty=item['qty'],
                price=item['price'],
                total=Decimal(item['qty']) * Decimal(item['price']),
                price_wo_gst=Decimal(item['price_wo_gst']),  # Store price without GST
                gst_rates_final=Decimal(item['gst_applied'])
            )

        cart_total_amount_rounded = round(cart_total_amount, 2)
        cart_total_amount_words = num2words(cart_total_amount_rounded, lang='en_IN')

        invoice_number, created = InvoiceNumber.objects.get_or_create()

        # Increment the invoice number
        invoice_number.increment()

        # Use the incremented invoice number for the current invoice
        invoice_no = str(invoice_number)

        half_total_gst_amount = total_gst / Decimal(2)

        context = {
            "price_wo_gst_total": price_wo_gst_total,
            "total_gst": total_gst,
            "cgst_amounts": cgst_amounts,
            "sgst_amounts": sgst_amounts,
            "igst_amounts": igst_amounts,
            "zipcode": zipcode,
            "maharashtra_zipcodes": maharashtra_zipcodes,
            'first_name': first_name,
            'last_name': last_name,
            'company_name': company_name,
            'gst_number': gst_number,
            'zipcode': zipcode,
            'city': city,
            'billing_address': billing_address,
            'phone': phone,
            'current_datetime': current_datetime,
            'email': email,
            "cgst_amount": cgst_amount,
            "sgst_amount": sgst_amount,
            "igst_amount": igst_amount,
            "igst_amounts": igst_amounts,
            "gst_rates_final": gst_rates_final,
            "shipping_address": shipping_address,
            "cart_total_amount_words": cart_total_amount_words,
            'invoice_no': invoice_no,
            "half_total_gst_amount": half_total_gst_amount,
            "gst_amounts": gst_amounts,
            "gst_rate": gst_rate,
            "gst_amounts_combined": gst_amounts_combined,
            'cart_data': request.session.get('cart_data_obj', {}),
            'totalcartitems': len(request.session.get('cart_data_obj', {})),
            'cart_total_amount': cart_total_amount,
            'cart_items': request.session.get('cart_data_obj', {})
        }
        subject = 'Payment Invoice'
        from_email = 'billing@vrhealthscience.com'
        to_email = email
        cc_email = 'sprince1500@gmail.com'  # Add the CC email address here
        html_message = render_to_string('core/thankyou-order.html', {'context': context})
        plain_message = strip_tags(html_message)

        # Generate PDF using xhtml2pdf
        html_template = render_to_string('core/payment_invoice.html', context)
        pdf_file = BytesIO()
        pisa_status = pisa.CreatePDF(html_template, dest=pdf_file)
        pdf_file.seek(0)

        # Create the email message for the primary recipient
        email_message = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
        email_message.attach_alternative(html_message, "text/html")

        if not pisa_status.err:
            email_message.attach('invoice.pdf', pdf_file.read(), 'application/pdf')

        # Send the email to the primary recipient
        email_message.send()

        # Render the CC email template
        cc_html_message = render_to_string('core/cc_invoice.html', context)
        cc_plain_message = strip_tags(cc_html_message)

        # Create the email message for the CC recipient
        cc_email_message = EmailMultiAlternatives(subject, cc_plain_message, from_email, [cc_email])
        cc_email_message.attach_alternative(cc_html_message, "text/html")

        if not pisa_status.err:
            pdf_file.seek(0)  # Reset the file pointer to the beginning before attaching
            cc_email_message.attach('invoice.pdf', pdf_file.read(), 'application/pdf')

        # Send the email to the CC recipient
        cc_email_message.send()

        # Render the invoice before clearing the cart data
        response = render(request, "core/payment_invoice.html", context)

        # Clear cart data after successful purchase and rendering the invoice
        if 'cart_data_obj' in request.session:
            del request.session['cart_data_obj']
            request.session.modified = True

        return response


def load_maharashtra_zipcodes():
    try:
        with open('new_delhi_zipcodes.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


@login_required
def dashboard(request):
    return render(request, "core/account_dashboard.html")

def faq(request):
    return render(request, "core/faqs.html")

def cc_invoice(request):
    return render(request, "core/cc_invoice.html")

def thankyouorder(request):
    return render(request, "core/thankyou-order.html")

def shipping_policy(request):
    return render(request, "core/shipping-policy.html")

def return_policy(request):
    return render(request, "core/return_policy.html")

def download_invoice(request):
    return render(request, "core/download_invoice.html")

def cancellationandrefund(request):
    return render(request, "core/cancellationandrefund.html")

@login_required
def orders(request):
    orders = CartOrder.objects.filter(user=request.user).order_by("-id")
    context = {
        "orders": orders
    }
    return render(request, "core/account_orders.html", context)

def order_detail(request, id):
    order = CartOrder.objects.filter(user=request.user, id=id)
    products = CartOrderItems.objects.filter(order=order)

    context = {
        "products": products,
    }
    return render(request, "core/order-detail.html", context)

@login_required
def address(request):
    return render(request, "core/account_address.html")

def international_shipping(request):
    privacy_policy = InternationalShipping.objects.first()  # Assuming you have a PrivacyPolicy instance
    context = {
        'privacy_policy_content': privacy_policy.international_shipping_content if privacy_policy else ''
    }
    return render(request, 'core/international-shipping.html', context)

class RobotsTxtView(View):
    def get(self, request, *args, **kwargs):
        # Specify the path to your robots.txt file
        robots_txt_path = os.path.join(settings.BASE_DIR, 'static', 'robots.txt')

        with open(robots_txt_path, 'r') as f:
            content = f.read()

        return HttpResponse(content, content_type='text/plain')
    
def product_new(request, product_slug):
    product = Product.objects.filter(product_slug=product_slug, product_status='published').first()
    if not product:
        raise Http404("Product not found")
    product_variants = ProductVarient.objects.filter(product=product)
    product_variant_types = ProductVariantTypes.objects.filter(product_variant__in=product_variants)
    related_products = Product.objects.filter(main_category=product.main_category).exclude(pid=product.pid)[:10]
    related_maincategory = product.main_category

    # Check if variants and variations exist
    has_variants = product_variants.exists()

    # Fetching GST rate
    gst_rate = product_variant_types.first().gst_rate if product_variant_types.exists() else product.gst_rate

    # Calculating default price including GST
    base_price = product_variant_types.first().varient_price if product_variant_types.exists() else product.price

    # Calculate GST amount
    gst_amount_applied = base_price * Decimal(gst_rate.strip('%')) / (100 + Decimal(gst_rate.strip('%')))

    # Fetching rate without GST
    price_wo_gst = base_price - gst_amount_applied

    price_wo_gst = price_wo_gst.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    # Round the GST amount to 2 decimal places
    gst_amount_applied = gst_amount_applied.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    usd_rates = base_price / Decimal('83.52')

    product_images = ProductImages.objects.filter(product=product)

    product_description = ProductDescription.objects.filter(product=product).first()

    product_variant_type_images = ProductVariantTypeImages.objects.filter(product_variant_type__in=product_variant_types)

    context = {
        "products": product,
        "product_variants": product_variants,
        "product_variant_types": product_variant_types,
        "product_images": product_images,
        "price_wo_gst": price_wo_gst,
        "gst_amount_applied": gst_amount_applied,
        "gst_rate": gst_rate,
        "usd_rates": usd_rates,
        "has_variants": has_variants,
        "related_products": related_products,
        "related_maincategory":  related_maincategory,
        "product_description": product_description,
        "product_variant_type_images": product_variant_type_images,
        "in_stock": product.in_stock,
    }

    return render(request, "core/product.html", context)

def export_cart_orders_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="cart_orders.csv"'

    writer = csv.writer(response)
    writer.writerow(['Price', 'Courier Partner', 'Tracking ID', 'Paid Status', 'Order Date', 'Product Status',
                     'First Name', 'Last Name', 'Zip Code', 'City', 'District', 'Division', 'State',
                     'Billing Address', 'Shipping Address', 'Phone', 'Email'])

    orders = CartOrder.objects.all().values_list('price', 'courier_partner', 'tracking_id', 'paid_status', 'order_date', 'product_status',
                                                 'firstname', 'lastname', 'zipcode', 'city', 'district', 'division', 'state',
                                                 'billingaddress', 'shippingaddress', 'phone', 'email')
    for order in orders:
        writer.writerow(order)

    return response


def generate_invoice(request, order_id):
    # Get the order object
    order = get_object_or_404(CartOrder, pk=order_id)
    
    # Fetch related cart items
    cart_items = CartOrderItems.objects.filter(order=order)

    # Prepare data for the invoice
    cart_data = {}
    price_wo_gst_total = Decimal('0')
    for item in cart_items:
        cart_data[item.id] = {
            'title': item.item,  # Assuming 'item' is a string
            'qty': item.qty,
            'price': item.price,
            'image': item.image,
            'invoice_no': item.invoice_no,
            'product_status': item.product_status,
            'total': item.total,
            'price_wo_gst': item.price_wo_gst,  # Use the correct field name
            'gst_rates_final': item.gst_rates_final,  # Include gst_rates_final
            'first_name': order.firstname,
            'last_name': order.lastname,
            'zipcode': order.zipcode,
            'email': order.email,
            'phone': order.phone,
            'pin_details': order.pin_details,
            'city': order.city,
            'district': order.district,
            'division': order.division,
            'state': order.state,
            'billing_address': order.billingaddress,
            'shipping_address': order.shippingaddress,
            'company_name': order.companyname,
            'gst_number': order.gstnumber,
        }
        price_wo_gst_total += item.price_wo_gst * item.qty
        cart_total_amount_words = num2words(price_wo_gst_total, lang='en_IN')

    context = {
        'order': order,
        'cart_data': cart_data,  # Adjust if needed
        'first_name': order.firstname,
        'last_name': order.lastname,
        'zipcode': order.zipcode,
        'email': order.email,
        'phone': order.phone,
        'pin_details': order.pin_details,
        'city': order.city,
        'district': order.district,
        'division': order.division,
        'state': order.state,
        'billing_address': order.billingaddress,
        'shipping_address': order.shippingaddress,
        'company_name': order.companyname,
        'gst_number': order.gstnumber,
        'price_wo_gst_total': price_wo_gst_total,  # Add price_wo_gst_total to context
        'cart_total_amount_words': cart_total_amount_words
    }

    # Render the invoice template with the context
    return render(request, 'core/download_invoice.html', context)


def contact_us_view(request):
    if request.method == "POST":
        form = UserQueryForm(request.POST)
        if form.is_valid():
            # Extract data from the form
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']
            
            # Send an email
            subject = f'Contact Us Form Submission from {name}'
            message_body = f'Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage:\n{message}'
            from_email = 'billing@vrhealthscience.com'
            recipient_list = ['scriptforprince@gmail.com']  # Replace with actual recipient email

            send_mail(
                subject,
                message_body,
                from_email,
                recipient_list,
                fail_silently=False,
            )
            
            messages.success(request, 'Your message has been sent successfully.')
            return redirect('contact-us')  # Replace with your desired redirect URL
    else:
        form = UserQueryForm()

    context = {
        'form' : form,
    }
    
    return render(request, 'core/contact_us.html', context)

def subscribe_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            send_mail(
                'New Newsletter Subscription',
                f'New subscription from: {email}',
                'scriptforprince@gmail.com',
                ['scriptforprince@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, 'Subscribed successfully!')
            return redirect('newsletter')
    else:
        form = NewsletterForm()

    return render(request, 'partials/base.html', {'form': form})




