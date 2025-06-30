from PIL import Image

# Image dimensions
width = 1000
height = 88

# Color and transparency settings
start_color = (0, 109, 99)  # RGB
transparency_factor = 1   # Max opacity at the left side

# Create a new transparent image
gradient_image = Image.new('RGBA', (width, height))

# Generate the left-to-right fade
for x in range(width):
    fade_progress = x / width
    alpha = int(255 * (1 - fade_progress) * transparency_factor)

    r, g, b = start_color
    for y in range(height):
        gradient_image.putpixel((x, y), (r, g, b, alpha))

# Save the image
gradient_image.save("pdf_gradient_bar_horizontal_fade_left_to_right.png")
print("Image saved as pdf_gradient_bar_horizontal_fade_left_to_right.png")