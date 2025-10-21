from django.shortcuts import redirect, render
from .models import Teacher, Discipline
from .forms import TeacherLoginForm

###########################################################################
# webhook
import subprocess
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def github_webhook(request):
    if request.method == "POST":
        # Запускаємо скрипт оновлення асинхронно
        subprocess.Popen(["/bin/bash", "/home/librwebapp/update_site.sh"])
        return HttpResponse("Update started", status=200)
    return HttpResponse("OK")


############################################################################


def index(request):
    return render(request, "index.html")


def teacher(request):
    email = request.session.get("email")
    if not email or not Teacher.objects.filter(email=email).exists():
        return redirect("login")
    return render(
        request,
        "teacher.html",
        {
            "email": email,
        },
    )


def login(request):
    form = TeacherLoginForm()
    if request.method == "POST":
        form = TeacherLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            if Teacher.objects.filter(email=email).exists():
                user = Teacher.objects.get(email=email)
                if user.password == password:
                    request.session["email"] = email
                    return redirect(
                        "teacher",
                    )
            return render(
                request,
                "login.html",
                {"form": form, "error": "Неправильна пошта або пароль"},
            )

    return render(
        request,
        "login.html",
        {
            "form": form,
        },
    )
