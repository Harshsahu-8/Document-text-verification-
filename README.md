# Document Verifier Project

This project is a Django application designed to convert images of documents, such as Aadhar cards and PAN cards, into text. It verifies the extracted information against a MySQL database and automates the process of verification and data correction. Alerts are sent for admin approval upon detecting errors.

## Features

- Image upload and processing using Tesseract for Optical Character Recognition (OCR).
- Data verification against a MySQL database.
- Automated error detection and correction suggestions.
- Admin alerts for manual approval of corrections.

## Technologies Used

- Django: Web framework for building the application.
- Tesseract: OCR engine for text extraction from images.
- OpenCV: Library for image processing.
- NumPy: Library for numerical operations on images.
- spaCy: NLP library for text validation and correction.
- MySQL: Database for storing user and document information.

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd doc-verifier
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Configure the database:**
   Update the `DATABASES` setting in `doc_verifier/settings.py` to connect to your MySQL database.

5. **Run migrations:**
   ```
   python manage.py migrate
   ```

6. **Start the development server:**
   ```
   python manage.py runserver
   ```

7. **Access the application:**
   Open your web browser and go to `http://127.0.0.1:8000/verification/`.

## Usage

- Upload images of Aadhar cards or PAN cards through the web interface.
- The application will process the images, extract text, and verify the information.
- Admins will receive alerts for any discrepancies that require approval.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.