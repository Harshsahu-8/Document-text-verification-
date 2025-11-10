from django.test import TestCase
from .models import Document
from .ocr_utils import extract_text_from_image
from .nlp_utils import validate_extracted_data

class DocumentVerificationTests(TestCase):

    def setUp(self):
        self.document = Document.objects.create(
            image='path/to/test/image.jpg',
            aadhar_number='1234-5678-9012',
            pan_number='ABCDE1234F'
        )

    def test_extract_text_from_image(self):
        extracted_text = extract_text_from_image(self.document.image.path)
        self.assertIsInstance(extracted_text, str)

    def test_validate_extracted_data(self):
        valid_aadhar = validate_extracted_data(self.document.aadhar_number, 'Aadhar')
        valid_pan = validate_extracted_data(self.document.pan_number, 'PAN')
        self.assertTrue(valid_aadhar)
        self.assertTrue(valid_pan)

    def test_document_verification(self):
        extracted_text = extract_text_from_image(self.document.image.path)
        self.assertIn(self.document.aadhar_number, extracted_text)
        self.assertIn(self.document.pan_number, extracted_text)