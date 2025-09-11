# notices/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notice
from .forms import NoticeForm
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q # Needed for complex lookups

@login_required
def notice_list_view(request):
    """
    This view now ONLY shows notices that are either permanent
    or have not expired yet.
    """
    now = timezone.now()
    # The Q object allows us to make an "OR" query:
    # Get notices where expiry_date is NULL (permanent) OR expiry_date is in the future.
    all_notices = Notice.objects.filter(
        Q(expiry_date__isnull=True) | Q(expiry_date__gt=now)
    )
    
    context = { 'notices': all_notices }
    return render(request, 'notices/notices.html', context)

@login_required
def post_notice_view(request):
    """
    This view now calculates and saves the expiry_date based on the user's choice.
    """
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.author = request.user
            
            # --- NEW LOGIC TO CALCULATE EXPIRY DATE ---
            duration = form.cleaned_data['expiry_duration']
            if duration == '1_hour':
                notice.expiry_date = timezone.now() + timedelta(hours=1)
            elif duration == '1_day':
                notice.expiry_date = timezone.now() + timedelta(days=1)
            elif duration == '7_days':
                notice.expiry_date = timezone.now() + timedelta(days=7)
            elif duration == 'never':
                notice.expiry_date = None # Set to None for permanent
            
            notice.save()
            return redirect('notices')
    else:
        form = NoticeForm()

    context = { 'form': form }
    return render(request, 'notices/post_notice.html', context)