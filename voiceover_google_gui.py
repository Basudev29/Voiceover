import os
import tempfile

from gtts import gTTS
from pydub import AudioSegment
from playsound import playsound

import tkinter as tk
from tkinter import (
    Tk,
    Label,
    Text,
    Button,
    StringVar,
    filedialog,
    messagebox,
    Frame,
    Scale,
    DoubleVar,
    END,
)

# ------------ Global state ------------

bg_music_path = ""
ACTIVE_BG = "#4CAF50"
ACTIVE_FG = "white"
NORMAL_BG = "#E0E0E0"
NORMAL_FG = "black"


def generate_voiceover():
    """Main function: text → TTS → optional BG music → save & play."""
    text = text_input.get("1.0", END).strip()
    lang = lang_var.get()

    if not text:
        status_label.config(text="Please enter some text!", fg="red")
        return

    try:
        # Step 1: Generate raw voice TTS in temp file
        tts = gTTS(text=text, lang=lang)
        tmp_voice = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp_voice.name)

        final_audio = tmp_voice.name

        # Step 2: If background music selected, mix
        if bg_music_path:
            try:
                bg_music = AudioSegment.from_file(bg_music_path)
                voice = AudioSegment.from_file(tmp_voice.name)

                # Apply BG volume
                bg_gain = bg_volume.get()
                bg_music = bg_music.apply_gain(bg_gain)

                # Ensure music length ≥ voice length
                if len(bg_music) < len(voice):
                    repeat = len(voice) // len(bg_music) + 1
                    bg_music = bg_music * repeat

                combined = voice.overlay(bg_music[: len(voice)])

                # Save combined to another temp file
                tmp_combined = tempfile.NamedTemporaryFile(
                    delete=False, suffix=".mp3"
                )
                combined.export(tmp_combined.name, format="mp3")
                final_audio = tmp_combined.name

            except Exception as e:
                messagebox.showerror(
                    "Error", f"Background music mixing failed: {str(e)}"
                )

        # Step 3: Ask user where to save
        file_path = filedialog.asksaveasfilename(
            defaultextension=".mp3",
            filetypes=[("MP3 files", "*.mp3")],
            title="Save Voiceover As",
        )

        if file_path:
            # Export final audio
            audio_segment = AudioSegment.from_file(final_audio)
            audio_segment.export(file_path, format="mp3")

            status_label.config(text=f"Voiceover saved: {file_path}", fg="green")

            # Play the generated voice
            try:
                playsound(file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Unable to play audio: {str(e)}")
        else:
            status_label.config(text="Save cancelled.", fg="orange")

    except Exception as e:
        status_label.config(text=f"Error: {str(e)}", fg="red")
        messagebox.showerror("Error", str(e))

    finally:
        # Clean temp voice file
        try:
            if os.path.exists(tmp_voice.name):
                os.remove(tmp_voice.name)
        except Exception:
            pass


def select_bg_music():
    """Let user select optional background music file."""
    global bg_music_path
    path = filedialog.askopenfilename(
        title="Select Background Music",
        filetypes=(("MP3 files", "*.mp3"), ("All files", "*.*")),
    )
    if path:
        bg_music_path = path
        bg_label.config(text=os.path.basename(bg_music_path))
        status_label.config(text="Background music selected.", fg="green")
    else:
        bg_music_path = ""
        bg_label.config(text="No music selected")
        status_label.config(text="No background music.", fg="orange")


def update_language(lang):
    """Update selected language and button styles."""
    lang_var.set(lang)

    # Reset style
    hindi_btn.config(bg=NORMAL_BG, fg=NORMAL_FG, relief="raised")
    english_btn.config(bg=NORMAL_BG, fg=NORMAL_FG, relief="raised")

    # Highlight active
    if lang == "hi":
        hindi_btn.config(bg=ACTIVE_BG, fg=ACTIVE_FG, relief="sunken")
    else:
        english_btn.config(bg=ACTIVE_BG, fg=ACTIVE_FG, relief="sunken")


# ------------ GUI setup ------------

root = Tk()
root.title("Google TTS Voiceover Generator")
root.geometry("550x500")

# Text input
Label(root, text="Enter Text:", font=("Arial", 11, "bold")).pack(pady=5)
text_input = Text(root, height=10, width=60)
text_input.pack(pady=5)

# Language selection
Label(root, text="Select Language", font=("Arial", 12, "bold")).pack(pady=10)

btn_frame = Frame(root)
btn_frame.pack(pady=5)

lang_var = StringVar(value="hi")

hindi_btn = Button(
    btn_frame,
    text="Hindi",
    width=12,
    command=lambda: update_language("hi"),
)
hindi_btn.grid(row=0, column=0, padx=10, pady=5)

english_btn = Button(
    btn_frame,
    text="English",
    width=12,
    command=lambda: update_language("en"),
)
english_btn.grid(row=0, column=1, padx=10, pady=5)

# Background music selection
Button(
    root,
    text="Select Background Music (Optional)",
    command=select_bg_music,
).pack(pady=10)

bg_label = Label(root, text="No music selected")
bg_label.pack()

# Background Music Volume Control
Label(root, text="Background Music Volume (dB)").pack(pady=5)
bg_volume = DoubleVar(value=-10)
volume_slider = Scale(
    root,
    from_=-30,
    to=10,
    orient="horizontal",
    variable=bg_volume,
    length=300,
)
volume_slider.pack()

# Generate button
Button(
    root,
    text="Generate Voiceover",
    font=("Arial", 11, "bold"),
    command=generate_voiceover,
    bg="#2196F3",
    fg="white",
).pack(pady=15)

# Status label
status_label = Label(root, text="", fg="green")
status_label.pack(pady=10)

# Default language highlight
update_language("hi")

root.mainloop()
