from django.shortcuts import redirect, render
from .models import Teacher, Discipline
from .forms import TeacherLoginForm, AddDisciplineForm
from django.contrib.auth.models import User

from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


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
    if request.method == "POST":
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="discipline_list.pdf"'

        p = canvas.Canvas(response, pagesize=A4)
        width, height = A4
        y = height - 80

        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, y, "Список затверджених дисциплін")
        y -= 40

        p.setFont("Helvetica", 12)
        for d in disciplines:
            p.drawString(80, y, f"Назва: {d.title}")
            y -= 20
            p.drawString(80, y, f"Опис: {d.description}")
            y -= 20
            p.drawString(80, y, f"Викладач: {d.teacher.email}")
            y -= 40

            # якщо місце закінчується — створюємо нову сторінку
            if y < 100:
                p.showPage()
                y = height - 80
                p.setFont("Helvetica", 12)

        p.showPage()
        p.save()
        return response
    return render(request, "index.html", {"disciplines": disciplines})


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


def discipline_requests(request):
    if request.method == "POST":
        action = request.POST.get("action")
        discipline = Discipline.objects.get(id=request.POST.get("discipline_id"))
        if action == "approve":
            discipline.is_approved = True
            discipline.save()
        elif action == "reject":
            discipline.is_approved = False
            discipline.delete()
    disciplines = Discipline.objects.filter(is_approved=False)
    return render(request, "discipline_requests.html", {"disciplines": disciplines})
