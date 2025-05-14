from django.contrib.auth.decorators import login_required
from django.shortcuts import render , redirect
from .forms import TrackedCoinForm
from .models import TrackedCoin
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def track_coin_view(request):
    if request.method == 'POST':
        coin_name = request.POST.get('coin_name')
        # You may need to fetch coin details from an external API
        coin_symbol = "BTC"  # Example, fetch the actual symbol based on the coin_name
        tracked_coin = TrackedCoin.objects.create(
            user=request.user,
            name=coin_name,
            symbol=coin_symbol,
        )
        return redirect('dashboard')

    return render(request, 'track_coin.html')

def custom_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout

@login_required
def dashboard(request):
    user_coins = TrackedCoin.objects.filter(user=request.user)
    if request.method == 'POST':
        form = TrackedCoinForm(request.POST)
        if form.is_valid():
            coin = form.save(commit=False)
            coin.user = request.user

            # Check if the user is already tracking this coin
            exists = TrackedCoin.objects.filter(user=request.user, coin_name=coin.coin_name).exists()

            if not exists:
                coin.save()
            else:
                messages.warning(request, f"You are already tracking {coin.coin_name.capitalize()}.")

            return redirect('dashboard')

    else:
        form = TrackedCoinForm()
    return render(request, 'dashboard.html', {'form': form, 'coins': user_coins})


@login_required
@require_POST
def delete_tracked_coin_ajax(request):
    coin_id = request.POST.get('coin_id')
    coin = get_object_or_404(TrackedCoin, id=coin_id, user=request.user)
    coin.delete()
    return JsonResponse({'success': True, 'coin_id': coin_id})
