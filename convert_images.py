"""
convert_images.py

This script allows users to convert multiple image files to a selected output format
using a graphical user interface. Users can select the input files, choose the output
directory, and specify the desired output format from a predefined list (PNG, JPEG, BMP, GIF, TIFF).

Usage:
1. Run the script.
2. Select the images you want to convert.
3. Choose the directory where the converted images will be saved.
4. Select the desired output format from the dropdown menu.
5. Click the "Proceed" button to start the conversion.

The script uses the following libraries:
- tkinter: For the graphical user interface
- PIL (Pillow): For image processing

Author: Christian Brandt
Date: 2024-05-22
"""

from tkinter import filedialog, messagebox, Tk, simpledialog
from tkinter import Toplevel, Label, Button, StringVar, OptionMenu
import os
from PIL import Image

def convert_images():
    """Main function to handle the image conversion process."""
    # Hide the main Tkinter window
    root = Tk()
    root.withdraw()

    try:
        # Select image files to convert
        files = filedialog.askopenfilenames(
            title="Select Images to convert",
            filetypes=[("Image files", "*.jpeg *.jpg *.bmp *.gif *.tiff *.png")]
        )
        if not files:
            messagebox.showinfo("Cancelled", "No files selected")
            return

        # Select the output directory
        output_dir = filedialog.askdirectory(title="Where should the new files be saved?")
        if not output_dir:
            messagebox.showinfo("Cancelled", "Operation Cancelled")
            return

        # Create a top-level window for format selection
        options_window = Toplevel(root)
        options_window.title("Select Output Format")

        # Format options
        format_label = Label(options_window, text="Select output format:")
        format_label.pack()
        
        formats = ["PNG", "JPEG", "BMP", "GIF", "TIFF"]
        selected_format = StringVar(options_window)
        selected_format.set(formats[0])  # Default value

        format_menu = OptionMenu(options_window, selected_format, *formats)
        format_menu.pack()

        # Proceed button
        def proceed():
            options_window.destroy()
            process_images(files, output_dir, selected_format.get())

        proceed_button = Button(options_window, text="Proceed", command=proceed)
        proceed_button.pack()

        options_window.mainloop()

    except Exception as e:
        print(f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

def process_images(files, output_dir, output_format):
    """Function to process and convert the images."""
    for file_path in files:
        try:
            im = Image.open(file_path)
            # Set the output path
            output_path = os.path.join(output_dir, os.path.splitext(os.path.basename(file_path))[0] + '.' + output_format.lower())
            im.save(output_path, output_format.upper())
            print(f"Converted {file_path} to {output_path}")
        except Exception as e:
            print(f"Failed to convert {file_path}: {e}")
            messagebox.showerror("Error", f"Failed to convert {file_path}: {e}")

    messagebox.showinfo("Success", "Images converted and saved to " + output_dir)

if __name__ == "__main__":
    convert_images()
