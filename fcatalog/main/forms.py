from .models import Teacher
from django.forms import CharField, Form, TextInput


class TeacherLoginForm(Form):
    email = CharField(
        widget=TextInput(
            attrs={
                "id": "email",
                "placeholder": "Електронна пошта",
            }
        )
    )
    password = CharField(
        widget=TextInput(
            attrs={
                "id": "password",
                "placeholder": "Пароль",
            }
        )
    )
