"""
Step 4: Create a block letter image.
Generates a block letter (default "S") on a white background with specified dimensions.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def create_block_letter_s(
    height: int,
    width: int,
    letter: str = "S",
    font_size_ratio: float = 0.9
) -> np.ndarray:
    """
    Generate a block letter image matching the specified dimensions.
    
    Parameters
    ----------
    height : int
        Height of the output image in pixels
    width : int
        Width of the output image in pixels
    letter : str
        The letter to render. Default "S".
    font_size_ratio : float
        Ratio of font size to the smaller dimension (height or width).
        Controls how large the letter appears. Default 0.9.
    
    Returns
    -------
    img_array : np.ndarray
        2D numpy array (height, width) with values in [0, 1]
        - 0.0 represents black (the letter)
        - 1.0 represents white (background)
    """
    # Create a white background image
    img = Image.new('L', (width, height), color=255)
    draw = ImageDraw.Draw(img)
    
    # Calculate font size based on the smaller dimension
    min_dimension = min(height, width)
    font_size = int(min_dimension * font_size_ratio)
    
    # Try to use a bold/block font, fallback to default if not available
    try:
        # Try to load a bold system font
        # On macOS, try Arial Bold or Helvetica Bold
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", font_size)
    except (OSError, IOError):
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        except (OSError, IOError):
            try:
                # Try a common Linux font path
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except (OSError, IOError):
                # Fallback to default font
                font = ImageFont.load_default()
                # Scale default font if possible
                if hasattr(font, 'size'):
                    # Default font is small, so we'll use textbbox to estimate and scale
                    pass
    
    # Get text bounding box to center the letter
    # Use textbbox for accurate measurement (available in Pillow 8.0.0+)
    try:
        bbox = draw.textbbox((0, 0), letter, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        # Calculate position to center the text
        x = (width - text_width) // 2 - bbox[0]
        y = (height - text_height) // 2 - bbox[1]
    except AttributeError:
        # Fallback for older PIL versions that don't have textbbox
        # Use textsize (deprecated but available in older versions)
        try:
            text_width, text_height = draw.textsize(letter, font=font)
            x = (width - text_width) // 2
            y = (height - text_height) // 2
        except AttributeError:
            # Ultimate fallback: approximate centering
            x = width // 2
            y = height // 2
    
    # Draw the letter in black (0)
    draw.text((x, y), letter, fill=0, font=font)
    
    # Convert PIL image to numpy array and normalize to [0, 1]
    img_array = np.array(img, dtype=np.float32) / 255.0
    
    # Invert so that 0.0 is black (letter) and 1.0 is white (background)
    # Since we drew black (0) on white (255), after normalization:
    # - Black pixels become 0.0
    # - White pixels become 1.0
    # This is already what we want, so no inversion needed
    
    return img_array

