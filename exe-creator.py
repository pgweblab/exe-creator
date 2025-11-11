import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import subprocess
import os
import venv
import ast
import re
import threading
import queue
from pathlib import Path
import time
import shutil

class ModernExeCreatorApp:
    def __init__(self, root):
        self.root = root
        root.title("EXE Creator Pro - Virtual Environment Edition")
        root.geometry("1000x900")
        
        # Colori tema scuro
        self.bg_primary = "#1e1e1e"
        self.bg_secondary = "#2d2d2d"
        self.bg_card = "#3a3a3a"
        self.text_primary = "#ffffff"
        self.text_secondary = "#b0b0b0"
        self.accent_color = "#00d4ff"
        self.success_color = "#00ff88"
        self.error_color = "#ff4444"
        self.warning_color = "#ffaa00"
        
        root.configure(bg=self.bg_primary)
        
        self.setup_styles()
        
        # Variabili
        self.venv_path = Path(__file__).parent / "pyinstaller_env"
        self.venv_python = self.get_venv_python_path()
        self.installation_thread = None
        self.cancel_installation = False
        self.message_queue = queue.Queue()
        self.script_path = ""
        self.icon_path = ""
        
        # HEADER
        self.create_header()
        
        # CONTENT FRAME
        content = ttk.Frame(root, style="TFrame")
        content.pack(fill="both", expand=True, padx=20, pady=15)
        
        # STATUS FRAME
        self.create_status_frame(content)
        
        # SOFTWARE NAME
        self.create_software_name_frame(content)
        
        # SCRIPT SELECTION
        self.create_script_frame(content)
        
        # OPTIONS
        self.create_options_frame(content)
        
        # DEPENDENCIES
        self.create_dependencies_frame(content)
        
        # CREATE BUTTON
        self.create_main_button(content)
        
        # OUTPUT
        self.create_output_frame(content)
        
        # Updates
        self.check_message_queue()
        self.periodic_ui_update()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("TFrame", background=self.bg_primary)
        style.configure("Card.TFrame", background=self.bg_card, relief="flat", borderwidth=1)
        style.configure("Header.TFrame", background=self.bg_secondary)
        
        style.configure("TLabel", background=self.bg_primary, foreground=self.text_primary, font=("Segoe UI", 10))
        style.configure("Header.TLabel", background=self.bg_secondary, foreground=self.accent_color, font=("Segoe UI", 14, "bold"))
        style.configure("Section.TLabel", background=self.bg_card, foreground=self.accent_color, font=("Segoe UI", 10, "bold"))
        style.configure("Info.TLabel", background=self.bg_card, foreground=self.text_secondary, font=("Segoe UI", 9))
        
        style.configure("TButton", font=("Segoe UI", 10), relief="flat", padding=10)
        style.map("TButton", foreground=[("active", self.bg_primary)], background=[("active", self.accent_color)])
        
        style.configure("Primary.TButton", background=self.accent_color, foreground=self.bg_primary, font=("Segoe UI", 11, "bold"))
        style.map("Primary.TButton", background=[("active", "#00b8d4")])
        
        style.configure("Success.TButton", background=self.success_color, foreground=self.bg_primary, font=("Segoe UI", 11, "bold"))
        style.map("Success.TButton", background=[("active", "#00dd77")])
        
        style.configure("Danger.TButton", background=self.error_color, foreground=self.text_primary, font=("Segoe UI", 10, "bold"))
        
        style.configure("TCheckbutton", background=self.bg_card, foreground=self.text_primary, font=("Segoe UI", 10))
        
        style.configure("TEntry", fieldbackground=self.bg_secondary, foreground=self.text_primary, font=("Segoe UI", 10), padding=5)
        
        style.configure("TProgressbar", background=self.accent_color, troughcolor=self.bg_secondary)

    def create_header(self):
        header = ttk.Frame(self.root, style="Header.TFrame", height=80)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        
        content = ttk.Frame(header, style="Header.TFrame")
        content.pack(fill="both", expand=True, padx=20, pady=15)
        
        title = ttk.Label(content, text="⚙️  EXE Creator Pro", style="Header.TLabel")
        title.pack(anchor="w")
        
        subtitle = ttk.Label(content, text="Converti script Python in eseguibili Windows", 
                            background=self.bg_secondary, foreground=self.text_secondary, font=("Segoe UI", 9))
        subtitle.pack(anchor="w", pady=(5, 0))

    def create_status_frame(self, parent):
        frame = ttk.Frame(parent, style="Card.TFrame")
        frame.pack(fill="x", pady=(0, 15), padx=5, ipady=10, ipadx=10)
        
        title = ttk.Label(frame, text="🔧 Stato Ambiente", style="Section.TLabel")
        title.pack(anchor="w", pady=(0, 8))
        
        self.env_status_label = ttk.Label(frame, text="Non configurato", style="Info.TLabel", justify="left")
        self.env_status_label.pack(anchor="w", pady=(0, 10))
        
        self.setup_env_btn = ttk.Button(frame, text="Configura Ambiente", command=self.setup_environment, style="Success.TButton")
        self.setup_env_btn.pack(fill="x", ipady=8)

    def create_software_name_frame(self, parent):
        frame = ttk.Frame(parent, style="Card.TFrame")
        frame.pack(fill="x", pady=(0, 15), padx=5, ipady=10, ipadx=10)
        
        label = ttk.Label(frame, text="📦 Nome del Software", style="Section.TLabel")
        label.pack(anchor="w", pady=(0, 8))
        
        self.software_name = ttk.Entry(frame, width=50)
        self.software_name.pack(fill="x", ipady=8)

    def create_script_frame(self, parent):
        frame = ttk.Frame(parent, style="Card.TFrame")
        frame.pack(fill="x", pady=(0, 15), padx=5, ipady=10, ipadx=10)
        
        label = ttk.Label(frame, text="📄 Script Python", style="Section.TLabel")
        label.pack(anchor="w", pady=(0, 8))
        
        self.attach_btn = ttk.Button(frame, text="Seleziona Script", command=self.attach_script, style="Primary.TButton")
        self.attach_btn.pack(fill="x", ipady=8, pady=(0, 8))
        
        self.script_label = ttk.Label(frame, text="Nessuno script selezionato", style="Info.TLabel")
        self.script_label.pack(anchor="w")

    def create_options_frame(self, parent):
        frame = ttk.Frame(parent, style="Card.TFrame")
        frame.pack(fill="x", pady=(0, 15), padx=5, ipady=10, ipadx=10)
        
        label = ttk.Label(frame, text="🎛️ Opzioni Build", style="Section.TLabel")
        label.pack(anchor="w", pady=(0, 8))
        
        self.console_var = tk.BooleanVar()
        console_check = ttk.Checkbutton(frame, text="📺 Mostra console all'avvio", variable=self.console_var)
        console_check.pack(anchor="w", pady=5)
        
        self.icon_var = tk.BooleanVar()
        icon_check = ttk.Checkbutton(frame, text="🎨 Usa icona personalizzata", variable=self.icon_var, command=self.toggle_icon_btn)
        icon_check.pack(anchor="w", pady=5)
        
        self.icon_frame = ttk.Frame(frame, style="Card.TFrame")
        self.icon_frame.pack(fill="x", pady=(5, 0))
        self.icon_frame.pack_forget()
        
        self.load_icon_btn = ttk.Button(self.icon_frame, text="Carica Icona (.ico)", command=self.load_icon, style="Primary.TButton")
        self.load_icon_btn.pack(fill="x", ipady=8, pady=(0, 8))
        
        self.icon_label = ttk.Label(self.icon_frame, text="", style="Info.TLabel")
        self.icon_label.pack(anchor="w")

    def create_dependencies_frame(self, parent):
        frame = ttk.Frame(parent, style="Card.TFrame")
        frame.pack(fill="x", pady=(0, 15), padx=5, ipady=10, ipadx=10)
        
        label = ttk.Label(frame, text="📦 Gestione Dipendenze", style="Section.TLabel")
        label.pack(anchor="w", pady=(0, 8))
        
        buttons_frame = ttk.Frame(frame, style="Card.TFrame")
        buttons_frame.pack(fill="x", pady=(0, 8))
        
        self.analyze_deps_btn = ttk.Button(buttons_frame, text="Analizza Dipendenze", command=self.analyze_dependencies, style="Primary.TButton")
        self.analyze_deps_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.load_req_btn = ttk.Button(buttons_frame, text="Carica requirements.txt", command=self.load_requirements_file, style="Primary.TButton")
        self.load_req_btn.pack(side="left", fill="x", expand=True)
        
        deps_label = ttk.Label(frame, text="Dipendenze (una per riga):", style="Info.TLabel")
        deps_label.pack(anchor="w", pady=(0, 5))
        
        scroll_frame = ttk.Frame(frame, style="Card.TFrame")
        scroll_frame.pack(fill="both", expand=True, pady=(0, 8))
        
        scrollbar = ttk.Scrollbar(scroll_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.deps_text = tk.Text(scroll_frame, height=5, font=("Courier", 9), bg=self.bg_secondary, fg=self.text_primary, insertbackground=self.accent_color)
        self.deps_text.pack(fill="both", expand=True, side="left")
        self.deps_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.deps_text.yview)
        
        actions_frame = ttk.Frame(frame, style="Card.TFrame")
        actions_frame.pack(fill="x")
        
        self.install_deps_btn = ttk.Button(actions_frame, text="Installa Dipendenze", command=self.install_dependencies, style="Success.TButton")
        self.install_deps_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.cleanup_btn = ttk.Button(actions_frame, text="Pulisci Ambiente", command=self.cleanup_environment, style="Primary.TButton")
        self.cleanup_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.cancel_btn = ttk.Button(actions_frame, text="Cancella", command=self.cancel_installation_process, style="Danger.TButton")
        self.cancel_btn.pack(side="left", fill="x", expand=True)
        self.cancel_btn.pack_forget()
        
        self.progress_frame = ttk.Frame(frame, style="Card.TFrame")
        self.progress_frame.pack(fill="x", pady=(8, 0))
        self.progress_frame.pack_forget()
        
        self.progress_label = ttk.Label(self.progress_frame, text="", style="Info.TLabel")
        self.progress_label.pack(anchor="w", pady=(0, 5))
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='indeterminate')
        self.progress_bar.pack(fill="x", ipady=4)

    def create_main_button(self, parent):
        frame = ttk.Frame(parent, style="TFrame")
        frame.pack(fill="x", pady=(0, 15))
        
        self.create_btn = ttk.Button(frame, text="✨ CREA EXE", command=self.create_exe, style="Primary.TButton")
        self.create_btn.pack(fill="x", ipady=12)

    def create_output_frame(self, parent):
        frame = ttk.Frame(parent, style="Card.TFrame")
        frame.pack(fill="both", expand=True, padx=5, ipady=10, ipadx=10)
        
        label = ttk.Label(frame, text="📋 Output", style="Section.TLabel")
        label.pack(anchor="w", pady=(0, 8))
        
        scroll_frame = ttk.Frame(frame, style="Card.TFrame")
        scroll_frame.pack(fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(scroll_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.output_text = tk.Text(scroll_frame, height=15, font=("Courier", 9), bg=self.bg_secondary, fg=self.text_primary, insertbackground=self.accent_color, wrap="word")
        self.output_text.pack(fill="both", expand=True, side="left")
        self.output_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.output_text.yview)
        
        self.output_text.tag_config("success", foreground=self.success_color)
        self.output_text.tag_config("error", foreground=self.error_color)
        self.output_text.tag_config("warning", foreground=self.warning_color)
        self.output_text.tag_config("info", foreground=self.accent_color)

    def get_venv_python_path(self):
        if os.name == 'nt':
            return self.venv_path / "Scripts" / "python.exe"
        else:
            return self.venv_path / "bin" / "python"

    def check_environment_status(self):
        if not self.venv_path.exists():
            self.env_status_label.config(text="❌ Non configurato", foreground=self.error_color)
            self.create_btn.config(state="disabled")
            return False
        
        if not self.venv_python.exists():
            self.env_status_label.config(text="❌ Python mancante", foreground=self.error_color)
            self.create_btn.config(state="disabled")
            return False
        
        try:
            result = subprocess.run([str(self.venv_python), "-m", "pip", "show", "pyinstaller"], capture_output=True, text=True)
            if result.returncode == 0:
                self.env_status_label.config(text="✅ Pronto", foreground=self.success_color)
                self.create_btn.config(state="normal")
                return True
            else:
                self.env_status_label.config(text="⚠️ PyInstaller non trovato", foreground=self.warning_color)
                self.create_btn.config(state="disabled")
                return False
        except Exception:
            self.env_status_label.config(text="❌ Errore", foreground=self.error_color)
            self.create_btn.config(state="disabled")
            return False

    def log_output(self, message, tag=""):
        self.output_text.insert(tk.END, message + "\n", tag)
        self.output_text.see(tk.END)
        self.output_text.update()

    def setup_environment(self):
        self.output_text.delete(1.0, tk.END)
        self.log_output("🔧 Configurazione ambiente...", "info")
        
        try:
            if not self.venv_path.exists():
                self.log_output("📁 Creazione ambiente virtuale...", "info")
                venv.create(self.venv_path, with_pip=True)
                self.log_output("✅ Ambiente creato!", "success")
            
            self.log_output("🔄 Aggiornamento pip...", "info")
            subprocess.run([str(self.venv_python), "-m", "pip", "install", "--upgrade", "pip"], capture_output=True, text=True)
            self.log_output("✅ Pip aggiornato!", "success")
            
            self.log_output("📦 Installazione PyInstaller...", "info")
            result = subprocess.run([str(self.venv_python), "-m", "pip", "install", "pyinstaller"], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log_output("✅ PyInstaller installato!", "success")
                self.check_environment_status()
                messagebox.showinfo("Successo", "Ambiente configurato!")
            else:
                self.log_output("❌ Errore: " + result.stderr, "error")
                messagebox.showerror("Errore", "Errore nell'installazione")
        except Exception as e:
            self.log_output(f"❌ Errore: {str(e)}", "error")
            messagebox.showerror("Errore", str(e))

    def get_problematic_packages(self):
        return {
            'typing': 'Backport obsoleto',
            'pathlib': 'Backport obsoleto',
            'enum34': 'Backport obsoleto',
            'functools32': 'Backport obsoleto',
            'importlib-metadata': 'Conflitti con PyInstaller',
            'backports.functools-lru-cache': 'Backport obsoleto',
        }

    def detect_problematic_packages(self):
        if not self.check_environment_status():
            return []
        
        problematic = self.get_problematic_packages()
        found_problems = []
        
        try:
            result = subprocess.run([str(self.venv_python), "-m", "pip", "list", "--format=freeze"], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                for package_line in result.stdout.strip().split('\n'):
                    if '==' in package_line:
                        package_name = package_line.split('==')[0].lower()
                        for prob_package in problematic.keys():
                            if package_name == prob_package.lower():
                                found_problems.append({'name': prob_package, 'reason': problematic[prob_package]})
        except Exception as e:
            self.log_output(f"⚠️ Errore: {str(e)}", "warning")
        
        return found_problems

    def remove_problematic_packages(self, packages_to_remove):
        if not packages_to_remove:
            return True
        
        self.log_output(f"🧹 Rimozione {len(packages_to_remove)} pacchetti...", "warning")
        
        success_count = 0
        failed_removals = []
        
        for package_info in packages_to_remove:
            package_name = package_info['name']
            self.log_output(f"🗑️ Rimozione {package_name}...", "info")
            
            try:
                result = subprocess.run([str(self.venv_python), "-m", "pip", "uninstall", package_name, "-y"], capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    self.log_output(f"✅ {package_name} rimosso", "success")
                    success_count += 1
                else:
                    self.log_output(f"❌ Errore: {package_name}", "error")
                    failed_removals.append(package_name)
            except Exception as e:
                self.log_output(f"❌ Errore: {str(e)}", "error")
                failed_removals.append(package_name)
        
        self.log_output(f"📊 Rimossi: {success_count}, Fallimenti: {len(failed_removals)}", "info")
        return len(failed_removals) == 0

    def cleanup_environment(self):
        if not self.check_environment_status():
            messagebox.showerror("Errore", "Configura ambiente prima.")
            return
        
        self.log_output("🔍 Ricerca pacchetti problematici...", "info")
        problematic_packages = self.detect_problematic_packages()
        
        if not problematic_packages:
            self.log_output("✅ Nessun pacchetto problematico", "success")
            messagebox.showinfo("OK", "Ambiente pulito")
            return
        
        response = messagebox.askyesno("Pacchetti Problematici", f"Trovati {len(problematic_packages)} pacchetti\n\nRimuoverli?")
        
        if response:
            success = self.remove_problematic_packages(problematic_packages)
            if success:
                messagebox.showinfo("Successo", "Pacchetti rimossi!")
            else:
                messagebox.showwarning("Attenzione", "Alcuni non rimossi")
        else:
            self.log_output("❌ Annullato", "warning")

    def auto_cleanup_before_build(self):
        self.log_output("🔍 Controllo pacchetti...", "info")
        problematic_packages = self.detect_problematic_packages()
        
        if problematic_packages:
            self.log_output(f"⚠️ Trovati {len(problematic_packages)}, rimossione...", "warning")
            return self.remove_problematic_packages(problematic_packages)
        else:
            self.log_output("✅ OK", "success")
            return True

    def get_package_mapping(self):
        return {
            'cv2': 'opencv-python', 'PIL': 'Pillow', 'skimage': 'scikit-image',
            'sklearn': 'scikit-learn', 'yaml': 'PyYAML', 'serial': 'pyserial',
            'psutil': 'psutil', 'win32api': 'pywin32', 'win32con': 'pywin32',
            'win32gui': 'pywin32', 'pythoncom': 'pywin32', 'pywintypes': 'pywin32',
            'OpenGL': 'PyOpenGL', 'wx': 'wxPython', 'PySide2': 'PySide2',
            'PySide6': 'PySide6', 'PyQt5': 'PyQt5', 'PyQt6': 'PyQt6',
            'kivy': 'Kivy', 'telegram': 'python-telegram-bot', 'discord': 'discord.py',
            'bs4': 'beautifulsoup4', 'lxml': 'lxml', 'pymongo': 'pymongo',
            'sqlalchemy': 'SQLAlchemy', 'flask': 'Flask', 'django': 'Django',
            'fastapi': 'fastapi', 'streamlit': 'streamlit', 'dash': 'dash',
            'plotly': 'plotly', 'seaborn': 'seaborn', 'matplotlib': 'matplotlib',
            'pandas': 'pandas', 'numpy': 'numpy', 'scipy': 'scipy',
            'requests': 'requests', 'aiohttp': 'aiohttp', 'selenium': 'selenium',
            'pytest': 'pytest', 'paramiko': 'paramiko', 'fabric': 'fabric',
            'celery': 'celery', 'redis': 'redis', 'psycopg2': 'psycopg2-binary',
            'mysql': 'mysql-connector-python', 'cx_Oracle': 'cx_Oracle',
        }

    def map_imports_to_packages(self, imports):
        mapping = self.get_package_mapping()
        return [mapping.get(imp, imp) for imp in imports]

    def extract_imports_from_file(self, filepath):
        imports = set()
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.add(alias.name.split('.')[0])
                    elif isinstance(node, ast.ImportFrom) and node.module:
                        imports.add(node.module.split('.')[0])
            except SyntaxError:
                import_patterns = [r'^\s*import\s+([a-zA-Z_][a-zA-Z0-9_]*)', r'^\s*from\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+import']
                for line in content.split('\n'):
                    for pattern in import_patterns:
                        match = re.match(pattern, line)
                        if match:
                            imports.add(match.group(1))
        except Exception as e:
            self.log_output(f"❌ Errore: {str(e)}", "error")
        
        return imports

    def filter_standard_library(self, imports):
        standard_modules = {
            'os', 'sys', 'json', 'csv', 're', 'time', 'datetime', 'random',
            'math', 'collections', 'itertools', 'functools', 'operator',
            'pathlib', 'urllib', 'http', 'socket', 'threading', 'multiprocessing',
            'subprocess', 'logging', 'argparse', 'configparser', 'pickle',
            'sqlite3', 'tkinter', 'unittest', 'doctest', 'pdb', 'profile',
            'traceback', 'warnings', 'typing', 'enum', 'dataclasses',
            'abc', 'contextlib', 'copy', 'weakref', 'gc', 'inspect',
            'ast', 'keyword', 'token', 'tokenize', 'parser', 'symbol',
            'email', 'html', 'xml', 'base64', 'binascii', 'struct',
            'codecs', 'locale', 'calendar', 'heapq', 'bisect', 'array',
            'queue', 'sched', 'mutex', 'string', 'textwrap', 'unicodedata',
            'stringprep', 'readline', 'rlcompleter', 'io', 'tempfile',
            'glob', 'fnmatch', 'linecache', 'shutil', 'macpath', 'stat',
            'fileinput', 'filecmp', 'zipfile', 'tarfile', 'gzip', 'bz2',
            'lzma', 'zlib', 'hashlib', 'hmac', 'secrets', 'ssl', 'imaplib',
            'nntplib', 'poplib', 'smtplib', 'telnetlib', 'uuid', 'socketserver',
            'wsgiref', 'ftplib', 'platform', 'errno', 'ctypes', 'mmap',
            'winreg', 'winsound', 'msvcrt', 'atexit', 'signal', 'pyclbr',
            'venv', '__future__', 'builtins', '__builtin__',
        }
        return [imp for imp in imports if imp not in standard_modules]

    def analyze_dependencies(self):
        if not self.script_path:
            messagebox.showerror("Errore", "Seleziona uno script prima.")
            return
        
        if not os.path.exists(self.script_path):
            messagebox.showerror("Errore", "File non esiste più.")
            self.script_path = ""
            self.script_label.config(text="Nessuno script selezionato")
            return
        
        self.log_output("="*60, "info")
        self.log_output(f"🔍 Analisi: {os.path.basename(self.script_path)}", "info")
        
        imports = self.extract_imports_from_file(self.script_path)
        external_imports = self.filter_standard_library(imports)
        external_packages = self.map_imports_to_packages(external_imports)
        
        self.log_output(f"📦 Trovati {len(external_packages)} pacchetti:", "info")
        
        if external_packages:
            deps_text = "\n".join(sorted(external_packages))
            self.deps_text.delete(1.0, tk.END)
            self.deps_text.insert(1.0, deps_text)
            
            for dep in sorted(external_packages):
                self.log_output(f"  - {dep}", "info")
            
            self.log_output("✅ Inseriti nel campo", "success")
        else:
            self.log_output("ℹ️ Nessuna dipendenza esterna", "info")
            self.deps_text.delete(1.0, tk.END)
        
        self.log_output("="*60, "info")

    def load_requirements_file(self):
        req_file = filedialog.askopenfilename(filetypes=[("requirements.txt", "requirements.txt"), ("Text files", "*.txt")])
        
        if not req_file:
            return
        
        try:
            with open(req_file, 'r', encoding='utf-8') as f:
                requirements = []
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        package = line.split('==')[0].split('>=')[0].split('<=')[0]
                        requirements.append(package.strip())
            
            if requirements:
                self.deps_text.delete(1.0, tk.END)
                self.deps_text.insert(1.0, "\n".join(requirements))
                self.log_output(f"📄 Caricate {len(requirements)} dipendenze", "success")
                messagebox.showinfo("OK", f"Caricate {len(requirements)} dipendenze")
            else:
                messagebox.showinfo("Info", "Nessuna dipendenza trovata")
        except Exception as e:
            self.log_output(f"❌ Errore: {str(e)}", "error")
            messagebox.showerror("Errore", str(e))

    def install_dependencies(self):
        if not self.check_environment_status():
            messagebox.showerror("Errore", "Configura ambiente prima.")
            return
        
        if self.installation_thread and self.installation_thread.is_alive():
            messagebox.showwarning("Attenzione", "Un'installazione è in corso.")
            return
        
        deps_content = self.deps_text.get(1.0, tk.END).strip()
        if not deps_content:
            messagebox.showinfo("Info", "Nessuna dipendenza da installare.")
            return
        
        dependencies = [dep.strip() for dep in deps_content.split('\n') if dep.strip()]
        
        if not dependencies:
            messagebox.showinfo("Info", "Nessuna dipendenza valida.")
            return
        
        self.cancel_installation = False
        self.show_installation_ui(True)
        
        self.installation_thread = threading.Thread(target=self.install_dependencies_worker, args=(dependencies,), daemon=True)
        self.installation_thread.start()

    def install_dependencies_worker(self, dependencies):
        try:
            self.message_queue.put(("log", f"📦 Installazione di {len(dependencies)} dipendenze...", "info"))
            
            success_count = 0
            failed_deps = []
            
            for i, dep in enumerate(dependencies, 1):
                if self.cancel_installation:
                    self.message_queue.put(("log", "❌ Annullato", "warning"))
                    self.message_queue.put(("finished", {"cancelled": True}))
                    return
                
                self.message_queue.put(("progress", f"Installazione {dep} ({i}/{len(dependencies)})"))
                self.message_queue.put(("log", f"📥 {dep}...", "info"))
                
                try:
                    result = subprocess.run([str(self.venv_python), "-m", "pip", "install", dep], capture_output=True, text=True, timeout=120)
                    
                    if result.returncode == 0:
                        self.message_queue.put(("log", f"✅ {dep} OK", "success"))
                        success_count += 1
                    else:
                        self.message_queue.put(("log", f"❌ Errore: {dep}", "error"))
                        failed_deps.append(dep)
                except subprocess.TimeoutExpired:
                    self.message_queue.put(("log", f"⏱️ Timeout: {dep}", "warning"))
                    failed_deps.append(dep)
                except Exception as e:
                    self.message_queue.put(("log", f"❌ {dep}: {str(e)}", "error"))
                    failed_deps.append(dep)
            
            self.message_queue.put(("log", f"📊 Successi: {success_count}, Fallimenti: {len(failed_deps)}", "info"))
            self.message_queue.put(("finished", {"success_count": success_count, "failed_deps": failed_deps, "cancelled": False}))
            
        except Exception as e:
            self.message_queue.put(("error", f"Errore: {str(e)}", "error"))

    def cancel_installation_process(self):
        if messagebox.askyesno("Conferma", "Cancellare l'installazione?"):
            self.cancel_installation = True

    def check_message_queue(self):
        try:
            while True:
                msg_data = self.message_queue.get_nowait()
                
                if len(msg_data) == 3:
                    message_type, message, tag = msg_data
                else:
                    message_type, message = msg_data
                    tag = ""
                
                if message_type == "log":
                    self.log_output(message, tag)
                elif message_type == "progress":
                    self.progress_label.config(text=message)
                elif message_type == "finished":
                    self.installation_finished(message)
                elif message_type == "error":
                    self.installation_error(message)
        except queue.Empty:
            pass
        
        self.root.after(100, self.check_message_queue)

    def periodic_ui_update(self):
        self.check_environment_status()
        self.root.after(1000, self.periodic_ui_update)

    def show_installation_ui(self, show):
        if show:
            self.progress_frame.pack(fill="x", pady=(8, 0))
            self.cancel_btn.pack(side="left", fill="x", expand=True)
            self.progress_bar.start()
        else:
            self.progress_frame.pack_forget()
            self.cancel_btn.pack_forget()
            self.progress_bar.stop()
            self.progress_label.config(text="")

    def installation_finished(self, result):
        self.show_installation_ui(False)
        
        if result.get("cancelled"):
            messagebox.showinfo("Annullato", "Installazione annullata.")
        elif result.get("failed_deps"):
            messagebox.showwarning("Attenzione", f"Falliti: {', '.join(result['failed_deps'])}")
        else:
            messagebox.showinfo("Successo", "Tutte le dipendenze installate!")

    def installation_error(self, error_msg):
        self.show_installation_ui(False)
        messagebox.showerror("Errore", error_msg)

    def attach_script(self):
        script_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        if script_path:
            self.script_path = script_path
            self.script_label.config(text=f"✓ {os.path.basename(script_path)}")
            self.deps_text.delete(1.0, tk.END)
            self.output_text.delete(1.0, tk.END)
            self.log_output(f"✅ Script: {os.path.basename(script_path)}", "success")
    
    def toggle_icon_btn(self):
        if self.icon_var.get():
            self.icon_frame.pack(fill="x", pady=(5, 0))
        else:
            self.icon_frame.pack_forget()
            self.icon_path = ""
            self.icon_label.config(text="")

    def load_icon(self):
        icon_path = filedialog.askopenfilename(filetypes=[("Icon files", "*.ico")])
        if icon_path:
            self.icon_path = icon_path
            self.icon_label.config(text=f"✓ {os.path.basename(icon_path)}")

    def cleanup_build_directories(self):
        script_dir = os.path.dirname(self.script_path)
        build_dir = os.path.join(script_dir, "build")
        dist_dir = os.path.join(script_dir, "dist")
        
        for dir_path in [build_dir, dist_dir]:
            if os.path.exists(dir_path):
                try:
                    self.log_output(f"🧹 Pulizia: {os.path.basename(dir_path)}", "info")
                    shutil.rmtree(dir_path)
                    self.log_output("✅ Rimossa", "success")
                    time.sleep(0.5)
                except Exception as e:
                    self.log_output(f"⚠️ Impossibile: {str(e)}", "warning")

    def create_exe(self):
        if not self.script_path:
            messagebox.showerror("Errore", "Seleziona uno script.")
            return

        if not self.check_environment_status():
            messagebox.showerror("Errore", "Configura ambiente prima.")
            return

        deps_content = self.deps_text.get(1.0, tk.END).strip()
        if deps_content and messagebox.askyesno("Dipendenze", "Installare dipendenze ora?"):
            self.install_dependencies()
            return

        self.output_text.delete(1.0, tk.END)
        
        self.log_output("🧹 Pulizia...", "info")
        if not self.auto_cleanup_before_build():
            self.log_output("⚠️ Alcuni pacchetti non rimossi, continuo...", "warning")
        
        self.cleanup_build_directories()
        
        cmd = [str(self.venv_python), "-m", "PyInstaller", "--onefile"]
        
        if not self.console_var.get():
            cmd.append("--noconsole")

        icon_enabled = False
        if self.icon_path and os.path.exists(self.icon_path):
            try:
                with open(self.icon_path, 'rb') as f:
                    f.read(1)
                cmd.extend(["--icon", self.icon_path])
                icon_enabled = True
                self.log_output(f"🎨 Icona: {os.path.basename(self.icon_path)}", "info")
            except Exception as e:
                self.log_output(f"⚠️ Icona non usabile: {str(e)}", "warning")

        software_name = self.software_name.get().strip()
        if software_name:
            cmd.extend(["--name", software_name])

        cmd.append(self.script_path)
        
        self.log_output("🚀 " + "="*60, "info")
        self.log_output("Comando:", "info")
        self.log_output(" ".join(cmd), "info")
        self.log_output("="*60, "info")
        
        success = self.run_pyinstaller(cmd)
        
        if not success and icon_enabled:
            self.log_output("\n⚠️ Riprovo senza icona...", "warning")
            cmd_no_icon = [c for c in cmd if c != "--icon" and c != self.icon_path]
            success = self.run_pyinstaller(cmd_no_icon)
        
        if success:
            dist_dir = os.path.join(os.path.dirname(self.script_path), "dist")
            if os.path.exists(dist_dir):
                exe_files = [f for f in os.listdir(dist_dir) if f.endswith('.exe')]
                if exe_files:
                    exe_path = os.path.join(dist_dir, exe_files[0])
                    self.log_output(f"📁 EXE: {exe_path}", "success")
            
            messagebox.showinfo("Successo", "EXE creato!")
        else:
            messagebox.showerror("Errore", "Creazione fallita.")

    def run_pyinstaller(self, cmd):
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, universal_newlines=True)
            
            for line in process.stdout:
                self.log_output(line.rstrip(), "info")
            
            process.wait()
            
            if process.returncode == 0:
                self.log_output("\n🎉 EXE creato!", "success")
                return True
            else:
                self.log_output(f"\n❌ Errore (codice: {process.returncode})", "error")
                return False
        except Exception as e:
            self.log_output(f"\n❌ Errore: {str(e)}", "error")
            return False


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernExeCreatorApp(root)
    root.mainloop()
