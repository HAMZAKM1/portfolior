from django.contrib import admin
from .models import (
    Profile,
    Skill,
    Category,
    Project,
    ProjectGallery,
    TechStack,
    BlogPost,
    Testimonial,
    Resume,
    Contact,
    Visitor
)

# =========================
# Project Inlines
# =========================
class ProjectGalleryInline(admin.TabularInline):
    model = ProjectGallery
    extra = 1


# =========================
# Project Admin (FEATURED ENABLED ✅)
# =========================
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'featured_badge',
        'title',
        'category',
        'project_type',
        'is_featured',
        'created_at',
    )

    list_editable = ('is_featured',)

    list_filter = (
        'category',
        'project_type',
        'is_featured',
    )

    search_fields = (
        'title',
        'description',
        'technologies',
    )

    inlines = [
        ProjectGalleryInline,
    ]

    # ⭐ FEATURED STAR BADGE
    def featured_badge(self, obj):
        return "⭐" if obj.is_featured else "—"

    featured_badge.short_description = "Featured"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'location')
    search_fields = ('user__username', 'full_name', 'location')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'level')
    list_filter = ('category', 'level')
    search_fields = ('name',)


admin.site.register(Category)
admin.site.register(ProjectGallery)
admin.site.register(TechStack)
admin.site.register(BlogPost)
admin.site.register(Testimonial)
admin.site.register(Resume)
admin.site.register(Contact)
admin.site.register(Visitor)
