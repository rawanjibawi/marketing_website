from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart
from items.models import Item
from django.http import JsonResponse

# Create your views here.


'''
"add_to_cart" handles adding items to the shopping cart. 
If an item with the same product ID already exists 
in the user's cart, we increase its quantity by 1. 
Otherwise, we create a new cart item with quantity 1. 
We then redirect to the cart detail page.
'''
@login_required
def add_to_cart(request, product_id):
    print("hi cart")
    item = get_object_or_404(Item, id=product_id) # retreive the item we want to filter
    
    cart_item = Cart.objects.filter(user=request.user, Item=item).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, "Item added to your cart.")
    else:
        Cart.objects.create(user=request.user, Item=item)
        messages.success(request, "Item added to your cart.")

    return redirect("cart:cart_detail")

'''
"remove_from_cart" handles removing items from the 
shopping cart. We first retrieve the cart item with the 
given ID. If it belongs to the current user, we delete it 
from the database. We then redirect to the cart detail 
page.
'''
@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id)

    if cart_item.user == request.user:
        cart_item.delete()
        messages.success(request, "Item removed from your cart.")

    return redirect("cart:cart_detail")

'''
"cart_detail" displays the contents of the user's 
shopping cart. We retrieve all cart items belonging 
to the current user and calculate the total price of 
all items. We then render a template with this information
'''


@login_required
def cart_detail(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.quantity * item.Item.price for item in cart_items)
    total_prices_per_item = [instance.total_price_per_item() for instance in cart_items]
    # total_prices_per_item = [item.quantity * item.Item.price for item in cart_items]
    print(total_prices_per_item)
    context = {
        "cart_items": cart_items,
        "total_price": total_price,
        "total_price_per_item": total_prices_per_item
    }

    return render(request, "cart_detail.html", context)

# decrementing quantity


@login_required
def decrement_quantity(request, product_id):
    print("hello decerment")
    item = get_object_or_404(Item, id=product_id)
    cart_item = Cart.objects.filter(user=request.user, Item=item).first()

    if cart_item.user == request.user:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            messages.success(request, "Quantity decremented.")
        else:
            cart_item.delete()
            messages.success(request, "Item removed from your cart.")

        # total_price_per_item = cart_item.total_price_per_item()
        # return JsonResponse({'success': True, 'quantity': cart_item.quantity, 'total_price_per_item': total_price_per_item})
    # else:
        # return JsonResponse({'success': False, 'message': 'Permission denied'})
    return redirect("cart:cart_detail")
