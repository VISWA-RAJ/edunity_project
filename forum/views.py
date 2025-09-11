# forum/views.py

# --- THE FIXES ARE IN THESE IMPORT LINES ---
from django.shortcuts import render, redirect, get_object_or_404  # <-- ADDED get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Doubt, Reply  # <-- ADDED Reply
from .forms import DoubtForm, ReplyForm  # <-- ADDED ReplyForm
from django.core.paginator import Paginator # <-- ADD THIS LINE

@login_required
def forum_home_view(request):
    # Get the 5 most recent doubts for the main page
    recent_doubts = Doubt.objects.all()[:5]
    context = {
        'recent_doubts': recent_doubts
    }
    return render(request, 'forum/forum.html', context)

@login_required
def ask_doubt_view(request):
    if request.method == 'POST':
        # --- THE CHANGE IS HERE ---
        # We must add request.FILES to handle the image upload
        form = DoubtForm(request.POST, request.FILES)
        if form.is_valid():
            doubt = form.save(commit=False)
            doubt.author = request.user
            doubt.save()
            return redirect('forum')
    else:
        form = DoubtForm()
    
    return render(request, 'forum/ask_doubt.html', {'form': form})

@login_required
def doubt_list_view(request):
    all_doubts_list = Doubt.objects.all()
    
    # --- NEW PAGINATION LOGIC ---
    paginator = Paginator(all_doubts_list, 6) # Show 6 doubts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'forum/doubt_list.html', {'doubts': page_obj})


@login_required
def doubt_detail_view(request, doubt_id):
    doubt = get_object_or_404(Doubt, id=doubt_id)
    replies = doubt.replies.all()
    
    if request.method == 'POST':
        # This part handles submitting a new reply
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.doubt = doubt
            reply.author = request.user
            reply.save()
            return redirect('doubt_detail', doubt_id=doubt.id)
    else:
        # This part handles displaying the page initially
        reply_form = ReplyForm()

    context = {
        'doubt': doubt,
        'replies': replies,
        'reply_form': reply_form, # --- THE FIX: The context variable is now correct ---
    }
    return render(request, 'forum/doubt_detail.html', context)


@login_required
def vote_reply_view(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    
    if request.method == 'POST':
        vote_type = request.POST.get('vote_type')

        # Logic for upvoting
        if vote_type == 'upvote':
            if request.user in reply.upvotes.all():
                # User has already upvoted, so remove the upvote (neutral)
                reply.upvotes.remove(request.user)
            else:
                # User has not upvoted, so add the upvote
                reply.upvotes.add(request.user)
                # Ensure user is not in downvotes
                reply.downvotes.remove(request.user)
        
        # Logic for downvoting
        elif vote_type == 'downvote':
            if request.user in reply.downvotes.all():
                # User has already downvoted, so remove the downvote (neutral)
                reply.downvotes.remove(request.user)
            else:
                # User has not downvoted, so add the downvote
                reply.downvotes.add(request.user)
                # Ensure user is not in upvotes
                reply.upvotes.remove(request.user)

    # Redirect back to the doubt detail page where the vote happened
    return redirect('doubt_detail', doubt_id=reply.doubt.id)