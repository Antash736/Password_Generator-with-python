import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import itertools

digits = [chr(i) for i in range(48, 58)]
small = [chr(i) for i in range(97, 123)]
caps = [chr(i) for i in range(65, 91)]
specials = [chr(i) for i in range(33, 48)] + [chr(i) for i in range(58, 65)] + \
           [chr(i) for i in range(91, 97)] + [chr(i) for i in range(123, 127)]

options = {
    "Numbers": digits,
    "Lowercase": small,
    "Uppercase": caps,
    "Lowercase + Uppercase": small + caps,
    "Numbers + Lowercase": digits + small,
    "Numbers + Uppercase": digits + caps,
    "Numbers + All Letters": digits + small + caps,
    "Numbers + Specials": digits + specials,
    "Lowercase + Specials": small + specials,
    "Uppercase + Specials": caps + specials,
    "All Letters + Specials": small + caps + specials,
    "Numbers + All Letters + Specials": digits + small + caps + specials
}

def generate_passwords():
    try:
        length = int(length_entry.get())
        charset = options[option_var.get()]
        output_mode = output_var.get()

        if length <= 0:
            raise ValueError

        total = len(charset) ** length
        if total > 1_000_000:
            confirm = messagebox.askyesno("Warning", f"{total:,} passwords will be generated. Continue?")
            if not confirm:
                return

        passwords = (''.join(p) for p in itertools.product(charset, repeat=length))

        if output_mode == "Display in Window":
            output_text.config(state="normal")
            output_text.delete(1.0, tk.END)
            count = 0
            for pw in passwords:
                output_text.insert(tk.END, pw + "\n")
                count += 1
                if count >= 100000:
                    output_text.insert(tk.END, "\n[Output stopped after 100,000 lines]")
                    break
            output_text.config(state="disabled")

        elif output_mode == "Save to File":
            path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            if not path:
                return
            with open(path, "w") as f:
                for pw in passwords:
                    f.write(pw + "\n")
            messagebox.showinfo("Done", f"Passwords saved to:\n{path}")

    except ValueError:
        messagebox.showerror("Error", "Enter a valid password length.")

root = tk.Tk()
root.title("Brute Forcer")
root.geometry("700x650")
root.configure(bg="black")

title = tk.Label(root, text="===[ Brute Forcer GUI ]===", font=("Courier", 18, "bold"),
                 bg="black", fg="#00FF00")
title.pack(pady=20)

frame = tk.Frame(root, bg="black")
frame.pack()

tk.Label(frame, text="Password Length:", font=("Courier", 12), bg="black", fg="#00FF00").grid(row=0, column=0, padx=10, pady=5, sticky="w")
length_entry = tk.Entry(frame, font=("Courier", 12), width=10, bg="black", fg="#00FF00", insertbackground="#00FF00")
length_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame, text="Charset:", font=("Courier", 12), bg="black", fg="#00FF00").grid(row=1, column=0, padx=10, pady=5, sticky="w")
option_var = tk.StringVar()
option_menu = ttk.Combobox(frame, textvariable=option_var, values=list(options.keys()), state="readonly", width=30)
option_menu.grid(row=1, column=1, padx=10, pady=5)
option_menu.set("Numbers")

tk.Label(frame, text="Output Mode:", font=("Courier", 12), bg="black", fg="#00FF00").grid(row=2, column=0, padx=10, pady=5, sticky="w")
output_var = tk.StringVar()
output_menu = ttk.Combobox(frame, textvariable=output_var, values=["Display in Window", "Save to File"], state="readonly", width=30)
output_menu.grid(row=2, column=1, padx=10, pady=5)
output_menu.set("Display in Window")

generate_btn = tk.Button(root, text="[ GENERATE ]", command=generate_passwords,
                         font=("Courier", 12, "bold"), bg="#111", fg="#00FF00", activebackground="#222", activeforeground="#00FF00")
generate_btn.pack(pady=20)

output_text = scrolledtext.ScrolledText(root, width=80, height=20, font=("Courier", 10), bg="black", fg="#00FF00", insertbackground="#00FF00")
output_text.pack(padx=10, pady=10)
output_text.config(state="disabled")

style = ttk.Style()
style.theme_use('clam')
style.configure("TCombobox", fieldbackground="black", background="black", foreground="#00FF00")
style.map("TCombobox", fieldbackground=[('readonly', 'black')],
          background=[('readonly', 'black')],
          foreground=[('readonly', '#00FF00')])

root.mainloop()
