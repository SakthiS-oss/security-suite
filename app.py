import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import threading
import time
import csv
import logic 

class PasswordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Security Suite")
        self.root.geometry("800x850")
        
        self.stop_event = threading.Event()
        self.show_pwd_state = False 

        # Style configuration for a cleaner look
        self.style = ttk.Style()
        self.style.configure("TNotebook.Tab", padding=[15, 5])

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        # Tabs
        self.tab_auditor = tk.Frame(self.notebook, bg="#f8f9fa")
        self.tab_generator = tk.Frame(self.notebook, bg="#f8f9fa")
        self.tab_batch = tk.Frame(self.notebook, bg="#f8f9fa")
        self.tab_cracker = tk.Frame(self.notebook, bg="#f8f9fa")

        self.notebook.add(self.tab_auditor, text="  Single Auditor  ")
        self.notebook.add(self.tab_generator, text="  Generator  ")
        self.notebook.add(self.tab_batch, text="  Batch Analysis  ")
        self.notebook.add(self.tab_cracker, text="  Hash Cracker  ")

        self.setup_auditor()
        self.setup_generator()
        self.setup_batch()
        self.setup_cracker()

    # --- TAB 1: AUDITOR (Restored Details) ---
    def setup_auditor(self):
        tk.Label(self.tab_auditor, text="🛡️ Real-Time Auditor", font=("Arial", 18, "bold"), bg="#f8f9fa").pack(pady=20)
        
        entry_frame = tk.Frame(self.tab_auditor, bg="#f8f9fa")
        entry_frame.pack(pady=10)
        self.auditor_entry = tk.Entry(entry_frame, width=30, font=("Courier", 14), show="*")
        self.auditor_entry.grid(row=0, column=0, padx=5)
        self.auditor_entry.bind("<KeyRelease>", self.update_auditor_ui)
        
        self.toggle_btn = tk.Button(entry_frame, text="Show", command=self.toggle_password_visibility, width=6)
        self.toggle_btn.grid(row=0, column=1)

        self.auditor_canvas = tk.Canvas(self.tab_auditor, width=400, height=25, bg="#ecf0f1", highlightthickness=0)
        self.auditor_canvas.pack(pady=5)
        self.auditor_rect = self.auditor_canvas.create_rectangle(0, 0, 0, 25, fill="red")

        self.auditor_label = tk.Label(self.tab_auditor, text="Entropy: 0 bits (N/A)", font=("Arial", 11), bg="#f8f9fa")
        self.auditor_label.pack(pady=5)

        tk.Button(self.tab_auditor, text="Check Breach Database", command=self.handle_single_leak, 
                  width=25, bg="#3498db", fg="white", font=("Arial", 10, "bold")).pack(pady=15)
        
        self.auditor_status = tk.Label(self.tab_auditor, text="", font=("Arial", 11, "bold"), bg="#f8f9fa")
        self.auditor_status.pack()

    # --- TAB 2: GENERATOR (Restored Spinner) ---
    def setup_generator(self):
        tk.Label(self.tab_generator, text="🔑 Secure Generator", font=("Arial", 18, "bold"), bg="#f8f9fa").pack(pady=20)
        tk.Label(self.tab_generator, text="Password Length:", bg="#f8f9fa").pack()
        self.len_spinner = tk.Spinbox(self.tab_generator, from_=8, to=64, width=5, font=("Arial", 12))
        self.len_spinner.delete(0, "end"); self.len_spinner.insert(0, "16"); self.len_spinner.pack(pady=5)
        
        tk.Button(self.tab_generator, text="Generate", command=self.handle_tab_gen, bg="#27ae60", fg="white", width=20).pack(pady=10)
        self.gen_output = tk.Entry(self.tab_generator, width=40, font=("Courier", 14), justify="center")
        self.gen_output.pack(pady=10)
        tk.Button(self.tab_generator, text="Copy to Clipboard", command=self.copy_to_clipboard).pack()

    # --- TAB 3: BATCH (Restored Table Colors & Timer) ---
    def setup_batch(self):
        tk.Label(self.tab_batch, text="📊 Batch Analysis Report", font=("Arial", 16, "bold"), bg="#f8f9fa").pack(pady=15)
        
        self.batch_timer_label = tk.Label(self.tab_batch, text="Time: 0.0s | Processed: 0", font=("Courier", 10), bg="#f8f9fa")
        self.batch_timer_label.pack()

        self.progress = ttk.Progressbar(self.tab_batch, orient="horizontal", length=600, mode="determinate")
        self.progress.pack(pady=10)

        ctrl_frame = tk.Frame(self.tab_batch, bg="#f8f9fa")
        ctrl_frame.pack()
        tk.Button(ctrl_frame, text="📁 Upload TXT", command=self.start_batch_thread, width=15).grid(row=0, column=0, padx=5)
        self.stop_btn = tk.Button(ctrl_frame, text="🛑 Stop", command=self.stop_batch, state="disabled", bg="#c0392b", fg="white", width=10).grid(row=0, column=1, padx=5)
        self.export_btn = tk.Button(ctrl_frame, text="💾 Export CSV", command=self.save_csv_results, state="disabled", width=15).grid(row=0, column=2, padx=5)

        cols = ("password", "entropy", "leaks", "status")
        self.tree = ttk.Treeview(self.tab_batch, columns=cols, show="headings", height=18)
        for col in cols: self.tree.heading(col, text=col.title())
        
        # RESTORED TABLE COLORS
        self.tree.tag_configure('RISK_LEAK', background='#ffcccc') # Light Red
        self.tree.tag_configure('RISK_WEAK', background='#fff3cd') # Light Yellow
        self.tree.tag_configure('SECURE', background='#d4edda')    # Light Green
        self.tree.pack(pady=10, padx=20, fill="both", expand=True)

    # --- TAB 4: HASH CRACKER (Restored Functionality) ---
    def setup_cracker(self):
        tk.Label(self.tab_cracker, text="🔓 Hash Cracker", font=("Arial", 18, "bold"), bg="#f8f9fa").pack(pady=20)
        tk.Label(self.tab_cracker, text="Target Hash:", bg="#f8f9fa").pack()
        self.hash_input = tk.Entry(self.tab_cracker, width=55, font=("Courier", 12))
        self.hash_input.pack(pady=5)
        
        tk.Label(self.tab_cracker, text="Algorithm:", bg="#f8f9fa").pack()
        self.hash_algo = ttk.Combobox(self.tab_cracker, values=["sha1", "md5", "sha256"], state="readonly")
        self.hash_algo.set("sha1")
        self.hash_algo.pack(pady=5)

        tk.Button(self.tab_cracker, text="📂 Load Dictionary & Crack", command=self.start_crack_thread, 
                  bg="#8e44ad", fg="white", width=30, height=2).pack(pady=20)
        self.crack_result = tk.Label(self.tab_cracker, text="Status: Ready", font=("Arial", 12, "bold"), bg="#f8f9fa")
        self.crack_result.pack()

    # --- LOGIC INTEGRATION ---
    def update_auditor_ui(self, event=None):
        pwd = self.auditor_entry.get()
        bits, rating = logic.calculate_entropy(pwd)
        self.auditor_label.config(text=f"Entropy: {bits} bits ({rating})")
        width = min(bits * 4, 400)
        color = "#e74c3c" if bits < 40 else "#f39c12" if bits < 60 else "#2ecc71"
        self.auditor_canvas.coords(self.auditor_rect, 0, 0, width, 25)
        self.auditor_canvas.itemconfig(self.auditor_rect, fill=color)

    def toggle_password_visibility(self):
        self.show_pwd_state = not self.show_pwd_state
        self.auditor_entry.config(show="" if self.show_pwd_state else "*")
        self.toggle_btn.config(text="Hide" if self.show_pwd_state else "Show")

    def handle_single_leak(self):
        pwd = self.auditor_entry.get()
        if not pwd: return
        self.auditor_status.config(text="Searching...", fg="gray")
        self.root.update_idletasks()
        count = logic.get_pwned_count(pwd)
        if count > 0: self.auditor_status.config(text=f"🚨 Found in {count:,} leaks!", fg="#c0392b")
        else: self.auditor_status.config(text="✅ No leaks found.", fg="#27ae60")

    def start_batch_thread(self):
        f = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not f: return
        self.stop_event.clear()
        self.stop_btn.config(state="normal")
        for item in self.tree.get_children(): self.tree.delete(item)
        threading.Thread(target=self.run_batch_analysis, args=(f,), daemon=True).start()

    def stop_batch(self):
        self.stop_event.set()

    def run_batch_analysis(self, file_path):
        start_time = time.time()
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                pwds = [l.strip() for l in f if l.strip()]
            self.progress["maximum"] = len(pwds)
            self.current_batch_results = []

            for i, p in enumerate(pwds):
                if self.stop_event.is_set(): break
                bits, _ = logic.calculate_entropy(p)
                leaks = logic.get_pwned_count(p)
                
                # RESTORED DIAGNOSTICS
                if leaks > 0: tag, risk = 'RISK_LEAK', "🚨 LEAKED"
                elif bits < 50: tag, risk = 'RISK_WEAK', "⚠️ WEAK"
                else: tag, risk = 'SECURE', "✅ Safe"

                elapsed = round(time.time() - start_time, 1)
                self.root.after(0, self.update_batch_ui, p, bits, leaks, risk, tag, i+1, elapsed)
                self.current_batch_results.append({"password": p, "entropy": bits, "leaks": leaks, "status": risk})

            self.root.after(0, lambda: self.stop_btn.config(state="disabled"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))

    def update_batch_ui(self, p, b, l, r, t, count, elap):
        self.tree.insert("", "end", values=(p, b, f"{l:,}", r), tags=(t,))
        self.progress["value"] = count
        self.batch_timer_label.config(text=f"Time: {elap}s | Processed: {count}")

    def start_crack_thread(self):
        target = self.hash_input.get().strip()
        algo = self.hash_algo.get()
        f = filedialog.askopenfilename()
        if target and f:
            self.crack_result.config(text="🔍 Cracking...", fg="orange")
            threading.Thread(target=self.run_crack, args=(target, f, algo), daemon=True).start()

    def run_crack(self, target, f, algo):
        match = logic.crack_hash(target, f, algo)
        if match: self.root.after(0, lambda: self.crack_result.config(text=f"🔓 FOUND: {match}", fg="#27ae60"))
        else: self.root.after(0, lambda: self.crack_result.config(text="❌ Not found", fg="#c0392b"))

    def handle_tab_gen(self):
        pwd = logic.generate_secure_password(int(self.len_spinner.get()))
        self.gen_output.delete(0, tk.END); self.gen_output.insert(0, pwd)

    def copy_to_clipboard(self):
        self.root.clipboard_clear(); self.root.clipboard_append(self.gen_output.get())
        messagebox.showinfo("Clipboard", "Password copied!")

    def save_csv_results(self):
        # Implementation of CSV saving as before...
        pass

    

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordApp(root)
    root.mainloop()