import uuid
from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponseRedirect
from django.utils.timezone import now

from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from users.models import User, EmailVerification
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from products.models import Basket
from django.contrib.auth.views import LogoutView, LoginView
from common.views import TitleMixin
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.base import TemplateView


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'GeekShop - Авторизация'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        messages.success(self.request, f'{username}, вы успешно вошли!')
        return super().form_valid(form)


class UserRegistrationView(TitleMixin, CreateView):
    model = User
    template_name = 'users/registration.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    title = 'GeekShop - Регистрация'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        response = super().form_valid(form)

        messages.success(self.request, f'Аккаунт успешно создан! Здравствуйте, {username}, вам на почту отправлено письмо с подтверждением аккаунта!')
        return response


class EmailVerificationView(TitleMixin, TemplateView):
    template_name = 'users/email_verification.html'
    title = 'GeekShop - Подтверждение почты'

    def get(self, request, *args, **kwargs):
        code = kwargs.get('code')
        user = User.objects.get(email=kwargs.get('email'))
        email_verification = EmailVerification.objects.filter(user=user, code=code).first()

        if email_verification.is_expired:
            email_verification.code = uuid.uuid4()
            email_verification.expiration = now() + timedelta(hours=48)
            email_verification.save()
            email_verification.send_verification_email(is_expired=True)
            messages.error(request, 'Срок действия ссылки истек! Новая ссылка отправлена на почту!')
            return HttpResponseRedirect(reverse('index'))


        if email_verification:
            user.is_verified_email = True
            user.save()
            messages.success(request, 'Ваша почта успешно подтверждена, можете авторизоваться!')
            return super().get(request, *args, **kwargs)
        else:
            messages.error(request, 'Срок действия ссылки истек! Новая ссылка отправлена на вашу почту!')
            return HttpResponseRedirect(reverse('index'))


class UserProfileView(TitleMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    login_url = reverse_lazy('users:login')
    title = 'Store - Профиль'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.object.id})


class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        username = request.user.username
        messages.success(request, f'{username}, вы вышли из аккаунта 😒!')
        return super().dispatch(request, *args, **kwargs)










