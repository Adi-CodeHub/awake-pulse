from PIL import Image, ImageDraw

def create_awake_icon(output_ico="icon.ico", output_png="icon.png"):
    size = (256, 256)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Outer soft glow circle (Dark Slate Cyan/Indigo)
    draw.ellipse([8, 8, 248, 248], fill="#0F172A", outline="#38BDF8", width=8)

    # Inner circular background
    draw.ellipse([24, 24, 232, 232], fill="#1E293B")

    # Vibrant Lightning Bolt / Energy Pulse shape
    # Points creating a sharp electric bolt
    bolt_points = [
        (135, 45),   # Top point
        (85, 135),   # Left middle
        (130, 135),  # Inner right
        (115, 210),  # Bottom sharp tip
        (175, 115),  # Right middle
        (130, 115),  # Inner left
    ]
    
    # Outer glow of the bolt
    glow_color = "#38BDF8"  # Cyan glow
    draw.polygon(bolt_points, fill="#0284C7")

    # Center vibrant highlight of bolt (Electric Emerald / Amber shine)
    inner_bolt = [
        (135, 52),
        (92, 133),
        (132, 133),
        (120, 200),
        (170, 117),
        (132, 117),
    ]
    draw.polygon(inner_bolt, fill="#38BDF8")

    # Little dot highlight at bottom
    draw.ellipse([124, 215, 132, 223], fill="#38BDF8")

    # Save PNG
    img.save(output_png)

    # Save multi-resolution Windows ICO file (16x16, 32x32, 48x48, 64x64, 128x128, 256x256)
    img.save(
        output_ico,
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    )
    print("Icon generated successfully as icon.ico and icon.png!")

if __name__ == "__main__":
    create_awake_icon()
