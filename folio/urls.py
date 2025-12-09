from django.urls import path
from .views import user_settings
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("index/", views.index, name="index"),
    path("resume/", views.resume_view, name="resume"),
    path("newsletter/", views.newsletter_subscribe, name="newsletter"),

    # Projects CRUD
    
    path('projects/', views.projects, name='projects'),
    path("projects/add/", views.add_project, name="add_project"),
    path("projects/edit/<int:pk>/", views.edit_project, name="edit_project"),
    path("projects/delete/<int:pk>/", views.delete_project, name="delete_project"),
    path("projects/<int:pk>/", views.project_detail, name="project_detail"),

    # Blog
   
    path("blog/", views.blog_list, name="blog"),  # name changed from blog_list → blog

    path("blog/<int:pk>/", views.blog_detail, name="blog_detail"),

    # Contact
    
    path("contact/", views.contact_view, name="contact_page"),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path("contact/success/", views.contact_success, name="contact_success"),
    path('contact/', views.contact_view, name='contact'),
    # Authentication
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
   
    path("settings/", user_settings, name="settings"),
 
    path("skills/", views.skills_page, name="skills"),
    path("skills/add/", views.add_skill, name="add_skill"),
    path("skills/update/<int:skill_id>/", views.update_skill, name="update_skill"),
    path("skills/delete/<int:skill_id>/", views.delete_skill, name="delete_skill"),
    path("about/", views.about, name="about"),
    path("settings/privacy/update/", views.update_privacy, name="update_privacy"),
    path("settings/logout-other-sessions/", views.logout_other_sessions, name="logout_other_sessions"),
    path("logout-other-sessions/", views.logout_other_sessions, name="logout_other_sessions"),
    path("export-data/", views.export_data, name="export_data"),
    # SETTINGS
    path("settings/", views.user_settings, name="user_settings"),
    path('settings/2fa/enable/', views.enable_2fa, name='enable_2fa'),
    path('settings/2fa/disable/', views.disable_2fa, name='disable_2fa'),
    path("change-password/", views.change_password, name="change_password"),
    path("update-notifications/", views.update_notifications, name="update_notifications"),
    path("delete-account/", views.delete_account, name="delete_account"),
    path("settings/", views.settings_page, name="settings"),
    path("featured-projects/", views.featured_projects, name="featured_projects"),
    path("latest-projects/", views.latest_projects, name="latest_projects"),
    path("experience/", views.experience, name="experience"),
    path("education/", views.education, name="education"),
    path("testimonials/", views.testimonials, name="testimonials"), 
    # Other pages
    path("products/", views.all_products, name="all_products"),
    path("category_list/", views.category_list, name="category_list"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("orders/", views.orders, name="orders"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("messages/", views.messages_view, name="messages"),
    path("help/", views.help_view, name="help"),
]
