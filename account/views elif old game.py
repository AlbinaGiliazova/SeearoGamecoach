# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import User
from account.forms import UploadPhotoForm, SettingsForm
from account.models import GameDirection, Game, Direction, Region

default_context = {'trademark': settings.TRADEMARK,
                   'current_year': datetime.now().strftime('%Y')}

def level_up(current_level):
    # how much experience needed for the next level
    dict = {2: 1500,
            3: 2500,
            4: 4000,
            5: 6000,
            6: 8500,
            7: 10500,
            8: 12800,
            9: 14200,
            10: 16700}
    # далее по 10 процентов шаг или около того
    # взяв лвл, экспа считается с 0
    if current_level + 1 in dict:
        return dict[current_level + 1]
    else:
        return round(dict[10] * 1.1 ** (current_level - 10))


class AccountView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = default_context
            user = User.objects.get(username=request.user)
            context['user'] = user
            if user.profile.photo:
                context['photo'] = user.profile.photo.url
            else:
                context['photo'] = ''
            context['settings_form'] = SettingsForm()
            return render(request, 'account/account.html', context=context)
        else:
            return redirect('index.html')


class AchievementsView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = default_context
            user = User.objects.get(username=request.user)
            context['user'] = user
            return render(request, 'account/achievements.html', context=context)
        else:
            return redirect('index.html')


class BookmarksView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = default_context
            user = User.objects.get(username=request.user)
            context['user'] = user
            return render(request, 'account/bookmarks.html', context=context)
        else:
            return redirect('index.html')


class ChatidView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = default_context
            user = User.objects.get(username=request.user)
            context['user'] = user
            return render(request, 'account/chatid1598737bi.html', context=context)
        else:
            return redirect('index.html')


class CoachOfficeView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = default_context
            user = User.objects.get(username=request.user)
            context['user'] = user
            return render(request, 'account/coach-office.html', context=context)
        else:
            return redirect('index.html')


class DiaryView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = default_context
            user = User.objects.get(username=request.user)
            context['user'] = user
            return render(request, 'account/diary.html', context=context)
        else:
            return redirect('index.html')


class FriendsView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = default_context
            user = User.objects.get(username=request.user)
            context['user'] = user
            return render(request, 'account/friends.html', context=context)
        else:
            return redirect('index.html')


class MessageView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = default_context
            user = User.objects.get(username=request.user)
            context['user'] = user
            return render(request, 'account/message.html', context=context)
        else:
            return redirect('index.html')


class ProfileView(View):

    def get(self, request, user_id, *args, **kwargs):
        if request.user.is_authenticated:
            context = default_context
            # https://stackoverflow.com/questions/17312831/what-does-request-user-refer-to-in-django
            user = User.objects.get(username=request.user)
            context['user'] = user
            if request.user.id == user_id:
                if user.profile.games and str(user.profile.games) != 'account.Game.None':
                    context['games'] = user.profile.games
                else:
                    context['games'] = ''
                context['level_up'] = level_up(user.profile.level)
                context['value_now'] = round(user.profile.level / context['level_up'] * 100)
                if user.profile.photo:
                    context['photo'] = user.profile.photo.url
                else:
                    context['photo'] = ''
                context['upload_photo_form'] = UploadPhotoForm()
                return render(request, 'account/profile.html', context=context)
            else:
                context['other_user'] = User.objects.get(id=user_id)
                return render(request, 'account/other/profile.html', context=context)
        else:
            return render(request, 'account/other/profile.html', context=default_context)

class SettingsView(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            form = SettingsForm(request.POST, request.FILES, instance=request.user.profile)
            if form.is_valid():
                if request.FILES.get('photo'):
                    user.profile.photo = request.FILES.get('photo')
                if request.POST.get('first_name'):
                    user.first_name = request.POST.get('first_name')
                if request.POST.get('last_name'):
                    user.last_name = request.POST.get('last_name')
                if request.POST.get('nickname'):
                    user.profile.nickname = request.POST.get('nickname')
                if request.POST.get('game') or request.POST.get('direction') or request.POST.get('region'):
                    gamedirection = GameDirection()
                    if request.POST.get('game'):
                        gamedirection.game = Game.objects.get(id = request.POST.get('game'))
                    elif user.profile.gamedirections[0].game:
                        gamedirection.game = user.profile.gamedirections[0].game
                    if request.POST.get('direction'):
                        gamedirection.direction = Direction.objects.get(id = request.POST.get('direction'))
                    elif user.profile.gamedirections[0].direction:
                        gamedirection.direction = user.profile.gamedirections[0].direction
                    if request.POST.get('region'):
                        gamedirection.region = Region.objects.get(id = request.POST.get('region'))
                    elif user.profile.gamedirections[0].region:
                        gamedirection.region = user.profile.gamedirections[0].region
                    for gd in GameDirection.objects.all():
                        if gd.game == gamedirection.game \
                        and gd.direction == gamedirection.direction \
                        and gd.region == gamedirection.region:
                            gamedirection = gd
                            break
                    user.profile.gamedirections.add(gamedirection)
                if request.POST.get('contacts'):
                    user.profile.contacts = request.POST.get('contacts')
                user.save()
            return redirect('../account/profile.html/user_id{0}'.format(user.id))

        else:
            return redirect('index.html')


class UploadPhotoView(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            # https://qna.habr.com/q/71870
            form = UploadPhotoForm(request.FILES, instance=request.user.profile)
            if form.is_valid():
                if request.FILES.get('photo'):
                    user.profile.photo = request.FILES.get('photo')
                    user.save()
            return redirect('profile.html/user_id{0}'.format(user.id))

        else:
            return redirect('index.html')