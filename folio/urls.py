from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Home / Index
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("index/", views.index, name="index"),

    # Resume & Newsletter
    path("resume/", views.resume_view, name="resume"),
    path("newsletter/", views.newsletter_subscribe, name="newsletter"),

    # User settings
    path("user-settings/", views.user_settings, name="user_settings"),

    path("settings/privacy/update/", views.update_privacy, name="update_privacy"),
    path("settings/2fa/enable/", views.enable_2fa, name="enable_2fa"),
    path("settings/2fa/disable/", views.disable_2fa, name="disable_2fa"),
    path("change-password/", views.change_password, name="change_password"),
    path("update-notifications/", views.update_notifications, name="update_notifications"),
    path("delete-account/", views.delete_account, name="delete_account"),

    # Projects
    path("projects/", views.projects, name="projects"),
    path("projects/add/", views.add_project, name="add_project"),
    path("projects/edit/<int:pk>/", views.edit_project, name="edit_project"),
    path("projects/delete/<int:pk>/", views.delete_project, name="delete_project"),
    path("projects/<int:pk>/", views.project_detail, name="project_detail"),

    # Skills
    path("skills/", views.skills_page, name="skills"),
    path("skills/add/", views.add_skill, name="add_skill"),
    path("skills/update/<int:skill_id>/", views.update_skill, name="update_skill"),
    path("skills/delete/<int:skill_id>/", views.delete_skill, name="delete_skill"),

    # Blog
    path("blog/", views.blog_list, name="blog"),
    path("blog/<int:pk>/", views.blog_detail, name="blog_detail"),

    # Contact & Profile
    path("contact/", views.contact_view, name="contact_page"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),

    # Other pages
    path("about/", views.about, name="about"),
    path("experience/", views.experience, name="experience"),
    path("education/", views.education, name="education"),
    path("testimonials/", views.testimonials, name="testimonials"),

    # Export Data
    path("export-data/", views.export_data, name="export_data"),
]

# Serve static & media files in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
