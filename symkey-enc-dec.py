import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  # Requires: pip install Pillow
from cryptography.fernet import Fernet
import os

class SymmetricFileApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Symmetric AES File Tool")
        self.root.geometry("400x480")
        
        # --- LOGO SECTION ---
        try:
            img = Image.open("logo.png")
            img = img.resize((100, 100), Image.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
            tk.Label(root, image=self.logo_img).pack(pady=15)
        except Exception:
            tk.Label(root, text="[ AES Secure File ]", fg="lightgrey", font=("Arial", 10, "italic")).pack(pady=15)

        # --- UI ELEMENTS ---
        tk.Label(root, text="Symmetric File Tool", font=("Arial", 14, "bold")).pack()
        
        self.file_path = ""
        self.key_path = ""

        # File Selection
        self.lbl_file = tk.Label(root, text="No file selected", fg="grey", wraplength=300)
        self.lbl_file.pack(pady=(10, 0))
        tk.Button(root, text="1. Select File", command=self.select_file, width=20).pack()

        # Key Selection
        self.lbl_key = tk.Label(root, text="No .key selected", fg="grey", wraplength=300)
        self.lbl_key.pack(pady=(10, 0))
        tk.Button(root, text="2. Select Shared Key", command=self.select_key, width=20).pack()

        # Action Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=30)
        tk.Button(btn_frame, text="Encrypt", bg="#3498db", fg="white", width=12, height=2,
                  command=self.encrypt_file).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Decrypt", bg="#27ae60", fg="white", width=12, height=2,
                  command=self.decrypt_file).grid(row=0, column=1, padx=10)

    def select_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.lbl_file.config(text=os.path.basename(self.file_path), fg="black")

    def select_key(self):
        self.key_path = filedialog.askopenfilename(filetypes=[("Key files", "*.key")])
        if self.key_path:
            self.lbl_key.config(text=os.path.basename(self.key_path), fg="black")

    def encrypt_file(self):
        if not self.file_path or not self.key_path:
            return messagebox.showwarning("Error", "Please select a file and the shared .key file.")
        
        try:
            with open(self.key_path, "rb") as kf:
                key = kf.read()
            fernet = Fernet(key)

            with open(self.file_path, "rb") as f:
                original_data = f.read()
            
            encrypted_data = fernet.encrypt(original_data)

            output_file = self.file_path + ".aes"
            with open(output_file, "wb") as f:
                f.write(encrypted_data)
            
            messagebox.showinfo("Success", f"Encrypted as:\n{os.path.basename(output_file)}")
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {str(e)}")

    def decrypt_file(self):
        if not self.file_path or not self.key_path:
            return messagebox.showwarning("Error", "Please select the .aes file and the shared .key file.")
        
        try:
            with open(self.key_path, "rb") as kf:
                key = kf.read()
            fernet = Fernet(key)

            with open(self.file_path, "rb") as f:
                encrypted_data = f.read()
            
            decrypted_data = fernet.decrypt(encrypted_data)

            # Remove .aes extension if present
            output_file = self.file_path.replace(".aes", ".decrypted")
            with open(output_file, "wb") as f:
                f.write(decrypted_data)
            
            messagebox.showinfo("Success", f"Decrypted as:\n{os.path.basename(output_file)}")
        except Exception:
            messagebox.showerror("Error", "Decryption failed. Ensure you have the correct key and the file hasn't been modified.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SymmetricFileApp(root)
    root.mainloop()
