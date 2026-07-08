import re
import spacy


class SpacyService:
    """
    Service responsible for extracting basic information
    from a resume using spaCy and regular expressions.
    """

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def process(self, text: str):
        return self.nlp(text)

    def extract_name(self, doc):
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        return None

    def extract_email(self, text: str):
        pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        match = re.search(pattern, text)
        return match.group(0) if match else None

    def extract_phone(self, text: str):
        pattern = r"(\+?\d[\d\s\-\(\)]{8,15}\d)"
        match = re.search(pattern, text)
        return match.group(0) if match else None

    def extract_linkedin(self, text: str):
        pattern = r"https?://(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+/?"
        match = re.search(pattern, text)
        return match.group(0) if match else None

    def extract_github(self, text: str):
        pattern = r"https?://(?:www\.)?github\.com/[A-Za-z0-9_-]+/?"
        match = re.search(pattern, text)
        return match.group(0) if match else None

    def extract_location(self, text: str, doc):

        lines = text.split("\n")[:5]

        pattern = r"([A-Za-z\s]+,\s*[A-Za-z\s]+)"

        for line in lines:
            match = re.search(pattern, line)

            if match:
                return match.group(1).strip()

        # --------- Method 2 : spaCy Fallback ---------
        for ent in doc.ents:
            if ent.label_ in ("GPE", "LOC"):
                return ent.text

         