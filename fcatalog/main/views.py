from django.shortcuts import redirect, render
from .models import Teacher, Discipline
from .forms import TeacherLoginForm, AddDisciplineForm
from django.contrib.auth.models import User

from django.http import HttpResponse, FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
import io
from reportlab.platypus import (
    SimpleDocTemplate,
    LongTable,
    TableStyle,
    Paragraph,
    PageBreak,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.ttfonts import TTFont

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


def download(disciplines):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="Wrapped",
            parent=styles["Normal"],
            wordWrap="CJK",  # або "RTL" або "LTR" — але CJK найкраще переносить довгі рядки
        )
    )

    styles["Normal"].fontName = "DejaVuSerif"
    styles["Heading2"].fontName = "DejaVuSerif"
    pdfmetrics.registerFont(TTFont("DejaVuSerif", "DejaVuSerif.ttf", "UTF-8"))

    # Заголовок
    elements.append(
        Paragraph("<b>Таблиця 1. Викладач - Назва дисципліни</b>", styles["Heading2"])
    )
    data1 = [["Викладач", "Назва дисципліни"]]
    for d in disciplines:
        link = f'<a href="#{d.id}">{d.title}</a>'
        data1.append(
            [
                Paragraph(d.teacher.email, styles["Wrapped"]),
                Paragraph(link, styles["Normal"]),
            ]
        )

    table1 = LongTable(data1, repeatRows=1, colWidths=[150, 350])
    table1.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "DejaVuSerif"),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    elements.append(table1)
    elements.append(PageBreak())

    # Друга таблиця
    elements.append(
        Paragraph(
            "<b>Таблиця 2. Викладач - Назва - Опис дисципліни</b>", styles["Heading2"]
        )
    )
    data2 = [["№", "Викладач", "Назва", "Опис дисципліни"]]
    counter = 0
    for d in disciplines:
        counter += 1
        title_with_anchor = f'<a name="{d.id}"/>{d.title}'
        description = d.description
        chunk_size = 1000
        for i in range(0, len(description), chunk_size):
            if len(description) < chunk_size:
                chunk = description
            else:
                chunk = description[i : i + chunk_size]
            if i > 0:
                title_with_anchor = f"{d.title}"
            data2.append(
                [
                    Paragraph(str(counter), styles["Normal"]),
                    Paragraph(d.teacher.email, styles["Wrapped"]),
                    Paragraph(title_with_anchor, styles["Normal"]),
                    Paragraph(chunk, styles["Normal"]),
                ]
            )

    table2 = LongTable(data2, repeatRows=1, colWidths=[40, 80, 120, 260])
    table2.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "DejaVuSerif"),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    elements.append(table2)

    # Створення PDF
    doc.build(elements)
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename="disciplines-catalog.pdf")


def index(request):
    disciplines = Discipline.objects.filter(is_approved=True)
    if request.method == "POST":
        return download(disciplines)
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
