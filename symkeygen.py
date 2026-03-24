import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  # Requires: pip install Pillow
from cryptography.fernet import Fernet
import os

class SymmetricKeyGenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AES Shared Key Generator")
        self.root.geometry("400x480")
        
        # --- LOGO SECTION ---
        try:
            img = Image.open("logo.png")
            img = img.resize((100, 100), Image.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
            tk.Label(root, image=self.logo_img).pack(pady=15)
        except Exception:
            tk.Label(root, text="[ AES Security Tool ]", fg="lightgrey", font=("Arial", 10, "italic")).pack(pady=15)

        # --- UI ELEMENTS ---
        tk.Label(root, text="Symmetric Shared Key Generator", font=("Arial", 12, "bold")).pack()
        tk.Label(root, text="Generates a single key for both\nencryption and decryption.", 
                 fg="grey", justify="center").pack(pady=5)

        # Path display
        self.save_path = os.getcwd()
        self.lbl_path = tk.Label(root, text=f"Output Folder:\n{self.save_path}", 
                                 wraplength=300, fg="#333", bg="#f8f8f8", pady=10)
        self.lbl_path.pack(pady=20, fill="x", padx=40)

        # Action Buttons
        tk.Button(root, text="Change Folder", command=self.select_folder).pack()
        
        tk.Button(root, text="GENERATE SHARED KEY", bg="#2ecc71", fg="white", 
                  font=("Arial", 11, "bold"), height=2, width=22,
                  command=self.generate_shared_key).pack(pady=30)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.save_path = folder
            self.lbl_path.config(text=f"Output Folder:\n{self.save_path}")

    def generate_shared_key(self):
        try:
            # Generate a URL-safe base64-encoded 32-byte key
            key = Fernet.generate_key()
            
            key_file = os.path.join(self.save_path, "secret.key")
            with open(key_file, "wb") as f:
                f.write(key)

            messagebox.showinfo("Success", f"Shared key saved as:\n{key_file}\n\nKeep this file safe!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate key: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SymmetricKeyGenApp(root)
    root.mainloop()
