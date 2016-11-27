from django import forms
class UserForm(forms.ModelForm):
    class Meta:
        model = Name_space
        widgets = {
        'password': forms.PasswordInput(),
    }