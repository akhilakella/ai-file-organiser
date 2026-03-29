import os
import shutil
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from datetime import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

# ── Model ────────────────────────────────────────────────────────────────────
model = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.environ.get("GROQ_API_KEY")
)

# ── File type map ─────────────────────────────────────────────────────────────
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".pptx", ".xlsx", ".csv"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Audio": [".mp3", ".wav", ".flac", ".m4a"],
    "Code": [".py", ".js", ".html", ".css", ".json", ".ts", ".java", ".kt"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Other": []
}

def get_file_type(ext):
    for category, extensions in FILE_TYPES.items():
        if ext.lower() in extensions:
            return category
    return "Other"

def get_file_hash(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def get_ai_topic(filename):
    prompt = f"""Given the filename "{filename}", suggest a single short project or topic name (2-3 words max) that this file likely belongs to.
Examples: Windfall, CrashGuard, School, Personal, Finance, Travel.
Reply with ONLY the topic name, nothing else."""
    response = model.invoke([HumanMessage(content=prompt)])
    return response.content.strip().replace(" ", "_")

def organise_folder(folder, log):
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    hashes = {}
    duplicates = []

    log(f"Found {len(files)} files. Starting organisation...\n")

    for filename in files:
        filepath = os.path.join(folder, filename)
        ext = os.path.splitext(filename)[1]
        file_type = get_file_type(ext)
        date_str = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%Y-%m")
        topic = get_ai_topic(filename)
        file_hash = get_file_hash(filepath)

        # Check for duplicates
        if file_hash in hashes:
            duplicates.append((filepath, hashes[file_hash]))
            log(f"⚠ Duplicate found: {filename}")
            continue
        hashes[file_hash] = filepath

        # Build destination path
        dest_dir = os.path.join(folder, file_type, date_str, topic)
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, filename)

        shutil.move(filepath, dest_path)
        log(f"✓ {filename} → {file_type}/{date_str}/{topic}/")

    # Handle duplicates one by one
    for dup_path, original_path in duplicates:
        answer = messagebox.askyesnocancel(
            "Duplicate Found",
            f"Duplicate:\n{dup_path}\n\nOriginal:\n{original_path}\n\nMove to Duplicates folder? (No = delete, Cancel = keep)"
        )
        if answer is True:
            dup_dir = os.path.join(folder, "Duplicates")
            os.makedirs(dup_dir, exist_ok=True)
            shutil.move(dup_path, os.path.join(dup_dir, os.path.basename(dup_path)))
            log(f"↪ Moved duplicate to Duplicates/")
        elif answer is False:
            os.remove(dup_path)
            log(f"🗑 Deleted duplicate: {os.path.basename(dup_path)}")
        else:
            log(f"⏭ Kept duplicate: {os.path.basename(dup_path)}")

    log("\n✅ Done!")

# ── GUI ───────────────────────────────────────────────────────────────────────
def launch_gui():
    root = tk.Tk()
    root.title("AI File Organiser")
    root.geometry("600x450")
    root.resizable(False, False)

    folder_var = tk.StringVar()

    tk.Label(root, text="AI File Organiser", font=("Helvetica", 16, "bold")).pack(pady=10)

    frame = tk.Frame(root)
    frame.pack(pady=5)
    tk.Entry(frame, textvariable=folder_var, width=50).pack(side=tk.LEFT, padx=5)
    tk.Button(frame, text="Browse", command=lambda: folder_var.set(
        filedialog.askdirectory(title="Select folder to organise")
    )).pack(side=tk.LEFT)

    log_box = scrolledtext.ScrolledText(root, width=70, height=18, state="disabled")
    log_box.pack(pady=10)

    def log(msg):
        log_box.config(state="normal")
        log_box.insert(tk.END, msg + "\n")
        log_box.see(tk.END)
        log_box.config(state="disabled")
        root.update()

    def run():
        folder = folder_var.get()
        if not folder:
            messagebox.showwarning("No folder", "Please select a folder first.")
            return
        log_box.config(state="normal")
        log_box.delete("1.0", tk.END)
        log_box.config(state="disabled")
        organise_folder(folder, log)

    tk.Button(root, text="🗂 Organise Folder", command=run,
              bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"),
              padx=10, pady=5).pack()

    root.mainloop()

if __name__ == "__main__":
    launch_gui() 
  
