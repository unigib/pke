import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  # Requires: pip install Pillow
import hashlib
import os

class HasherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SHA-512 File Hasher")
        self.root.geometry("400x480")
        
        # --- LOGO SECTION ---
        try:
            img = Image.open("logo.png")
            img = img.resize((100, 100), Image.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
            tk.Label(root, image=self.logo_img).pack(pady=15)
        except Exception:
            tk.Label(root, text="[ Integrity Tool ]", fg="lightgrey", font=("Arial", 10, "italic")).pack(pady=15)

        # --- UI ELEMENTS ---
        tk.Label(root, text="SHA-512 Integrity Hasher", font=("Arial", 14, "bold")).pack()
        
        self.file_path = ""

        # File Selection
        self.lbl_file = tk.Label(root, text="No file selected", fg="grey", wraplength=300)
        self.lbl_file.pack(pady=20)
        tk.Button(root, text="1. Select File to Hash", command=self.select_file, width=20).pack()

        # Result Display (Read-Only)
        tk.Label(root, text="Generated Hash:", font=("Arial", 10, "bold")).pack(pady=(20, 5))
        self.hash_display = tk.Text(root, height=4, width=40, font=("Courier New", 9), bg="#f4f4f4")
        self.hash_display.pack(padx=20)

        # Action Button
        tk.Button(root, text="GENERATE & SAVE HASH", bg="#9b59b6", fg="white", 
                  font=("Arial", 10, "bold"), height=2, command=self.process_hash).pack(pady=20)

    def select_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.lbl_file.config(text=os.path.basename(self.file_path), fg="black")
            self.hash_display.delete("1.0", tk.END)

    def process_hash(self):
        if not self.file_path:
            return messagebox.showwarning("Error", "Please select a file first.")
        
        try:
            # Create the SHA-512 object
            sha512 = hashlib.sha512()

            # Read file in 64KB chunks for efficiency
            with open(self.file_path, "rb") as f:
                while chunk := f.read(65536):
                    sha512.update(chunk)
            
            file_hash = sha512.hexdigest()

            # Display hash in GUI
            self.hash_display.delete("1.0", tk.END)
            self.hash_display.insert(tk.END, file_hash)

            # Save to .txt file
            save_name = self.file_path + ".sha512.txt"
            with open(save_name, "w") as f:
                f.write(file_hash)
            
            messagebox.showinfo("Success", f"Hash saved to:\n{os.path.basename(save_name)}")

        except Exception as e:
            messagebox.showerror("Error", f"Hashing failed: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HasherApp(root)
    root.mainloop()
