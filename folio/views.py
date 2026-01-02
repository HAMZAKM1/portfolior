
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .forms import ProfileForm
from .forms import ContactForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Skill
from .forms import SkillForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.contrib.auth import update_session_auth_hash
import json
from .models import Project, Category
from django.http import HttpResponse
import csv
from .models import Project
from .forms import ProjectForm, ProjectGalleryForm
from .models import Project, ProjectGallery
from .forms import ProjectForm
from django.http import HttpResponse
from .models import Project
from .models import Profile, Skill, Project   # make sure Project exists
from .forms import ProjectForm, ProjectGalleryForm
from .models import Project
from django.contrib import messages
from .forms import ProjectForm, ProjectGalleryForm
from .models import Project, ProjectGallery

from .models import (
    Profile, Skill, Project, Category, BlogPost, Testimonial,
    Resume, Visitor
)




def home(request):
    projects = Project.objects.all()
    skills = Skill.objects.all()
    return render(request, "folio/home.html", {"projects": projects, "skills": skills})


# --- Visitor logging ---
def log_visitor(request):
    ip = get_client_ip(request)
    Visitor.objects.create(ip_address=ip, visited_at=timezone.now())

def get_client_ip(request):
    """Retrieve client IP address"""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


# --- Homepage ---
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


# --- Resume ---
def resume_view(request):
    resume_file = Resume.objects.last()
    return render(request, "folio/resume.html", {"resume": resume_file})


# --- Project views ---



def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, "folio/project_detail.html", {"project": project})
# views.py



def project_create(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        gallery_form = ProjectGalleryForm(request.POST, request.FILES)

        if project_form.is_valid() and gallery_form.is_valid():
            project = project_form.save()

            # Handle multiple images
            images = request.FILES.getlist('images')
            for img in images:
                ProjectGallery.objects.create(project=project, image=img)

            return redirect('project_list')
    else:
        project_form = ProjectForm()
        gallery_form = ProjectGalleryForm()

    return render(request, 'folio/project_form.html', {
        'form': project_form,
        'gallery_form': gallery_form,
        'title': 'Add Project'
    })


# --- Blog views ---
def blog_list(request):
    posts = BlogPost.objects.all()
    return render(request, "folio/blog_list.html", {"posts": posts})


def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, "folio/blog_detail.html", {"post": post})


# --- Contact ---
def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.sent_at = timezone.now()
            contact.save()

            # Send email
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


# --- Newsletter subscription ---
def newsletter_subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            # Optional: save to DB
            # Newsletter.objects.create(email=email)
            messages.success(request, f"Subscribed {email} successfully!")
        else:
            messages.error(request, "Please enter a valid email.")
    return redirect('index')


# --- Authentication ---
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


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("index")
def dashboard(request):
    profile = Profile.objects.first()
    projects = Project.objects.all()
    skills = Skill.objects.all()
    blogs = BlogPost.objects.all()
    visitors = Visitor.objects.all()

    return render(request, "folio/dashboard.html", {
        "profile": profile,
        "projects": projects,
        "skills": skills,
        "blogs": blogs,
        "visitors": visitors,
    })

def all_products(request):
    return render(request, 'all_products.html')
def category_list(request):
    return render(request, 'category_list.html')
def wishlist(request):
    return render(request, 'wishlist.html')
def orders(request):
    return render(request, 'orders.html')
def portfolio(request):
    return render(request, 'folio/portfolio.html')
def blog(request):
    return render(request, 'folio/blog.html')
@login_required
def messages_view(request):
    return render(request, 'folio/messages.html')  # create this template
def help_view(request):
    return render(request, 'folio/help.html')  # create help.html in templates/folio/
def projects(request):
    all_projects = Project.objects.all().order_by('-created_at')
    featured_projects = Project.objects.filter(is_featured=True)
    latest_projects = Project.objects.order_by('-created_at')[:4]

    return render(request, 'folio/projects.html', {
        'projects': all_projects,
        'featured_projects': featured_projects,
        'latest_projects': latest_projects,
    })

def project_list(request, category_slug=None):
    projects = Project.objects.all()
    if category_slug:
        projects = projects.filter(category__slug=category_slug)

    # Convert comma-separated technologies into list for template
    for project in projects:
        project.tech_list = [tech.strip() for tech in (project.technologies or "").split(',')]

    # Pass categories for filter buttons in template
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

            # Handle multiple images
            images = request.FILES.getlist("image")  # matches 'image' field in ProjectGalleryForm
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
def portfolio(request):
    projects = Project.objects.all()
    return render(request, "folio/portfolio.html", {"projects": projects})

@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)

    # SAFE FIX → avoid "no file associated with it" error
    profile_image_url = profile.profile_image.url if profile.profile_image else None

    # Real project + skill queries
    projects = Project.objects.filter(user=request.user)
    skills = Skill.objects.filter(user=request.user)

    # Dashboard subsets
    recent_projects = projects[:3]
    top_skills = skills.order_by('-level')[:5]
    recent_skills = skills[:3]

    # Activity list (replace with real Activity model later)
    activity = [
        "Updated profile",
        "Added new skill",
        "Uploaded new project",
    ]

    # Visitors list (example only)
    visitor_list = [
        {"name": "Hassan", "time": "2 hours ago"},
        {"name": "Ameer", "time": "Yesterday"},
        {"name": "Ali", "time": "3 days ago"},
    ]

    # Contact messages (example only)
    contact_list = [
        {"name": "Client 1", "message": "Need a project", "time": "1 day ago"},
        {"name": "Client 2", "message": "Contact me", "time": "3 days ago"},
    ]

    context = {
        "profile": profile,
        "profile_image_url": profile_image_url,

        "projects": projects,
        "skills": skills,

        "recent_projects": recent_projects,
        "top_skills": top_skills,
        "recent_skills": recent_skills,

        "activity": activity,
        "visitor_list": visitor_list,
        "contact_list": contact_list,
    }

    return render(request, "folio/profile.html", context)




@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")  # Redirect to profile page
    else:
        form = ProfileForm(instance=profile)

    return render(request, "folio/edit_profile.html", {"form": form})

def user_settings(request):
    return render(request, "folio/settings.html")

# folio/views.py



# -------------------------------
# SKILL VIEWS
# -------------------------------

@login_required
def skills_page(request):
    skills = Skill.objects.all().order_by('-id')
    return render(request, "folio/skills.html", {"skills": skills})


@login_required
def add_skill(request):
    if request.method == "POST":
        name = request.POST.get("name")
        level = request.POST.get("level")

        if not name or not level:
            messages.error(request, "All fields are required!")
            return redirect("skills")

        Skill.objects.create(name=name, level=level)
        messages.success(request, "Skill added successfully!")
        return redirect("skills")

    return redirect("skills")


@login_required
def update_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)

    if request.method == "POST":
        skill.name = request.POST.get("name")
        skill.level = request.POST.get("level")
        skill.save()
        messages.success(request, "Skill updated Successfully!")
        return redirect("skills")

    return redirect("skills")


@login_required
def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    skill.delete()
    messages.warning(request, "Skill deleted!")
    return redirect("skills")



def featured_projects(request):
    featured_projects = Project.objects.filter(is_featured=True)
    categories = Category.objects.all()

    return render(request, 'folio/featured_projects.html', {
        'featured_projects': featured_projects,
        'categories': categories,
    })

def latest_projects(request):
    latest_projects = Project.objects.order_by('-created_at')[:6]
    return render(request, 'folio/latest_projects.html', {
        'latest_projects': latest_projects,
    })

def about(request):
    return render(request, "folio/about.html")
def experience(request):
    return render(request, "folio/experience.html")
def education(request):
    return render(request, "folio/education.html")
def testimonials(request):
    return render(request, "folio/testimonials.html")
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'folio/profile.html', {'profile': profile})

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


@login_required
def change_password(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")

        # Validate
        if not request.user.check_password(old_password):
            messages.error(request, "Current password is incorrect")
            return redirect("user_settings")

        if new_password1 != new_password2:
            messages.error(request, "New passwords do not match")
            return redirect("user_settings")

        # Save new password
        request.user.set_password(new_password1)
        request.user.save()

        # Keep user logged in
        update_session_auth_hash(request, request.user)

        messages.success(request, "Password changed successfully!")
        return redirect("user_settings")

    return redirect("user_settings")
@login_required
def update_notifications(request):
    profile = request.user.profile
    profile.email_updates = "email_updates" in request.POST
    profile.product_emails = "product_emails" in request.POST
    profile.save()
    messages.success(request, "Notification preferences updated")
    return redirect("user_settings")
@login_required
def delete_account(request):
    user = request.user
    user.delete()
    return redirect("home")   # Or a goodbye page

@login_required
def enable_2fa(request):
    profile = request.user.profile
    profile.two_factor_enabled = True
    profile.save()
    messages.success(request, "Two-factor authentication enabled!")
    return redirect('settings')

@login_required
def disable_2fa(request):
    profile = request.user.profile
    profile.two_factor_enabled = False
    profile.save()
    messages.warning(request, "Two-factor authentication disabled.")
    return redirect('settings')

@login_required
def update_privacy(request):
    profile = request.user.profile

    if request.method == "POST":
        profile.show_email = 'show_email' in request.POST
        profile.show_profile = 'show_profile' in request.POST
        profile.allow_messages = 'allow_messages' in request.POST

        profile.save()
        messages.success(request, "Privacy settings updated!")
    
    return redirect("settings")
@login_required
def logout_other_sessions(request):
    if request.method == "POST":
        current_session = request.session.session_key

        # Delete all sessions except the current one
        all_sessions = Session.objects.filter(expire_date__gt=timezone.now())

        for session in all_sessions:
            data = session.get_decoded()
            if data.get('_auth_user_id') == str(request.user.id) and session.session_key != current_session:
                session.delete()

        messages.success(request, "Logged out from all other devices successfully!")

    return redirect("settings")

@login_required
def logout_other_sessions(request):
    current_session_key = request.session.session_key
    user_sessions = Session.objects.filter(expire_date__gt=timezone.now())

    for session in user_sessions:
        data = session.get_decoded()
        if data.get('_auth_user_id') == str(request.user.id):
            if session.session_key != current_session_key:
                session.delete()

    return redirect('settings')
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
    
    # Fetch active sessions
    sessions = []
    all_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    for s in all_sessions:
        data = s.get_decoded()
        if data.get('_auth_user_id') == str(request.user.id):
            sessions.append({
                'device': 'Unknown',
                'ip': data.get('ip', 'N/A'),
                'last_active': s.expire_date,
            })

    context = {
        'form': form,
        'profile': profile,
        'sessions': sessions,
    }
    return render(request, 'folio/settings.html', context)

@login_required
def export_data(request):
    user = request.user
    data = {
        "username": user.username,
        "email": user.email,
        "date_joined": str(user.date_joined),
        "first_name": user.first_name,
        "last_name": user.last_name,
    }

    response = HttpResponse(
        json.dumps(data, indent=4),
        content_type="application/json"
    )
    response['Content-Disposition'] = 'attachment; filename="user_data.json"'
    return response
def support_page(request):
    return render(request, "folio/support.html")  # Make sure this template exists
def faq_page(request):
    return render(request, "folio/faq.html")  # make sure you have this template


def export_data(request):
    # Example CSV export
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data_export.csv"'

    writer = csv.writer(response)
    writer.writerow(["Name", "Email"])
    writer.writerow([request.user.username, request.user.email])

    return response
@login_required
def logout_other_sessions(request):
    request.user.session_set.exclude(session_key=request.session.session_key).delete()
    messages.success(request, "Other sessions logged out.")
    return redirect("settings")
def skill_detail(request, tech):
    return render(request, f"skills/{tech}.html")
def python_view(request):
    return render(request, "skills/python.html")

def java_view(request):
    return render(request, "skills/java.html")

def react_view(request):
    return render(request, "skills/react.html")

def django_view(request):
    return render(request, "skills/django.html")

def aws_view(request):
    return render(request, "skills/aws.html")

def ml_view(request):
    return render(request, "skills/ml.html")

def flutter_view(request):
    return render(request, "skills/flutter.html")

def c_view(request):
    return render(request, "skills/c.html")
from django.shortcuts import render

def contact(request):
    return render(request, "folio/contact.html")


def skills(request):
    skills = Skill.objects.all()
    return render(request, 'folio/skills.html', {'skills': skills})


def add_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('skills')
    else:
        form = SkillForm()
    return render(request, 'folio/add_skill.html', {'form': form})


def update_skill(request, id):
    skill = get_object_or_404(Skill, id=id)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('skills')
    else:
        form = SkillForm(instance=skill)
    return render(request, 'folio/update_skill.html', {'form': form})


def delete_skill(request, id):
    skill = get_object_or_404(Skill, id=id)
    skill.delete()
    return redirect('skills')
