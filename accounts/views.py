from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from .models import Profile
from . import forms
from .tokens import account_activation_token
from .decorators import ajax_required
import re

def login(request):
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            username = cd['username']
            password = cd['password']
            user = authenticate(request, username=username, password=password)
            forget = False
            if user:
                if user.is_staff:
                    auth_views.login(request, user)
                    return redirect('/admin/')
                else:
                    auth_views.login(request, user)
                    return redirect(reverse('home', args=[user.id]))
            else:
                forget = True
                return render(request, 'registration/login.html', {'error': _('username or password is invalid.'),
                                                                   'register_form': forms.SignUpForm(),
                                                                   'login_form': forms.LoginForm(),
                                                                   'forget':forget,
                                                                   'active': 'login'
                                                                   })
    else:
        return render(request, 'registration/login.html', {'register_form': forms.SignUpForm(),
                                                           'login_form': forms.LoginForm(),
                                                           'active': 'login'
                                                           })


def register(request):
    if request.method == 'POST':
        register_form = forms.SignUpForm(request.POST)
        if register_form.is_valid():
            cd = register_form.cleaned_data
            email = cd['email']
            exist = User.objects.filter(email=email)
            if exist:
                return render(request, 'registration/login.html', {'register_form': forms.SignUpForm(request.POST),
                                                                   'login_form': forms.LoginForm(),
                                                                   'error': 'an user already exist with this email.',
                                                                   'active': 'register'
                                                                   })
            p = re.compile('[\w]+@ut\.ac\.ir')
            # p = re.compile('[\w]+@gmail.com')
            if not p.match(email):
                return render(request, 'registration/login.html', {'register_form': forms.SignUpForm(request.POST),
                                                                   'login_form': forms.LoginForm(),
                                                                   'error': 'incorrect email',
                                                                   'active': 'register'
                                                                   })
            user = register_form.save(commit=False)
            q = re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$")
            if not q.match(cd['password']):
                return render(request, 'registration/login.html', {'register_form': forms.SignUpForm(request.POST),
                                                                   'login_form': forms.LoginForm(),
                                                                   'error': 'weal password',
                                                                   'active': 'register'
                                                                   })
            user.set_password(cd['password'])
            user.is_active = False
            user.save()
            Profile.objects.create(user=user, student_id=cd['student_id'], major=cd['major'])
            user.profile.save()
            # maybe a better subject
            subject = 'Activate your accounts'
            current_site = get_current_site(request)
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            print(message)
            send_mail(subject, message, 'mehransi95@gmail.com', [user.email])
            # return redirect(reverse('accounts:account_activation_sent'))
            return HttpResponse('successful.')
        else:
            return render(request, 'registration/login.html', {'register_form': forms.SignUpForm(request.POST),
                                                               'login_form': forms.LoginForm(),
                                                               'error': register_form.errors,
                                                               'active': 'register'
                                                               })
    else:
        return render(request, 'registration/login.html', {
            'register_form': forms.SignUpForm(),
            'login_form': forms.LoginForm(),
            'active': 'register'
        })


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.profile.email_confirmed = True
        user.is_active = True
        user.save()
        # redirect user to home with a success message
        return redirect(reverse('login'))
    return HttpResponse('Invalid activation code.')


@ajax_required
def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists(),
    }
    if data['is_taken']:
        data['error_message'] = _('An user with this username already exists.')
    return JsonResponse(data)
