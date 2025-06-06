#!/usr/bin/env python3

from PIL import Image
import os

def convert_jpg_to_png(input_file, output_file):
    try:
        if not os.path.exists(input_file):
            print(f"Error: Input file {input_file} not found")
            return False
            
        img = Image.open(input_file)
        img.save(output_file, "PNG")
        print(f"Successfully converted {input_file} to {output_file}")
        return True
    except Exception as e:
        print(f"Error converting image: {e}")
        return False

if __name__ == "__main__":
    input_file = "ICON_dashboard-editor.jpg"
    output_file = "startup-dashboard-editor.png"
    convert_jpg_to_png(input_file, output_file)

