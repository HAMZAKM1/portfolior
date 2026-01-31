from django import forms
from django.forms.widgets import FileInput
from .models import Profile, Skill, Visitor, Project, ProjectGallery, Category, BlogPost, Testimonial, Resume
from .models import Contact
from .models import Blog
from .models import Certificate
from django import forms
from .models import Course  # make sure you have a Course model
# -------------------------
# Multi-file upload widget
# -------------------------
class MultiFileInput(FileInput):
    allow_multiple_selected = True


# -------------------------
# Profile Form
# -------------------------
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'bio',
            'profile_image',
            'email_updates',
            'product_emails',
            'show_email',
            'show_profile',
            'allow_messages',
            'two_factor_enabled',
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }


# -------------------------
# Skill Form
# -------------------------
class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'level', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


# -------------------------
# Contact Form (needs Contact model)
# -------------------------
# Define a Contact model if not already:
# class Contact(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     subject = models.CharField(max_length=200)
#     message = models.TextField()
#     sent_at = models.DateTimeField(null=True, blank=True)
#     def __str__(self): return self.name

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
                }
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'category', 'technologies', 'is_featured']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'technologies': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'is_featured': forms.CheckboxInput(),
        }


# -------------------------
# Project Media Form (single file)
# -------------------------
class ProjectMediaForm(forms.ModelForm):
    class Meta:
        model = ProjectGallery  # single media file saved to ProjectGallery
        fields = ['image']


# -------------------------
# Project Gallery Form (multiple images)
# -------------------------
class ProjectGalleryForm(forms.ModelForm):
    class Meta:
        model = ProjectGallery
        fields = ['image']
        widgets = {
            'image': MultiFileInput(attrs={'multiple': True}),
        }


# -------------------------
# Blog Form (optional)
# -------------------------
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'rows': 6, 'class': 'form-control'}),
        }


# -------------------------
# Testimonial Form (optional)
# -------------------------
class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'position', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }


# -------------------------
# Resume Form (optional)
# -------------------------
class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['file']
# folio/forms.py

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content']
    
# folio/forms.py
class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = [
            'title',
            'subject',
            'certificate_type',
            'issuer',
            'issue_date',
            'year',
            'description',
            'file',
        ]
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'issuer': forms.TextInput(attrs={'class': 'form-control'}),
            'certificate_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
# folio/forms.py



class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'completed']