from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.http import HttpResponse
import json
import csv
from .models import (
    Profile, Skill, Project, ProjectGallery, Category,
    BlogPost, Testimonial, Resume, Visitor
)
from .forms import (
    ProfileForm, ContactForm, SkillForm,
    ProjectForm, ProjectGalleryForm
)


# ============================
# HOME / INDEX / VISITOR LOG
# ============================

def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip

def log_visitor(request):
    ip = get_client_ip(request)
    Visitor.objects.create(ip_address=ip, visited_at=timezone.now())

def home(request):
    projects = Project.objects.all()
    skills = Skill.objects.all()
    return render(request, "folio/home.html", {"projects": projects, "skills": skills})

def index(request):
    log_visitor(request)
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    projects = Project.objects.all()
    testimonials = Testimonial.objects.all()
    resume = Resume.objects.last()
    return render(request, "folio/index.html", {
        "profile": profile,
        "skills": skills,
        "projects": projects,
        "testimonials": testimonials,
        "resume": resume,
    })


# ============================
# PROJECT VIEWS
# ============================

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, "folio/project_detail.html", {"project": project})

@login_required
def project_create(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        gallery_form = ProjectGalleryForm(request.POST, request.FILES)

        if project_form.is_valid() and gallery_form.is_valid():
            project = project_form.save()

            images = request.FILES.getlist('images')
            for img in images:
                ProjectGallery.objects.create(project=project, image=img)

            messages.success(request, "Project created successfully!")
            return redirect('project_list')
    else:
        project_form = ProjectForm()
        gallery_form = ProjectGalleryForm()

    return render(request, 'folio/project_form.html', {
        'form': project_form,
        'gallery_form': gallery_form,
        'title': 'Add Project'
    })

@login_required
def project_list(request, category_slug=None):
    projects = Project.objects.all()
    if category_slug:
        projects = projects.filter(category__slug=category_slug)

    for project in projects:
        project.tech_list = [tech.strip() for tech in (project.technologies or "").split(',')]

    categories = Category.objects.all()
    
    return render(request, 'folio/projects.html', {
        'projects': projects,
        'categories': categories,
    })

@login_required
def add_project(request):
    if request.method == "POST":
        project_form = ProjectForm(request.POST)
        gallery_form = ProjectGalleryForm(request.POST, request.FILES)

        if project_form.is_valid():
            project = project_form.save()

            images = request.FILES.getlist("image")
            for img in images:
                ProjectGallery.objects.create(project=project, image=img)

            messages.success(request, "Project added successfully!")
            return redirect("project_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        project_form = ProjectForm()
        gallery_form = ProjectGalleryForm()

    return render(request, "folio/project_form.html", {
        "form": project_form,
        "gallery_form": gallery_form,
        "title": "Add Project",
    })

@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        gallery_form = ProjectGalleryForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            images = request.FILES.getlist("image")
            for img in images:
                ProjectGallery.objects.create(project=project, image=img)

            messages.success(request, "Project updated successfully!")
            return redirect("project_list")
    else:
        form = ProjectForm(instance=project)
        gallery_form = ProjectGalleryForm()

    return render(request, "folio/project_form.html", {
        "form": form,
        "gallery_form": gallery_form,
        "title": "Edit Project",
    })

@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project deleted successfully!")
        return redirect("project_list")
    return render(request, "folio/project_confirm_delete.html", {"project": project})


# ============================
# SKILL VIEWS
# ============================

@login_required
def skills_page(request):
    skills = Skill.objects.all().order_by('-id')
    return render(request, "folio/skills.html", {"skills": skills})

@login_required
def add_skill(request):
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill added successfully!")
            return redirect("skills")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SkillForm()
    return render(request, "folio/add_skill.html", {"form": form})

@login_required
def update_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill updated successfully!")
            return redirect("skills")
    else:
        form = SkillForm(instance=skill)
    return render(request, "folio/update_skill.html", {"form": form})

@login_required
def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    skill.delete()
    messages.warning(request, "Skill deleted!")
    return redirect("skills")


# ============================
# PROFILE VIEWS
# ============================

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'folio/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'folio/edit_profile.html', {'form': form})


# ============================
# AUTHENTICATION
# ============================

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("index")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, "folio/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect("index")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "folio/login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("index")


# ============================
# SETTINGS / PASSWORD / PRIVACY
# ============================

@login_required
def change_password(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")

        if not request.user.check_password(old_password):
            messages.error(request, "Current password is incorrect")
            return redirect("user_settings")

        if new_password1 != new_password2:
            messages.error(request, "New passwords do not match")
            return redirect("user_settings")

        request.user.set_password(new_password1)
        request.user.save()
        update_session_auth_hash(request, request.user)

        messages.success(request, "Password changed successfully!")
    return redirect("user_settings")


@login_required
def settings_view(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Settings updated successfully!")
            return redirect('settings')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=profile)

    sessions = []
    for s in Session.objects.filter(expire_date__gte=timezone.now()):
        data = s.get_decoded()
        if data.get('_auth_user_id') == str(request.user.id):
            sessions.append({
                'device': 'Unknown',
                'ip': data.get('ip', 'N/A'),
                'last_active': s.expire_date,
            })

    return render(request, 'folio/settings.html', {'form': form, 'profile': profile, 'sessions': sessions})


# ============================
# CONTACT / SUPPORT / BLOG
# ============================

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.sent_at = timezone.now()
            contact.save()

            send_mail(
                subject=f"New Contact Message from {contact.name}",
                message=f"{contact.message}\n\nReply to: {contact.email}",
                from_email="your-email@example.com",
                recipient_list=["your-email@example.com"],
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully!")
            return redirect("contact_success")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()
    return render(request, "folio/contact_page.html", {"form": form})

def contact_success(request):
    return render(request, "folio/contact_success.html")

def support_page(request):
    return render(request, "folio/support.html")

def faq_page(request):
    return render(request, "folio/faq.html")

def blog_list(request):
    posts = BlogPost.objects.all()
    return render(request, "folio/blog_list.html", {"posts": posts})

def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, "folio/blog_detail.html", {"post": post})

def user_settings(request):
    return render(request, 'folio/user_settings.html')