from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import DocumentUploadForm
from .models import Document, VerificationError
import pytesseract
import cv2
import tempfile, os


def document_upload(request):
    """
    Handle multiple image uploads (via form) and run OCR on each.
    """
    if request.method == 'POST':
        files = request.FILES.getlist('image')  # get multiple files
        document_type = request.POST.get('document_type', 'Unknown')

        if not files:
            return render(request, 'verification/index.html', {
                'form': DocumentUploadForm(),
                'error': 'No files uploaded.'
            })

        # Create parent Document
        doc = Document.objects.create(document_type=document_type, verification_status='pending')

        results = []
        has_error = False
        combined_text = ""

        for f in files:
            # Save temporarily
            temp_path = os.path.join(tempfile.gettempdir(), f.name)
            with open(temp_path, 'wb+') as dest:
                for chunk in f.chunks():
                    dest.write(chunk)

            # Run OCR
            img = cv2.imread(temp_path)
            extracted_text = pytesseract.image_to_string(img)

            results.append({"filename": f.name, "text": extracted_text})
            combined_text += f"\n\n---- {f.name} ----\n{extracted_text}"

            # Rule check
            if "error" in extracted_text.lower():
                has_error = True
                VerificationError.objects.create(
                    document=doc,
                    error_description=f"Detected error in {f.name}",
                    notified_admin=False
                )

        # Save combined OCR text in DB (for reference)
        doc.extracted_text = combined_text
        doc.verification_status = 'error' if has_error else 'verified'
        doc.save()

        return render(request, 'verification/result.html', {
            'document': doc,
            'errors': VerificationError.objects.filter(document=doc),
            'results': results
        })

    else:
        form = DocumentUploadForm()
    return render(request, 'verification/index.html', {'form': form})


def verify_document(request):
    """
    API endpoint for JSON-based verification.
    Accepts multiple images + document_type, returns JSON response.
    """
    if request.method == 'POST':
        files = request.FILES.getlist('images')
        document_type = request.POST.get('document_type', 'Unknown')

        if not files:
            return JsonResponse({'status': 'error', 'message': 'No images uploaded'}, status=400)

        doc = Document.objects.create(document_type=document_type, verification_status='pending')

        results = []
        has_error = False
        combined_text = ""

        for f in files:
            temp_path = os.path.join(tempfile.gettempdir(), f.name)
            with open(temp_path, 'wb+') as dest:
                for chunk in f.chunks():
                    dest.write(chunk)

            img = cv2.imread(temp_path)
            extracted_text = pytesseract.image_to_string(img)

            results.append({"filename": f.name, "text": extracted_text})
            combined_text += f"\n\n---- {f.name} ----\n{extracted_text}"

            if "error" in extracted_text.lower():
                has_error = True
                VerificationError.objects.create(
                    document=doc,
                    error_description=f"Detected error in {f.name}",
                    notified_admin=False
                )

        doc.extracted_text = combined_text
        doc.verification_status = 'error' if has_error else 'verified'
        doc.save()

        return JsonResponse({
            'status': 'error' if has_error else 'success',
            'document_id': doc.id,
            'message': 'Errors detected' if has_error else 'All documents verified successfully',
            'files': results
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


def verification_result(request, doc_id):
    """
    Display the verification result for a document.
    """
    doc = get_object_or_404(Document, id=doc_id)
    errors = VerificationError.objects.filter(document=doc)

    # split stored text just in case, but normally results come from upload
    results = []
    if doc.extracted_text:
        for block in doc.extracted_text.split("----"):
            if block.strip():
                results.append({"filename": "Unknown", "text": block.strip()})

    return render(request, 'verification/result.html', {
        'document': doc,
        'errors': errors,
        'results': results
    })