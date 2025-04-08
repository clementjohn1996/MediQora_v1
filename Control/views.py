from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.templatetags.static import static
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from .forms import UserForm, UserProfileForm

@login_required
def dashboard_view(request):
    return render(request, 'control/dashboard.html')

@login_required
def profile_view(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/profile.html', {'user': request.user}, request=request)
        return JsonResponse({'html': html})
    return redirect('dashboard')  # fallback if accessed normally




@login_required
def settings_view(request):
    user = request.user
    profile = getattr(user, 'profile', None)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return JsonResponse({"success": True})
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    html = render_to_string("settings.html", {
        "user_form": user_form,
        "profile_form": profile_form
    }, request=request)

    return JsonResponse({"html": html})


@login_required
def charts_view(request):
    return render(request, 'control/charts.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'Control/login.html')
