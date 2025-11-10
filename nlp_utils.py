from typing import List, Tuple
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_entities(text: str) -> List[Tuple[str, str]]:
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def validate_aadhar_number(aadhar_number: str) -> bool:
    return len(aadhar_number) == 12 and aadhar_number.isdigit()

def validate_pan_number(pan_number: str) -> bool:
    return len(pan_number) == 10 and pan_number[:5].isalpha() and pan_number[5:9].isdigit() and pan_number[9].isalpha()

def correct_text(text: str) -> str:
    # Placeholder for text correction logic
    return text.strip()

def validate_extracted_data(text):
    # Dummy validation logic
    return True