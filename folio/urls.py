from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns = [
    # Home / Index
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("index/", views.index, name="index"),

    # Resume & Newsletter
    path("resume/", views.resume_view, name="resume"),
    path("newsletter/", views.newsletter_subscribe, name="newsletter"),
   
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='folio/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path("resume/software/", views.resume_software, name="resume_software"),
    path("resume/hardware/", views.resume_hardware, name="resume_hardware"),
    path("resume/accounting/", views.resume_accounting, name="resume_accounting"),
    path("resume/finance/", views.resume_finance, name="resume_finance"),
    path("resume/mobile/", views.resume_mobile, name="resume_mobile"),
    path("resume/cooker/", views.resume_cooker, name="resume_cooker"),
    path("resume/auto/", views.resume_auto, name="resume_auto"),
    path("resume/graphic/", views.resume_graphic, name="resume_graphic"),
    path("resume/video/", views.resume_video, name="resume_video"),
    path("resume/photography/", views.resume_photography, name="resume_photography"),
    # User settings / profile
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/', views.courses_view, name='courses'),
    path('career/', views.career_view, name='career'),
    path('courses/<int:pk>/', views.course_detail_view, name='course_detail'),
    path("user-settings/", views.user_settings, name="user_settings"),
    path("settings/", views.settings_view, name='settings'),
    path("change-password/", views.change_password, name="change_password"),
    path("settings/privacy/update/", views.update_privacy, name="update_privacy"),
    path("settings/2fa/enable/", views.enable_2fa, name="enable_2fa"),
    path("settings/2fa/disable/", views.disable_2fa, name="disable_2fa"),
    path("update-notifications/", views.update_notifications, name="update_notifications"),
    path("delete-account/", views.delete_account, name="delete_account"),
    path("logout-other-sessions/", views.logout_other_sessions, name="logout_other_sessions"),
    path('contact/', views.contact, name='contact'),
    # Projects
    path("projects/", views.projects, name="projects"),
    path("projects/add/", views.add_project, name="add_project"),
    path("projects/edit/<int:pk>/", views.edit_project, name="edit_project"),
    path("projects/delete/<int:pk>/", views.delete_project, name="delete_project"),
    path("projects/<int:pk>/", views.project_detail, name="project_detail"),
    path('featured-projects/', views.featured_projects, name='featured_projects'),
    path('latest-projects/', views.latest_projects, name='latest_projects'),

    # Skills
    path("skills/", views.skills_page, name="skills"),
    path("skills/add/", views.add_skill, name="add_skill"),
    path("skills/update/<int:skill_id>/", views.update_skill, name="update_skill"),
    path("skills/delete/<int:skill_id>/", views.delete_skill, name="delete_skill"),
    path("skills/<slug:slug>/", views.skill_detail, name='skill_detail'),

    # Skill / category pages
    path("software-engineering/", views.software_engineering, name="software_engineering"),
    path("web-development/", views.web_development, name="web_development"),
    path("ai-ml/", views.ai_ml, name="ai_ml"),
    path("cloud-computing/", views.cloud_computing, name="cloud_computing"),
    path("financial-management/", views.financial_management, name="financial_management"),
    path("accounting/", views.accounting, name="accounting"),
    path("business-admin/", views.business_admin, name="business_admin"),
    path("mobile-mechanic/", views.mobile_mechanic, name="mobile_mechanic"),
    path("auto-repair/", views.auto_repair, name="auto_repair"),
    path("electrical-technician/", views.electrical_technician, name="electrical_technician"),
    path("hvac/", views.hvac, name="hvac"),
    path("hvac-technician/", views.hvac_technician, name="hvac_technician"),
    path("graphic-design/", views.graphic_design, name="graphic_design"),
    path("video-editing/", views.video_editing, name="video_editing"),
    path("photography/", views.photography, name="photography"),

    # Blog
    path("blog/", views.blog_list, name="blog"),
    path("blog/<int:pk>/", views.blog_detail, name="blog_detail"),

    # Contact
    path("contact/", views.contact_view, name="contact_page"),
    path('certificates/', views.certificates, name='certificates'),  # ✅ Listing page
    path('certificates/add/', views.certificate_create, name='certificate_create'),  # ✅ Add page

    # Profile
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),

    # Other pages
    path("about/", views.about, name="about"),
    path("experience/", views.experience, name="experience"),
    path("education/", views.education, name="education"),
    path("testimonials/", views.testimonials, name="testimonials"),

    # Export data
    path('courses/', views.courses, name='courses'),           # ✅ add this
    path('python/', views.python_section, name='python'),     # ✅ add this
    path('frontend/', views.frontend_section, name='frontend'),# ✅ add this
    path('projects/', views.projects, name='projects'),       # ✅ add this
    path('career/', views.career, name='career'),             # ✅ add this
    path('skills/create/', views.skill_create, name='skill_create'),

    path('blog/create/', views.blog_create, name='blog_create'),
    path("projects/add/", views.project_create, name="project_create"),
    path("export-data/", views.export_data, name="export_data"),

]

# Serve static & media files in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
