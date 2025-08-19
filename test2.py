from PIL import Image, ImageOps, ImageFilter

def high_fidelity_overlay(src_image_path, target_image_path, output_image_path):
    # Load the source image and convert to grayscale
    src_image = Image.open(src_image_path).convert("L")
    
    # Focus on the top third of the image
    src_width, src_height = src_image.size
    top_third = src_image.crop((0, 0, src_width, src_height // 3))
    
    # Apply Gaussian blur to reduce noise
    smoothed = top_third.filter(ImageFilter.GaussianBlur(radius=1))
    
    # Thresholding to isolate white writing in the top third
    # Simulating adaptive threshold by determining local maxima
    threshold = smoothed.point(lambda p: 255 if p > smoothed.getextrema()[1] * 0.9 else 0)

    # Apply a sharpening filter to enhance the text edges
    sharpened_mask = threshold.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

    # Load the target image
    target_image = Image.open(target_image_path)

    # Convert sharpened_mask to an RGBA image where white is replaced with transparent
    sharpened_mask = sharpened_mask.convert("L")
    white_text = ImageOps.colorize(sharpened_mask, "black", "white")
    white_text.putalpha(sharpened_mask)

    # Overlay the white writing onto the target image
    # Ensure the mask size matches the target image if necessary
    mask_width, mask_height = white_text.size
    target_width, target_height = target_image.size
    if mask_width != target_width:
        # Resize or extend the mask to cover the entire width of the target image
        new_mask = Image.new("RGBA", (target_width, mask_height))
        new_mask.paste(white_text, ((target_width - mask_width) // 2, 0))
        white_text = new_mask

    # Paste the white text onto the target image, preserving the original background
    target_image.paste(white_text, (0, 0), white_text)
    target_image.save(output_image_path)

# Uncomment to test the function with actual file paths
high_fidelity_overlay("image1.jpg", "image2.jpg", "output_image.jpg")
