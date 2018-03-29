from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

from user.forms import UserAuthForm, UserLoginForm, TwoFactorForm
from user.utils import generate_secret, confirm_totp_token


def register(request):
    if request.method == 'POST':
        form = UserAuthForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            login(request, user=user)
            two_factor_form = TwoFactorForm()
            secret_key = generate_secret()
            user.secret_key = secret_key
            user.save()
            context = {'secret_key': secret_key, 'form': two_factor_form}
            return render(request, 'user/two_factor.html', context)
            # return HttpResponse("Thank you very much %s, this is your login page" % request.user.username)
        else:
            context = {'form': form}
            return render(request, 'user/register.html', context=context)
    else:
        form = UserAuthForm()
        context = {'form': form}
        return render(request, 'user/register.html', context=context)


def two_factor_view(request):
    user = request.user
    form = TwoFactorForm(request.POST)
    if form.is_valid():
        otp = form.cleaned_data['OTP']
        if confirm_totp_token(otp, user.secret_key):
            return render(request, 'user/index.html', context={'user': user})
        else:
            form.add_error('OTP', 'OTP is wrong, enter again')
            context = {'form': form}
            return render(request, 'user/two_factor.html', context=context)
    else:
        context = {'form': form}
        return render(request, 'user/two_factor.html', context=context)


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request=request, username=data['username'], password=data['password'])
            if user is not None:
                login(request, user=user)
                two_factor_form = TwoFactorForm()
                context = {'form': two_factor_form}
                return render(request, 'user/two_factor.html', context)
            else:
                return HttpResponse('The user is not registered')
        else:
            context = {'form': form}
            return render(request, 'user/login.html', context=context)
    else:
        form = UserLoginForm()
        context = {'form': form}
        return render(request, 'user/login.html', context=context)


def me(request):
    print(request.user)
    return HttpResponse(request.user.username)


def logout_view(request):
    logout(request)
    return HttpResponse("You have been logged out :)")
