from django.shortcuts import redirect, render
from .models import Teacher, Discipline
from .forms import TeacherLoginForm, AddDisciplineForm
from django.contrib.auth.models import User

###########################################################################
# webhook
import subprocess
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def github_webhook(request):
    print("test code")
    if request.method == "POST":
        # Запускаємо скрипт оновлення асинхронно
        subprocess.Popen(["/bin/bash", "/home/librwebapp/update_site.sh"])
        return HttpResponse("Update started", status=200)
    return HttpResponse("OK", status=200)


############################################################################


def index(request):
    disciplines = Discipline.objects.filter(is_approved=True)
    for discipline in disciplines:
        print(discipline)
    return render(request, "index.html")


def teacher(request):
    email = request.session.get("email")
    if not email or not Teacher.objects.filter(email=email).exists():
        return redirect("login")
    form = AddDisciplineForm()
    if request.method == "POST":
        form = AddDisciplineForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            disciplines = Discipline.objects.filter(title=title)
            for discipline in disciplines:
                if discipline.is_approved == True:
                    return render(
                        request,
                        "teacher.html",
                        {
                            "email": email,
                            "form": form,
                            "error": "Така дисципліна вже існує",
                        },
                    )
            description = form.cleaned_data["description"]
            Discipline.objects.create(
                title=title,
                description=description,
                teacher=Teacher.objects.get(email=email),
                admin=User.objects.get(id=1),
            )

    return render(
        request,
        "teacher.html",
        {
            "email": email,
            "form": form,
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


def logout(request):
    request.session.flush()
    return redirect("/")
