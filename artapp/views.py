from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from artapp.models import *
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm
from django.contrib.auth import authenticate, login,logout
from .middlewares import *
from .forms import OrderForm
from django.utils.html import format_html



# Create your views here.
@guest
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('dashboard')
    else:
        initial_data = {'username':'', 'password1':'','password2':""}
        form = UserCreationForm(initial=initial_data)
    return render(request, 'register.html',{'form':form})

@guest
def Login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('dashboard')
    else:
        initial_data = {'username':'', 'password':''}
        form = AuthenticationForm(initial=initial_data)
    return render(request, 'Login.html',{'form':form}) 

@auth
def dashboard_view(request):
    return render(request, 'home.html')


def Logout(request):
    logout(request)
    return redirect('Login')


@guest
def home(request):
    arts=Arts.objects.all()[:11]
    data={
        'arts': arts
    }
    return render(request, 'home.html', data)
@auth
def theart(request,url):
    theart=Arts.objects.get(url=url)
    return render(request, 'arts.html', {'theart':theart })

@auth
def Paintings(request):
    arts=Arts.objects.all()[:11]
    data={
        'arts': arts,
    }
    return render(request, 'paintings.html', data)

@auth
def Artistss(request):
    artists = Artists.objects.all()
    return render(request, 'artist.html', {'artists': artists})
@auth
def view_artist(request, url):
    artist = get_object_or_404(Artists, url=url)
    artworks = Arts.objects.filter(ArtistName=artist)
    return render(request, 'view_artist.html', {'artist': artist, 'artworks': artworks})

def About(request):
    return render(request, 'about.html')


#carttt
@auth
def add_to_cart(request, art_id):
    art = get_object_or_404(Arts, pk=art_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, art=art)


    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_view')

@auth
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total = sum(item.art.price * item.quantity for item in cart_items)
    for item in cart_items:
        item.item_total = item.art.price * item.quantity
    
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


@auth
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_view')


#orders
@auth
def place_order(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total = sum(item.quantity * item.art.price for item in cart_items)

    for item in cart_items:
        item.total_amount = item.quantity * item.art.price
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                total_amount=total,
                shipping_address=form.cleaned_data['shipping_address'],
                status='Pending'
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    art=item.art,
                    quantity=item.quantity,
                    price=item.art.price
                )
            cart_items.delete()
            messages.success(request, "Your order was placed successfully!")
            return redirect('orders')
    else:
        form = OrderForm()

    return render(request, 'place_order.html', {'form': form, 'total': total, 'cart_items': cart_items})

@auth
def orders(request):
    user_orders = Order.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': user_orders})


@auth
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status != 'Canceled':
        order.status = 'Canceled'
        order.save()
        messages.success(request, 'Order has been canceled successfully.')
    else:
        messages.error(request, 'Order is already canceled.')
    return redirect('orders')


def view_art(request, url):
    artwork = get_object_or_404(Arts, url=url)
    return render(request, 'view_art.html', {'artwork': artwork})

