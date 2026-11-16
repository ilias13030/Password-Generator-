import secrets
import string
import tkinter as tk
from tkinter import messagebox


def generate_password(length, use_lowercase, use_uppercase, use_digits, use_symbols):
    groups = []
    if use_lowercase:
        groups.append(string.ascii_lowercase)
    if use_uppercase:
        groups.append(string.ascii_uppercase)
    if use_digits:
        groups.append(string.digits)
    if use_symbols:
        groups.append("!@#$%^&*()-_=+")

    if not groups:
        raise ValueError("Select at least one character type.")
    if length < len(groups):
        raise ValueError("Length must allow at least one character from each selected type.")

    characters = [secrets.choice(group) for group in groups]
    all_characters = "".join(groups)
    characters.extend(
        secrets.choice(all_characters) for _ in range(length - len(characters))
    )
    secrets.SystemRandom().shuffle(characters)
    return "".join(characters)


def main():
    root = tk.Tk()
    root.title("Random Password Generator")
    root.geometry("390x350")
    root.resizable(False, False)
    root.configure(bg="#111827")

    tk.Label(
        root,
        text="Random Password Generator",
        font=("Arial", 16, "bold"),
        fg="white",
        bg="#111827",
    ).pack(pady=(18, 12))

    options = tk.Frame(root, bg="#111827")
    options.pack()

    tk.Label(options, text="Length:", fg="white", bg="#111827").grid(
        row=0, column=0, sticky="w", padx=8, pady=5
    )
    length_value = tk.StringVar(value="16")
    tk.Spinbox(options, from_=1, to=64, textvariable=length_value, width=8).grid(
        row=0, column=1, sticky="w", padx=8, pady=5
    )

    lowercase = tk.BooleanVar(value=True)
    uppercase = tk.BooleanVar(value=True)
    digits = tk.BooleanVar(value=True)
    symbols = tk.BooleanVar(value=True)
    for row, (label, variable) in enumerate(
        (
            ("Lowercase letters", lowercase),
            ("Uppercase letters", uppercase),
            ("Numbers", digits),
            ("Symbols", symbols),
        ),
        start=1,
    ):
        tk.Checkbutton(
            options,
            text=label,
            variable=variable,
            fg="white",
            bg="#111827",
            activebackground="#111827",
            selectcolor="#374151",
        ).grid(row=row, column=0, columnspan=2, sticky="w", padx=8)

    password_value = tk.StringVar()
    password_entry = tk.Entry(
        root,
        textvariable=password_value,
        font=("Consolas", 13),
        justify="center",
        state="readonly",
        readonlybackground="white",
        width=30,
    )
    password_entry.pack(pady=14)

    def create_password():
        try:
            length = int(length_value.get())
            password = generate_password(
                length,
                lowercase.get(),
                uppercase.get(),
                digits.get(),
                symbols.get(),
            )
        except ValueError as error:
            messagebox.showerror("Can't generate password", str(error), parent=root)
            return

        password_value.set(password)

    def copy_password():
        password = password_value.get()
        if not password:
            messagebox.showinfo("Nothing to copy", "Generate a password first.", parent=root)
            return
        root.clipboard_clear()
        root.clipboard_append(password)
        root.update()
        messagebox.showinfo("Copied", "Password copied to the clipboard.", parent=root)

    buttons = tk.Frame(root, bg="#111827")
    buttons.pack(pady=4)
    tk.Button(buttons, text="Generate", command=create_password).pack(
        side="left", padx=6
    )
    tk.Button(buttons, text="Copy", command=copy_password).pack(side="left", padx=6)

    tk.Label(
        root,
        text="Use a password manager to store your password securely.",
        fg="#cbd5e1",
        bg="#111827",
        wraplength=340,
    ).pack(pady=12)

    root.mainloop()


if __name__ == "__main__":
    main()
