from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

@login_required
def home(request):
    game = Game.objects.all()
    return render(request, 'site/home.html', {'game': game})

def index(request):
    user = request.user    
    games = Game.objects.all()
    data_game = []
    for game in games:
        data_game.append(    
            {
            'games': game,
            'liked': game.user_liked(user) if user.is_authenticated else False,
            'comments': Comment.objects.filter(game=game)
            }
        )
    return render(request, 'site/index.html', {'games': data_game})

@login_required
def like_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    like, created = Like.objects.get_or_create(user=request.user, game=game)
    if not created:
        like.delete()
    return redirect('index')

@login_required
def comment_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(user=request.user, game=game, content=content)
    return redirect('index')

@login_required
def create(request):
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Jogo cadastrado com sucesso!')
            return redirect('home')
    else:
        form = GameForm()
    return render(request, 'site/create.html', {'form': form})

@login_required
def edit(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            form.save()
            messages.success(request, 'Jogo editado com sucesso!')
            return redirect('index')
    else:
        form = GameForm(instance=game)
    return render(request, "site/update.html",{"form":form, "game":game})

@login_required
def delete_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.method == 'POST':
        game.delete()
        messages.success(request, 'Jogo deletado com sucesso!')
        return redirect('home')
    return render(request, 'site/delete.html', {'game': game})

def add_to_cart(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, game=game, quantity=1)
    cart_count = CartItem.objects.filter(cart=cart).count() if request.user.is_authenticated else 0
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return JsonResponse({'success': 'true', 'quantity': cart_item.quantity, 'cart_count': cart_count})

def remove_from_cart(request, game_id):
    cart_item = get_object_or_404(CartItem, id=game_id)
    cart_item.delete()
    return JsonResponse({'success': 'true'})

def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    cart_count = CartItem.objects.filter(cart=cart).count() if request.user.is_authenticated else 0
    return render(request, 'site/cart.html', {'cart': cart, 'items': items, 'cart_count': cart_count})

def update_cart_item(request, game_id):
    cart_item = get_object_or_404(CartItem, id=game_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1
        cart_item.save()
        return JsonResponse({'success': 'true', 'quantity': cart_item.quantity})

def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    total_price = sum( item.quantity * item.game.value for item in items)
    if request.method == 'POST':
        cart.delete()
        messages.success(request, 'Compra realizada com sucesso!')
        return redirect('index')
    return render(request, 'site/checkout.html', {'cart': cart, 'total_price': total_price})

@login_required
def dashboard(request):
    user = request.user
    users = User.objects.all()
    games = Game.objects.all()
    data_game = []
    for game in games:
        data_game.append(    
            {
            'games': game,
            'liked': game.user_liked(user) if user.is_authenticated else False,
            'comments': Comment.objects.filter(game=game)
            }
        )
    return render(request, 'site/dashboard.html', {'games': data_game, 'users': users})

def user_list(request):
    users = User.objects.all()

    return render(request, 'site/dash/user_list.html', {'users': users})

def game_list(request):
    user = request.user
    games = Game.objects.all()
    data_game = []
    for game in games:
        data_game.append(    
            {
            'games': game,
            'liked': game.user_liked(user) if user.is_authenticated else False,
            'comments': Comment.objects.filter(game=game)
            }
        )
    return render(request, 'site/dash/game_list.html', {'games': data_game})