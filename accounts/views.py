from django.contrib.auth import login, authenticate
from django.shortcuts import render, get_object_or_404,  redirect
from .forms import RegisterForm, EditForm
from django.contrib.auth.models import User
from .models import Profile
from upost.models import Post

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()	
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('post_list')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def profile(request, pk=None):
	# 	user = Profile.objects.filter(user=request.user.id)[0]
	if pk:
		user = get_object_or_404(User, pk=pk)
	else:
		user = request.user
	posts = Post.objects.filter(user=user)
	return render(request, 'registration/profile.html', {'profile_user': user, 'posts':posts})

def edit_profile(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == "POST":
        form = EditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False) #Table not changed yet
            if profile.user == request.user:
                profile.save() # since commit = True, changes saved to table
            return redirect('profile')
    else:
        form = EditForm(instance=profile)
    return render(request, 'registration/edit_profile.html', {'form': form})