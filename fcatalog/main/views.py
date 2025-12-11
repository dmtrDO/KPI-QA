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

from urllib.parse import urlencode
from django.urls import reverse


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
            wordWrap="CJK",
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




@csrf_exempt
def index(request):
    disciplines = Discipline.objects.filter(is_approved=True)
    if request.method == "POST":
        return download(disciplines)
    return render(request, "index.html", {"disciplines": disciplines})




def teacher_discips(request):
    context = {}

    email = request.session.get("email")
    if not email or not Teacher.objects.filter(email=email).exists():
        return redirect("login")
    form = AddDisciplineForm()

    disciplines = Discipline.objects.filter(is_approved=True)
    array = []
    num = 0
    if disciplines is not None:
        buff_arr = []
        for num2 in range(len(disciplines)):
            if disciplines[num2].teacher.email==email:
                num = num + 1
                buff_arr.append(disciplines[num2])
                if num==3 or num2+1==len(disciplines) :
                    num = 0
                    array.append(buff_arr.copy())
                    buff_arr = []
    context['disciplines'] = array

    if request.session.get('type_out') is None:
        request.session['type_out'] = 0

    if request.method == "POST":
        type_page = request.POST.get('next_page')
        id_item = request.POST.get('id')
        type_out = request.POST.get('type_out')
        if type_page is not None and type_page=='new_discipline':
            form = AddDisciplineForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data["title"]
                disciplines = Discipline.objects.filter(title=title)
                for discipline in disciplines:
                    if discipline.is_approved == True:
                        context["email"] = email
                        context["form"] = form
                        context["error"] = "Така дисципліна вже існує"
                        return render(request,"new_teacher_gen.html",context)
                description = form.cleaned_data["description"]
                Discipline.objects.create(
                    title=title,
                    description=description,
                    teacher=Teacher.objects.get(email=email),
                    admin=User.objects.get(id=1),)
        elif type_out is not None:
            if request.session.get('type_out')==0:
                request.session['type_out'] = 1
            else:
                request.session['type_out'] = 0
        elif id_item is not None:
            obj1 = reverse("teacher_descrip")
            obj2 = urlencode({"id":id_item})
            url = f"{obj1}?{obj2}"
            return redirect(url)
        else:
            pass
    
    context["type_out"] = request.session.get('type_out')
    context["email"] = email
    context["form"] = form
    return render(request,"new_teacher_choo.html",context)


def teacher_descrip(request):
    context = {}
    id = request.GET.get('id')
    object = Discipline.objects.get(id=id)
    
    email = request.session.get("email")
    if not email or not Teacher.objects.filter(email=email).exists():
        return redirect("login")
    form = AddDisciplineForm()

    if request.method == "POST":
        type_page = request.POST.get('next_page')
        if type_page is not None and type_page=='new_discipline':
            form = AddDisciplineForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data["title"]
                disciplines = Discipline.objects.filter(title=title)
                for discipline in disciplines:
                    if discipline.is_approved == True:
                        context["email"] = email
                        context["form"] = form
                        context["error"] = "Така дисципліна вже існує"
                        return render(request,"new_teacher_gen.html",context)
                description = form.cleaned_data["description"]
                Discipline.objects.create(
                    title=title,
                    description=description,
                    teacher=Teacher.objects.get(email=email),
                    admin=User.objects.get(id=1),)

    context['discipline'] = object
    context["email"] = email
    context["form"] = form
    return render(request,"new_teacher_descr.html",context)




def login(request):
    context = {}

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
                    return redirect("teacher_discips")
            context["form"] = form
            context["error"] = "Неправильна пошта або пароль"
            return render(request,"new_login.html",context)

    context["form"] = form
    return render(request,"new_login.html",context)


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
