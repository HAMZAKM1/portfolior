from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    email_updates = models.BooleanField(default=True)
    product_emails = models.BooleanField(default=True)
    show_email = models.BooleanField(default=True)
    show_profile = models.BooleanField(default=True)
    allow_messages = models.BooleanField(default=True)
    two_factor_enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend'),
        ('Database', 'Database'),
        ('Tools', 'Tools'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    level = models.PositiveIntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ============================
# PROJECTS
# ============================
class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=300, blank=True, help_text="Comma separated tech stack")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# ============================
# PROJECT GALLERY (IMAGES)
# ============================
class ProjectGallery(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='project_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.project.title}"


# ============================
# BLOG POSTS
# ============================
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# ============================
# TESTIMONIALS
# ============================
class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.position}"


# ============================
# RESUME
# ============================
class Resume(models.Model):
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume uploaded at {self.uploaded_at}"


# ============================
# VISITORS
# ============================
class Visitor(models.Model):
    ip_address = models.GenericIPAddressField()
    visited_at = models.DateTimeField()

    def __str__(self):
        return f"{self.ip_address} at {self.visited_at}"
class TechStack(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class Certificate(models.Model):
    CERT_TYPE = [
        ('course', 'Course'),
        ('internship', 'Internship'),
        ('workshop', 'Workshop'),
        ('degree', 'Degree'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=150)

    certificate_type = models.CharField(
        max_length=20,
        choices=CERT_TYPE,
        default='course'   # ✅ REQUIRED
    )

    issuer = models.CharField(max_length=150, default='Unknown')  # ✅ REQUIRED

    issue_date = models.DateField(default=timezone.now)  # ✅ REQUIRED
    year = models.IntegerField(default=2025)             # ✅ REQUIRED

    description = models.TextField(blank=True)
    file = models.FileField(upload_to='certificates/')

    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved')],
        default='Pending'
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"
    # folio/models.py

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
class Career(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.JSONField(default=list, blank=True)
    goals = models.JSONField(default=list, blank=True)
    certificates = models.ManyToManyField(Certificate, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Career"