import os
import string as st
from dateutil import parser
import matplotlib.image as mpimg
import cv2
from passporteye import read_mrz
import easyocr
import warnings
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

# Initialize EasyOCR reader (enable GPU if available)
reader = easyocr.Reader(lang_list=['en'], gpu=True)

# Initialize FastAPI app
app = FastAPI()

def parse_date(date_string):
    """Parse date from YYMMDD format to DD/MM/YYYY."""
    try:
        date = parser.parse(date_string, yearfirst=True).date()
        return date.strftime('%d/%m/%Y')
    except Exception as e:
        print(f"Error parsing date: {e}")
        return "Invalid Date"

def clean(string):
    """Clean string by removing non-alphanumeric characters."""
    return ''.join(char for char in string if char.isalnum()).upper()

def get_country_name(country_code):
    """Handle known MRZ country code misreads."""
    return country_code.replace('1', 'I').replace('0', 'O')

def get_gender(code):
    """Convert MRZ gender code to 'M' or 'F'."""
    if code.upper() in ['M', 'F']:
        return code.upper()
    return 'M' if code == '0' else 'F'

@app.post("/extract-passport-data/")
async def extract_passport_data(file: UploadFile = File(...)):
    """Extract passport data from uploaded image."""
    temp_image_path = "tmp.png"

    try:
        # Save the uploaded file temporarily
        contents = await file.read()
        with open(file.filename, "wb") as f:
            f.write(contents)

        # Step 1: Crop to MRZ zone using PassportEye
        mrz = read_mrz(file.filename, save_roi=True)
        if not mrz:
            raise HTTPException(status_code=400, detail="Unable to read MRZ from image.")

        # Save the cropped MRZ region temporarily
        mpimg.imsave(temp_image_path, mrz.aux["roi"], cmap="gray")

        # Step 2: Preprocess the MRZ image for better OCR
        img = cv2.imread(temp_image_path)
        img = cv2.resize(img, (1110, 140))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Step 3: Perform OCR on the MRZ image
        allowlist = st.ascii_letters + st.digits + "< "
        code = reader.readtext(img, paragraph=False, detail=0, allowlist=allowlist)

        # Handle potential OCR output issues
        if len(code) < 2:
            raise HTTPException(status_code=400, detail="OCR failed to read MRZ lines properly.")

        a, b = code[0].upper(), code[1].upper()

        # Ensure MRZ lines are of correct length (44 characters)
        a = a + "<" * (44 - len(a)) if len(a) < 44 else a
        b = b + "<" * (44 - len(b)) if len(b) < 44 else b

        # Extract and map passport data
        surname, names = (a[5:44].split("<<", 1) + [""])[:2]
        passport_data = {
            "surname": surname.replace("<", " ").strip(),
            "name": names.replace("<", " ").strip(),
            "gender": get_gender(clean(b[20])),
            "date_of_birth": parse_date(b[13:19]),
            "nationality": get_country_name(clean(b[10:13])),
            "passport_type": clean(a[0:2]),
            "passport_number": clean(b[0:9]),
            "issuing_country": get_country_name(clean(a[2:5])),
            "expiration_date": parse_date(b[21:27]),
            "personal_number": clean(b[28:42]),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

    finally:
        # Clean up temporary files
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)
        if os.path.exists(file.filename):
            os.remove(file.filename)

    return JSONResponse(content=passport_data)
