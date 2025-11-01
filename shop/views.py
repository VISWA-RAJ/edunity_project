from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ShopItem
from core.models import Profile # We need the Profile to manage tokens and inventory

@login_required
def shop_home_view(request):
    """
    Displays all available shop items.
    It also checks what the user already owns and how many tokens they have.
    """
    all_items = ShopItem.objects.all()
    profile = request.user.profile
    user_tokens = profile.tokens
    
    # Get a list of IDs for items the user has already purchased
    user_inventory_ids = profile.purchased_items.values_list('id', flat=True)

    context = {
        'all_items': all_items,
        'user_tokens': user_tokens,
        'user_inventory_ids': list(user_inventory_ids), # Pass the list of IDs to the template
    }
    return render(request, 'shop/shop.html', context)


@login_required
def buy_item_view(request, item_id):
    """
    Handles the logic for purchasing a single item.
    """
    if request.method == 'POST':
        item_to_buy = get_object_or_404(ShopItem, id=item_id)
        profile = request.user.profile

        # 1. Check if user already owns the item
        if profile.purchased_items.filter(id=item_to_buy.id).exists():
            messages.error(request, "You already own this item!")
            return redirect('shop')

        # 2. Check if user has enough tokens
        if profile.tokens < item_to_buy.price:
            messages.error(request, "You don't have enough tokens to buy this.")
            return redirect('shop')
            
        # 3. All checks passed: Perform the transaction
        profile.tokens -= item_to_buy.price
        profile.purchased_items.add(item_to_buy)
        profile.save()

        messages.success(request, f"Successfully purchased {item_to_buy.name}!")

    return redirect('shop')
