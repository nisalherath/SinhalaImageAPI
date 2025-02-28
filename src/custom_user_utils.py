import os
import uuid
import logging
from image_utils import create_image

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

IMAGE_DIRECTORY = "static/images"

# List of Sinhala consonants (base letters)
CONSONANTS = [
    "ක", "ඛ", "ග", "ඝ", "ච", "ජ", "ට", "ඩ", "ත", "ද", "ධ", "න", "ඳ",
    "ප", "බ", "ම", "ය", "ර", "ල", "ව", "ස", "හ", "ළ", "ෆ"
]

# Vowel signs to remove
VOWEL_SIGNS = [
    "ැ", "ෑ", "ි", "ී", "ු", "ූ", "ෙ", "ේ", "ො", "ෝ", "ෞ",  # Basic vowel signs
    "ෟ", "ෛ", "ඣ", "ෙ", "ැය", "ෑය", "ීය", "ුය", "ූය", "ෙය", "ේය", "ෝය", "ෞය", # Extended vowel signs
    "ො", "ෝා", "ිං", "ීං", "ුං", "ූං", "ෙං", "ේං", "ොං", "ෝං", "ෞං",  # Special vowel forms with signs
    "ා", "ඇ", "ඈ", "ි", "ී", "ු", "ූ", "ෙ", "ො", "ේ", "ේ්", "ො", "ෝ", # Other variations
]


def remove_vowel_signs(word: str) -> str:
    """
    Remove vowel signs from the word to accurately count consonants.
    """
    word_without_vowels = ''.join([char for char in word if char not in VOWEL_SIGNS])
    logging.debug(f"Original word: {word}")
    logging.debug(f"Word after removing vowel signs: {word_without_vowels}")
    return word_without_vowels

def validate_word(word: str):
    """Ensure the provided word is exactly 3 base consonants (after removing vowel signs)."""
    # Strip vowel signs to count only consonants
    word_without_vowels = remove_vowel_signs(word)

    # Log the word without vowel signs
    logging.debug(f"Word without vowel signs: {word_without_vowels}")

    # Check if the length of the consonants-only word is 3
    if len(word_without_vowels) != 3:
        raise ValueError("Word must be exactly three base consonants long (excluding vowel signs).")

    # Ensure that the word (after removing vowel signs) contains only valid consonants
    if not all(char in CONSONANTS for char in word_without_vowels):
        raise ValueError("Word must contain only valid consonants (excluding vowel signs).")

    logging.debug(f"Validated word: {word_without_vowels}")
    return word.lower()  # Convert to lowercase for consistency

def process_custom_word(word: str):
    """
    Validate and generate an image for the user-provided word.
    Returns the image URL if successful, else raises an error.
    """
    try:
        validated_word = validate_word(word)
        unique_filename = f"{validated_word}_{uuid.uuid4().hex}.jpg"
        image_path = os.path.join(IMAGE_DIRECTORY, unique_filename)

        # Generate the image with the original word (including vowel signs)
        generated_image_path = create_image(word)  # Use the original word here
        if generated_image_path and os.path.exists(generated_image_path):
            os.rename(generated_image_path, image_path)
            logging.info(f"Custom image created for '{validated_word}': {image_path}")
            return f"/static/images/{unique_filename}"
        else:
            raise RuntimeError("Image generation failed.")

    except ValueError as ve:
        logging.error(f"Validation error: {ve}")
        raise ve
    except Exception as e:
        logging.error(f"Error processing custom word '{word}': {e}")
        raise RuntimeError("An internal server error occurred.")
