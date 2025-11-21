"""
Script to generate the statistics meme by running all steps in sequence.
"""

from step1_prepare_image import prepare_image
from step2_create_stipple import create_stipple
from step4_create_block_letter import create_block_letter_s
from step5_create_masked import create_masked_stipple
from create_meme import create_statistics_meme

# Step 1: Prepare the image
print("=" * 60)
print("Step 1: Preparing image...")
print("=" * 60)
img_path = 'vikramgoyal2.jpeg'  # Change this to your image file
gray_image = prepare_image(img_path, max_size=512)
print(f"Prepared image shape: {gray_image.shape}\n")

# Step 2: Create stippled image
print("=" * 60)
print("Step 2: Creating stippled image...")
print("=" * 60)
stipple_pattern, samples = create_stipple(
    gray_image,
    percentage=0.08,
    sigma=0.9,
    content_bias=0.9
)
print(f"Stipple pattern shape: {stipple_pattern.shape}\n")

# Step 4: Create block letter
print("=" * 60)
print("Step 4: Creating block letter...")
print("=" * 60)
h, w = gray_image.shape
block_letter = create_block_letter_s(
    height=h,
    width=w,
    letter="S",
    font_size_ratio=0.9
)
print(f"Block letter shape: {block_letter.shape}\n")

# Step 5: Create masked stipple
print("=" * 60)
print("Step 5: Creating masked stipple...")
print("=" * 60)
masked_stipple = create_masked_stipple(
    stipple_img=stipple_pattern,
    mask_img=block_letter,
    threshold=0.5
)
print(f"Masked stipple shape: {masked_stipple.shape}\n")

# Final: Create the statistics meme
print("=" * 60)
print("Creating final statistics meme...")
print("=" * 60)
create_statistics_meme(
    original_img=gray_image,
    stipple_img=stipple_pattern,
    block_letter_img=block_letter,
    masked_stipple_img=masked_stipple,
    output_path="statistics_meme.png",
    dpi=150,
    background_color="white"
)

print("\n" + "=" * 60)
print("✅ Statistics meme generated successfully!")
print("=" * 60)
print(f"Output file: statistics_meme.png")

