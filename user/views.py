from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout

from user.forms import UserAuthForm, UserLoginForm, TwoFactorForm
from user.utils import generate_secret, confirm_totp_token, verify_user, two_factor_login_required


def register(request):
    if request.method == 'POST':
        form = UserAuthForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            login(request, user=user)
            return HttpResponseRedirect(reverse_lazy('two-factor-verification', kwargs={'source': 'register'}))
        else:
            context = {'form': form}
            return render(request, 'user/register.html', context=context)
    else:
        form = UserAuthForm()
        context = {'form': form}
        return render(request, 'user/register.html', context=context)


@login_required(login_url=reverse_lazy('login'))
def two_factor_view(request, source):
    user = request.user
    if request.method == 'POST':
        form = TwoFactorForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['OTP']
            g_response = form.cleaned_data['g_recaptcha_response']
            if not verify_user(g_response):
                form.add_error(None, "ReCapcha can't verify you!")
                context = {'form': form}
                return render(request, 'user/two_factor.html', context=context)
            if confirm_totp_token(otp, user.secret_key):
                user.auth_complete = True
                # TODO: redirect to the login page, instead of just
                return render(request, 'user/index.html', context={'user': user})
            else:
                form.add_error('OTP', 'OTP is wrong, enter again')
                context = {'form': form}
                return render(request, 'user/two_factor.html', context=context)
        else:
            context = {'form': form}
            return render(request, 'user/two_factor.html', context=context)
    else:
        if source == 'register':
            if user.secret_key:
                return HttpResponseRedirect(reverse_lazy('two-factor-verification', kwargs={'source': 'login'}))
            two_factor_form = TwoFactorForm()
            secret_key = generate_secret()
            user.secret_key = secret_key
            user.save()
            context = {'secret_key': secret_key, 'form': two_factor_form, 'user': user}
            return render(request, 'user/two_factor.html', context)
        elif source == 'login':
            two_factor_form = TwoFactorForm()
            context = {'form': two_factor_form, 'user': user}
            return render(request, 'user/two_factor.html', context)
        else:
            raise Http404("Not Found")


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request=request, username=data['username'], password=data['password'])
            if user is not None:
                login(request, user=user)
                return HttpResponseRedirect(reverse_lazy('two-factor-verification', kwargs={'source': 'login'}))
            else:
                # return HttpResponse('Wrong credentials')
                form.add_error(None, "Wrong Credentials")
                context = {'form': form}
                return render(request, 'user/login.html', context=context)
        else:
            context = {'form': form}
            return render(request, 'user/login.html', context=context)
    else:
        form = UserLoginForm()
        context = {'form': form}
        return render(request, 'user/login.html', context=context)


@login_required(login_url=reverse_lazy('login'))
@two_factor_login_required
def me(request):
    user = request.user
    return render(request, 'user/index.html', context={'user': user})


def logout_view(request):
    request.user.auth_complete = False
    logout(request)
    return HttpResponseRedirect(reverse_lazy('index'))
