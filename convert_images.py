from tkinter import filedialog, messagebox, Tk, simpledialog
from tkinter import Toplevel, Label, Button, StringVar, OptionMenu
import os
from PIL import Image

def convert_images():
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
