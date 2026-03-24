import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  # Requires: pip install Pillow
import os

class HexViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Binary Hex Inspector")
        self.root.geometry("750x600")
        
        # --- LOGO SECTION ---
        try:
            img = Image.open("logo.png")
            img = img.resize((80, 80), Image.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
            tk.Label(root, image=self.logo_img).pack(pady=10)
        except Exception:
            tk.Label(root, text="[ Hex Inspector ]", fg="lightgrey", font=("Arial", 10, "italic")).pack(pady=10)

        # --- UI ELEMENTS ---
        tk.Label(root, text="Encrypted File Hex Viewer", font=("Arial", 14, "bold")).pack()
        
        # Controls
        ctrl_frame = tk.Frame(root)
        ctrl_frame.pack(pady=10)
        tk.Button(ctrl_frame, text="Open File to Inspect", command=self.open_file, width=25).grid(row=0, column=0, padx=5)
        self.lbl_info = tk.Label(root, text="No file loaded", fg="grey")
        self.lbl_info.pack()

        # Hex Display Area (with Scrollbar)
        display_frame = tk.Frame(root)
        display_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.scrollbar = tk.Scrollbar(display_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Using a monospaced font is critical for hex alignment
        self.txt = tk.Text(display_frame, font=("Courier New", 10), 
                           wrap="none", bg="#1e1e1e", fg="#00ff00", 
                           yscrollcommand=self.scrollbar.set)
        self.txt.pack(expand=True, fill="both")
        self.scrollbar.config(command=self.txt.yview)

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        try:
            with open(file_path, "rb") as f:
                content = f.read()
            
            # Clear previous content
            self.txt.config(state="normal")
            self.txt.delete("1.0", tk.END)
            
            self.lbl_info.config(text=f"Viewing: {os.path.basename(file_path)} ({len(content)} bytes)", fg="black")

            # Process data in 16-byte chunks
            lines = []
            for i in range(0, len(content), 16):
                chunk = content[i:i+16]
                
                # Create the Hex part: "48 65 6C 6C 6F..."
                hex_part = " ".join(f"{b:02X}" for b in chunk)
                
                # Create the ASCII part: Replace non-printables with "."
                ascii_part = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)
                
                # Format: [Offset]  [Hex Data]  [ASCII]
                # <47 ensures the hex column stays the same width
                line = f"{i:08X}  {hex_part:<47}  |{ascii_part}|"
                lines.append(line)

            self.txt.insert(tk.END, "\n".join(lines))
            self.txt.config(state="disabled") # Make read-only
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HexViewerApp(root)
    root.mainloop()
