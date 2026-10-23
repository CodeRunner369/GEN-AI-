"""
Sample Data & Presets Generator.
Provides ready-to-test construction site and defect surface images using Pillow.
"""

from PIL import Image, ImageDraw, ImageFont
import os
from typing import Dict

def create_synthetic_safety_image_1() -> Image.Image:
    """Generates a realistic construction site inspection scene with workers & scaffolding."""
    img = Image.new("RGB", (800, 550), color=(180, 195, 210))  # Sky/ambient background
    draw = ImageDraw.Draw(img)

    # Distant skyline / concrete structures
    draw.rectangle([0, 300, 800, 550], fill=(70, 75, 80))  # Concrete deck
    draw.rectangle([50, 100, 200, 450], fill=(100, 105, 115))  # Concrete shear wall
    draw.rectangle([600, 50, 750, 450], fill=(90, 95, 105))   # Column stack

    # Tower crane yellow jib across top
    draw.line([0, 70, 800, 70], fill=(245, 158, 11), width=10)
    draw.line([350, 0, 350, 300], fill=(245, 158, 11), width=12)  # Mast
    draw.line([350, 70, 480, 220], fill=(40, 40, 40), width=3)   # Cable

    # Tubular steel scaffolding grid
    for x in range(220, 580, 70):
        draw.line([x, 150, x, 450], fill=(160, 170, 180), width=4)
    for y in range(150, 480, 60):
        draw.line([220, y, 560, y], fill=(160, 170, 180), width=4)
        draw.line([220, y, 290, y+60], fill=(140, 150, 160), width=2)

    # Worker 1: Fully compliant (Yellow hard hat, Neon vest, Harness)
    # Head & Helmet
    draw.ellipse([270, 230, 295, 255], fill=(250, 204, 21))  # Yellow helmet
    draw.rectangle([268, 252, 297, 256], fill=(234, 179, 8))  # Helmet brim
    # Body with neon vest
    draw.rectangle([265, 256, 300, 310], fill=(234, 88, 12))  # Orange hi-vis vest
    draw.line([270, 270, 295, 270], fill=(254, 240, 138), width=3)  # Reflective stripe
    # Legs & Boots
    draw.rectangle([267, 310, 281, 360], fill=(30, 41, 59))  # Denim jeans
    draw.rectangle([284, 310, 298, 360], fill=(30, 41, 59))
    draw.rectangle([265, 355, 282, 368], fill=(60, 40, 20))  # Steel-toe boots
    draw.rectangle([283, 355, 300, 368], fill=(60, 40, 20))

    # Worker 2: High-vis vest, but VIOLATION (Missing helmet / cap only)
    draw.ellipse([420, 240, 442, 260], fill=(120, 50, 40))   # Brown hair / no helmet
    draw.rectangle([415, 260, 447, 315], fill=(234, 88, 12))  # Hi-vis vest
    draw.line([418, 275, 444, 275], fill=(254, 240, 138), width=3)
    draw.rectangle([417, 315, 430, 365], fill=(30, 41, 59))
    draw.rectangle([432, 315, 445, 365], fill=(30, 41, 59))
    draw.rectangle([415, 360, 431, 370], fill=(60, 40, 20))
    draw.rectangle([431, 360, 447, 370], fill=(60, 40, 20))

    # Worker 3 & 4 (Operating rebar area)
    draw.ellipse([140, 330, 160, 350], fill=(255, 255, 255)) # White supervisor helmet
    draw.rectangle([138, 350, 162, 395], fill=(34, 197, 94))  # Green safety vest
    draw.rectangle([139, 395, 150, 440], fill=(50, 50, 60))
    draw.rectangle([151, 395, 161, 440], fill=(50, 50, 60))

    # Starter bars / Rebar impalement hazard without caps
    for rx in range(480, 560, 12):
        draw.line([rx, 350, rx, 410], fill=(130, 90, 60), width=4)  # Exposed rusty rebars

    # Floor edge drop
    draw.line([50, 450, 750, 450], fill=(239, 68, 68), width=4)  # Floor boundary
    draw.text((60, 460), "[ZONE A-3] Superstructure Deck 14F - Inspection Stream", fill=(240, 240, 240))
    
    return img


def create_synthetic_crack_image_1() -> Image.Image:
    """Generates a realistic structural diagonal shear crack pattern on concrete."""
    img = Image.new("RGB", (800, 550), color=(165, 168, 172))  # Concrete gray
    draw = ImageDraw.Draw(img)

    # Concrete texture mottling
    for i in range(0, 800, 40):
        for j in range(0, 550, 40):
            val = 150 + ((i * 13 + j * 7) % 30)
            draw.rectangle([i, j, i+38, j+38], fill=(val, val+2, val-1))

    # Beam-Column Interface Lines
    draw.rectangle([0, 0, 800, 120], fill=(140, 142, 146))  # Heavy RC Beam Soffit
    draw.rectangle([520, 120, 800, 550], fill=(135, 138, 142)) # Column Face
    draw.line([0, 120, 800, 120], fill=(80, 80, 85), width=3)  # Beam soffit chamfer
    draw.line([520, 120, 520, 550], fill=(80, 80, 85), width=3) # Joint line

    # Prominent 45-degree diagonal shear fracture traversing beam-column intersection
    crack_points = [
        (180, 130), (220, 160), (280, 210), (330, 250), (390, 310), 
        (450, 370), (490, 410), (530, 440), (580, 480)
    ]
    # Draw dark inner crack fracture
    draw.line(crack_points, fill=(25, 25, 30), width=5)
    # Secondary splinter micro-cracks
    draw.line([(330, 250), (360, 230), (390, 220)], fill=(40, 40, 45), width=2)
    draw.line([(450, 370), (480, 360), (510, 345)], fill=(40, 40, 45), width=2)

    # Engineering Crack Width Gauge Card (Avongard style)
    draw.rectangle([100, 260, 210, 360], fill=(250, 250, 250), outline=(30, 30, 30), width=2)
    draw.text((110, 270), "STRUCTURAL GAUGE", fill=(20, 20, 20))
    draw.text((110, 290), "Width Scale: mm", fill=(50, 50, 50))
    draw.line([115, 310, 195, 310], fill=(239, 68, 68), width=3)
    draw.text((115, 320), "Aperture: ~2.4 mm", fill=(200, 30, 30))
    draw.text((115, 338), "IS 456 Limit: 0.3mm", fill=(60, 60, 60))

    return img


def create_synthetic_spalling_image() -> Image.Image:
    """Generates concrete spalling with exposed corroded reinforcement."""
    img = Image.new("RGB", (800, 550), color=(170, 172, 175))
    draw = ImageDraw.Draw(img)

    # Spalled pit cavity
    draw.ellipse([250, 140, 580, 420], fill=(110, 112, 115), outline=(70, 72, 75), width=4)

    # Exposed corroded rebar
    draw.line([320, 100, 320, 460], fill=(160, 65, 30), width=16)  # Rusty Rebar 1
    draw.line([430, 110, 430, 450], fill=(145, 55, 20), width=16)  # Rusty Rebar 2
    draw.line([510, 130, 510, 430], fill=(150, 60, 25), width=14)  # Rusty Rebar 3

    # Stirrup tie cross bars
    draw.line([270, 220, 560, 220], fill=(130, 50, 20), width=8)
    draw.line([280, 340, 550, 340], fill=(130, 50, 20), width=8)

    # Delamination spall tags
    draw.text((40, 490), "DEFECT: Concrete Cover Spalling & Carbonation-Induced Rebar Rusting", fill=(20, 20, 20))

    return img


def get_all_sample_presets() -> Dict[str, Image.Image]:
    """Returns dictionary of all preset sample images for instant testing."""
    return {
        "Site Scene 1: Active Deck & Scaffold (Mixed PPE)": create_synthetic_safety_image_1(),
        "Defect 1: RC Beam-Column Diagonal Shear Crack (2.4mm)": create_synthetic_crack_image_1(),
        "Defect 2: Concrete Spalling & Corroded Rebar": create_synthetic_spalling_image()
    }
