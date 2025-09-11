# polls/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Poll, Choice
from .forms import PollForm

@login_required
def polls_home_view(request):
    polls = Poll.objects.all().order_by('-created_at')
    return render(request, 'polls/polls.html', {'polls': polls})

@login_required
def create_poll_view(request):
    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            # Create the Poll object first
            new_poll = Poll.objects.create(
                question=form.cleaned_data['question'],
                created_by=request.user
            )
            # Create the required Choice objects
            Choice.objects.create(poll=new_poll, text=form.cleaned_data['choice1'])
            Choice.objects.create(poll=new_poll, text=form.cleaned_data['choice2'])
            
            # Create optional Choice objects if they were filled out
            if form.cleaned_data['choice3']:
                Choice.objects.create(poll=new_poll, text=form.cleaned_data['choice3'])
            if form.cleaned_data['choice4']:
                Choice.objects.create(poll=new_poll, text=form.cleaned_data['choice4'])
            
            return redirect('polls')
    else:
        form = PollForm()
    
    return render(request, 'polls/create_poll.html', {'form': form})

@login_required
def vote_view(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    
    if request.method == 'POST':
        # Check if user has already voted
        if request.user in poll.voters.all():
            messages.error(request, "You have already voted on this poll.")
            return redirect('polls')

        choice_id = request.POST.get('choice')
        if choice_id:
            choice = get_object_or_404(Choice, id=choice_id)
            choice.votes += 1
            choice.save()
            # Add user to the list of voters for this poll
            poll.voters.add(request.user)
            messages.success(request, "Your vote has been recorded!")
        else:
            messages.error(request, "You didn't select a choice.")

    return redirect('polls')