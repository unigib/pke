import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  # Requires: pip install Pillow
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet
import os

class RSAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RSA Secure File Tool")
        self.root.geometry("400x450")
        
        # --- LOGO SECTION ---
        try:
            # Load and resize logo (change 'logo.png' to your filename)
            img = Image.open("logo.png")
            img = img.resize((100, 100), Image.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
            logo_label = tk.Label(root, image=self.logo_img)
            logo_label.pack(pady=10)
        except Exception:
            tk.Label(root, text="[ Logo Missing ]", fg="lightgrey").pack(pady=10)

        # --- REST OF UI ---
        tk.Label(root, text="RSA Encryption & Decryption", font=("Arial", 12, "bold")).pack()
        
        self.file_path = ""
        self.key_path = ""

        self.lbl_file = tk.Label(root, text="No file selected", fg="grey")
        self.lbl_file.pack(pady=(10, 0))
        tk.Button(root, text="1. Select File", command=self.select_file).pack()

        self.lbl_key = tk.Label(root, text="No key selected", fg="grey")
        self.lbl_key.pack(pady=(10, 0))
        tk.Button(root, text="2. Select Key (.pem)", command=self.select_key).pack()

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=30)
        tk.Button(btn_frame, text="Encrypt", bg="#add8e6", width=12, command=self.encrypt).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Decrypt", bg="#90ee90", width=12, command=self.decrypt).grid(row=0, column=1, padx=10)

    # ... (select_file, select_key, encrypt, and decrypt methods remain the same as previous)
    def select_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path: self.lbl_file.config(text=os.path.basename(self.file_path), fg="black")

    def select_key(self):
        self.key_path = filedialog.askopenfilename(filetypes=[("PEM files", "*.pem")])
        if self.key_path: self.lbl_key.config(text=os.path.basename(self.key_path), fg="black")

    def encrypt(self):
        if not self.file_path or not self.key_path: return messagebox.showwarning("Error", "Select file and Public Key")
        try:
            with open(self.key_path, "rb") as kf:
                pub_key = serialization.load_pem_public_key(kf.read())
            sym_key = Fernet.generate_key()
            fernet = Fernet(sym_key)
            with open(self.file_path, "rb") as f:
                enc_data = fernet.encrypt(f.read())
            enc_sym_key = pub_key.encrypt(
                sym_key,
                padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
            )
            with open(self.file_path + ".enc", "wb") as f:
                f.write(len(enc_sym_key).to_bytes(4, 'big'))
                f.write(enc_sym_key)
                f.write(enc_data)
            messagebox.showinfo("Success", "File encrypted!")
        except Exception as e: messagebox.showerror("Error", str(e))

    def decrypt(self):
        if not self.file_path or not self.key_path: return messagebox.showwarning("Error", "Select .enc file and Private Key")
        try:
            with open(self.key_path, "rb") as kf:
                priv_key = serialization.load_pem_private_key(kf.read(), password=None)
            with open(self.file_path, "rb") as f:
                key_len = int.from_bytes(f.read(4), 'big')
                enc_sym_key = f.read(key_len)
                enc_data = f.read()
            sym_key = priv_key.decrypt(
                enc_sym_key,
                padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
            )
            dec_data = Fernet(sym_key).decrypt(enc_data)
            with open(self.file_path.replace(".enc", ".decrypted"), "wb") as f:
                f.write(dec_data)
            messagebox.showinfo("Success", "File decrypted!")
        except Exception as e: messagebox.showerror("Error", "Decryption failed.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RSAApp(root)
    root.mainloop()
