from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.utils.translation import ugettext_lazy as _

from accounts.models import Major


class SignUpForm(forms.ModelForm):

    username = forms.CharField(label=_('username'),
                               widget=forms.TextInput(attrs={'class': 'form-control'}),
                               max_length=30,
                               required=True,
                               )
    password = forms.CharField(label=_('password'),
                               widget=forms.PasswordInput(attrs={'class': 'form-control'})
                               )

    confirm_password = forms.CharField(label=_('confirm_password'),
                                       widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                       required=True)
    email = forms.CharField(label=_('email'),
                            widget=forms.EmailInput(attrs={'class': 'form-control'}),
                            required=True,
                            max_length=75)
    student_id = forms.IntegerField(max_value=999999999, min_value=10**8,)

    major = forms.ModelChoiceField(queryset=Major.objects.all())


    class Meta:
        model = User
        exclude = ['last_login', 'date_joined']
        fields = ['username', 'email', 'password', 'confirm_password', 'student_id']

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            self._errors['password'] = self.error_class(
                [_('Passwords don\'t match')])
        else:
            user = self.save(commit=False)
            password_validation.validate_password(password, user)
        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(label=_('username'),
                               widget=forms.TextInput(attrs={'class': 'form-control'}),
                               max_length=30,
                               required=True,
                               )
    password = forms.CharField(label=_('password'),
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
