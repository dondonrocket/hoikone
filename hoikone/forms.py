from django import forms
from .models import CustomUser
from django.contrib.auth.forms import (
    UserCreationForm, PasswordResetForm, SetPasswordForm,
    AuthenticationForm, UserCreationForm, PasswordChangeForm,
)
from django.contrib.auth import get_user_model
#from django.contrib.auth.models import CustomUser

CustomUser = get_user_model()

class MyPasswordResetForm(PasswordResetForm):
    """パスワード忘れたときのフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MySetPasswordForm(SetPasswordForm):
    """パスワード再設定用フォーム(パスワード忘れて再設定)"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class NewPasswordForm(forms.Form):
    current_password = forms.CharField(label='Current Password', widget=forms.PasswordInput)
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput)
    confirm_new_password = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        if new_password and confirm_new_password and new_password != confirm_new_password:
            raise forms.ValidationError("新しいパスワードが一致しません。")

        return cleaned_data


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class MyPasswordChangeForm(PasswordChangeForm):
    """パスワード変更フォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class EmailChangeForm(forms.ModelForm):
    """メールアドレス変更フォーム"""

    class Meta:
        model = CustomUser
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        CustomUser.objects.filter(email=email, is_active=False).delete()
        return email