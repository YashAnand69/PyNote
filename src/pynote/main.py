# src/pynote/main.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

APP_TITLE = "PyNote"


class PyNoteApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)
        self.geometry("800x600")

        self.filepath = None

        # -------- Text area --------
        self.text = tk.Text(self, wrap="word", undo=True)
        self.scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=self.text.yview
        )
        self.text.config(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)

        # -------- Status bar --------
        self.status = tk.StringVar()
        self.status.set("Ln 1, Col 0")

        self.status_bar = ttk.Label(
            self, textvariable=self.status, anchor="w"
        )
        self.status_bar.pack(side="bottom", fill="x")

        # -------- Bind events --------
        self.text.bind("<KeyRelease>", self.update_status)
        self.text.bind("<ButtonRelease>", self.update_status)

        self.create_menu()
        self.bind_shortcuts()

    # ---------------- Menu ----------------
    def create_menu(self):
        menu = tk.Menu(self)
        file_menu = tk.Menu(menu, tearoff=0)

        file_menu.add_command(
            label="New",
            accelerator="Ctrl+N",
            command=self.new_file
        )
        file_menu.add_command(
            label="Open",
            accelerator="Ctrl+O",
            command=self.open_file
        )
        file_menu.add_command(
            label="Save",
            accelerator="Ctrl+S",
            command=self.save_file
        )
        file_menu.add_command(
            label="Save As",
            command=self.save_as
        )

        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        menu.add_cascade(label="File", menu=file_menu)
        self.config(menu=menu)

    # ---------------- Shortcuts ----------------
    def bind_shortcuts(self):
        self.bind("<Control-n>", lambda e: self.new_file())
        self.bind("<Command-n>", lambda e: self.new_file())
        self.bind("<Control-o>", lambda e: self.open_file())
        self.bind("<Control-s>", lambda e: self.save_file())
        self.bind("<Control-z>", lambda e: self.text.event_generate("<<Undo>>"))
        self.bind("<Control-y>", lambda e: self.text.event_generate("<<Redo>>"))

    # ---------------- File actions ----------------
    def new_file(self):
        if not self.confirm_discard():
            return

        self.text.delete("1.0", tk.END)
        self.filepath = None
        self.title(APP_TITLE)

    def open_file(self):
        if not self.confirm_discard():
            return

        path = filedialog.askopenfilename(
            filetypes=[
                ("Text Files", "*.txt;*.md;*.py"),
                ("All Files", "*.*")
            ]
        )

        if path:
            try:
                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()

                self.text.delete("1.0", tk.END)
                self.text.insert("1.0", content)

                self.filepath = path
                self.title(f"{APP_TITLE} - {path}")

            except Exception as error:
                messagebox.showerror(
                    "Error",
                    f"Failed to open file: {error}"
                )

    def save_file(self):
        if self.filepath:
            try:
                with open(self.filepath, "w", encoding="utf-8") as file:
                    file.write(self.text.get("1.0", tk.END))

                self.text.edit_modified(False)
                messagebox.showinfo("Saved", "File saved successfully")

            except Exception as error:
                messagebox.showerror(
                    "Error",
                    f"Failed to save file: {error}"
                )
        else:
            self.save_as()

    def save_as(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt;*.md;*.py"),
                ("All Files", "*.*")
            ]
        )

        if path:
            try:
                with open(path, "w", encoding="utf-8") as file:
                    file.write(self.text.get("1.0", tk.END))

                self.filepath = path
                self.title(f"{APP_TITLE} - {path}")
                self.text.edit_modified(False)

                messagebox.showinfo("Saved", "File saved successfully")

            except Exception as error:
                messagebox.showerror(
                    "Error",
                    f"Failed to save file: {error}"
                )

    # ---------------- Helpers ----------------
    def update_status(self, event=None):
        line, col = self.text.index(tk.INSERT).split(".")
        self.status.set(f"Ln {line}, Col {col}")

    def confirm_discard(self):
        if self.text.edit_modified():
            choice = messagebox.askyesnocancel(
                "Unsaved changes",
                "You have unsaved changes. Save before continuing?"
            )

            if choice is None:
                return False
            if choice:
                self.save_file()

        return True
if __name__ == "__main__":
    app = PyNoteApp()
    app.mainloop()
