from django.shortcuts import render
from core.models import Project, SiteSettings
from django.utils import timezone
from core.models import *
from core.models import ThemeSettings

# In any view that uses base.html
theme_settings, created = ThemeSettings.objects.get_or_create(pk=1)




    


# core/views.py
def homepage(request):
    site_settings, created = SiteSettings.objects.get_or_create(pk=1)
    projects = Project.objects.all().order_by('-year')
    card_projects = projects[:4] 
    carousel_projects = projects[4:12]  
    current_cv = CV.objects.last()
    year = timezone.now().year

    # For gallery: get all images from all projects
    all_projects = Project.objects.all()
    all_images = []
    for project in all_projects:
        all_images.append({
            'image': project.featured_image.url,
            'category': project.category,
            'title': project.title
        })
        for extra in project.extra_images.all():
            all_images.append({
                'image': extra.image.url,
                'category': project.category,
                'title': project.title
            })

    # Get unique categories for filtering
    categories = list(set(Project.objects.values_list('category', flat=True)))
    # Load Goal Items
    goal_items = GoalItem.objects.all()

    return render(request, 'index.html', {
        'site_settings': site_settings,
        'projects': projects,
        'card_projects':card_projects,
        'carousel_projects': carousel_projects,
        'current_cv': current_cv,
        'year': year,
        'all_images': all_images,
        'categories': categories,
        'goal_items': goal_items,
        'theme_settings': theme_settings
    })




def all_projects_view(request):
    site_settings, created = SiteSettings.objects.get_or_create(pk=1)
    projects = Project.objects.all().order_by('-year')
    return render(request, 'projects.html', {
        'site_settings': site_settings,
        'projects': projects,
        'page_title': 'All Projects'
    })
    
    
from django.shortcuts import get_object_or_404

def project_detail_view(request, slug):
    site_settings, created = SiteSettings.objects.get_or_create(pk=1)
    project = get_object_or_404(Project, slug=slug)
    extra_images = project.extra_images.all()  # From ForeignKey relationship
    return render(request, 'project_detail.html', {
        'site_settings': site_settings,
        'project': project,
        'extra_images': extra_images,
        'page_title': project.title,
        'theme_settings': theme_settings
    })
    
    



def about_view(request):
    site_settings, created = SiteSettings.objects.get_or_create(pk=1)
    current_cv = CV.objects.last()  # Get latest uploaded CV
    about_info, created = AboutInfo.objects.get_or_create(pk=1)  # Single record
    
    # Process skills into a list with stripped whitespace
    # skills = []
    # if about_info.skills:
    #     skills = [s.strip() for s in about_info.skills.split(',') if s.strip()]


    return render(request, 'about.html', {
        'site_settings': site_settings,
        'current_cv': current_cv,
        'about_info': about_info,
        'page_title': 'About Me',
        'theme_settings': theme_settings
    })




# views.py from core app

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from core.models import SiteSettings


def contact_view(request):
    site_settings, created = SiteSettings.objects.get_or_create(pk=1)
    success = False

    if request.method == 'POST':
        name = request.POST.get('name')
        visitor_email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Construct the full message
        full_message = f"Message from: {name} <{visitor_email}>\n\n{message}"
        recipient_email = site_settings.email or settings.DEFAULT_FROM_EMAIL

        try:
            send_mail(
                subject=f"Contact Form Submission: {subject}",
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                fail_silently=False,
            )
            success = True
        except Exception as e:
            print("Error sending email:", e)

    return render(request, 'contact.html', {
        'site_settings': site_settings,
        'success': success,
        'theme_settings': theme_settings
    })























