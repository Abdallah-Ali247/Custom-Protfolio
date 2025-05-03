from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from core.models import *


site_settings, created = SiteSettings.objects.get_or_create(pk=1)

def dashboard_login(request):
    site_settings, created = SiteSettings.objects.get_or_create(pk=1)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('dashboard_home')
        else:
            messages.error(request, 'Invalid login credentials or access denied.')

    return render(request, 'dashboard/login.html', {
        'site_title': site_settings.site_title,
        'site_settings': site_settings
    })


def dashboard_logout(request):
    logout(request)
    return redirect('homepage')



def dashboard_home(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, 'You must be logged in to access the dashboard.')
        return redirect('dashboard_login')

    site_settings, created = SiteSettings.objects.get_or_create(pk=1)
    total_projects = Project.objects.count()
    current_cv = CV.objects.last()
    last_project = Project.objects.order_by('-created_at').first()

    return render(request, 'dashboard/home.html', {
        'site_settings': site_settings,
        'total_projects': total_projects,
        'current_cv': current_cv,
        'last_project': last_project,
    })



# ***********************************************************************************************************
# *********************************************  Manage Projects  *******************************************
# ***********************************************************************************************************



def dashboard_projects(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, 'You must be logged in to access this page.')
        return redirect('dashboard_login')

    projects = Project.objects.all().order_by('-year')
    return render(request, 'dashboard/projects/list.html', {
        'projects': projects,
        'page_title': 'Manage Projects',
        'site_settings': site_settings
    })



from django.core.exceptions import ValidationError

def dashboard_project_add(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, 'You must be logged in to access this page.')
        return redirect('dashboard_login')

    if request.method == "POST":
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        description = request.POST.get('description')
        category = request.POST.get('category')
        location = request.POST.get('location')
        year = request.POST.get('year')
        featured_image = request.FILES.get('featured_image')
        image_files = request.FILES.getlist('images')  # For multiple images
        tags = request.POST.get('tags','')

        try:
            project = Project.objects.create(
                title=title,
                slug=slug,
                description=description,
                category=category,
                location=location,
                year=year,
                featured_image=featured_image,
                tags=tags
            )

            for img_file in image_files:
                ProjectImage.objects.create(image=img_file, project=project)

            messages.success(request, "Project added successfully!")
            return redirect('dashboard_projects')

        except ValidationError as e:
            messages.error(request, f"Validation error: {e}")
        except Exception as e:
            messages.error(request, f"Error adding project: {e}")

    return render(request, 'dashboard/projects/add.html', {
        'page_title': 'Add New Project',
        'site_settings': site_settings
    })



from django.core.exceptions import ObjectDoesNotExist
def dashboard_project_edit(request, project_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, 'You must be logged in to access this page.')
        return redirect('dashboard_login')

    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        messages.error(request, 'Project not found.')
        return redirect('dashboard_projects')

    if request.method == "POST":
        project.title = request.POST.get('title')
        project.slug = request.POST.get('slug')
        project.description = request.POST.get('description')
        project.category = request.POST.get('category')
        project.location = request.POST.get('location')
        project.year = request.POST.get('year')
        project.tags = request.POST.get('tags', '')

        # Update featured image if provided
        featured_image = request.FILES.get('featured_image')
        if featured_image:
            project.featured_image = featured_image

        # Handle additional images
        image_files = request.FILES.getlist('images')
        for img_file in image_files:
            ProjectImage.objects.create(image=img_file, project=project)

        try:
            project.save()
            messages.success(request, 'Project updated successfully!')
            return redirect('dashboard_projects')
        except Exception as e:
            messages.error(request, f'Error saving project: {e}')

    extra_images = project.extra_images.all()  # Get related extra images
    return render(request, 'dashboard/projects/edit.html', {
        'project': project,
        'extra_images': extra_images,
        'page_title': f'Edit Project: {project.title}',
        'site_settings': site_settings
    })



def dashboard_project_delete(request, project_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, 'You must be logged in to access this page.')
        return redirect('dashboard_login')

    try:
        project = Project.objects.get(id=project_id)
        project.delete()
        messages.success(request, 'Project deleted successfully!')
    except Project.DoesNotExist:
        messages.error(request, 'Project not found.')

    return redirect('dashboard_projects')


def dashboard_project_image_delete(request, image_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, 'You must be logged in to perform this action.')
        return redirect('dashboard_login')

    try:
        image = ProjectImage.objects.get(id=image_id)
        project = image.project
        image.delete()
        messages.success(request, 'Image deleted successfully!')
    except ProjectImage.DoesNotExist:
        messages.error(request, 'Image not found.')

    return redirect('dashboard_project_edit', project_id=project.id)


# ***********************************************************************************************************
# *********************************************  Site Settings  *********************************************
# ***********************************************************************************************************

def dashboard_settings(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, 'You must be logged in to access this page.')
        return redirect('dashboard_login')

    # Get or create the single settings object
    site_settings, created = SiteSettings.objects.get_or_create(pk=1)

    if request.method == 'POST':
        site_settings.site_title = request.POST.get('site_title', '')
        site_settings.email = request.POST.get('email', '')
        site_settings.phone = request.POST.get('phone', '')
        site_settings.address = request.POST.get('address', '')
        site_settings.about_me = request.POST.get('about_me', '')
        
        # Handle image uploads
        if request.FILES.get('logo'):
            site_settings.logo = request.FILES['logo']
        if request.FILES.get('favicon'):
            site_settings.favicon = request.FILES['favicon']

        # Social links
        site_settings.social_facebook = request.POST.get('social_facebook', '')
        site_settings.social_instagram = request.POST.get('social_instagram', '')
        site_settings.social_linkedin = request.POST.get('social_linkedin', '')

        try:
            site_settings.save()
            messages.success(request, 'Site settings updated successfully!')
        except Exception as e:
            messages.error(request, f'Error saving settings: {e}')

    return render(request, 'dashboard/settings/settings.html', {
        'site_settings': site_settings,
        'page_title': 'Site Settings'
    })



# ***********************************************************************************************************
# *********************************************  CV Upload  *********************************************
# ***********************************************************************************************************


def dashboard_cv_upload(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, 'You must be logged in to access this page.')
        return redirect('dashboard_login')

    current_cv = CV.objects.last()  # Get latest uploaded CV

    if request.method == 'POST':
        cv_file = request.FILES.get('cv_file')

        if not cv_file:
            messages.error(request, 'Please select a file to upload.')
        elif not cv_file.name.endswith('.pdf'):
            messages.error(request, 'Only PDF files are allowed.')
        else:
            try:
                # Delete old CV if exists
                CV.objects.all().delete()
                # Save new CV
                CV.objects.create(cv_file=cv_file)
                messages.success(request, 'CV uploaded successfully!')
                return redirect('dashboard_cv_upload')
            except Exception as e:
                messages.error(request, f'Error uploading CV: {e}')

    return render(request, 'dashboard/cv/upload.html', {
        'current_cv': current_cv,
        'page_title': 'Upload CV',
        'site_settings': site_settings
    })




def dashboard_about_edit(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, 'You must be logged in to access this page.')
        return redirect('dashboard_login')

    about_info, created = AboutInfo.objects.get_or_create(pk=1)

    if request.method == 'POST':
        about_info.full_name = request.POST.get('full_name')
        about_info.headline = request.POST.get('headline')
        about_info.bio = request.POST.get('bio')
        about_info.experience_summary = request.POST.get('experience_summary')
        about_info.education = request.POST.get('education')
        about_info.skills = request.POST.get('skills')

        try:
            about_info.save()
            messages.success(request, 'About info updated successfully!')
            return redirect('dashboard_about_edit')
        except Exception as e:
            messages.error(request, f'Error saving about info: {e}')

    return render(request, 'dashboard/about/edit.html', {
        'about_info': about_info,
        'page_title': 'Edit About Page',
        'site_settings': site_settings
    })




def dashboard_goals_edit(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, 'You must be logged in to access this page.')
        return redirect('dashboard_login')

    goal_items = GoalItem.objects.all()

    if request.method == 'POST':
        # Delete existing and save new ones
        GoalItem.objects.all().delete()

        titles = request.POST.getlist('title')
        descriptions = request.POST.getlist('description')
        orders = request.POST.getlist('order')

        for i, (title, desc, order) in enumerate(zip(titles, descriptions, orders)):
            GoalItem.objects.create(
                title=title,
                description=desc,
                order=int(order) if order.isdigit() else i
            )

        messages.success(request, 'Goals updated successfully!')
        return redirect('dashboard_goals_edit')

    return render(request, 'dashboard/goals/edit.html', {
        'goal_items': goal_items,
        'page_title': 'Edit Goals',
        'site_settings': site_settings
    })


def dashboard_theme_settings(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, 'You must be logged in to access this page.')
        return redirect('dashboard_login')

    theme_settings, created = ThemeSettings.objects.get_or_create(pk=1)

    if request.method == 'POST':
        theme_settings.color_bg = request.POST.get('color_bg', '#1b1f2a')
        theme_settings.color_bg_alt = request.POST.get('color_bg_alt', '#2a2f3a')
        theme_settings.color_text = request.POST.get('color_text', '#e0d8c3')
        theme_settings.color_accent = request.POST.get('color_accent', '#9d77c3')
        theme_settings.color_accent_hover = request.POST.get('color_accent_hover', '#b39ddb')
        theme_settings.glow_color = request.POST.get('glow_color', '#d8b4fe')

        try:
            theme_settings.save()
            messages.success(request, 'Theme updated successfully!')
        except Exception as e:
            messages.error(request, f'Error saving theme: {e}')

    return render(request, 'dashboard/theme/edit.html', {
        'theme': theme_settings,
        'page_title': 'Edit Theme',
        'site_settings': site_settings
    })





