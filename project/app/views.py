from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Profile, Post, Job,JobApplication


@login_required
def home_view(request):
    return render(request, "home.html")


# SIGNUP

def signup_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error": "Username already exists"
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # user login automatically
        login(request, user)

        return redirect("feed")

    return render(request, "signup.html")

# LOGIN
def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("feed")

        else:
            return render(request, "login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "login.html")


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect("login")


# FEED (POST SYSTEM)
@login_required
def feed_view(request):

    if request.method == "POST":

        content = request.POST.get("content")

        if content:
            Post.objects.create(
                user=request.user,
                content=content
            )

        return redirect("feed")

    posts = Post.objects.all().order_by("-created_at")

    return render(request, "feed.html", {
        "posts": posts
    })


# PROFILE
@login_required
def profile_view(request):

    profile = Profile.objects.get(user=request.user)

    posts = Post.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(request, "profile.html", {
        "profile": profile,
        "posts": posts
    })


# EDIT PROFILE
@login_required
def edit_profile(request):

    profile = request.user.profile

    if request.method == "POST":

        profile.bio = request.POST.get("bio")
        profile.location = request.POST.get("location")

        if request.FILES.get("profile_image"):
            profile.profile_image = request.FILES.get("profile_image")

        profile.save()

        return redirect("profile")

    return render(request, "edit_profile.html", {"profile": profile})

# JOBS PAGE
@login_required
def jobs_view(request):

    jobs = Job.objects.all().order_by("-created_at")

    return render(request, "jobs.html", {
        "jobs": jobs
    })


# ADMIN DASHBOARD
@staff_member_required
def admin_dashboard(request):

    total_users = User.objects.count()
    total_jobs = Job.objects.count()
    latest_jobs = Job.objects.order_by("-created_at")[:5]

    return render(request, "admin_dashboard.html", {
        "total_users": total_users,
        "total_jobs": total_jobs,
        "latest_jobs": latest_jobs
    })


# ADMIN USERS
@staff_member_required
def admin_users_list(request):

    users = User.objects.all().order_by("-date_joined")

    return render(request, "admin_users.html", {
        "users": users
    })


# ADMIN JOB LIST
@staff_member_required
def admin_job_list(request):

    jobs = Job.objects.all().order_by("-created_at")

    return render(request, "admin/job_list.html", {
        "jobs": jobs
    })


# ADD JOB
@staff_member_required
def admin_add_job(request):

    if request.method == "POST":

        title = request.POST.get("title")
        company = request.POST.get("company")
        location = request.POST.get("location")
        description = request.POST.get("description")

        Job.objects.create(
            title=title,
            company=company,
            location=location,
            description=description,
            posted_by=request.user
        )

        return redirect("admin_jobs")

    return render(request, "admin/add_job.html")


# EDIT JOB
@staff_member_required
def admin_edit_job(request, id):

    job = get_object_or_404(Job, id=id)

    if request.method == "POST":

        job.title = request.POST.get("title")
        job.company = request.POST.get("company")
        job.location = request.POST.get("location")
        job.description = request.POST.get("description")

        job.save()

        return redirect("admin_jobs")

    return render(request, "admin/edit_job.html", {
        "job": job
    })


# DELETE JOB
@staff_member_required
def admin_delete_job(request, id):

    job = get_object_or_404(Job, id=id)

    job.delete()

    return redirect("admin_jobs")


#Jon Appliye..

@login_required
def apply_job(request, id):

    job = get_object_or_404(Job, id=id)

    already_applied = JobApplication.objects.filter(
        user=request.user,
        job=job
    ).exists()

    if not already_applied:
        JobApplication.objects.create(
            user=request.user,
            job=job
        )

    return redirect('jobs')