from django import forms
from django.forms.widgets import FileInput
from .models import Profile, Skill, Contact, Project, ProjectGallery, ProjectMedia

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
            'full_name',
            'location',
            'bio',
            'profile_image',
            'github',
            'linkedin',
            'twitter',
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

# -------------------------
# Skill Form
# -------------------------
class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'level']
        widgets = {
            'level': forms.NumberInput(attrs={
                'type': 'range',
                'min': '0',
                'max': '100',
            })
        }

# -------------------------
# Contact Form
# -------------------------
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }

# -------------------------
# Project Form
# -------------------------
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'image', 'link', 'category', 'technologies', 'project_type']

# -------------------------
# Project Media Form (single file)
# -------------------------
class ProjectMediaForm(forms.ModelForm):
    class Meta:
        model = ProjectMedia
        fields = ['file']

# -------------------------
# Project Gallery Form (multiple images)
# -------------------------
class ProjectGalleryForm(forms.ModelForm):
    class Meta:
        model = ProjectGallery
        fields = ['image']
        widgets = {
            'image': MultiFileInput(attrs={'multiple': True})
        }
