from django.db import models
from django.contrib.auth.models import User

# ==========================================================
# PROFILE
# ==========================================================
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.username

# ==========================================================
# SKILL MODEL
# ==========================================================


# ==========================================================
# EDUCATION MODEL
# ==========================================================
class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.degree} - {self.institution}"

# ==========================================================
# EXPERIENCE MODEL
# ==========================================================
class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.company}"

# ==========================================================
# CERTIFICATIONS
# ==========================================================
class Certification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255)
    issue_date = models.DateField()
    credential_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.issuer}"

# ==========================================================
# PROJECT CATEGORY
# ==========================================================
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Project(models.Model):
    PROJECT_TYPES = [
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend'),
        ('Fullstack', 'Fullstack'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)

    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    technologies = models.CharField(max_length=300, blank=True)
    project_type = models.CharField(
        max_length=20,
        choices=PROJECT_TYPES,
        default='Frontend'
    )

    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProjectGallery(models.Model):
    project = models.ForeignKey(Project, related_name="gallery", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="projects/gallery/")

    def __str__(self):
        return f"Image for {self.project.title}"

# ==========================================================
# PROJECT MEDIA
# ==========================================================
class ProjectMedia(models.Model):
    project = models.ForeignKey(Project, related_name="media", on_delete=models.CASCADE)
    file = models.FileField(upload_to="projects/media/")

    def __str__(self):
        return f"Media for {self.project.title}"

# ==========================================================
# TECH STACK
# ==========================================================
class TechStack(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# ==========================================================
# BLOG
# ==========================================================
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to="blog/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ==========================================================
# TESTIMONIALS
# ==========================================================
class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True, null=True)
    feedback = models.TextField()
    photo = models.ImageField(upload_to="testimonials/", blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.role}"

# ==========================================================
# RESUME
# ==========================================================
class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="resume/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Resume"

# ==========================================================
# CONTACT MESSAGES
# ==========================================================
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

# ==========================================================
# VISITOR ANALYTICS
# ==========================================================
class Visitor(models.Model):
    ip_address = models.GenericIPAddressField()
    visited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip_address


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend'),
        ('Database', 'Database'),
        ('Tools', 'Tools'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    level = models.PositiveIntegerField(help_text="0–100")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name
