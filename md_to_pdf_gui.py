#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown to PDF Converter - GUI
MD dosyalarını PDF'e çeviren programın grafik arayüzü
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import threading
import os
import subprocess
import platform
import tempfile
from md_to_pdf import convert_md_to_pdf, get_default_css


class MarkdownToPDFGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Markdown to PDF Converter 📄")
        self.root.geometry("900x900")
        self.root.resizable(True, True)
        
        # Değişkenler
        self.md_file_path = tk.StringVar()
        self.md_mode = tk.StringVar(value="file")  # "file" veya "paste"
        self.css_file_path = tk.StringVar()
        self.css_code = tk.StringVar()
        self.css_mode = tk.StringVar(value="file")  # "file" veya "code"
        self.output_file_path = tk.StringVar()
        self.is_processing = False
        self.css_text_widget = None
        self.md_text_widget = None
        
        # Stil ayarları
        self.setup_styles()
        
        # UI oluştur
        self.create_widgets()
        
        # Pencereyi ortala
        self.center_window()
    
    def setup_styles(self):
        """Modern görünüm için stil ayarları"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Buton stilleri
        style.configure('Action.TButton', padding=10, font=('Helvetica', 10))
        style.configure('Browse.TButton', padding=5, font=('Helvetica', 9))
    
    def center_window(self):
        """Pencereyi ekranın ortasına yerleştir"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Ana widget'ları oluştur"""
        # Ana container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Grid ağırlıkları
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Başlık
        title_label = ttk.Label(
            main_frame,
            text="📄 Markdown to PDF Converter",
            font=('Helvetica', 18, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Markdown girişi için LabelFrame
        md_label_frame = ttk.LabelFrame(main_frame, text="Markdown İçeriği", padding="10")
        md_label_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        md_label_frame.columnconfigure(0, weight=1)
        
        # Markdown modu seçimi (Radio buttons)
        md_mode_frame = ttk.Frame(md_label_frame)
        md_mode_frame.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        ttk.Radiobutton(
            md_mode_frame,
            text="Dosyadan Seç",
            variable=self.md_mode,
            value="file",
            command=self.toggle_md_mode
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Radiobutton(
            md_mode_frame,
            text="İçeriği Yapıştır",
            variable=self.md_mode,
            value="paste",
            command=self.toggle_md_mode
        ).pack(side=tk.LEFT)
        
        # Markdown dosyası seçimi frame
        self.md_file_frame = ttk.Frame(md_label_frame)
        self.md_file_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        self.md_file_frame.columnconfigure(0, weight=1)
        
        ttk.Label(
            self.md_file_frame,
            text="Markdown Dosyası:",
            font=('Helvetica', 9)
        ).grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        md_file_input_frame = ttk.Frame(self.md_file_frame)
        md_file_input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        md_file_input_frame.columnconfigure(0, weight=1)
        
        self.md_entry = ttk.Entry(md_file_input_frame, textvariable=self.md_file_path, width=50)
        self.md_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(
            md_file_input_frame,
            text="Gözat...",
            command=self.browse_md_file,
            style='Browse.TButton'
        ).grid(row=0, column=1)
        
        # Markdown içeriği yapıştırma frame
        self.md_paste_frame = ttk.Frame(md_label_frame)
        self.md_paste_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        self.md_paste_frame.columnconfigure(0, weight=1)
        self.md_paste_frame.rowconfigure(1, weight=1)
        
        ttk.Label(
            self.md_paste_frame,
            text="Markdown İçeriği:",
            font=('Helvetica', 9)
        ).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        md_paste_container = ttk.Frame(self.md_paste_frame)
        md_paste_container.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        md_paste_container.columnconfigure(0, weight=1)
        md_paste_container.rowconfigure(0, weight=1)
        
        self.md_text_widget = scrolledtext.ScrolledText(
            md_paste_container,
            height=12,
            width=70,
            font=('Courier', 10),
            wrap=tk.WORD
        )
        self.md_text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Placeholder text
        self.md_text_widget.insert('1.0', '# Markdown içeriğinizi buraya yapıştırın...\n\nÖrnek:\n# Başlık\n\nBu bir paragraf.\n\n- Liste öğesi 1\n- Liste öğesi 2')
        self.md_text_widget.config(foreground='gray')
        self.md_text_widget.bind('<FocusIn>', self._on_md_text_focus_in)
        self.md_text_widget.bind('<FocusOut>', self._on_md_text_focus_out)
        
        # Başlangıçta dosya modunu göster
        self.toggle_md_mode()
        
        # Grid ağırlıkları
        md_label_frame.rowconfigure(1, weight=1)
        
        # CSS seçimi (opsiyonel)
        css_label_frame = ttk.LabelFrame(main_frame, text="CSS Stilleri (Opsiyonel)", padding="10")
        css_label_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        css_label_frame.columnconfigure(1, weight=1)
        
        # CSS modu seçimi (Radio buttons)
        css_mode_frame = ttk.Frame(css_label_frame)
        css_mode_frame.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
        
        ttk.Radiobutton(
            css_mode_frame,
            text="CSS Dosyasından",
            variable=self.css_mode,
            value="file",
            command=self.toggle_css_mode
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Radiobutton(
            css_mode_frame,
            text="CSS Kodunu Doğrudan Gir",
            variable=self.css_mode,
            value="code",
            command=self.toggle_css_mode
        ).pack(side=tk.LEFT)
        
        # CSS dosyası seçimi
        self.css_file_frame = ttk.Frame(css_label_frame)
        self.css_file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        self.css_file_frame.columnconfigure(0, weight=1)
        
        ttk.Label(
            self.css_file_frame,
            text="CSS Dosyası:",
            font=('Helvetica', 9)
        ).grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        self.css_entry = ttk.Entry(self.css_file_frame, textvariable=self.css_file_path, width=50)
        self.css_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(
            self.css_file_frame,
            text="Gözat...",
            command=self.browse_css_file,
            style='Browse.TButton'
        ).grid(row=0, column=2, padx=(0, 5))
        
        ttk.Button(
            self.css_file_frame,
            text="Temizle",
            command=self.clear_css_file,
            style='Browse.TButton'
        ).grid(row=0, column=3)
        
        # CSS kod girişi
        self.css_code_frame = ttk.Frame(css_label_frame)
        self.css_code_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        self.css_code_frame.columnconfigure(0, weight=1)
        self.css_code_frame.rowconfigure(1, weight=1)
        
        ttk.Label(
            self.css_code_frame,
            text="CSS Kodu:",
            font=('Helvetica', 9)
        ).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        css_code_container = ttk.Frame(self.css_code_frame)
        css_code_container.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        css_code_container.columnconfigure(0, weight=1)
        css_code_container.rowconfigure(0, weight=1)
        
        self.css_text_widget = scrolledtext.ScrolledText(
            css_code_container,
            height=8,
            width=70,
            font=('Courier', 9),
            wrap=tk.NONE
        )
        self.css_text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Varsayılan CSS'i yükle
        self.css_text_widget.insert('1.0', get_default_css())
        
        ttk.Button(
            self.css_code_frame,
            text="Varsayılan CSS'i Yükle",
            command=self.load_default_css,
            style='Browse.TButton'
        ).grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        
        # Başlangıçta dosya modunu göster
        self.toggle_css_mode()
        
        # Çıktı dosyası seçimi
        ttk.Label(
            main_frame,
            text="Çıktı PDF Dosyası:",
            font=('Helvetica', 10)
        ).grid(row=3, column=0, sticky=tk.W, pady=10)
        
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=3, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        output_frame.columnconfigure(0, weight=1)
        
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_file_path, width=50)
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(
            output_frame,
            text="Gözat...",
            command=self.browse_output_file,
            style='Browse.TButton'
        ).grid(row=0, column=1)
        
        ttk.Label(
            main_frame,
            text="(Boş bırakılırsa, markdown dosyasıyla aynı isimde oluşturulur)",
            font=('Helvetica', 8),
            foreground='gray'
        ).grid(row=4, column=1, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Ayırıcı
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20
        )
        
        # Dönüştür butonu
        self.convert_button = ttk.Button(
            main_frame,
            text="🔄 PDF'e Dönüştür",
            command=self.convert_to_pdf,
            style='Action.TButton'
        )
        self.convert_button.grid(row=6, column=0, columnspan=3, pady=20)
        
        # İlerleme çubuğu
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=400
        )
        self.progress.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Durum metni
        self.status_text = tk.StringVar(value="Hazır")
        self.status_label = ttk.Label(
            main_frame,
            textvariable=self.status_text,
            font=('Helvetica', 9),
            foreground='green'
        )
        self.status_label.grid(row=8, column=0, columnspan=3, pady=5)
        
        # Log alanı
        log_label = ttk.Label(
            main_frame,
            text="İşlem Logları:",
            font=('Helvetica', 10, 'bold')
        )
        log_label.grid(row=9, column=0, columnspan=3, sticky=tk.W, pady=(20, 5))
        
        self.log_text = scrolledtext.ScrolledText(
            main_frame,
            height=6,
            width=70,
            font=('Courier', 9),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.log_text.grid(row=10, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Grid ağırlıkları
        css_label_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(10, weight=1)
    
    def toggle_md_mode(self):
        """Markdown modu değiştiğinde görünümü güncelle"""
        if self.md_mode.get() == "file":
            self.md_file_frame.grid()
            self.md_paste_frame.grid_remove()
        else:
            self.md_file_frame.grid_remove()
            self.md_paste_frame.grid()
    
    def _on_md_text_focus_in(self, event):
        """Markdown text widget'a odaklanıldığında placeholder'ı temizle"""
        if self.md_text_widget.get('1.0', 'end-1c').strip().startswith('# Markdown içeriğinizi'):
            self.md_text_widget.delete('1.0', tk.END)
            self.md_text_widget.config(foreground='black')
    
    def _on_md_text_focus_out(self, event):
        """Markdown text widget'tan odak çıktığında boşsa placeholder ekle"""
        if not self.md_text_widget.get('1.0', 'end-1c').strip():
            self.md_text_widget.insert('1.0', '# Markdown içeriğinizi buraya yapıştırın...\n\nÖrnek:\n# Başlık\n\nBu bir paragraf.\n\n- Liste öğesi 1\n- Liste öğesi 2')
            self.md_text_widget.config(foreground='gray')
    
    def browse_md_file(self):
        """Markdown dosyası seç"""
        filename = filedialog.askopenfilename(
            title="Markdown Dosyası Seç",
            filetypes=[
                ("Markdown files", "*.md"),
                ("Markdown files", "*.markdown"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.md_file_path.set(filename)
            # Otomatik olarak çıktı dosyası yolunu ayarla
            if not self.output_file_path.get():
                output_path = Path(filename).with_suffix('.pdf')
                self.output_file_path.set(str(output_path))
            self.log_message(f"Markdown dosyası seçildi: {filename}")
    
    def browse_css_file(self):
        """CSS dosyası seç"""
        filename = filedialog.askopenfilename(
            title="CSS Dosyası Seç",
            filetypes=[
                ("CSS files", "*.css"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.css_file_path.set(filename)
            self.log_message(f"CSS dosyası seçildi: {filename}")
    
    def clear_css_file(self):
        """CSS dosyası yolunu temizle"""
        self.css_file_path.set("")
        self.log_message("CSS dosyası temizlendi, varsayılan CSS kullanılacak")
    
    def toggle_css_mode(self):
        """CSS modu değiştiğinde görünümü güncelle"""
        if self.css_mode.get() == "file":
            self.css_file_frame.grid()
            self.css_code_frame.grid_remove()
        else:
            self.css_file_frame.grid_remove()
            self.css_code_frame.grid()
    
    def load_default_css(self):
        """Varsayılan CSS'i yükle"""
        if self.css_text_widget:
            self.css_text_widget.delete('1.0', tk.END)
            self.css_text_widget.insert('1.0', get_default_css())
            self.log_message("Varsayılan CSS yüklendi")
    
    def browse_output_file(self):
        """Çıktı PDF dosyası seç"""
        filename = filedialog.asksaveasfilename(
            title="PDF Dosyasını Kaydet",
            defaultextension=".pdf",
            filetypes=[
                ("PDF files", "*.pdf"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.output_file_path.set(filename)
            self.log_message(f"Çıktı dosyası belirlendi: {filename}")
    
    def log_message(self, message):
        """Log mesajı ekle"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update_idletasks()
    
    def validate_inputs(self):
        """Girdileri doğrula"""
        # Markdown içeriği kontrolü
        if self.md_mode.get() == "file":
            if not self.md_file_path.get():
                messagebox.showerror("Hata", "Lütfen bir Markdown dosyası seçin!")
                return False
            
            md_path = Path(self.md_file_path.get())
            if not md_path.exists():
                messagebox.showerror("Hata", f"Markdown dosyası bulunamadı:\n{md_path}")
                return False
            
            if not md_path.suffix.lower() in ['.md', '.markdown', '.txt']:
                messagebox.showerror("Hata", "Lütfen geçerli bir Markdown dosyası seçin!")
                return False
        else:  # paste mode
            if not self.md_text_widget:
                messagebox.showerror("Hata", "Markdown içeriği girişi bulunamadı!")
                return False
            
            md_content = self.md_text_widget.get('1.0', tk.END).strip()
            # Placeholder kontrolü
            if not md_content or md_content.startswith('# Markdown içeriğinizi'):
                messagebox.showerror("Hata", "Lütfen Markdown içeriğini yapıştırın!")
                return False
        
        # CSS kontrolü (opsiyonel)
        if self.css_mode.get() == "file" and self.css_file_path.get():
            css_path = Path(self.css_file_path.get())
            if not css_path.exists():
                messagebox.showerror("Hata", f"CSS dosyası bulunamadı:\n{css_path}")
                return False
        
        return True
    
    def convert_to_pdf(self):
        """PDF'e dönüştür"""
        if self.is_processing:
            messagebox.showwarning("Uyarı", "Dönüştürme işlemi devam ediyor...")
            return
        
        if not self.validate_inputs():
            return
        
        # UI'ı güncelle
        self.is_processing = True
        self.convert_button.config(state=tk.DISABLED)
        self.progress.start()
        self.status_text.set("Dönüştürülüyor...")
        self.status_label.config(foreground='blue')
        self.log_message("\n" + "="*50)
        self.log_message("Dönüştürme işlemi başlatıldı...")
        
        # Thread'de çalıştır (UI donmasın diye)
        thread = threading.Thread(target=self._convert_thread)
        thread.daemon = True
        thread.start()
    
    def _convert_thread(self):
        """Dönüştürme işlemini thread'de çalıştır"""
        try:
            # Markdown içeriğini al
            if self.md_mode.get() == "file":
                md_file = self.md_file_path.get()
                output_file = self.output_file_path.get() if self.output_file_path.get() else None
                self.log_message(f"Kaynak: {md_file}")
            else:  # paste mode
                md_content = self.md_text_widget.get('1.0', tk.END).strip()
                # Geçici dosya oluştur
                with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as tmp_file:
                    tmp_file.write(md_content)
                    md_file = tmp_file.name
                self.log_message(f"Kaynak: Yapıştırılan içerik (geçici dosya: {md_file})")
                
                # Çıktı dosyası belirlenmemişse varsayılan isim kullan
                if not self.output_file_path.get():
                    output_file = "output.pdf"
                else:
                    output_file = self.output_file_path.get()
            
            # CSS moduna göre CSS'i belirle
            css_file = None
            css_string = None
            
            if self.css_mode.get() == "code":
                # CSS kodunu text widget'tan al
                if self.css_text_widget:
                    css_string = self.css_text_widget.get('1.0', tk.END).strip()
                    if css_string:
                        self.log_message(f"CSS: Kod olarak girildi ({len(css_string)} karakter)")
                    else:
                        self.log_message("CSS: Varsayılan CSS kullanılıyor")
            else:
                # CSS dosyasından
                css_file = self.css_file_path.get() if self.css_file_path.get() else None
                if css_file:
                    self.log_message(f"CSS: {css_file}")
                else:
                    self.log_message("CSS: Varsayılan CSS kullanılıyor")
            
            # Dönüştür
            result_path = convert_md_to_pdf(md_file, output_file, css_file, css_string)
            
            # Geçici dosyayı sil (eğer paste modundaysa)
            if self.md_mode.get() == "paste" and os.path.exists(md_file):
                try:
                    os.unlink(md_file)
                except:
                    pass
            
            # Başarılı
            self.root.after(0, self._conversion_success, result_path)
            
        except Exception as e:
            # Geçici dosyayı temizle (hata durumunda)
            if self.md_mode.get() == "paste" and 'md_file' in locals() and os.path.exists(md_file):
                try:
                    os.unlink(md_file)
                except:
                    pass
            # Hata
            self.root.after(0, self._conversion_error, str(e))
    
    def _conversion_success(self, output_path):
        """Dönüştürme başarılı"""
        self.is_processing = False
        self.progress.stop()
        self.convert_button.config(state=tk.NORMAL)
        self.status_text.set("✓ Başarılı!")
        self.status_label.config(foreground='green')
        self.log_message(f"✓ PDF başarıyla oluşturuldu: {output_path}")
        self.log_message("="*50 + "\n")
        
        # Başarı mesajı göster
        result = messagebox.askyesno(
            "Başarılı!",
            f"PDF başarıyla oluşturuldu!\n\n{output_path}\n\nDosyayı açmak ister misiniz?"
        )
        
        if result:
            try:
                if platform.system() == 'Darwin':  # macOS
                    subprocess.call(['open', output_path])
                elif platform.system() == 'Windows':
                    os.startfile(output_path)
                else:  # Linux
                    subprocess.call(['xdg-open', output_path])
            except Exception as e:
                self.log_message(f"Dosya açılırken hata: {e}")
    
    def _conversion_error(self, error_message):
        """Dönüştürme hatası"""
        self.is_processing = False
        self.progress.stop()
        self.convert_button.config(state=tk.NORMAL)
        self.status_text.set("✗ Hata!")
        self.status_label.config(foreground='red')
        self.log_message(f"✗ Hata: {error_message}")
        self.log_message("="*50 + "\n")
        
        messagebox.showerror("Hata", f"PDF oluşturulurken hata oluştu:\n\n{error_message}")


def main():
    """Ana fonksiyon"""
    root = tk.Tk()
    app = MarkdownToPDFGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()

