# Google TTS Voiceover GUI

Ye ek simple open-source Python GUI app hai jo text ko Hindi/English me **voiceover** me convert karta hai using **Google TTS (gTTS)**. Ye students, YouTubers, teachers aur content creators ke liye useful hai jo free me voiceover banana chahte hain.

## Features

- Hindi aur English language support
- Text se high-quality MP3 voiceover generate
- Optional background music mix with volume control
- Voiceover ko MP3 file ke roop me save karo
- Generated audio ko turant play karne ka option

## Installation

1. Repository clone karo:

https://github.com/Basudev29/Voiceover.git
cd voiceover


2. Virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate


3. Dependencies install karo:
pip install -r requirements.txt


## Usage

1. App run karo:

python voiceover_google_gui.py





2. Steps:

- Text area me apna text likho (Hindi/English).
- “Hindi” ya “English” button se language choose karo.
- Agar chaaho toh “Select Background Music (Optional)” se koi MP3 background music select karo.
- Background music volume slider se volume set karo.
- “Generate Voiceover” button dabao.
- App tumse poochega ki MP3 kaha save karna hai, save ke baad audio automatically play bhi ho sakta hai.

## Requirements

- Python 3.8+ recommended
- Internet connection (gTTS ke liye Google TTS API hit hota hai)
- `gTTS`, `pydub`, `playsound`, `tk` (sab `requirements.txt` me listed hain)

## License

Ye project MIT License ke under release kiya gaya hai. Aap isko free me use, modify aur distribute kar sakte hain, bas license file ka respect karna hoga.


