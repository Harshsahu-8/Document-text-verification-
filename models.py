from django.db import models

class Document(models.Model):
    document_type = models.CharField(max_length=50)  # e.g., Aadhar, PAN
    image = models.ImageField(upload_to='documents/')
    extracted_text = models.TextField(blank=True, null=True)
    verification_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('error', 'Error'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.document_type} - {self.verification_status}"

class VerificationError(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    error_description = models.TextField()
    notified_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Error in {self.document.document_type} - {self.error_description[:50]}"