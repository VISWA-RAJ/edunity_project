# lostandfound/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator
# --- THIS IS THE NEW IMPORT ---
from django.contrib import messages 
from .models import LostItem
from .forms import LostItemForm
from core.models import Notification

@login_required
def lostandfound_home_view(request):
    recent_items = LostItem.objects.filter(status='Lost')[:6]
    context = { 'recent_items': recent_items }
    return render(request, 'lostandfound/lost-and-found.html', context)

@login_required
def report_lost_view(request):
    if request.method == 'POST':
        form = LostItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.reported_by = request.user
            item.save()
            messages.success(request, 'Your lost item has been successfully reported!')
            return redirect('lost_and_found')
    else:
        form = LostItemForm()
    return render(request, 'lostandfound/report-lost.html', {'form': form})

@login_required
def all_lost_items_view(request):
    all_items_list = LostItem.objects.filter(status='Lost')
    paginator = Paginator(all_items_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'lostandfound/all_lost_items.html', {'items': page_obj})

@login_required
def item_detail_view(request, item_id):
    item = get_object_or_404(LostItem, id=item_id)
    return render(request, 'lostandfound/item_detail.html', {'item': item})

# --- THIS VIEW IS NOW UPGRADED TO CREATE A MESSAGE ---
@login_required
def found_item_view(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(LostItem, id=item_id)
        
        if item.reported_by != request.user:
            finder_profile_link = reverse('view_user_profile', args=[request.user.username])
            
            Notification.objects.create(
                recipient=item.reported_by,
                sender=request.user,
                message=f'Good news! "{request.user.username}" may have found your item: "{item.item_name}"',
                link=finder_profile_link
            )
            # --- THIS IS THE NEW PART ---
            # This creates a success message that will be shown on the next page
            messages.success(request, f"A notification has been sent to {item.reported_by.username}!")
        else:
            # This creates an error message if they click on their own item
            messages.error(request, "You cannot 'find' your own item.")
            
    # Redirect back to the main list page, where the message will be displayed
    return redirect('lost_and_found')


@login_required
def delete_lost_item_view(request, item_id):
    item = get_object_or_404(LostItem, id=item_id)
    if item.reported_by == request.user and request.method == 'POST':
        item.delete()
        messages.success(request, 'Your post has been deleted.')
    return redirect('lost_and_found')