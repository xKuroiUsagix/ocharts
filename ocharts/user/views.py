from django.shortcuts import redirect
from django.views import View
from django.conf import settings
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth import login, get_user_model
from django.utils.crypto import get_random_string

from osu import AuthHandler, Client, Scope

from .models import UserProfile


User = get_user_model()


class LoginView(View):
    def get(self, request: HttpRequest):
        user_code = request.GET.get('code')

        if not user_code:
            return redirect('home:index')

        auth = self.get_osu_auth(request)
        auth.get_auth_token(user_code)

        client = Client(auth)
        client_data = client.get_own_data()

        user_profile = UserProfile.objects.filter(osu_id=client_data.id).first()

        if user_profile:
            login(request, user_profile.user)
            return redirect('home:index')

        username = get_random_string(32)
        while User.objects.filter(username=username).exists():
            username = get_random_string(32)

        user = User(username=username)
        user.set_password(get_random_string(32))
        user.save()

        user_profile = UserProfile.objects.create(
            user=user,
            osu_id=client_data.id,
            osu_avatar=client_data.avatar_url,
            osu_username=client_data.username,
        )

        login(request, user_profile.user)
        return redirect('home:index', permanent=True)

    def post(self, request: HttpRequest):
        auth = self.get_osu_auth(request)
        url = auth.get_auth_url()

        return redirect(url)

    def get_osu_auth(self, request) -> AuthHandler:
        redirect_uri = request.build_absolute_uri(reverse('user:osu-auth'))
        return AuthHandler(
            settings.OSU_CLIENT_ID,
            settings.OSU_CLIENT_SECRET,
            redirect_uri,
            Scope.identify(),
        )
