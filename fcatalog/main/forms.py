from django.forms import CharField, Form, TextInput


class TeacherLoginForm(Form):
    email = CharField(
        widget=TextInput(
            attrs={
                "id": "email",
                "placeholder": "Електронна пошта",
            }
        ),
        # щоб джанго не перевіряв сам (перевірку робимо вручну через js)
        required=False,
    )
    password = CharField(
        widget=TextInput(
            attrs={
                "id": "password",
                "placeholder": "Пароль",
            }
        ),
        # щоб джанго не перевіряв сам (перевірку робимо вручну через js)
        required=False,
    )
