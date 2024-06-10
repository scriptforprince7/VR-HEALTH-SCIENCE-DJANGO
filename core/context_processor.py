from core.models import *

def default(request):
    main_categories = Main_category.objects.filter(active_status='published')

    return {
        "main_cat": main_categories,
    }


def defaultOne(request):
    products = Product.objects.all()

    return {
        "products_count": products,
    }

def defaultTwo(request):
    ingredients = Ingredients.objects.filter(active_status='published')

    return {
        "ingredients": ingredients,
    }

def cart_context(request):
    cart_total_amount = 0
    total_cart_items = 0
    cart_data = {}

    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']

        for p_id, item in cart_data.items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            total_cart_items += int(item['qty'])

    return {
        'cart_total_amount': cart_total_amount,
        'total_cart_items': total_cart_items,
        'cart_data': cart_data  # Include cart_data in the context
    }



