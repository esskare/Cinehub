"""
handles different views form other pages, other views will appear here

"""
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

#retrieves home tmeplate 
def home(request):
	movies = Movie.objects.all()
	context = {'movies': movies}
	return render(request, "home.html", context)


#retrieves login template
def login_page(request):
	if request.method == "POST":
		try:
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = User.objects.filter(username=username) 
			
			if not user.exists():
				messages.error(request, "Username not found")
				return redirect('/login/')
			
			user = authenticate(username=username, password=password)
			
			if user:
				login(request, user)
				return redirect('/')
			
			messages.error(request, "Wrong Password")
			return redirect('/login/')
		
		except Exception as e:
			messages.error(request, "Something went wrong")
			return redirect('/register/')
	
	return render(request, "login.html")

#retrieves the register template
def register_page(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is taken")
                return redirect('/register/')

            if password != confirm_password:
                messages.error(request, "Passwords do not match")
                return redirect('/register/')

            user = User.objects.create_user(username=username, email=email, password=password)

            messages.success(request, "Account created")
            return redirect('/login/')

        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('/register/')

    return render(request, "register.html")
@login_required(login_url="/login/")

def add_cart(request, movie_uid):
	user = request.user
	movie_obj = Movie.objects.get(uid=movie_uid)
	
	cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
	cart_items = CartItems.objects.create(cart=cart, movie=movie_obj)
	
	return redirect('/')
@login_required(login_url='/login/')

#renders the cart template
def cart(request):
	cart = Cart.objects.get(is_paid=False, user=request.user)
	context = {'carts': cart}
	return render(request, "cart.html", context)
@login_required(login_url='/login/')

#redirects to cart after a specific item has been removed
def remove_cart_item(request, cart_item_uid):
	try:
		CartItems.objects.get(uid=cart_item_uid).delete()
		return redirect('/cart/')
	except Exception as e:
		print(e)


