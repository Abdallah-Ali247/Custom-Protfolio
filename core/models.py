from django.db import models


class SiteSettings(models.Model):
    site_title = models.CharField(max_length=100, default="Architect Portfolio")
    logo = models.ImageField(upload_to='site/', null=True, blank=True)
    favicon = models.ImageField(upload_to='site/', null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    social_facebook = models.URLField(null=True, blank=True)
    social_instagram = models.URLField(null=True, blank=True)
    social_linkedin = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.site_title


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True,blank=True)
    description = models.TextField()
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    year = models.PositiveIntegerField()
    featured_image = models.ImageField(upload_to='projects/')
    images = models.ManyToManyField('ProjectImage', related_name='project_images', blank=True)
    tags = models.CharField(max_length=200, help_text="Comma-separated tags (e.g., residential, modern)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# class ProjectImage(models.Model):
#     image = models.ImageField(upload_to='projects/extra')
    
#     def __str__(self):
#         return f"Image {self.id}"
    
    
class ProjectImage(models.Model):
    image = models.ImageField(upload_to='projects/extra')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='extra_images')
    
    def __str__(self):
        return f"Image {self.id} for {self.project.title}"




class CV(models.Model):
    cv_file = models.FileField(upload_to='cv/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CV Uploaded on {self.uploaded_at.strftime('%Y-%m-%d')}"



class AboutInfo(models.Model):
    full_name = models.CharField(max_length=100, default="Architect Name")
    headline = models.CharField(max_length=200, default="Architect & Interior Designer")
    bio = models.TextField(blank=True, null=True)
    
    # Professional Experience
    experience_summary = models.TextField(blank=True, null=True)

    # Education
    education = models.TextField(blank=True, null=True)

    # Skills
    skills = models.TextField(help_text="Enter skills separated by commas", blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"About Info - {self.full_name}"




class GoalItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title



class ThemeSettings(models.Model):
    # Color Variables
    color_bg = models.CharField(max_length=7, default="#1b1f2a", help_text="Background color")
    color_bg_alt = models.CharField(max_length=7, default="#2a2f3a", help_text="Alternative background (cards, modals)")
    color_text = models.CharField(max_length=7, default="#e0d8c3", help_text="Main text color")
    color_accent = models.CharField(max_length=7, default="#9d77c3", help_text="Accent color (buttons, links)")
    color_accent_hover = models.CharField(max_length=7, default="#b39ddb", help_text="Hover version of accent color")
    glow_color = models.CharField(max_length=7, default="#d8b4fe", help_text="Glow/hover effects")

    def __str__(self):
        return "Theme Settings"






