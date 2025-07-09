from django.db import models
from django.contrib.auth.models import User

class Snippet(models.Model):
    CATEGORY_CHOICES = [
        ('html', 'Html'),
        ('python', 'Python'),
        ('css', 'CSS'),
        ('javascript', 'JavaScript'),
        ('docker', 'Docker'),
        ('k8s', 'Kubernetes'),
        ('bash', 'Bash'),
        ('deploy', 'Deployment'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    code = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    tags = models.CharField(max_length=255, blank=True, help_text='Comma-separated')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title