"""
Create Statistics Meme: Assemble four panels into a professional meme.
Combines the original image, stippled image, block letter mask, and masked stipple
into a 1×4 layout demonstrating selection bias.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def create_statistics_meme(
    original_img: np.ndarray,
    stipple_img: np.ndarray,
    block_letter_img: np.ndarray,
    masked_stipple_img: np.ndarray,
    output_path: str,
    dpi: int = 150,
    background_color: str = "white"
) -> None:
    """
    Assemble all four panels into a professional-looking statistics meme.
    
    Creates a 1×4 layout (four panels side by side) with labels:
    - "Reality": Original image
    - "Your Model": Stippled image
    - "Selection Bias": Block letter mask
    - "Estimate": Masked stipple image
    
    Parameters
    ----------
    original_img : np.ndarray
        2D array (height, width) with values in [0, 1] - original grayscale image
    stipple_img : np.ndarray
        2D array (height, width) with values in [0, 1] - stippled version
    block_letter_img : np.ndarray
        2D array (height, width) with values in [0, 1] - block letter mask
    masked_stipple_img : np.ndarray
        2D array (height, width) with values in [0, 1] - masked stipple result
    output_path : str
        Path where the final meme PNG will be saved
    dpi : int
        Resolution (dots per inch) for the output image. Default 150.
        Use 150-300 for publication quality.
    background_color : str
        Background color for the figure. Default "white".
    
    Returns
    -------
    None
        Saves the meme as a PNG file at output_path.
    """
    # Get image dimensions
    h, w = original_img.shape
    
    # Ensure all images have the same dimensions
    images = [original_img, stipple_img, block_letter_img, masked_stipple_img]
    labels = ["Reality", "Your Model", "Selection Bias", "Estimate"]
    
    # Check and resize if necessary
    for i, img in enumerate(images):
        if img.shape != (h, w):
            print(f"Warning: Image {i} ({labels[i]}) has shape {img.shape}, "
                  f"expected {(h, w)}. Resizing...")
            from PIL import Image
            img_pil = Image.fromarray((img * 255).astype(np.uint8))
            img_pil = img_pil.resize((w, h), Image.Resampling.LANCZOS)
            images[i] = np.array(img_pil, dtype=np.float32) / 255.0
    
    # Create figure with 1×4 layout
    # Use a wider figure to accommodate 4 panels side by side
    fig_width = 16  # inches
    fig_height = 4  # inches
    
    fig = plt.figure(figsize=(fig_width, fig_height), facecolor=background_color)
    gs = gridspec.GridSpec(1, 4, figure=fig, 
                          left=0.02, right=0.98, 
                          top=0.92, bottom=0.08,
                          wspace=0.05, hspace=0.1)
    
    # Plot each panel
    for i, (img, label) in enumerate(zip(images, labels)):
        ax = fig.add_subplot(gs[0, i])
        
        # Display the image
        ax.imshow(img, cmap='gray', vmin=0, vmax=1, aspect='auto')
        
        # Remove axes ticks and labels for clean look
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Add border around each panel
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_edgecolor('black')
            spine.set_linewidth(2)
        
        # Add label above the panel
        ax.text(0.5, 1.05, label, 
                transform=ax.transAxes,
                fontsize=16,
                fontweight='bold',
                ha='center',
                va='bottom',
                color='black')
    
    # Add overall title (optional - can be removed if not needed)
    # fig.suptitle('Selection Bias Visualization', 
    #              fontsize=20, fontweight='bold', y=0.98)
    
    # Save the figure
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight', 
                facecolor=background_color, edgecolor='none')
    plt.close()
    
    print(f"Statistics meme saved to: {output_path}")
    print(f"Image dimensions: {fig_width}×{fig_height} inches at {dpi} DPI")
    print(f"Output resolution: {int(fig_width * dpi)}×{int(fig_height * dpi)} pixels")

