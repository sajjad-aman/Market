from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
# Create your views here.


def store(request):

	if request.user.is_authenticated:
		Customer = request.user.customer
		order, created = Order.objects.get_or_create(Customer=Customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}
		cartItems = order['get_cart_items']
	Products = Product.objects.all()
	context = {'Products':Products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        Customer =request.user.customer
        order, created = Order.objects.get_or_create(Customer=Customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items =[]
        order ={'get_cart_total':0,'get_cart_items':0}
        cartItems = Order['get_cart_items']

    context = {'items':items ,'order': order, 'cartItems':cartItems }
    return render(request,'store/cart.html',context)
    

def checkout(request):
    if request.user.is_authenticated:
        Customer = request.user.customer
        order , created = Order.objects.get_or_create(Customer=Customer,complete=False)
        items = order.orderitem_set.all()
        cartItems= order.get_cart_items
    else:
        order = {'get_cart_total':0,'get_cart_items':0}
        items = []
        cartItems = Order['get_cart_items']
    context={'items':items,'order':order, 'cartItems':cartItems }
    return render(request,'store/checkout.html',context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)