# Passport MRZ Extraction API

This project is a **FastAPI-based web service** that extracts **passport information** from Machine Readable Zone (MRZ) in passport images. It uses **EasyOCR** for optical character recognition (OCR) and **PassportEye** to crop the MRZ section.

## Features
- Extracts passport details such as:
  - Passport number
  - Name and surname
  - Nationality
  - Gender
  - Date of birth
  - Expiration date
- Supports image preprocessing for better OCR accuracy.
- Accepts image uploads through an API endpoint.
- Returns extracted passport data in **JSON format**.

---

## Installation

### Prerequisites
- **Python** 3.8 or higher
- **pip** for Python package management
- **Tesseract OCR** (needed by PassportEye):
  - **Ubuntu/Debian**:
    ```bash
    sudo apt update && sudo apt install tesseract-ocr
    ```
  - **Windows**:
    - Download and install Tesseract from [here](https://github.com/tesseract-ocr/tesseract).
    - Add Tesseract to your **PATH** environment variable.

---


### Clone the Repository

```bash
git clone https://github.com/irfanmahamud/extract-passport-information-python-fastapi.git
cd extract-passport-information-python-fastapi
```

### Install Dependencies
Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### Install the required packages:

```bash
pip install -r requirements.txt
```
If you don’t have a requirements.txt file, create one with the following contents:

fastapi
uvicorn
python-multipart
easyocr
passporteye
opencv-python-headless
matplotlib

Then, install the dependencies:

```bash
pip install -r requirements.txt
```
## How to Run the Project
### Step 1: Start the FastAPI Server
Use Uvicorn to run the FastAPI service:

```bash
uvicorn app:app --reload
```

The API will be accessible at: http://127.0.0.1:8000

### Step 2: Test the API via Swagger UI
Open your browser and navigate to:

http://127.0.0.1:8000/docs

Use the POST /extract-passport-data/ endpoint to upload a passport image.
Click Execute to see the extracted passport data in the JSON response.
Example JSON Response

```json
{
  "surname": "HOSSAIN",
  "name": "MD SHUMAN",
  "gender": "M",
  "date_of_birth": "15/02/1983",
  "nationality": "BGD",
  "passport_type": "P",
  "passport_number": "A00993322",
  "issuing_country": "BGD",
  "expiration_date": "06/02/2032",
  "personal_number": "77813859817419"
}
```

## Error Handling

400 Bad Request: If the MRZ section cannot be read from the image.
500 Internal Server Error: If there is an issue during OCR or image processing.
Development and Contribution
Feel free to contribute to this project by following these steps:

## Fork the repository.
Create a new branch for your feature or bug fix.
Submit a pull request with a detailed description of your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.

## Contact
If you have any questions or encounter issues, please feel free to open an issue in this repository.

## Acknowledgments
FastAPI – For building the web framework.
EasyOCR – For performing OCR.
PassportEye – For cropping the MRZ from passport images.

