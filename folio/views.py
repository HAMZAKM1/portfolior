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
from django.shortcuts import redirect
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Certificate
import json
import csv
from .models import Skill
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Certificate, Career
from .forms import BlogForm
from django.shortcuts import render, redirect
from .forms import SkillForm
from .forms import CertificateForm
from .models import Certificate
from .forms import CourseForm 
from .models import (
    Profile, Skill, Project, ProjectGallery, Category,
    BlogPost, Testimonial, Resume, Visitor
)
from .forms import (
    ProfileForm, ContactForm, SkillForm,
    ProjectForm, ProjectGalleryForm
)
from django.shortcuts import render

SKILLS = [
    {
        "name": "Software Engineering",
        "slug": "software-engineering",
        "description": "Design, build and deploy professional software systems.",
        "topics": ["Python","Django","APIs","Databases","Cloud"],
        "projects": ["E-Commerce Platform","Chat App","ERP System"],
        "certificates": ["Python Developer","Django Master"],
        "careers": "Software Engineer, Backend Developer",
        "level": 90
    },
    {
        "name": "Web Development",
        "slug": "web-development",
        "description": "Create fast and responsive websites.",
        "topics": ["HTML","CSS","JavaScript","Bootstrap","React"],
        "projects": ["Portfolio","Virtual Art Gallery"],
        "certificates": ["Frontend Developer"],
        "careers": "Web Developer, UI Engineer",
        "level": 85
    },
    {
        "name": "Accounting",
        "slug": "accounting",
        "description": "Manage finances, taxes and bookkeeping.",
        "topics": ["Tally","Excel","GST","Payroll"],
        "projects": ["Company Reports"],
        "certificates": ["Professional Accountant"],
        "careers": "Accountant, Finance Manager",
        "level": 75
    },
    {
        "name": "Mobile Mechanic",
        "slug": "mobile-mechanic",
        "description": "Repair and maintain smartphones.",
        "topics": ["Screen Repair","Flashing","Chipset Repair"],
        "projects": ["500+ Devices Repaired"],
        "certificates": ["Mobile Technician"],
        "careers": "Mobile Repair Engineer",
        "level": 85
    },
     {
        "name": "Graphic Design",
        "slug": "graphic-design",
        "description": "Create stunning visual content and graphics.",
        "topics": ["Photoshop", "Illustrator", "Figma"],
        "projects": ["Portfolio Design", "Branding Projects"],
        "certificates": ["Graphic Designer Certificate"],
        "careers": "Graphic Designer, UI/UX Designer",
        "level": 80
    }
]


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

<<<<<<< Updated upstream
def user_settings(request):
    return render(request, 'folio/user_settings.html')
def dashboard(request):
    return render(request, "folio/dashboard.html")
def resume_view(request):
    return render(request, "folio/resume.html")
def newsletter_subscribe(request):
    if request.method == "POST":
        return HttpResponse("Subscribed successfully")
    return HttpResponse("Newsletter page")
def update_privacy(request):
    if request.method == "POST":
        # later you can save privacy settings here
        return HttpResponse("Privacy settings updated successfully")
    return HttpResponse("Privacy settings page")
def enable_2fa(request):
    return HttpResponse("2FA enabled")

def disable_2fa(request):
    return HttpResponse("2FA disabled")
def update_notifications(request):
    messages.success(request, "Notification settings updated")
    return redirect("/")
def delete_account(request):
    messages.success(request, "Account deleted (demo)")
    return redirect("/")
def projects(request):
    projects = Project.objects.all()
    return render(request, "folio/projects.html", {
        "projects": projects
    })
    
=======
def dashboard(request):
    return render(request, "folio/dashboard.html")
def resume_view(request):
    resume = Resume.objects.last()
    return render(request, "folio/resume.html", {"resume": resume})
def newsletter_subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email")
        # You can later save email to a model
        messages.success(request, "Subscribed successfully!")
        return redirect("home")
    return redirect("home")
@login_required
def logout_other_sessions(request):
    """
    Logs out all other sessions except the current one
    """
    current_session_key = request.session.session_key

    sessions = Session.objects.filter(expire_date__gte=timezone.now())

    for session in sessions:
        data = session.get_decoded()
        if data.get('_auth_user_id') == str(request.user.id):
            if session.session_key != current_session_key:
                session.delete()

    messages.success(request, "Logged out from other sessions successfully.")
    return redirect("settings")
def export_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Sample', 'Data'])
    writer.writerow(['Hello', 'World'])

    return response
def projects(request):
    project_list = Project.objects.all()
    return render(request, 'folio/projects.html', {
        'projects': project_list
    })

def latest_projects(request):
    projects = Project.objects.order_by('-id')[:6]
    return render(request, 'folio/latest_projects.html', {
        'projects': projects
    })
def skills(request):
    skills = Skill.objects.all()
    return render(request, "folio/skills.html", {"skills": skills})

def featured_projects(request):
    projects = Project.objects.filter(is_featured=True)
    return render(request, "folio/featured_projects.html", {
        "projects": projects
    })
def contact(request):
    return render(request, "folio/contact.html")
def user_settings(request):
    # Replace 'folio/user_settings.html' with your actual template path
    return render(request, "folio/user_settings.html")
def update_privacy(request):
    # Replace with your actual template
    return render(request, "folio/update_privacy.html")
def enable_2fa(request):
    return render(request, "folio/enable_2fa.html")
def disable_2fa(request):
    return render(request, "folio/disable_2fa.html")
def update_notifications(request):
    return render(request, "folio/update_notifications.html")
def delete_account(request):
    return render(request, "folio/delete_account.html")

def about(request):
    return render(request, "folio/about.html")
def experience(request):
    return render(request, "folio/experience.html")
def education(request):
    return render(request, "folio/education.html")
def testimonials(request):
    return render(request, "folio/testimonials.html")

def export_data(request):
    # Temporary placeholder
    return HttpResponse("Export Data page placeholder.")
def featured_projects(request):
    return render(request, 'folio/featured_projects.html')
def latest_projects(request):
    return render(request, 'folio/latest_projects.html')
def settings_view(request):
    return render(request, 'folio/settings.html')
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'folio/register.html', {'form': form})


def contact(request):
    return render(request, 'folio/contact.html')

@login_required
def skills_page(request):
    skills = []
    categories = set()  # to collect unique categories

    for skill in SKILLS:
        # Calculate stars (1 star per 20% proficiency)
        stars = round(skill.get("level", 0) / 20)
        skill_copy = skill.copy()
        skill_copy["stars"] = stars
        skills.append(skill_copy)

        categories.add(skill.get("type", "Other"))  # collect unique types

    categories = sorted(categories)  # optional: sort alphabetically

    return render(request, "folio/skills.html", {
        "skills": skills,
        "categories": categories,
    })

def skill_detail(request, slug):
    """Display a single skill based on slug"""
    skill = next((s for s in SKILLS if s["slug"] == slug), None)
    if not skill:
        return HttpResponse("Skill not found", status=404)
    return render(request, "folio/skill_detail.html", {"skill": skill})


def skill_detail(request, slug):
    """Display a single skill based on slug"""
    skill = next((s for s in SKILLS if s["slug"] == slug), None)
    if not skill:
        return HttpResponse("Skill not found", status=404)
    return render(request, "folio/skill_detail.html", {"skill": skill})

def education(request):
    certificates = Certificate.objects.all().order_by("-year")
    return render(request, "folio/education.html", {
        "certificates": certificates
    })  
    

def software_engineering(request):
    return render(request, "folio/software_engineering.html")

def web_development(request):
    return render(request, "folio/web_development.html")

def ai_ml(request):
    return render(request, "folio/ai_ml.html")

def cloud_computing(request):
    return render(request, "folio/cloud_computing.html")

def accounting(request):
    return render(request, "folio/accounting.html")

def financial_management(request):
    return render(request, "folio/financial_management.html")

def business_admin(request):
    return render(request, "folio/business_admin.html")

def mobile_mechanic(request):
    return render(request, "folio/mobile_mechanic.html")

def auto_repair(request):
    return render(request, "folio/auto_repair.html")

def electrical_technician(request):
    return render(request, "folio/electrical_technician.html")

def hvac(request):
    return render(request, "folio/hvac.html")

def graphic_design(request):
    return render(request, "folio/graphic_design.html")

def video_editing(request):
    return render(request, "folio/video_editing.html")

def photography(request):
    return render(request, "folio/photography.html")
def financial_management(request):
    return render(request, "folio/financial_management.html")
def business_admin(request):
    return render(request, "folio/business_admin.html")

def auto_repair(request):
    return render(request, "folio/auto_repair.html")
def electrical_technician(request):
    return render(request, "folio/electrical_technician.html")
def hvac_technician(request):
    return render(request, "folio/hvac_technician.html")


def resume_software(request):
    return render(request, "folio/resume_software.html")

def resume_hardware(request):
    return render(request, "folio/resume_hardware.html")

def resume_accounting(request):
    return render(request, "folio/resume_accounting.html")

def resume_finance(request):
    return render(request, "folio/resume_finance.html")

def resume_mobile(request):
    return render(request, "folio/resume_mobile.html")

def resume_cooker(request):
    return render(request, "folio/resume_cooker.html")

def resume_auto(request):
    return render(request, "folio/resume_auto.html")

def resume_graphic(request):
    return render(request, "folio/resume_graphic.html")

def resume_video(request):
    return render(request, "folio/resume_video.html")

def resume_photography(request):
    return render(request, "folio/resume_photography.html")

@login_required
def logout_other_sessions(request):
    current_session_key = request.session.session_key

    # Delete all sessions for this user except the current one
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    for session in sessions:
        data = session.get_decoded()
        if data.get("_auth_user_id") == str(request.user.id):
            if session.session_key != current_session_key:
                session.delete()

    return redirect("settings")
def contact(request):
    return render(request, 'folio/contact.html', {'title': 'Contact Me'})
# views.py

def project_create(request):
    return render(request, "folio/project_form.html")
# folio/views.py
@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('dashboard')
    else:
        form = BlogForm()

    return render(request, 'folio/blog_create.html', {'form': form})
# views.py

def skill_create(request):
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = SkillForm()
    return render(request, 'folio/skill_form.html', {'form': form})

def education(request):
    return render(request, 'folio/education.html')

def certificates(request):
    return render(request, 'folio/certificate.html')

def courses(request):
    return render(request, 'folio/courses.html')

def python_section(request):
    return render(request, 'folio/python.html')

def frontend_section(request):
    return render(request, 'folio/frontend.html')

def projects(request):
    return render(request, 'folio/projects.html')

def career(request):
    return render(request, 'folio/career.html')

def dashboard(request):
    return render(request, 'folio/dashboard.html')
# List all certificates for the logged-in user
@login_required(login_url='login')
def certificates(request):
    certs = Certificate.objects.filter(user=request.user).order_by('-year')
    return render(request, 'folio/certificate.html', {'certificates': certs})

# Add a new certificate
@login_required(login_url='login')
def certificate_create(request):
    if request.method == 'POST':
        form = CertificateForm(request.POST, request.FILES)
        if form.is_valid():
            certificate = form.save(commit=False)
            certificate.user = request.user  # assign logged-in user
            certificate.save()
            return redirect('certificates')  # ✅ redirect to the certificate list
    else:
        form = CertificateForm()

    return render(request, 'folio/certificate_form.html', {'form': form})


def courses_view(request):
    courses = Course.objects.filter(id__isnull=False)
    return render(request, 'folio/courses.html', {'courses': courses})

def career_view(request):
    career = {
        "skills": ["Python", "Django", "SQL"],
        "goals": ["Become Backend Dev", "Deploy Projects"],
        "certificates": [{"title": "Python Cert"}, {"title": "Django Cert"}]
    }
    return render(request, 'folio/career.html', {'career': career})

# Detail page for a single course
def course_detail_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'folio/course_detail.html', {'course': course})


@login_required
def course_create(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user  # automatically assign logged-in user
            course.save()
            return redirect('courses')  # or any page you want to redirect to
    else:
        form = CourseForm()
    return render(request, 'folio/course_create.html', {'form': form})
def all_products(request):
    return render(request, "folio/all_products.html")
def category_list(request):
    return render(request, "folio/category_list.html")
def wishlist(request):
    return render(request, "folio/wishlist.html")
def orders(request):
    return render(request, "folio/orders.html")
def portfolio(request):
    return render(request, "folio/portfolio.html")
def messages_view(request):
    return render(request, "folio/messages.html")
def help_view(request):
    return render(request, "folio/help.html")
def skill_detail(request, tech):
    return render(request, "folio/skill_detail.html", {"tech": tech})
def python_view(request):
    return render(request, "folio/python_view.html")
def java_view(request):
    return render(request, "folio/java_view.html")
def react_view(request):
    return render(request, "folio/react_view.html")
def django_view(request):
    return render(request, "folio/django_view.html")
def aws_view(request):
    return render(request, "folio/aws.html")
def ml_view(request):
    return render(request, "folio/ml.html")
def flutter_view(request):
    return render(request, "folio/flutter.html")

def c_view(request):
    return render(request, "folio/c.html")

