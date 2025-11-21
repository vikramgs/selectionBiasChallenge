"""
Step 5: Create a masked stipple image.
Applies a block letter mask to the stippled image, removing stipples in the mask area
to create a "biased estimate" by systematically removing data points.
"""

import numpy as np


def create_masked_stipple(
    stipple_img: np.ndarray,
    mask_img: np.ndarray,
    threshold: float = 0.5
) -> np.ndarray:
    """
    Apply a block letter mask to a stippled image, removing stipples in the mask area.
    
    This creates a "biased estimate" by systematically removing data points where
    the mask is dark (the letter area), while keeping stipples where the mask is
    light (the background area).
    
    Parameters
    ----------
    stipple_img : np.ndarray
        Stippled image as 2D array (height, width) with values in [0, 1]
        - 0.0 represents black stipple dots
        - 1.0 represents white background
    mask_img : np.ndarray
        Mask image as 2D array (height, width) with values in [0, 1]
        - 0.0 represents black (mask area - where stipples will be removed)
        - 1.0 represents white (keep area - where stipples will be preserved)
    threshold : float
        Threshold value to determine what counts as "part of the mask".
        Pixels with mask value < threshold are considered mask area (remove stipples).
        Pixels with mask value >= threshold are considered keep area (preserve stipples).
        Default 0.5.
    
    Returns
    -------
    masked_stipple : np.ndarray
        2D numpy array (height, width) with values in [0, 1]
        - Same shape as input images
        - Where mask is dark (below threshold): stipples removed (set to 1.0/white)
        - Where mask is light (above threshold): stipples preserved as they were
    """
    # Validate that input images have the same shape
    if stipple_img.shape != mask_img.shape:
        raise ValueError(
            f"Input images must have the same shape. "
            f"stipple_img shape: {stipple_img.shape}, mask_img shape: {mask_img.shape}"
        )
    
    # Create a copy of the stipple image to avoid modifying the original
    masked_stipple = stipple_img.copy()
    
    # Apply the mask: where mask is dark (below threshold), remove stipples (set to white/1.0)
    # Where mask is light (above threshold), keep the stipples as they are
    mask_area = mask_img < threshold
    
    # Remove stipples in the mask area by setting those pixels to white (1.0)
    masked_stipple[mask_area] = 1.0
    
    # Count statistics for reporting
    num_removed = np.sum(mask_area)
    num_preserved = np.sum(~mask_area)
    total_pixels = mask_img.size
    
    print(f"Applied mask to stipple image")
    print(f"Mask threshold: {threshold}")
    print(f"Pixels in mask area (stipples removed): {num_removed} ({100*num_removed/total_pixels:.1f}%)")
    print(f"Pixels in keep area (stipples preserved): {num_preserved} ({100*num_preserved/total_pixels:.1f}%)")
    
    return masked_stipple

