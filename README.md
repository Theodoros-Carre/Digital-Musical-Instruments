# 🎶 Digital Musical Instruments

## 📁 Project Overview

This project is part of the 2024–2025 Human-Machine Interface (HMI) course and simulates digital musical instruments using Python and PyQt5. The application allows users to play and record music using three different instrument interfaces:

- 🎹 Piano
- 🎼 Xylophone
- 🎮 Video Game-style soundboard

---

## 💡 Features

- 🎛️ Select between Piano, Xylophone, and Video Game instruments
- 📂 File menu and toolbar:
  - `Open`: Load a musical score file and play it
  - `Record`: Record played notes into a new file
  - `Stop`: End recording and save the notes
  - `Quit`: Exit the application
- 🧩 Visual feedback on key presses
- 🔄 Persistent configuration (instrument and number of octaves saved across sessions)
- ⌨️ Play instruments using mouse or keyboard
- 🧰 Piano octave selection via spinbox (1 to 3)
- 🖼️ Resizes automatically based on selected instrument
- 🎨 Custom UI with icons and responsive layout

---

## 🧱 Technologies Used

- Python 3
- PyQt5 for GUI
- Custom audio playback via `instrument.py`
- JSON for configuration persistence

---

## 📦 Project Structure

```
.
├── Digital Musical Intruments App.py      # Main application
├── instrument.py                          # Audio logic (external, required)
├── config.json                            # Stores selected instrument and octave count
├── video game images/                     # Icons for video game instrument
├── mario.txt, bella_ciao.txt              # Example musical scores
├── Icons/                                 # Toolbar/menu icons (open.png, record.png, etc.)
```

---

## ▶️ How to Run

1. Ensure you have Python 3 and PyQt5 installed:
   ```
   pip install PyQt5
   ```

2. **Organize Your Files**  
   Place the following files in the **same main directory**:
   - `instrument.py`
   - `Digital Musical Instruments App.py`
   - Musical score files (e.g., `mario.txt`, `bella_ciao.txt`)
   - The image folder for the video game instrument called `images` 
   - Toolbar/menu icons:  
     - `open.png`  
     - `record.png`  
     - `stoprecord.png`  
     - `quit.png`

   ⚠️ **Important:**  
   - Do **not** place the toolbar/menu icons in the `images` subfolder. If these icons are not in the main directory, they will **not display properly** in the application.
   
3. Run the app:
   ```
   Digital Musical Intruments App.py
   ```

---

## 📚 Controls

### Mouse (main controls):
- Click keys to play notes.

### Keyboard shortcuts:
- Mapped for piano with support for 3 octaves.
- Common keys:
  - Octave 1: For the white keys: `W, X, C, V, B, N, ,`; for the black keys: `&é(-`` `
  - Octave 2: For the white keys: `A, Z, E, R, T, Y, U`; for the black keys: `1, 2, 4, 5, 3`
  - Octave 3: For the white keys: `Q, S, D, F, G, H, J`; for the black keys: `6, 7, 9, 0, 8`

- **For Xylophone and Video Game instruments**:  
  The shortcuts are limited to one octave using the following keys:  
  `A, Z, E, R, T, Y, U` (mapped to notes Do, Ré, Mi, Fa, Sol, La, Si)

- **Toolbar and menu buttons**:
  - Open: `Ctrl+O`
  - Record: `Ctrl+R`
  - Stop record: `Ctrl+S`
  - Quit: `Ctrl+Q`
  
---

## 💾 Saving and Loading

- `Record` opens a dialog to name your recording.
- Recorded notes saved as `.txt` in the format:
  ```
  Do 0.5
  Ré 0.5
  0 0.25  # Pause
  ```

- `Open` loads and plays score files line-by-line.

---

## 📝 Notes

- Configuration file `config.json` tracks:
  - Last selected instrument
  - Number of piano octaves

- Instruments display one at a time.

---

## 🎯 Objectives Checklist

✔ Piano, Xylophone, and Video Game instrument interfaces  
✔ Dynamic instrument switching  
✔ File menu and toolbar with key options  
✔ Octave selection for piano  
✔ Visual key press feedback  
✔ Data persistence across sessions  
✔ GUI properly sized per instrument  
✔ Use of PyQt5 widgets and layouts

---

## 🔧 Possible Improvements

While the project meets all the baseline requirements, there are several enhancements that could further elevate the experience:

- 🎹 **Improved Key Mapping for Shortcuts**  
  The current key layout works but could be more ergonomically optimized. Rearranging keys to better fit hand positioning would improve performance and make the digital instruments more playable, especially for users familiar with musical keyboards.

- 🎼 **Western-style Note Mapping**  
  Adopting a western musical notation system (C, D, E, F, G, A, B) internally would make it easier to parse standard music scores. This change would allow the application to load and play external musical scores without requiring translation or custom formatting.

- 🔊 **Enhanced Instrument Sound Quality**  
  Some instruments, such as the xylophone, could benefit from higher-quality or more realistic sound samples. Currently, the xylophone's tone lacks the bright, metallic resonance typical of the real instrument.

- 👁️ **Visual Feedback for Keyboard Shortcuts**  
  When using the keyboard to play notes, the corresponding virtual keys should light up or change color. This would give users clear visual feedback that a note was successfully triggered, improving usability and engagement.

---

## 👥 Contributors  
**The Team** : Thedoros CARRE, Luis RAMIREZ RAMIREZ, Yousuf HOSNY

---

## 📜 License  
This project is licensed under the **ESME License** – Free to use and modify.
