# memes/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Meme
from .forms import ImageMemeForm, VideoMemeForm, CommentForm

@login_required
def memes_home_view(request):
    return render(request, 'memes/memes.html')

@login_required
def meme_gallery_view(request):
    all_memes_list = Meme.objects.all()
    paginator = Paginator(all_memes_list, 9) # 9 per page for a nice 3x3 grid
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'memes/meme_gallery.html', {'memes': page_obj})

@login_required
def meme_detail_view(request, meme_id):
    meme = get_object_or_404(Meme, id=meme_id)
    comments = meme.comments.all()
    user_has_liked = meme.likes.filter(id=request.user.id).exists()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.meme = meme
            comment.author = request.user
            comment.save()
            return redirect('meme_detail', meme_id=meme.id)
    else:
        comment_form = CommentForm()
    context = {'meme': meme, 'comments': comments, 'comment_form': comment_form, 'user_has_liked': user_has_liked}
    return render(request, 'memes/meme_detail.html', context)

@login_required
def like_meme_view(request, meme_id):
    if request.method == 'POST':
        meme = get_object_or_404(Meme, id=meme_id)
        if meme.likes.filter(id=request.user.id).exists():
            meme.likes.remove(request.user)
        else:
            meme.likes.add(request.user)
    # Redirect back to the page the user was on
    return redirect(request.META.get('HTTP_REFERER', 'meme_gallery'))

@login_required
def post_image_meme_view(request):
    if request.method == 'POST':
        form = ImageMemeForm(request.POST, request.FILES)
        if form.is_valid():
            meme = form.save(commit=False)
            meme.author = request.user
            meme.meme_type = 'IMAGE'
            meme.save()
            return redirect('meme_gallery')
    else:
        form = ImageMemeForm()
    return render(request, 'memes/post_image_meme.html', {'form': form})

@login_required
def post_video_meme_view(request):
    if request.method == 'POST':
        form = VideoMemeForm(request.POST)
        if form.is_valid():
            meme = form.save(commit=False)
            meme.author = request.user
            meme.meme_type = 'VIDEO'
            meme.save()
            return redirect('meme_gallery')
    else:
        form = VideoMemeForm()
    return render(request, 'memes/post_video_meme.html', {'form': form})