from core.models import *

def default(request):
    main_categories = Main_category.objects.filter(active_status='published')
    categories_by_main_category = {main_cat.id: [] for main_cat in main_categories}

    categories = Category.objects.filter(main_category__in=main_categories)
    for category in categories:
        categories_by_main_category[category.main_category_id].append(category)

    return {
        "main_cat": main_categories,
        "categories_by_main_category": categories_by_main_category,
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

def defaultThree(request):
    concern = Concern.objects.filter(active_status='published')

    return {
        "concern": concern,
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



