import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  # Requires: pip install Pillow
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

class KeyGenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RSA Key Pair Generator")
        self.root.geometry("400x480")
        
        # --- LOGO SECTION ---
        try:
            # Load and resize logo
            img = Image.open("logo.png")
            img = img.resize((100, 100), Image.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
            logo_label = tk.Label(root, image=self.logo_img)
            logo_label.pack(pady=15)
        except Exception:
            tk.Label(root, text="[ Security Tool ]", fg="lightgrey", font=("Arial", 10, "italic")).pack(pady=15)

        # --- UI ELEMENTS ---
        tk.Label(root, text="RSA Key Generator", font=("Arial", 14, "bold")).pack()
        tk.Label(root, text="Create 2048-bit secure keys", fg="grey").pack(pady=5)

        # Save Path Display
        self.save_path = os.getcwd()
        self.lbl_path = tk.Label(root, text=f"Output Folder:\n{self.save_path}", 
                                 wraplength=300, fg="#333", bg="#f0f0f0", pady=10)
        self.lbl_path.pack(pady=20, fill="x", padx=40)

        # Buttons
        tk.Button(root, text="Change Folder", command=self.select_folder).pack()
        
        tk.Button(root, text="GENERATE KEY PAIR", bg="#ff9900", fg="white", 
                  font=("Arial", 11, "bold"), height=2, width=20,
                  command=self.generate_keys).pack(pady=30)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.save_path = folder
            self.lbl_path.config(text=f"Output Folder:\n{self.save_path}")

    def generate_keys(self):
        try:
            # Generate the RSA Private Key
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )

            # Extract Public Key
            public_key = private_key.public_key()

            # Serialize Private Key to PEM
            priv_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )

            # Serialize Public Key to PEM
            pub_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

            # Write files
            with open(os.path.join(self.save_path, "private_key.pem"), "wb") as f:
                f.write(priv_pem)
            with open(os.path.join(self.save_path, "public_key.pem"), "wb") as f:
                f.write(pub_pem)

            messagebox.showinfo("Success", f"Keys saved to:\n{self.save_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Generation failed: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyGenApp(root)
    root.mainloop()
