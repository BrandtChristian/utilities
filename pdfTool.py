from tkinter import filedialog, messagebox, Tk, Button, Label, Toplevel
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import fitz  # PyMuPDF

def merge_pdfs():
    files = filedialog.askopenfilenames(
        title="Select PDFs to merge",
        filetypes=[("PDF files", "*.pdf")]
    )
    if files:
        output = filedialog.asksaveasfilename(
            title="Where should the new file be saved?",
            filetypes=[("PDF files", "*.pdf")],
            defaultextension=".pdf"
        )
        if output:
            merger = PdfMerger()
            for pdf in files:
                merger.append(pdf)
            merger.write(output)
            merger.close()
            messagebox.showinfo("Success", "PDFs merged successfully into " + output)
        else:
            messagebox.showinfo("Cancelled", "Operation Cancelled")

def split_pdf():
    file = filedialog.askopenfilename(
        title="Select PDF to split",
        filetypes=[("PDF files", "*.pdf")]
    )
    if file:
        output_dir = filedialog.askdirectory(title="Select output directory")
        if output_dir:
            reader = PdfReader(file)
            for page_num in range(len(reader.pages)):
                writer = PdfWriter()
                writer.add_page(reader.pages[page_num])
                output = f"{output_dir}/page_{page_num + 1}.pdf"
                with open(output, "wb") as out_file:
                    writer.write(out_file)
            messagebox.showinfo("Success", f"PDF split into {len(reader.pages)} pages in {output_dir}")
        else:
            messagebox.showinfo("Cancelled", "Operation Cancelled")

def extract_text():
    file = filedialog.askopenfilename(
        title="Select PDF to extract text from",
        filetypes=[("PDF files", "*.pdf")]
    )
    if file:
        output = filedialog.asksaveasfilename(
            title="Where should the extracted text be saved?",
            defaultextension=".txt"
        )
        if output:
            reader = PdfReader(file)
            with open(output, "w", encoding="utf-8") as out_file:
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        out_file.write(text)
            messagebox.showinfo("Success", "Text extracted successfully into " + output)
        else:
            messagebox.showinfo("Cancelled", "Operation Cancelled")

def extract_images():
    file = filedialog.askopenfilename(
        title="Select PDF to extract images from",
        filetypes=[("PDF files", "*.pdf")]
    )
    if file:
        output_dir = filedialog.askdirectory(title="Select output directory")
        if output_dir:
            doc = fitz.open(file)
            for i in range(len(doc)):
                for img in doc.get_page_images(i):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    image_path = f"{output_dir}/image_page_{i + 1}_{xref}.{image_ext}"
                    with open(image_path, "wb") as img_file:
                        img_file.write(image_bytes)
            messagebox.showinfo("Success", f"Images extracted successfully into {output_dir}")
        else:
            messagebox.showinfo("Cancelled", "Operation Cancelled")

def main_menu():
    # Hide the main Tkinter window
    root = Tk()
    root.withdraw()

    menu_dialog = Toplevel(root)
    menu_dialog.title("PDF Tool Menu")

    Label(menu_dialog, text="Select an operation:").pack()

    Button(menu_dialog, text="Merge PDFs", command=lambda: [menu_dialog.destroy(), merge_pdfs()]).pack(pady=5)
    Button(menu_dialog, text="Split PDF", command=lambda: [menu_dialog.destroy(), split_pdf()]).pack(pady=5)
    Button(menu_dialog, text="Extract Text from PDF", command=lambda: [menu_dialog.destroy(), extract_text()]).pack(pady=5)
    Button(menu_dialog, text="Extract Images from PDF", command=lambda: [menu_dialog.destroy(), extract_images()]).pack(pady=5)

    menu_dialog.mainloop()

if __name__ == "__main__":
    main_menu()
