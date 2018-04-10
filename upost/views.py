from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm

def post_list(request):
    posts = Post.objects.order_by('-created')   #To fetch data in reverse order of created
    return render(request, 'upost/post_list.html', {'posts': posts}) 

@login_required
def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
		    post = form.save(commit=False)
		    post.user = request.user
		    post.save()
		    return redirect('post_list')
	else:
		form = PostForm()
		return render(request, 'upost/post_edit.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'upost/post_detail.html', {'post': post})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False) #Table not changed yet
            if post.user == request.user:
                post.save() # since commit = True, changes saved to table
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'upost/post_edit.html', {'form': form})

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user == request.user:
        post.delete()
    return redirect('post_list')

@login_required
def comment_add(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'upost/comment_add.html', {'form': form})

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.post.user == request.user or comment.user == request.user:
        comment.delete()
    return redirect('post_detail', pk=comment.post.pk)