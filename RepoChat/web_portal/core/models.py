from django.db import models

class Repository(models.Model):
    # Enums for Status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('indexed', 'Indexed / Ready'),
        ('failed', 'Failed'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # The actual file upload. 
    # 'upload_to' puts files in 'media/repos/' folder automatically.
    repo_files = models.FileField(upload_to='repos/')
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.status})"