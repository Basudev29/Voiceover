import os
from gtts import gTTS
from tkinter import Tk, Label, Text, Button, StringVar, OptionMenu, END, filedialog, messagebox, Frame, Scale, DoubleVar
from pydub import AudioSegment
from playsound import playsound
import tempfile

# Function to generate voiceover
def generate_voiceover():
    text = text_input.get("1.0", END).strip()
    language = lang_var.get()

    if not text:
        status_label.config(text="Please enter some text!", fg="red")
        return
    
    lang = lang_var.get()
    try:
        # Generate TTS
        tts = gTTS(text=text, lang=lang)
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp_file.name)
        
        # If background music is selected, combine
        if bg_music_path:
            bg_music = AudioSegment.from_file(bg_music_path)
            voice = AudioSegment.from_file(tmp_file.name)
            
            # adjust bg volume using slider
            bg_music = bg_music.apply_gain(bg_volume.get())
            # match length
            if len(bg_music) < len(voice):
                bg_music = bg_music * (len(voice) // len(bg_music) + 1)

            combined = voice.overlay(bg_music[:len(voice)])
        else:
            combined = AudioSegment.from_file(tmp_file.name)
        # Save output
        output_file = filedialog.asksaveasfilename(defaultextension=".mp3",
                                                   filetypes=[("MP3 files", "*.mp3")])
        if output_file:
            combined.export(output_file, format="mp3")
            messagebox.showinfo("Success", f"Voiceover saved as {output_file}")

        tmp_file.close()
        os.remove(tmp_file.name)

    except Exception as e:
        messagebox.showerror("Error", str(e))

        # Ask user to save file
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3",
                                                 filetypes=[("MP3 files", "*.mp3")])
        if file_path:
            tts.save(file_path)
            status_label.config(text=f"Voiceover saved: {file_path}", fg="green")
            # Play the generated voice
            playsound(file_path)
        else:
            status_label.config(text="Save cancelled.", fg="orange")

    except Exception as e:
        status_label.config(text=f"Error: {str(e)}", fg="red")

# Create GUI window
root = Tk()
root.title("Google TTS Voiceover Generator")
root.geometry("500x400")

# Text input
Label(root, text="Enter Text:").pack(pady=5)
text_input = Text(root, height=10, width=50)
text_input.pack(pady=5)

# Language selection
lang_var = StringVar(value="hi")  # Default Hindi
Button(root, text="Hindi", command=lambda: lang_var.set("hi")).pack()
Button(root, text="English", command=lambda: lang_var.set("en")).pack()

def update_language(lang):
    lang_var.set(lang)

    # Reset all buttons style
    hindi_btn.config(bg=NORMAL_BG, fg=NORMAL_FG, relief="raised")
    english_btn.config(bg=NORMAL_BG, fg=NORMAL_FG, relief="raised")

    # Highlight selected button
    if lang == "hi":
        hindi_btn.config(bg=ACTIVE_BG, fg=ACTIVE_FG, relief="sunken")
    else:
        english_btn.config(bg=ACTIVE_BG, fg=ACTIVE_FG, relief="sunken")
        



# Background music selection
bg_music_path = ""
def select_bg_music():
    global bg_music_path
    bg_music_path = filedialog.askopenfilename(title="Select Background Music",
                                               filetypes=(("MP3 files", "*.mp3"), ("All files", "*.*")))
    if bg_music_path:
        bg_label.config(text=os.path.basename(bg_music_path))

Button(root, text="Select Background Music (Optional)", command=select_bg_music).pack()
bg_label = Label(root, text="No music selected")
bg_label.pack()

# --- Background Music Volume Control ---
Label(root, text="Background Music Volume").pack(pady=5)

bg_volume = DoubleVar(value=-10)   # default lower volume

volume_slider = Scale(
    root,
    from_=-30,
    to=10,
    orient="horizontal",
    variable=bg_volume
)
volume_slider.pack()


# Generate button
Label(root, text="Select Language", font=("Arial", 12, "bold")).pack(pady=10)

btn_frame = Frame(root)
btn_frame.pack(pady=10)

# ---------- COLORS ----------
ACTIVE_BG = "#4CAF50"
ACTIVE_FG = "white"
NORMAL_BG = "#E0E0E0"
NORMAL_FG = "black"

lang_var = StringVar(value="hi")

def update_language(lang):
    lang_var.set(lang)

    # Reset style
    hindi_btn.config(bg=NORMAL_BG, fg=NORMAL_FG, relief="raised")
    english_btn.config(bg=NORMAL_BG, fg=NORMAL_FG, relief="raised")

    # Highlight active
    if lang == "hi":
        hindi_btn.config(bg=ACTIVE_BG, fg=ACTIVE_FG, relief="sunken")
    else:
        english_btn.config(bg=ACTIVE_BG, fg=ACTIVE_FG, relief="sunken")

hindi_btn = Button(
    btn_frame,
    text="Hindi",
    width=12,
    command=lambda: update_language("hi")
)
hindi_btn.grid(row=0, column=0, padx=10, pady=5)

english_btn = Button(
    btn_frame,
    text="English",
    width=12,
    command=lambda: update_language("en")
)
english_btn.grid(row=0, column=1, padx=10, pady=5)
# Status label
status_label = Label(root, text="", fg="green")
status_label.pack(pady=10)

# Set initial highlight
update_language("hi")

# Generate button
Button(root, text="Generate Voiceover", command=generate_voiceover).pack()



# Run GUI
root.mainloop()
