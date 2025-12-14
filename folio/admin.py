from django.contrib import admin
from .models import (
    Profile,
    Skill,
    Category,
    Project,
    ProjectGallery,
    ProjectMedia,
    TechStack,
    BlogPost,
    Testimonial,
    Resume,
    Contact,
    Visitor
)

# -------------------------
# Inline for Project Gallery
# -------------------------
class ProjectGalleryInline(admin.TabularInline):
    model = ProjectGallery
    extra = 1

# -------------------------
# Inline for Project Media
# -------------------------
class ProjectMediaInline(admin.TabularInline):
    model = ProjectMedia
    extra = 1

# -------------------------
# Project Admin
# -------------------------
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'project_type', 'created_at')
    search_fields = ('title', 'description', 'technologies')
    list_filter = ('category', 'project_type')
    inlines = [ProjectGalleryInline, ProjectMediaInline]

# -------------------------
# Profile Admin
# -------------------------
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'location')
    search_fields = ('user__username', 'full_name', 'location')

# -------------------------
# Skill Admin
# -------------------------
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'user')
    search_fields = ('name', 'user__username')
    list_filter = ('level',)

# -------------------------
# Other models
# -------------------------
admin.site.register(Category)
admin.site.register(ProjectGallery)
admin.site.register(ProjectMedia)
admin.site.register(TechStack)
admin.site.register(BlogPost)
admin.site.register(Testimonial)
admin.site.register(Resume)
admin.site.register(Contact)
admin.site.register(Visitor)
