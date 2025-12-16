from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user.forms import RegisterForm, ProfileForm


def register(request: HttpRequest):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user:login')

    else: form = RegisterForm()

    return render(request, 'auth/register.html', {
        'form': form
    })

@login_required
def profile(request: HttpRequest):
    return render(request, 'auth/profile.html')

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("user:profile")
    else:
        form = ProfileForm(instance=request.user)

    return render(request, "auth/edit-profile.html", {"form": form})
