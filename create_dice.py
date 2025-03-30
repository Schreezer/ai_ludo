from PIL import Image, ImageDraw, ImageFont
import os

def create_dice_image(number, size=(33, 33)):
    # Create a white image
    image = Image.new('RGB', size, 'white')
    draw = ImageDraw.Draw(image)
    
    # Draw black border
    draw.rectangle([(0, 0), (size[0]-1, size[1]-1)], outline='black')
    
    # Add number in center
    # Use a basic font since we may not have access to specific fonts
    font_size = size[0] // 2
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        font = ImageFont.load_default()
    
    # Get text size
    text = str(number)
    try:
        text_width = font.getlength(text)
    except:
        text_width = font_size // 2
    text_height = font_size
    
    # Calculate position to center the text
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Draw the number
    draw.text((x, y), text, fill='black', font=font)
    
    return image

# Create dice images
for i in range(1, 7):
    img = create_dice_image(i)
    img.save(f'images/Dice_{i}.jpg')

print("Dice images created successfully!")
