from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _

from . import forms
from .tokens import account_activation_token
from .decorators import ajax_required


def login(request):
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            username = cd['username']
            password = cd['password']
            user = authenticate(request, username=username, password=password)
            if user:
                auth_views.login(request, user)
                return HttpResponse('Hello {0}'.format(username))
            else:
                return render(request, 'registration/login.html', {'error': _('username or password is invalid.'),
                                                                   'register_form': forms.SignUpForm(),
                                                                   'login_form': forms.LoginForm(),
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
            user = register_form.save(commit=False)
            user.is_active = False
            user.set_password(cd['password'])
            user.save()
            # maybe a better subject
            subject = 'Activate your accounts'
            current_site = get_current_site(request)
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_mail(subject, message, 'admin@admin.com', [user.email])
            # return redirect(reverse('accounts:account_activation_sent'))
            return HttpResponse('An email was sent to your email.')
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
        return HttpResponse("Dear {0} your accounts successfully activate".format(user.username))
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
