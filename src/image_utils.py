from PIL import Image, ImageDraw, ImageFont
import os
import random
import math

# Font configuration
FONT_PATH = "font/NotoSansSinhala-Regular.ttf"  # Ensure this path is correct
FONT_SIZE = 200
VERSION_FONT_SIZE = 20  # Smaller font size for version text

# Image configuration
IMAGE_DIRECTORY = "data/images"
IMAGE_WIDTH = 1920  # Width for high resolution (16:9 aspect ratio)
IMAGE_HEIGHT = 1080  # Height for high resolution (16:9 aspect ratio)

# Watermark configuration
WATERMARK_PATH = (
    "watermark/watermarky2.png"  # Replace with the path to your watermark PNG
)
WATERMARK_SCALE = 1  # Scale factor for watermark size (adjust as needed)
WATERMARK_MARGIN = 0  # Margin from the edges (adjust as needed)
WATERMARK_Y_OFFSET = 0  # Offset to move watermark upwards


def generate_light_color():
    """Generate a vibrant light RGB color for the background."""
    r = random.randint(180, 255)
    g = random.randint(180, 255)
    b = random.randint(180, 255)

    # Ensure the color is not too similar to others
    if r < 200 and g < 200 and b < 200:
        r = random.randint(200, 255)
        g = random.randint(200, 255)
        b = random.randint(200, 255)

    return (r, g, b)


def generate_dark_color():
    """Generate a dark RGB color for the text."""
    return (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))


def create_gradient_background(image):
    """Create a vibrant gradient background for the image."""
    draw = ImageDraw.Draw(image)
    color1 = generate_light_color()
    color2 = generate_light_color()
    background_colors = [color1, color2]

    for i in range(IMAGE_HEIGHT):
        ratio = i / IMAGE_HEIGHT
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        background_colors.append((r, g, b))
        draw.line([(0, i), (IMAGE_WIDTH, i)], fill=(r, g, b))

    return background_colors


def add_watermark(image):
    """Add a watermark and version text to the image."""
    try:
        watermark = Image.open(WATERMARK_PATH).convert("RGBA")
        watermark_width, watermark_height = watermark.size

        # Scale the watermark
        watermark = watermark.resize(
            (
                int(watermark_width * WATERMARK_SCALE),
                int(watermark_height * WATERMARK_SCALE),
            ),
            Image.Resampling.LANCZOS,
        )

        watermark_width, watermark_height = watermark.size
        image_width, image_height = image.size

        # Position the watermark with offset
        position = (
            image_width - watermark_width - WATERMARK_MARGIN,
            image_height - watermark_height - WATERMARK_MARGIN - WATERMARK_Y_OFFSET,
        )

        # Apply watermark
        transparent = Image.new("RGBA", image.size, (0, 0, 0, 0))
        transparent.paste(image.convert("RGBA"), (0, 0))
        transparent.paste(watermark, position, watermark)
        image = transparent.convert("RGB")

        # Add version text below the watermark
        draw = ImageDraw.Draw(image)
        try:
            version_font = ImageFont.truetype(FONT_PATH, VERSION_FONT_SIZE)
        except IOError:
            print(f"Font file {FONT_PATH} not found.")
            version_font = ImageFont.load_default()

        version_text = "v1.20"
        text_bbox = draw.textbbox((0, 0), version_text, font=version_font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        version_x = position[0] + (watermark_width - text_width) // 2
        version_y = position[1] + watermark_height + WATERMARK_MARGIN // 2

        draw.text((version_x, version_y), version_text, font=version_font, fill="black")

    except IOError:
        print(f"Watermark file {WATERMARK_PATH} not found.")
        pass

    return image


def draw_text(image, word):
    """Render Sinhala text using PIL and paste it onto the image."""
    draw = ImageDraw.Draw(image)

    # Load the font
    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except IOError:
        print(f"Font file {FONT_PATH} not found.")
        return image

    # Generate a dark text color
    text_color = generate_dark_color()

    # Calculate text position
    text_bbox = draw.textbbox((0, 0), word, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x_pos = (IMAGE_WIDTH - text_width) // 2
    y_pos = (IMAGE_HEIGHT - text_height) // 2

    # Render text in dark color
    draw.text((x_pos, y_pos), word, font=font, fill=text_color)

    return image


def create_image(word):
    """Create a high-resolution image with the given word in 16:9 aspect ratio."""
    # Ensure the image directory exists
    if not os.path.exists(IMAGE_DIRECTORY):
        os.makedirs(IMAGE_DIRECTORY)

    # Create a new image with a gradient background
    image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), "white")
    background_colors = create_gradient_background(image)

    # Render the text and paste it onto the image
    image = draw_text(image, word)

    # Add watermark and version text
    image = add_watermark(image)

    # Save the image as a JPEG file
    image_path = os.path.join(IMAGE_DIRECTORY, f"{word}.jpg")
    try:
        image.save(image_path, "JPEG", quality=95)
    except Exception as e:
        print(f"An error occurred while saving the image: {e}")
        return None

    return image_path
