import random

# List of Sinhala consonants
CONSONANTS = [
    "ක",
    "ඛ",
    "ග",
    "ඝ",
    "ච",
    "ජ",
    "ට",
    "ඩ",
    "ත",
    "ද",
    "ධ",
    "න",
    "ඳ",
    "ප",
    "බ",
    "ම",
    "ය",
    "ර",
    "ල",
    "ව",
    "ස",
    "හ",
    "ළ",
    "ෆ",
]

# List of Sinhala standalone vowels
STANDALONE_VOWELS = [
    "අ",
    "ආ",
    "ඇ",
    "ඈ",
    "ඉ",
    "ඊ",
    "උ",
    "ඌ",
    "එ",
    "ඒ",
    "ඔ",
    "ඕ",
    "ඳ",
    "ඝ",
    "ෆ",
    "ඛ",
]

# List of Sinhala vowel signs
VOWEL_SIGNS = ["ැ", "ෑ", "ි", "ී", "ු", "ූ", "ෙ", "ේ", "ො", "ෝ", "ෞ"]

# List of valid two-letter combinations
TWO_LETTER_COMBINATIONS = [
    "කප",
    "සර",
    "වල",
    "බල",
    "පයි",
    "මට",
    "හර",
    "නයි",
    "සවු",
    "මල",
    "කය",
    "වයි",
    "ලප",
    "මැර",
    "මාර",
    "කර",
    "වර",
    "සර",
    "තන",
    "ටය",
    "පක",
    "හුත්",
    "‍රිය",
    "යිය",
    "යිය",
    "බර",
    "හිල",
    "හුත්",
]

# Letters that shouldn't appear in the middle or end
INVALID_MIDDLE_END_LETTERS = [
    "ඛ",
    "ඡ",
    "ඣ",
    "ඍ",
    "ඝ",
    "ඨ",
    "ඪ",
    "අ",
    "ආ",
    "ඇ",
    "ඈ",
    "ඉ",
    "ඊ",
    "උ",
    "ඌ",
    "එ",
    "ඒ",
    "ඔ",
    "ඕ",
]


def combine_consonant_vowel(consonant, vowel_sign=None):
    """Combine a consonant with an optional vowel sign."""
    if vowel_sign:
        return consonant + vowel_sign
    return consonant


def get_letter(vowel_chance):
    """Return a letter which might be a voweled consonant or plain consonant based on vowel_chance."""
    consonant = random.choice(CONSONANTS)
    if random.random() < vowel_chance:  # Chance to add a vowel sign
        vowel_sign = random.choice(VOWEL_SIGNS)
        return combine_consonant_vowel(consonant, vowel_sign)
    return consonant


def count_visual_characters(word):
    """Helper function to count the actual visual characters in a Sinhala word."""
    # Count consonants as one and ignore vowel signs when counting
    visual_chars = 0
    for char in word:
        if char in CONSONANTS or char in STANDALONE_VOWELS:
            visual_chars += 1
    return visual_chars


def generate_word():
    """Generate a random 3-letter word following Sinhala letter combination rules."""
    while True:
        # 20% chance of choosing a valid two-letter combination
        if random.random() < 0.20:
            # Choose a two-letter combination for the first two letters
            two_letter_combo = random.choice(TWO_LETTER_COMBINATIONS)
            letter1 = two_letter_combo[0]
            letter2 = two_letter_combo[1]
        else:
            # Generate the first two letters normally
            letter1 = get_letter(0.50)  # 50% chance for the first letter
            letter2 = get_letter(0.80)  # 80% chance for the second letter

        # Generate the third letter
        letter3 = get_letter(0.10)  # 10% chance for the third letter

        word = letter1 + letter2 + letter3

        # Count visual characters in the word (ignoring vowel signs)
        if count_visual_characters(word) == 3:
            # Ensure that the second and third letters are valid (not standalone vowels)
            if word[1] not in STANDALONE_VOWELS and word[2] not in STANDALONE_VOWELS:
                # Ensure that the second and third letters are not in the invalid set for middle or end
                if (
                    word[1] not in INVALID_MIDDLE_END_LETTERS
                    and word[2] not in INVALID_MIDDLE_END_LETTERS
                ):
                    return word
