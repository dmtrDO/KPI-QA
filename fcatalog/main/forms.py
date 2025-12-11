from django.forms import CharField, Form, TextInput, Textarea, PasswordInput


class TeacherLoginForm(Form):
    email = CharField(
        widget=TextInput(
            attrs={
                "id": "email",
                "type": "text",
                "placeholder": "Електронна пошта",
            }
        ),
        # щоб джанго не перевіряв сам (перевірку робимо вручну через js)
        required=False,
    )
    password = CharField(
        widget=PasswordInput(
            attrs={
                "id": "password",
                "type": "password",
                "placeholder": "Пароль",
            }
        ),
        # щоб джанго не перевіряв сам (перевірку робимо вручну через js)
        required=False,
    )


class AddDisciplineForm(Form):
    title = CharField(
        widget=TextInput(attrs={}),
        required=True,
    )

    description = CharField(
        widget=Textarea(
            attrs={
                "rows": 5,
            }
        ),
        required=True,
    )
