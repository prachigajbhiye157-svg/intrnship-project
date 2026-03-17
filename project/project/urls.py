"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[

    # Django Admin
    path('admin/', admin.site.urls),

    # AUTH
    path('', views.signup_view, name='signup'),


    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    # USER PAGES
    path('feed/', views.feed_view, name='feed'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('jobs/', views.jobs_view, name='jobs'),
    path('apply-job/<int:id>/', views.apply_job, name='apply_job'),

    # ADMIN PANEL
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/users/', views.admin_users_list, name='admin_users'),

    path('dashboard/jobs/', views.admin_job_list, name='admin_jobs'),
    path('dashboard/jobs/add/', views.admin_add_job, name='admin_add_job'),
    path('dashboard/jobs/edit/<int:id>/', views.admin_edit_job, name='admin_edit_job'),
    path('dashboard/jobs/delete/<int:id>/', views.admin_delete_job, name='admin_delete_job'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

