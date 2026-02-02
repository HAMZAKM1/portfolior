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
    Visitor,
    Certificate
)

# =========================
# Project Gallery Inline
# =========================
class ProjectGalleryInline(admin.TabularInline):
    model = ProjectGallery
    extra = 1


# =========================
# Project Admin
# =========================
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'featured_badge',
        'title',
        'category',
        'is_featured',
        'created_at',
    )
    list_editable = ('is_featured',)
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'description', 'technologies')
    inlines = [ProjectGalleryInline]

    def featured_badge(self, obj):
        return "⭐" if obj.is_featured else "—"

    featured_badge.short_description = "Featured"


# =========================
# Profile Admin
# =========================
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'show_profile',
        'email_updates',
        'two_factor_enabled',
    )
    search_fields = ('user__username', 'user__email')


# =========================
# Skill Admin
# =========================
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'level', 'user')
    list_filter = ('category',)
    search_fields = ('name',)


# =========================
# Certificate Admin (ADMIN ONLY UPLOAD)
# =========================
@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'title',
        'year',
        'status',
        'uploaded_at'
    )

    list_filter = (
        'status',
        'year',
    )

    search_fields = (
        'title',
        'user__username',
    )

    ordering = ('-uploaded_at',)
    readonly_fields = ('uploaded_at',)

    fieldsets = (
        ('Certificate Info', {
            'fields': ('user', 'title', 'year', 'file')
        }),
        ('Approval Status', {
            'fields': ('status',)
        }),
        ('System Info', {
            'fields': ('uploaded_at',)
        }),
    )

    actions = ['approve_certificates']

    def approve_certificates(self, request, queryset):
        queryset.update(status='Approved')

    approve_certificates.short_description = "✅ Approve selected certificates"


# =========================
# Register remaining models
# =========================
admin.site.register(Category)
admin.site.register(ProjectGallery)
admin.site.register(TechStack)
admin.site.register(BlogPost)
admin.site.register(Testimonial)
admin.site.register(Resume)
admin.site.register(Contact)
admin.site.register(Visitor)

