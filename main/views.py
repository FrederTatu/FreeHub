from django.shortcuts import render, get_object_or_404, redirect
from .models import Project
from .forms import ProjectForm, RegisterForm, UserEditForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, "main/home.html")

def catalog(request):
    projects = Project.objects.all()

    return render(request, "main/catalog.html", {
        "projects": projects
    })

def freelancers(request):
    return render(request, "main/freelancers.html")

def profile(request, username):

    profiles = {
        "admin": {
            "name": "Анна Крылова",
            "profession": "UX/UI дизайнер",
            "city": "Москва",
            "about": "Проектирую удобные и эстетичные интерфейсы для веб и мобильных приложений. Люблю продуманные пользовательские сценарии и чистый дизайн.",
            "skills": ["Figma", "UI/UX", "Web-дизайн"],

            "portfolio": [
                {
                    "title": "Дизайн музыкального приложения",
                    "image": "main/images/music_app.png"
                },
                {
                    "title": "Дизайн фитнес-приложения",
                    "image": "main/images/fitness_app.png"
                },
                {
                    "title": "Брендинг жилого комплекса",
                    "image": "main/images/home_app.png"
                },
                {
                    "title": "Платформа онлайн-обучения",
                    "image": "main/images/study_app.png"
                },
            ],
        },


        "ilya2": {
            "name": "Илья Морозов",
            "profession": "Веб-разработчик",
            "city": "Москва",
            "about": "Создаю современные, быстрые и удобные веб-приложения. Работаю с интерфейсами и серверной частью сайтов.",
            "skills": ["Python", "Django", "HTML/CSS"],

            "portfolio": [
                {
                    "title": "Сайт туристического сервиса",
                    "image": "main/images/world_app.png"
                },
                {
                    "title": "Платформа онлайн-обучения",
                    "image": "main/images/study_app.png"
                },
                {
                    "title": "Мобильный банковский сервис",
                    "image": "main/images/bank_app.png"
                },
                {
                    "title": "Дизайн музыкального приложения",
                    "image": "main/images/music_app.png"
                },
            ],
        },


        "maria": {
            "name": "Мария Лебедева",
            "profession": "Фотограф",
            "city": "Москва",
            "about": "Создаю атмосферные фотографии и визуальные истории. Работаю с предметной, городской и коммерческой съёмкой.",
            "skills": ["Фотография", "Lightroom", "Ретушь"],

            "portfolio": [
                {
                    "title": "Портретная съёмка",
                    "image": "main/images/maria_portrait.png"
                },
                {
                    "title": "Предметная съёмка",
                    "image": "main/images/maria_product.png"
                },
                {
                    "title": "Архитектурная съёмка",
                    "image": "main/images/maria_architecture.png"
                },
                {
                    "title": "Творческая съёмка",
                    "image": "main/images/maria_lifestyle.png"
                },
            ],
        },
    }

    profile_data = profiles.get(username)

    if profile_data is None:
        return redirect("freelancers")

    return render(request, "main/profile.html", {
        "profile_data": profile_data,
        "username": username,
    })

def project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tags = project.tags.split(",")

    return render(request, "main/project.html", {
        "project": project,
        "tags": tags
    })

@login_required
def add_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.save()

            return redirect("catalog")

    else:
        form = ProjectForm()

    return render(request, "main/add_project.html", {
        "form": form
    })

@login_required
def account(request):
    projects = Project.objects.filter(author=request.user)

    return render(request, "main/account.html", {
        "projects": projects
    })

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

        else:
            print(form.errors)

    else:
        form = RegisterForm()

    return render(request, "main/register.html", {
        "form": form
    })

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("account")

    return render(request, "main/login.html")


def user_logout(request):
    logout(request)
    return redirect("home")

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(
        Project,
        id=project_id,
        author=request.user
    )

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            form.save()
            return redirect("account")

    else:
        form = ProjectForm(instance=project)

    return render(request, "main/add_project.html", {
        "form": form,
        "edit_mode": True,
        "page_title": "Редактировать проект",
        "submit_text": "Сохранить"
    })


@login_required
def delete_project(request, project_id):
    project = get_object_or_404(
        Project,
        id=project_id,
        author=request.user
    )

    if request.method == "POST":
        project.delete()

    return redirect("account")


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect("account")

    else:
        form = UserEditForm(instance=request.user)

    return render(request, "main/edit_profile.html", {
        "form": form
    })