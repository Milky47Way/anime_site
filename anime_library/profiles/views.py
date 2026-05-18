from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from .models import Profile, UserAnime
from .forms import CustomUserCreationForm
from django.db.models import Sum


def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    watched_count = UserAnime.objects.filter(user=profile.user, status='COMPLETED').count()
    planning_count = UserAnime.objects.filter(user=profile.user, status='PLANNING').count()
    completed_entries = UserAnime.objects.filter(user=profile.user, status='COMPLETED')
    movies_count = completed_entries.aggregate(total=Sum('anime__movies_count'))['total'] or 0

    context = {
        'profile': profile,
        'watched_count': watched_count,
        'planning_count': planning_count,
        'movies_count': movies_count,
    }
    return render(request, 'profiles/profile1_detail.html', context)
@login_required
def my_list(request):
    anime_list = UserAnime.objects.filter(user=request.user)

    if request.method == 'POST':
        for item in anime_list:
            status_key = f'status_{item.id}'
            episodes_key = f'episodes_{item.id}'

            if status_key in request.POST:
                item.status = request.POST.get(status_key)
            if episodes_key in request.POST:
                item.episodes_watched = request.POST.get(episodes_key, 0)
            item.save()
        return redirect('profiles:my_list')

    return render(request, 'profiles/profile_list.html', {'anime_list': anime_list})


@login_required
def profile_settings(request):
    profile = request.user.profile

    if request.method == 'POST':
        profile.nickname = request.POST.get('nickname', '')
        profile.bio = request.POST.get('bio', '')
        profile.region = request.POST.get('region')
        if request.POST.get('birth_date'):
            profile.birth_date = request.POST.get('birth_date')

        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']

        if request.POST.get('avatar-clear'):
            profile.avatar = None

        profile.save()
        return redirect('profiles:profile_detail', pk=profile.pk)

    return render(request, 'profiles/settings.html', {'profile': profile})


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('anime:anime_list')
    return redirect('profiles:profile_settings')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if email and User.objects.filter(email=email).exists():
                form.add_error('email', "Ця пошта вже зайнята іншим користувачем!")
            else:
                user = form.save()
                Profile.objects.get_or_create(user=user)

                auth_login(request, user)
                return redirect('anime:anime_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'profiles/register.html', {'form': form})