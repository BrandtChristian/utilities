import whisper
import os
from tkinter import filedialog, Tk, simpledialog, StringVar, OptionMenu, Label, Button, Toplevel, messagebox

def transcribe_audio(input_file, output_file, model_size="base", language="en"):
    """
    Transcribe audio using Whisper model and save the transcription with proper sentence breaks in plain text.

    Args:
    input_file (str): Path to the input audio/video file.
    output_file (str): Path to the output transcription file.
    model_size (str): Size of the Whisper model to use. Default is "base".
    language (str): Language of the audio. Default is "en" (English).
    """
    try:
        # Check if the model is available or needs to be downloaded
        if not whisper.is_model_downloaded(model_size):
            user_response = messagebox.askyesno(
                "Model Download",
                f"The model '{model_size}' is not available locally. Do you want to download it? This may take some time."
            )
            if not user_response:
                print("Model download canceled by user. Exiting.")
                return

        # Load the model
        model = whisper.load_model(model_size)

        # Load and transcribe the audio
        result = model.transcribe(input_file, verbose=True, language=language)

        # Format and save the transcription
        format_and_save_transcription(result, output_file)
        print(f"Transcription saved to {output_file}")

    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def format_and_save_transcription(result, output_file):
    """
    Format and save the transcription result to a plain text file with proper sentence breaks.

    Args:
    result (dict): The transcription result from Whisper.
    output_file (str): Path to the output transcription file.
    """
    segments = result['segments']

    with open(output_file, "w", encoding="utf-8") as f:
        for segment in segments:
            text = segment['text'].strip()
            f.write(f"{text}\n\n")

if __name__ == "__main__":
    # Hide the main Tkinter window
    root = Tk()
    root.withdraw()

    # Prompt user to select the input audio/video file
    input_audio_file = filedialog.askopenfilename(
        title="Select Audio/Video File",
        filetypes=[("Audio/Video files", "*.mp3 *.wav *.m4a *.flac *.mp4 *.mkv *.mov *.avi")]
    )
    if not input_audio_file:
        print("No file selected. Exiting.")
        exit()

    # Prompt user to select the output directory and filename
    output_directory = filedialog.askdirectory(title="Select Output Directory")
    if not output_directory:
        print("No output directory selected. Exiting.")
        exit()

    output_filename = simpledialog.askstring("Output Filename", "Enter the output filename (without extension):")
    if not output_filename:
        print("No output filename provided. Exiting.")
        exit()

    output_transcription_file = os.path.join(output_directory, f"{output_filename}.txt")

    # Model size options and default value
    model_options = ["tiny", "base", "small", "medium", "large"]
    model_explanation = (
        "Select the model size:\n"
        " - tiny: Fastest, least accurate\n"
        " - base: Fast, good accuracy\n"
        " - small: Balanced speed and accuracy\n"
        " - medium: Slow, high accuracy\n"
        " - large: Slowest, highest accuracy\n"
    )
    model_size_var = StringVar(root)
    model_size_var.set("base")  # default value

    # Language options and default value
    language_options = ["en", "lt", "fr", "de", "es", "it", "pt", "nl", "da"]
    language_var = StringVar(root)
    language_var.set("en")  # default value

    # Create and display dropdown menus for model size and language
    model_size_dialog = Toplevel(root)
    model_size_dialog.title("Select Model Size and Language")

    Label(model_size_dialog, text=model_explanation).pack()

    Label(model_size_dialog, text="Model Size:").pack()
    OptionMenu(model_size_dialog, model_size_var, *model_options).pack()

    Label(model_size_dialog, text="Language:").pack()
    OptionMenu(model_size_dialog, language_var, *language_options).pack()

    def proceed():
        model_size_dialog.destroy()
        transcribe_audio(input_audio_file, output_transcription_file, model_size_var.get(), language_var.get())

    Button(model_size_dialog, text="Proceed", command=proceed).pack()

    model_size_dialog.mainloop()
