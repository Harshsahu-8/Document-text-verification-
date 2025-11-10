from django.contrib import admin
from .models import Document, VerificationError

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'document_type', 'extracted_text', 'verification_status', 'created_at')
    search_fields = ('document_type', 'extracted_text')
    list_filter = ('verification_status',)
    ordering = ('-created_at',)

@admin.register(VerificationError)
class VerificationErrorAdmin(admin.ModelAdmin):
    list_display = ('id', 'document', 'error_description', 'notified_admin', 'created_at')
    search_fields = ('document__document_type', 'error_description')
    list_filter = ('notified_admin',)
    ordering = ('-created_at',)
    