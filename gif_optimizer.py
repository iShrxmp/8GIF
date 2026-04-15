import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageSequence, ImageTk, ImageDraw
import threading
import os
import io
import math
import sys

def resource_path(relative_path):
    """PyInstaller ile paketlenmiş kaynakları bulur."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

LANG = {
    "TR": {
        "title": "8GIF",
        "load": "Yeni GIF Yükle",
        "orig_title": "Orijinal GIF",
        "mod_title": "Sonuç (Önizleme)",
        "crop_title": "Kırpma (Canvas'tan Seçiniz)",
        "res_title": "Yeniden Boyutlandır",
        "opt_title": "Optimizasyon",
        "btn_preview": "Önizlemeyi Güncelle",
        "btn_save": "Finalize & Kaydet",
        "discord_cb": "Discord Uyumlu (<10MB)",
        "mode_px": "Piksel (px)",
        "mode_perc": "Yüzde (%)",
        "slider_p": "Sıkıştırma Gücü: %",
        "discord_auto": "Sıkıştırma Gücü: Otomatik",
        "err_nofile": "Lütfen önce bir GIF yükleyin.",
        "log_ready": "Sistem hazır. Lütfen dosya yükleyin.",
        "log_analyzing": "Dosya analiz ediliyor: ",
        "log_discord_test": "Discord 10MB Limiti için test ediliyor...",
        "err_limit_warn": "10MB limitine inilemedi. Elde edilen en ufak dosya kaydedildi.",
        "log_saved": "İşaretlendi ve Kayıt Başarılı!",
        "log_preview_discord": "[ÖNİZLEME] Discord modu. Önizleme yalnızca temel kırpma/boyutlandırmayı gösterir. Otomatik sıkıştırma Kayıt sırasında hesaplanır.",
        "log_testing": "> Test ediliyor: %",
        "log_size": "=> Boyut: ",
        "log_err": "HATA: ",
        "log_prev_err": "Önizleme Hatası: ",
        "behavior": "Kırpma Davranışı:",
        "behav_adaptive": "Adaptive (Oranı Koru)",
        "behav_stretch": "Stretch (Tam Sığdır)",
        "shape": "Kırpma Maskesi (Şekil):",
        "shape_rect": "Rectangle (Dikdörtgen)",
        "shape_circle": "Circle (Daire/Elips)",
        "shape_star": "Star (Yıldız)",
        "shape_lasso": "Lasso (Serbest Çizim)"
    },
    "EN": {
        "title": "8GIF",
        "load": "Load New GIF",
        "orig_title": "Original GIF",
        "mod_title": "Result (Preview)",
        "crop_title": "Crop (Select on Canvas)",
        "res_title": "Resize",
        "opt_title": "Optimization",
        "btn_preview": "Update Preview",
        "btn_save": "Finalize & Save",
        "discord_cb": "Discord Friendly (<10MB)",
        "mode_px": "Pixels (px)",
        "mode_perc": "Percent (%)",
        "slider_p": "Compression Power: %",
        "discord_auto": "Compression: Auto",
        "err_nofile": "Please load a GIF first.",
        "log_ready": "System ready. Please load a file.",
        "log_analyzing": "Analyzing file: ",
        "log_discord_test": "Testing for Discord 10MB Limit...",
        "err_limit_warn": "Could not reach <10MB. Saved the smallest possible file instead.",
        "log_saved": "Finalized and Saved Successfully!",
        "log_preview_discord": "[PREVIEW] Discord mode selected. Auto-compression occurs during Save.",
        "log_testing": "> Testing compression %",
        "log_size": "=> Size: ",
        "log_err": "ERROR: ",
        "log_prev_err": "Preview Error: ",
        "behavior": "Crop Behavior:",
        "behav_adaptive": "Adaptive (Maintain Aspect)",
        "behav_stretch": "Stretch (Force Fit)",
        "shape": "Crop Mask (Shape):",
        "shape_rect": "Rectangle",
        "shape_circle": "Circle / Ellipse",
        "shape_star": "Star",
        "shape_lasso": "Free-style (Lasso)"
    },
    "DE": {
        "title": "8GIF",
        "load": "Neues GIF Laden",
        "orig_title": "Original GIF",
        "mod_title": "Ergebnis (Vorschau)",
        "crop_title": "Zuschneiden (Im Canvas wählen)",
        "res_title": "Größenänderung",
        "opt_title": "Optimierung",
        "btn_preview": "Vorschau Aktualisieren",
        "btn_save": "Abschließen & Speichern",
        "discord_cb": "Discord Kompatibel (<10MB)",
        "mode_px": "Pixel (px)",
        "mode_perc": "Prozent (%)",
        "slider_p": "Kompressionstärke: %",
        "discord_auto": "Kompression: Auto",
        "err_nofile": "Bitte laden Sie zuerst ein GIF.",
        "log_ready": "System bereit. Bitte Datei laden.",
        "log_analyzing": "Datei wird analysiert: ",
        "log_discord_test": "Prüfe auf Discord 10MB Limit...",
        "err_limit_warn": "<10MB konnte nicht erreicht werden. Die kleinstmögliche Datei wurde gespeichert.",
        "log_saved": "Erfolgreich Abgeschlossen und Gespeichert!",
        "log_preview_discord": "[VORSCHAU] Discord Modus. Auto-Kompression erfolgt beim Speichern.",
        "log_testing": "> Teste Kompression %",
        "log_size": "=> Größe: ",
        "log_err": "FEHLER: ",
        "log_prev_err": "Vorschau Fehler: ",
        "behavior": "Zuschneiden Verhalten:",
        "behav_adaptive": "Adaptiv (Seitenverhältnis beibehalten)",
        "behav_stretch": "Strecken (Erzwingen)",
        "shape": "Zuschneiden Maske (Form):",
        "shape_rect": "Rechteck",
        "shape_circle": "Kreis / Ellipse",
        "shape_star": "Stern",
        "shape_lasso": "Lasso"
    }
}

class GifOptimizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.lang = "EN"
        self.title(LANG[self.lang]["title"])
        self.geometry("1400x900")
        self.minsize(1100, 800)
        
        icon_path = resource_path("app_icon.ico")
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass

        self.filepath = None
        self.original_frames = []
        self.durations = []
        self.base_w = 0
        self.base_h = 0
        self.loop = 0
        self.transparency = None

        self.preview_scale = 1.0
        self.orig_tk_frames = []
        self.mod_tk_frames = []
        
        self.anim_running = False
        self.anim_idx_orig = 0
        self.anim_idx_mod = 0
        self.anim_id_orig = None
        self.anim_id_mod = None

        self.crop_drawing = False
        self.crop_start_x = 0
        self.crop_start_y = 0
        self.crop_rect_id = None
        self.lasso_points = []
        self.lasso_line_id = None

        self.create_ui()

    def tr(self, key):
        return LANG[self.lang].get(key, key)

    def log(self, message):
        def _append():
            self.console.configure(state="normal")
            self.console.insert("end", f"> {message}\n")
            self.console.see("end")
            self.console.configure(state="disabled")
        try:
            self.after(0, _append)
        except:
            pass

    def create_ui(self):
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=15, pady=5)
        
        self.btn_load = ctk.CTkButton(top_frame, text=self.tr("load"), font=ctk.CTkFont(weight="bold"), command=self.load_file)
        self.btn_load.pack(side="left", padx=(0, 8))

        self.btn_tools = ctk.CTkButton(top_frame, text="Image Tools", font=ctk.CTkFont(weight="bold"),
                                       fg_color="#5a3e8a", hover_color="#7a55b5", command=self.open_tools)
        self.btn_tools.pack(side="left")
        
        self.lang_var = ctk.StringVar(value=self.lang)
        self.lang_seg = ctk.CTkSegmentedButton(top_frame, values=["EN", "TR", "DE"], variable=self.lang_var, command=self.change_language)
        self.lang_seg.pack(side="right")

        middle_wrap = ctk.CTkFrame(self, fg_color="transparent")
        middle_wrap.pack(fill="both", expand=True, padx=15, pady=5)
        middle_wrap.grid_columnconfigure(0, weight=4) 
        middle_wrap.grid_columnconfigure(1, weight=4) 
        middle_wrap.grid_columnconfigure(2, weight=3) 
        middle_wrap.grid_rowconfigure(0, weight=1)

        self.frame_orig = ctk.CTkFrame(middle_wrap, corner_radius=10)
        self.frame_orig.grid(row=0, column=0, padx=5, sticky="nsew")
        self.frame_orig.grid_rowconfigure(1, weight=1)
        self.frame_orig.grid_columnconfigure(0, weight=1)
        
        self.lbl_orig_title = ctk.CTkLabel(self.frame_orig, text=self.tr("orig_title"), font=ctk.CTkFont(weight="bold", size=16))
        self.lbl_orig_title.grid(row=0, column=0, pady=10)
        self.canvas_orig = ctk.CTkCanvas(self.frame_orig, bg="#1a1a1a", highlightthickness=0)
        self.canvas_orig.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.lbl_orig_stats = ctk.CTkLabel(self.frame_orig, text="...", font=ctk.CTkFont(size=12))
        self.lbl_orig_stats.grid(row=2, column=0, pady=5)

        self.canvas_orig.bind("<ButtonPress-1>", self.on_crop_start)
        self.canvas_orig.bind("<B1-Motion>", self.on_crop_drag)
        self.canvas_orig.bind("<ButtonRelease-1>", self.on_crop_end)

        self.frame_mod = ctk.CTkFrame(middle_wrap, corner_radius=10)
        self.frame_mod.grid(row=0, column=1, padx=5, sticky="nsew")
        self.frame_mod.grid_rowconfigure(1, weight=1)
        self.frame_mod.grid_columnconfigure(0, weight=1)
        
        self.lbl_mod_title = ctk.CTkLabel(self.frame_mod, text=self.tr("mod_title"), font=ctk.CTkFont(weight="bold", size=16), text_color="#1DB954")
        self.lbl_mod_title.grid(row=0, column=0, pady=10)
        self.canvas_mod = ctk.CTkCanvas(self.frame_mod, bg="#1a1a1a", highlightthickness=0)
        self.canvas_mod.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.lbl_mod_stats = ctk.CTkLabel(self.frame_mod, text="...", font=ctk.CTkFont(size=12))
        self.lbl_mod_stats.grid(row=2, column=0, pady=5)

        self.frame_settings = ctk.CTkScrollableFrame(middle_wrap, corner_radius=10)
        self.frame_settings.grid(row=0, column=2, padx=5, sticky="nsew")

        self.lbl_crop_title = ctk.CTkLabel(self.frame_settings, text=self.tr("crop_title"), font=ctk.CTkFont(weight="bold"))
        self.lbl_crop_title.pack(anchor="w", padx=5, pady=(5,0))

        self.lbl_shape = ctk.CTkLabel(self.frame_settings, text=self.tr("shape"))
        self.lbl_shape.pack(anchor="w", padx=10, pady=(5,0))
        self.shape_var = ctk.StringVar(value=self.tr("shape_rect"))
        self.shape_menu = ctk.CTkOptionMenu(self.frame_settings, variable=self.shape_var, values=[self.tr("shape_rect"), self.tr("shape_circle"), self.tr("shape_star"), self.tr("shape_lasso")])
        self.shape_menu.pack(fill="x", padx=10, pady=(0,10))
        
        g_crop = ctk.CTkFrame(self.frame_settings, fg_color="transparent")
        g_crop.pack(fill="x", padx=5, pady=0)
        self.crop_x = ctk.CTkEntry(g_crop, width=70, placeholder_text="X"); self.crop_x.grid(row=0, column=0, padx=5, pady=5)
        self.crop_y = ctk.CTkEntry(g_crop, width=70, placeholder_text="Y"); self.crop_y.grid(row=0, column=1, padx=5, pady=5)
        self.crop_w = ctk.CTkEntry(g_crop, width=70, placeholder_text="W"); self.crop_w.grid(row=1, column=0, padx=5, pady=5)
        self.crop_h = ctk.CTkEntry(g_crop, width=70, placeholder_text="H"); self.crop_h.grid(row=1, column=1, padx=5, pady=5)

        self.lbl_res_title = ctk.CTkLabel(self.frame_settings, text=self.tr("res_title"), font=ctk.CTkFont(weight="bold"))
        self.lbl_res_title.pack(anchor="w", padx=5, pady=(15,0))
        
        self.lbl_behavior = ctk.CTkLabel(self.frame_settings, text=self.tr("behavior"))
        self.lbl_behavior.pack(anchor="w", padx=10, pady=(0,0))
        self.behav_var = ctk.StringVar(value=self.tr("behav_adaptive"))
        self.behav_menu = ctk.CTkOptionMenu(self.frame_settings, variable=self.behav_var, values=[self.tr("behav_adaptive"), self.tr("behav_stretch")])
        self.behav_menu.pack(fill="x", padx=10, pady=(0,10))

        self.res_mode_var = ctk.StringVar(value=self.tr("mode_px"))
        self.res_seg = ctk.CTkSegmentedButton(self.frame_settings, values=[self.tr("mode_px"), self.tr("mode_perc")], variable=self.res_mode_var, command=self.on_res_mode_change)
        self.res_seg.pack(padx=5, pady=5, fill="x")

        g_res = ctk.CTkFrame(self.frame_settings, fg_color="transparent")
        g_res.pack(fill="x", padx=5, pady=5)
        self.resize_w = ctk.CTkEntry(g_res, width=70, placeholder_text="W")
        self.resize_w.grid(row=0, column=0, padx=5, pady=5)
        self.resize_h = ctk.CTkEntry(g_res, width=70, placeholder_text="H")
        self.resize_h.grid(row=0, column=1, padx=5, pady=5)

        self.lbl_opt_title = ctk.CTkLabel(self.frame_settings, text=self.tr("opt_title"), font=ctk.CTkFont(weight="bold"))
        self.lbl_opt_title.pack(anchor="w", padx=5, pady=(15,0))
        
        self.lbl_slider = ctk.CTkLabel(self.frame_settings, text=f"{self.tr('slider_p')} 0")
        self.lbl_slider.pack(anchor="w", padx=10, pady=(5,0))
        
        self.slider_val = ctk.IntVar(value=0)
        self.slider = ctk.CTkSlider(self.frame_settings, from_=0, to=100, variable=self.slider_val, command=self.on_slider_change)
        self.slider.pack(fill="x", padx=10, pady=10)

        self.discord_var = ctk.BooleanVar(value=False)
        self.cb_discord = ctk.CTkCheckBox(self.frame_settings, text=self.tr("discord_cb"), variable=self.discord_var, command=self.on_discord_toggle, text_color="#1DB954")
        self.cb_discord.pack(anchor="w", padx=10, pady=10)

        self.btn_preview = ctk.CTkButton(self.frame_settings, text=self.tr("btn_preview"), height=40, command=self.generate_preview)
        self.btn_preview.pack(fill="x", padx=10, pady=(20, 10))

        self.btn_save = ctk.CTkButton(self.frame_settings, text=self.tr("btn_save"), height=50, fg_color="#1DB954", hover_color="#1aa34a", font=ctk.CTkFont(weight="bold", size=15), command=self.finalize_and_save)
        self.btn_save.pack(fill="x", padx=10, pady=10)

        self.progressbar = ctk.CTkProgressBar(self.frame_settings, mode="indeterminate", progress_color="#1DB954")

        self.console = ctk.CTkTextbox(self, height=120, font=ctk.CTkFont(family="Consolas", size=13), state="disabled", fg_color="#0d0d0d")
        self.console.pack(fill="x", padx=15, pady=(0,15))
        
        self.title(self.tr("title"))
        self.log(self.tr("log_ready"))

    def change_language(self, choice):
        old_val = self.res_mode_var.get()
        is_perc = (old_val == self.tr("mode_perc"))
        
        old_behav = self.behav_var.get()
        is_stretch = (old_behav == self.tr("behav_stretch"))

        old_shape = self.shape_var.get()
        shape_idx = 0
        for i, s in enumerate([self.tr("shape_rect"), self.tr("shape_circle"), self.tr("shape_star"), self.tr("shape_lasso")]):
            if old_shape == s: shape_idx = i

        self.lang = choice
        self.title(self.tr("title"))
        self.btn_load.configure(text=self.tr("load"))
        self.lbl_orig_title.configure(text=self.tr("orig_title"))
        self.lbl_mod_title.configure(text=self.tr("mod_title"))
        self.lbl_crop_title.configure(text=self.tr("crop_title"))
        self.lbl_res_title.configure(text=self.tr("res_title"))
        self.lbl_opt_title.configure(text=self.tr("opt_title"))
        self.btn_preview.configure(text=self.tr("btn_preview"))
        self.btn_save.configure(text=self.tr("btn_save"))
        self.cb_discord.configure(text=self.tr("discord_cb"))
        
        self.lbl_behavior.configure(text=self.tr("behavior"))
        self.behav_menu.configure(values=[self.tr("behav_adaptive"), self.tr("behav_stretch")])
        self.behav_var.set(self.tr("behav_stretch") if is_stretch else self.tr("behav_adaptive"))

        self.lbl_shape.configure(text=self.tr("shape"))
        shape_vals = [self.tr("shape_rect"), self.tr("shape_circle"), self.tr("shape_star"), self.tr("shape_lasso")]
        self.shape_menu.configure(values=shape_vals)
        self.shape_var.set(shape_vals[shape_idx])
        
        self.res_seg.configure(values=[self.tr("mode_px"), self.tr("mode_perc")])
        self.res_mode_var.set(self.tr("mode_perc") if is_perc else self.tr("mode_px"))

        if self.discord_var.get():
            self.lbl_slider.configure(text=self.tr("discord_auto"))
        else:
            self.lbl_slider.configure(text=f"{self.tr('slider_p')} {self.slider_val.get()}")

    def on_res_mode_change(self, choice):
        if choice == self.tr("mode_perc"):
            self.resize_w.delete(0, tk.END); self.resize_w.insert(0, "100")
            self.resize_h.delete(0, tk.END); self.resize_h.insert(0, "100")
        else:
            if hasattr(self, 'base_w'):
                cw = self.crop_w.get() or self.base_w
                ch = self.crop_h.get() or self.base_h
                self.resize_w.delete(0, tk.END); self.resize_w.insert(0, str(cw))
                self.resize_h.delete(0, tk.END); self.resize_h.insert(0, str(ch))

    def on_slider_change(self, val):
        if not self.discord_var.get():
            self.lbl_slider.configure(text=f"{self.tr('slider_p')} {int(val)}")

    def on_discord_toggle(self):
        if self.discord_var.get():
            self.slider.configure(state="disabled")
            self.lbl_slider.configure(text=self.tr("discord_auto"), text_color="#aaaaaa")
        else:
            self.slider.configure(state="normal")
            self.lbl_slider.configure(text=f"{self.tr('slider_p')} {int(self.slider_val.get())}", text_color=["black", "white"])

    def _cleanup_crop_visuals(self):
        if self.crop_rect_id:
            try: self.canvas_orig.delete(self.crop_rect_id)
            except: pass
        if self.lasso_line_id:
            try: self.canvas_orig.delete(self.lasso_line_id)
            except: pass
        self.crop_rect_id = None
        self.lasso_line_id = None
        self.lasso_points = []

    def on_crop_start(self, event):
        if not self.original_frames: return
        self.crop_drawing = True
        self.crop_start_x = event.x
        self.crop_start_y = event.y
        self._cleanup_crop_visuals()
        
        c_shape = self.shape_var.get()
        if c_shape == self.tr("shape_circle"):
            self.crop_rect_id = self.canvas_orig.create_oval(self.crop_start_x, self.crop_start_y, event.x+1, event.y+1, outline="yellow", dash=(4, 4), width=2)
        elif c_shape == self.tr("shape_lasso"):
            # create_line requires at least 4 coords (2 points)
            x, y = float(event.x), float(event.y)
            self.lasso_points = [x, y, x+1, y+1]
            self.lasso_line_id = self.canvas_orig.create_line(*self.lasso_points, fill="yellow", width=2, smooth=True)
        else:
            self.crop_rect_id = self.canvas_orig.create_rectangle(self.crop_start_x, self.crop_start_y, event.x+1, event.y+1, outline="yellow", dash=(4, 4), width=2)

    def _update_crop_entries(self, rx1, ry1, rx2, ry2, final=False):
        real_x = int(rx1 / self.preview_scale)
        real_y = int(ry1 / self.preview_scale)
        real_w = int((rx2 - rx1) / self.preview_scale)
        real_h = int((ry2 - ry1) / self.preview_scale)
        
        real_x = max(0, min(real_x, self.base_w))
        real_y = max(0, min(real_y, self.base_h))
        real_w = max(1, min(real_w, self.base_w - real_x))
        real_h = max(1, min(real_h, self.base_h - real_y))

        for e in [self.crop_x, self.crop_y, self.crop_w, self.crop_h]:
            e.delete(0, tk.END)
            
        self.crop_x.insert(0, str(real_x))
        self.crop_y.insert(0, str(real_y))
        self.crop_w.insert(0, str(real_w))
        self.crop_h.insert(0, str(real_h))

        if final and self.res_mode_var.get() == self.tr("mode_px"):
            self.resize_w.delete(0, tk.END)
            self.resize_w.insert(0, str(real_w))
            self.resize_h.delete(0, tk.END)
            self.resize_h.insert(0, str(real_h))
            self.log(f"[Action] Area Selected - X:{real_x} Y:{real_y} W:{real_w} H:{real_h}")

    def on_crop_drag(self, event):
        if not self.crop_drawing: return
        try:
            c_shape = self.shape_var.get()
            if c_shape == self.tr("shape_lasso"):
                if self.lasso_line_id:
                    self.lasso_points.extend([float(event.x), float(event.y)])
                    # tkinter canvas.coords() has arg limit; use itemconfig trick for long paths
                    try:
                        self.canvas_orig.coords(self.lasso_line_id, *self.lasso_points)
                    except tk.TclError:
                        # too many points for coords(), redraw the line
                        self.canvas_orig.delete(self.lasso_line_id)
                        self.lasso_line_id = self.canvas_orig.create_line(*self.lasso_points, fill="yellow", width=2, smooth=True)
            else:
                if self.crop_rect_id:
                    self.canvas_orig.coords(self.crop_rect_id, self.crop_start_x, self.crop_start_y, event.x, event.y)
                    rx1, rx2 = sorted([self.crop_start_x, event.x])
                    ry1, ry2 = sorted([self.crop_start_y, event.y])
                    self._update_crop_entries(rx1, ry1, rx2, ry2, final=False)
        except Exception as e:
            pass

    def on_crop_end(self, event):
        if not self.crop_drawing: return
        self.crop_drawing = False
        try:
            c_shape = self.shape_var.get()
            if c_shape == self.tr("shape_lasso"):
                if not self.lasso_points or len(self.lasso_points) < 4: return
                self.lasso_points.extend([self.lasso_points[0], self.lasso_points[1]]) # close loop
                self.canvas_orig.coords(self.lasso_line_id, *self.lasso_points)
                xs = self.lasso_points[0::2]
                ys = self.lasso_points[1::2]
                rx1, rx2 = min(xs), max(xs)
                ry1, ry2 = min(ys), max(ys)
                self._update_crop_entries(rx1, ry1, rx2, ry2, final=True)
            else:
                if not self.crop_rect_id: return
                coords = self.canvas_orig.coords(self.crop_rect_id)
                if not coords or len(coords) < 4: return
                x1, y1, x2, y2 = coords
                rx1, rx2 = sorted([x1, x2])
                ry1, ry2 = sorted([y1, y2])
                self._update_crop_entries(rx1, ry1, rx2, ry2, final=True)
        except Exception as e:
            self.log(f"Crop Canvas Error: {e}")

    def load_file(self):
        filepath = filedialog.askopenfilename(
            title="Select Image / GIF",
            filetypes=[
                ("All Supported", "*.gif *.png *.webp *.jpg *.jpeg *.bmp *.tiff *.tif"),
                ("GIF Files", "*.gif"),
                ("PNG Files", "*.png"),
                ("WebP Files", "*.webp"),
                ("JPEG Files", "*.jpg *.jpeg"),
                ("BMP / TIFF", "*.bmp *.tiff *.tif"),
                ("All Files", "*.*"),
            ]
        )
        if not filepath: return
        
        self.log(f"{self.tr('log_analyzing')} {os.path.basename(filepath)}")
        self.filepath = filepath
        
        try:
            img = Image.open(filepath)
            self.base_w = img.width
            self.base_h = img.height
            self.loop = img.info.get('loop', 0)
            self.transparency = img.info.get('transparency', None)
            
            self.original_frames = []
            self.durations = []
            # Try to iterate frames (GIF/APNG/WebP animated); fall back to single frame
            try:
                frame_count = 0
                for frame in ImageSequence.Iterator(img):
                    self.durations.append(frame.info.get('duration', 100))
                    self.original_frames.append(frame.convert("RGBA").copy())
                    frame_count += 1
                if frame_count == 0:
                    raise ValueError("no frames")
            except Exception:
                # Static image — treat as 1 frame
                self.original_frames = [img.convert("RGBA").copy()]
                self.durations = [100]
                
            sz_mb = os.path.getsize(filepath) / (1024*1024)
            self.lbl_orig_stats.configure(text=f"{self.base_w}x{self.base_h} | {len(self.original_frames)} frames | {sz_mb:.2f} MB")
            
            for e in [self.crop_x, self.crop_y, self.crop_w, self.crop_h, self.resize_w, self.resize_h]:
                e.delete(0, tk.END)
            self.crop_x.insert(0, "0"); self.crop_y.insert(0, "0")
            self.crop_w.insert(0, str(self.base_w)); self.crop_h.insert(0, str(self.base_h))
            
            if self.res_mode_var.get() == self.tr("mode_perc"):
                 self.resize_w.insert(0, "100"); self.resize_h.insert(0, "100")
            else:
                 self.resize_w.insert(0, str(self.base_w)); self.resize_h.insert(0, str(self.base_h))

            self.anim_running = False
            if self.anim_id_orig: self.after_cancel(self.anim_id_orig)
            if self.anim_id_mod: self.after_cancel(self.anim_id_mod)
            
            self.canvas_orig.delete("all")
            self._cleanup_crop_visuals()
            
            max_size = 450
            self.preview_scale = min(max_size / self.base_w, max_size / self.base_h) if (self.base_w > max_size or self.base_h > max_size) else 1.0
            
            pw = int(self.base_w * self.preview_scale)
            ph = int(self.base_h * self.preview_scale)
            
            self.orig_tk_frames = []
            for f in self.original_frames:
                thumb = f.resize((pw, ph), Image.Resampling.LANCZOS)
                self.orig_tk_frames.append(ImageTk.PhotoImage(thumb))

            self.img_orig_on_canvas = self.canvas_orig.create_image(0, 0, image=self.orig_tk_frames[0], anchor="nw")
            
            self.anim_running = True
            self.anim_idx_orig = 0
            self.update_animation_orig()
            self.generate_preview()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_animation_orig(self):
        if not self.anim_running or not self.orig_tk_frames: return
        self.canvas_orig.itemconfig(self.img_orig_on_canvas, image=self.orig_tk_frames[self.anim_idx_orig])
        dur = max(20, self.durations[self.anim_idx_orig])
        self.anim_idx_orig = (self.anim_idx_orig + 1) % len(self.orig_tk_frames)
        self.anim_id_orig = self.after(dur, self.update_animation_orig)

    def update_animation_mod(self):
        if not self.anim_running or not self.mod_tk_frames: return
        self.canvas_mod.itemconfig(self.img_mod_on_canvas, image=self.mod_tk_frames[self.anim_idx_mod])
        idx = self.anim_idx_mod % len(self.mod_new_durations)
        dur = max(20, self.mod_new_durations[idx])
        self.anim_idx_mod = (self.anim_idx_mod + 1) % len(self.mod_tk_frames)
        self.anim_id_mod = self.after(dur, self.update_animation_mod)

    def generate_preview(self):
        if not self.original_frames: return
        threading.Thread(target=self._compute_preview_thread, daemon=True).start()

    def _compute_preview_thread(self):
        self.after(0, lambda: self.progressbar.pack(fill="x", pady=5))
        self.after(0, self.progressbar.start)
        self.after(0, lambda: self.btn_preview.configure(state="disabled"))
        
        if self.discord_var.get():
            perc = 0 
            self.log(self.tr("log_preview_discord"))
        else:
            perc = self.slider_val.get()
            
        try:
            frames, durs = self.apply_transformations(perc)
            
            stream = io.BytesIO()
            kwa = {'save_all': True, 'loop': self.loop, 'disposal': 2, 'optimize': False}
            if self.transparency is not None: kwa['transparency'] = self.transparency
            if len(frames) > 1: frames[0].save(stream, format="GIF", append_images=frames[1:], duration=durs, **kwa)
            else: frames[0].save(stream, format="GIF", **kwa)
            sz_mb = stream.getbuffer().nbytes / (1024*1024)
            
            self.mod_tk_frames = []
            max_size = 450
            if not frames: return
            f_w, f_h = frames[0].size
            scale = min(max_size / f_w, max_size / f_h) if (f_w > max_size or f_h > max_size) else 1.0
            pw, ph = int(f_w * scale), int(f_h * scale)
            
            for f in frames:
                thumb = f.convert("RGBA").copy()
                thumb = thumb.resize((pw, ph), Image.Resampling.LANCZOS)
                self.mod_tk_frames.append(ImageTk.PhotoImage(thumb))

            self.after(0, self._render_preview_succ_ui, frames[0].size, len(frames), sz_mb, durs)
            
        except Exception as e:
            self.log(f"{self.tr('log_prev_err')}{str(e)}")
        finally:
            self.after(0, self.progressbar.stop)
            self.after(0, self.progressbar.pack_forget)
            self.after(0, lambda: self.btn_preview.configure(state="normal"))

    def _render_preview_succ_ui(self, size, count, sz_mb, durs):
        self.lbl_mod_stats.configure(text=f"{size[0]}x{size[1]} | {count} frames | {sz_mb:.2f} MB")
        self.canvas_mod.delete("all")
        if self.anim_id_mod: self.after_cancel(self.anim_id_mod)
        self.mod_new_durations = durs
        self.anim_idx_mod = 0
        if self.mod_tk_frames:
            self.img_mod_on_canvas = self.canvas_mod.create_image(0, 0, image=self.mod_tk_frames[0], anchor="nw")
            self.update_animation_mod()

    def generate_mask(self, width, height, shape_type):
        mask = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(mask)
        if shape_type == self.tr("shape_circle"):
            draw.ellipse((0, 0, width, height), fill=255)
        elif shape_type == self.tr("shape_star"):
            cx, cy = width/2, height/2
            r_outer = min(width, height) / 2
            r_inner = r_outer * 0.4
            points = []
            for i in range(10):
                angle = i * math.pi / 5 - math.pi / 2
                r = r_outer if i % 2 == 0 else r_inner
                points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
            draw.polygon(points, fill=255)
        elif shape_type == self.tr("shape_lasso") and len(self.lasso_points) > 4:
            try:
                cx = int(self.crop_x.get() or 0)
                cy = int(self.crop_y.get() or 0)
                pts = []
                for i in range(0, len(self.lasso_points), 2):
                    px = (self.lasso_points[i] / self.preview_scale) - cx
                    py = (self.lasso_points[i+1] / self.preview_scale) - cy
                    pts.append((px, py))
                draw.polygon(pts, fill=255)
            except:
                mask = Image.new("L", (width, height), 255)
        else:
            mask = Image.new("L", (width, height), 255)
        return mask

    def apply_transformations(self, percentage):
        cx = int(self.crop_x.get() or 0)
        cy = int(self.crop_y.get() or 0)
        cw = int(self.crop_w.get() or self.base_w)
        ch = int(self.crop_h.get() or self.base_h)

        if self.res_mode_var.get() == self.tr("mode_perc"):
            rw_p = float(self.resize_w.get() or 100) / 100.0
            rh_p = float(self.resize_h.get() or 100) / 100.0
            rw = int(cw * rw_p)
            rh = int(ch * rh_p)
        else:
            rw = int(self.resize_w.get() or cw)
            rh = int(self.resize_h.get() or ch)
            
        target_colors = 256
        scale_multip = 1.0
        skip_step = 1
        
        if percentage > 0:
            target_colors = max(16, int(256 - (240 * (percentage / 100))))
            scale_multip = 1.0 - (0.5 * (percentage / 100))
            if percentage >= 40: skip_step = 2 
            if percentage >= 80: skip_step = 3 
                 
        final_w = max(10, int(rw * scale_multip))
        final_h = max(10, int(rh * scale_multip))
        
        is_adaptive = (self.behav_var.get() == self.tr("behav_adaptive"))
        c_shape = self.shape_var.get()
        needs_mask = (c_shape != self.tr("shape_rect"))
        
        processed_frames = []
        new_durations = []
        
        current_dur = 0
        total = len(self.original_frames)
        
        if needs_mask:
            mask = self.generate_mask(cw, ch, c_shape)
        
        for i, frame in enumerate(self.original_frames):
            current_dur += self.durations[i]
            if skip_step > 1 and i % skip_step != 0 and i != 0 and i != (total - 1): continue
                
            f = frame.copy()
            if not (cx == 0 and cy == 0 and cw == self.base_w and ch == self.base_h):
                f = f.crop((cx, cy, cx + cw, cy + ch))
                
            if needs_mask:
                res = Image.new("RGBA", f.size, (0, 0, 0, 0))
                res.paste(f, (0, 0), mask=mask)
                f = res
                
            if is_adaptive:
                if final_w != cw or final_h != ch:
                    ratio = min(final_w / float(cw), final_h / float(ch))
                    new_w, new_h = max(1, int(cw * ratio)), max(1, int(ch * ratio))
                    f = f.resize((new_w, new_h), Image.Resampling.LANCZOS)
            else:
                if final_w != cw or final_h != ch:
                    f = f.resize((final_w, final_h), Image.Resampling.LANCZOS)
                
            if target_colors < 256 and not needs_mask:
                f = f.quantize(colors=target_colors, method=Image.Quantize.FASTOCTREE)
                f = f.convert("RGBA")
                
            processed_frames.append(f)
            new_durations.append(current_dur)
            current_dur = 0
            
        return processed_frames, new_durations

    def finalize_and_save(self):
        if not self.original_frames:
            messagebox.showwarning("Warning", self.tr("err_nofile"))
            return
            
        savepath = filedialog.asksaveasfilename(defaultextension=".gif", title="Save Post-Processed GIF", filetypes=[("GIF", "*.gif")])
        if not savepath: return
        threading.Thread(target=self._finalize_thread, args=(savepath,), daemon=True).start()

    def _finalize_thread(self, savepath):
        self.after(0, lambda: self.progressbar.pack(fill="x", pady=5))
        self.after(0, self.progressbar.start)
        self.after(0, lambda: self.btn_save.configure(state="disabled"))
        self.after(0, lambda: self.btn_preview.configure(state="disabled"))

        try:
            if self.discord_var.get():
                self.log(self.tr("log_discord_test"))
                best_frames = None
                best_dur = None
                found = False

                for p in range(0, 101, 15):
                    self.log(f"{self.tr('log_testing')}{p}")
                    frames, dur = self.apply_transformations(p)
                    
                    stream = io.BytesIO()
                    kwa = {'save_all': True, 'loop': self.loop, 'disposal': 2, 'optimize': False}
                    if self.transparency is not None: kwa['transparency'] = self.transparency
                    
                    if len(frames) > 1: frames[0].save(stream, format="GIF", append_images=frames[1:], duration=dur, **kwa)
                    else: frames[0].save(stream, format="GIF", **kwa)
                        
                    sz_mb = stream.getbuffer().nbytes / (1024*1024)
                    self.log(f"{self.tr('log_size')}{sz_mb:.2f} MB")
                    
                    if sz_mb <= 9.9:
                        best_frames = frames; best_dur = dur; found = True
                        break
                        
                if not found:
                    self.log(self.tr("err_limit_warn"))
                    best_frames, best_dur = self.apply_transformations(100)
                    
                frames, dur = best_frames, best_dur
            else:
                perc = self.slider_val.get()
                frames, dur = self.apply_transformations(perc)

            kwa = {'save_all': True, 'loop': self.loop, 'disposal': 2, 'optimize': False}
            if self.transparency is not None: kwa['transparency'] = self.transparency
            
            if len(frames) > 1: 
                frames[0].save(savepath, format="GIF", append_images=frames[1:], duration=dur, **kwa)
            else: 
                frames[0].save(savepath, format="GIF", **kwa)

            self.log(self.tr("log_saved") + f"-> {os.path.basename(savepath)}")
            self.after(0, lambda: messagebox.showinfo("Success", self.tr("log_saved")))
        
        except Exception as e:
            self.log(f"{self.tr('log_err')}{str(e)}")
            self.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally:
            self.after(0, self.progressbar.stop)
            self.after(0, self.progressbar.pack_forget)
            self.after(0, lambda: self.btn_save.configure(state="normal"))
            self.after(0, lambda: self.btn_preview.configure(state="normal"))

    def open_tools(self):
        ImageToolsWindow(self)


class ImageToolsWindow(ctk.CTkToplevel):
    """Standalone Image Tools: PNG→ICO converter + Background Eraser."""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Image Tools")
        self.geometry("960x680")
        self.minsize(860, 600)
        self.grab_set()  # modal

        icon_path = resource_path("app_icon.ico")
        if os.path.exists(icon_path):
            try: self.after(200, lambda: self.iconbitmap(icon_path))
            except: pass

        self.src_image: Image.Image | None = None   # original loaded image
        self.result_image: Image.Image | None = None  # after bg erase
        self.tk_preview = None
        self.pick_mode = False  # waiting for colour pick click

        self._build_ui()

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        #  Top bar 
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=14, pady=8)

        self.btn_open = ctk.CTkButton(top, text="Open Image", width=140,
                                      font=ctk.CTkFont(weight="bold"), command=self._open_image)
        self.btn_open.pack(side="left", padx=(0, 8))

        self.lbl_file = ctk.CTkLabel(top, text="No file loaded", text_color="#888888")
        self.lbl_file.pack(side="left")

        #  Main content area 
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=14, pady=0)
        content.grid_columnconfigure(0, weight=3)
        content.grid_columnconfigure(1, weight=2)
        content.grid_rowconfigure(0, weight=1)

        # Preview canvas
        prev_frame = ctk.CTkFrame(content, corner_radius=10)
        prev_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        prev_frame.grid_rowconfigure(1, weight=1)
        prev_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(prev_frame, text="Preview", font=ctk.CTkFont(weight="bold", size=14)).grid(row=0, column=0, pady=8)
        self.canvas = ctk.CTkCanvas(prev_frame, bg="#1a1a1a", highlightthickness=0)
        self.canvas.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.lbl_info = ctk.CTkLabel(prev_frame, text="...", font=ctk.CTkFont(size=11))
        self.lbl_info.grid(row=2, column=0, pady=4)

        # Settings panel
        panel = ctk.CTkScrollableFrame(content, corner_radius=10)
        panel.grid(row=0, column=1, sticky="nsew")

        #  Background Eraser section 
        ctk.CTkLabel(panel, text="Background Eraser",
                     font=ctk.CTkFont(weight="bold", size=14)).pack(anchor="w", padx=8, pady=(10, 2))

        ctk.CTkLabel(panel, text="Tolerance  (0 = exact match)",
                     font=ctk.CTkFont(size=12)).pack(anchor="w", padx=12, pady=(6, 0))
        self.tol_var = ctk.IntVar(value=30)
        self.lbl_tol = ctk.CTkLabel(panel, text="30", font=ctk.CTkFont(size=12))
        self.lbl_tol.pack(anchor="e", padx=14)
        ctk.CTkSlider(panel, from_=0, to=100, variable=self.tol_var,
                      command=lambda v: self.lbl_tol.configure(text=str(int(v)))
                      ).pack(fill="x", padx=12, pady=(0, 6))

        # Colour picker row
        cprow = ctk.CTkFrame(panel, fg_color="transparent")
        cprow.pack(fill="x", padx=8, pady=4)
        self.btn_pick = ctk.CTkButton(cprow, text="Pick Colour (click image)",
                                      width=200, command=self._enter_pick_mode)
        self.btn_pick.pack(side="left")
        self.lbl_picked = ctk.CTkLabel(cprow, text="—  ", fg_color="#333",
                                       corner_radius=4, width=40)
        self.lbl_picked.pack(side="left", padx=6)

        self.picked_color: tuple | None = None

        # Auto corners checkbox
        self.auto_corners_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(panel, text="Auto-detect corners (no pick needed)",
                        variable=self.auto_corners_var).pack(anchor="w", padx=12, pady=4)

        self.btn_erase = ctk.CTkButton(panel, text="Erase Background",
                                       height=36, command=self._erase_background)
        self.btn_erase.pack(fill="x", padx=12, pady=(6, 2))

        self.btn_reset = ctk.CTkButton(panel, text="↩ Reset to Original",
                                       height=32, fg_color="#555", hover_color="#777",
                                       command=self._reset_to_original)
        self.btn_reset.pack(fill="x", padx=12, pady=(2, 10))

        ctk.CTkLabel(panel, text="",
                     text_color="#444").pack(pady=4)

        #  PNG → ICO section 
        ctk.CTkLabel(panel, text="PNG → ICO Converter",
                     font=ctk.CTkFont(weight="bold", size=14)).pack(anchor="w", padx=8, pady=(6, 2))

        ctk.CTkLabel(panel, text="Include sizes:",
                     font=ctk.CTkFont(size=12)).pack(anchor="w", padx=12, pady=(6, 2))

        self.size_vars: dict[str, ctk.BooleanVar] = {}
        for sz in ["16", "32", "48", "64", "128", "256"]:
            v = ctk.BooleanVar(value=(sz in ("32", "64", "128", "256")))
            self.size_vars[sz] = v
            ctk.CTkCheckBox(panel, text=f"{sz} × {sz} px", variable=v).pack(
                anchor="w", padx=20, pady=1)

        self.btn_ico = ctk.CTkButton(panel, text="Save as .ICO",
                                     height=36, fg_color="#1DB954", hover_color="#1aa34a",
                                     font=ctk.CTkFont(weight="bold"),
                                     command=self._save_ico)
        self.btn_ico.pack(fill="x", padx=12, pady=(10, 4))

        ctk.CTkLabel(panel, text="",
                     text_color="#444").pack(pady=4)

        #  Save PNG section 
        ctk.CTkLabel(panel, text="Save Result",
                     font=ctk.CTkFont(weight="bold", size=14)).pack(anchor="w", padx=8, pady=(6, 2))

        self.btn_save_png = ctk.CTkButton(panel, text="Save as PNG (with transparency)",
                                          height=36, command=self._save_png)
        self.btn_save_png.pack(fill="x", padx=12, pady=(4, 10))

        #  Console 
        self.console = ctk.CTkTextbox(self, height=80,
                                      font=ctk.CTkFont(family="Consolas", size=12),
                                      state="disabled", fg_color="#0d0d0d")
        self.console.pack(fill="x", padx=14, pady=(4, 10))

    # ------------------------------------------------------------------ helpers
    def _log(self, msg):
        self.console.configure(state="normal")
        self.console.insert("end", f"> {msg}\n")
        self.console.see("end")
        self.console.configure(state="disabled")

    def _display_image(self, img: Image.Image):
        """Resize image to fit canvas and show it."""
        self.canvas.update_idletasks()
        cw = max(self.canvas.winfo_width(), 400)
        ch = max(self.canvas.winfo_height(), 400)
        ratio = min(cw / img.width, ch / img.height, 1.0)
        pw, ph = max(1, int(img.width * ratio)), max(1, int(img.height * ratio))
        thumb = img.convert("RGBA").resize((pw, ph), Image.Resampling.LANCZOS)
        # Checkerboard bg to show transparency
        checker = Image.new("RGBA", (pw, ph), (40, 40, 40, 255))
        square = 10
        for iy in range(0, ph, square):
            for ix in range(0, pw, square):
                if (ix // square + iy // square) % 2 == 0:
                    for dy in range(min(square, ph - iy)):
                        for dx in range(min(square, pw - ix)):
                            checker.putpixel((ix + dx, iy + dy), (60, 60, 60, 255))
        checker.paste(thumb, (0, 0), thumb)
        self.tk_preview = ImageTk.PhotoImage(checker)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.tk_preview, anchor="nw")
        self._canvas_scale = ratio

    # ------------------------------------------------------------------ actions
    def _open_image(self):
        path = filedialog.askopenfilename(
            title="Open Image",
            filetypes=[("Images", "*.png *.webp *.jpg *.jpeg *.bmp *.tiff *.gif"),
                       ("All Files", "*.*")]
        )
        if not path: return
        try:
            self.src_image = Image.open(path).convert("RGBA")
            self.result_image = self.src_image.copy()
            self.lbl_file.configure(text=os.path.basename(path), text_color="white")
            self.lbl_info.configure(text=f"{self.src_image.width} × {self.src_image.height} px")
            self._display_image(self.result_image)
            self._log(f"Loaded: {os.path.basename(path)}  ({self.src_image.width}×{self.src_image.height})")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _enter_pick_mode(self):
        if not self.src_image:
            messagebox.showwarning("No image", "Please open an image first."); return
        self.pick_mode = True
        self.btn_pick.configure(text="Click on the image...", fg_color="#c0392b")
        self._log("Pick mode ON — click on the background colour in the preview.")

    def _on_canvas_click(self, event):
        if not self.pick_mode or self.result_image is None: return
        self.pick_mode = False
        self.btn_pick.configure(text="Pick Colour (click image)", fg_color=("#3a7ebf", "#1f538d"))
        # Map canvas coords → image pixel
        scale = getattr(self, "_canvas_scale", 1.0)
        px = int(event.x / scale)
        py = int(event.y / scale)
        px = max(0, min(px, self.result_image.width - 1))
        py = max(0, min(py, self.result_image.height - 1))
        r, g, b, a = self.result_image.getpixel((px, py))
        self.picked_color = (r, g, b)
        hex_col = f"#{r:02x}{g:02x}{b:02x}"
        self.lbl_picked.configure(text=f"{hex_col}  ", fg_color=hex_col,
                                  text_color="white"if (r + g + b) < 384 else "black")
        self._log(f"Picked colour: rgb({r},{g},{b})  {hex_col}  at ({px},{py})")

    def _color_distance(self, c1: tuple, c2: tuple) -> float:
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1[:3], c2[:3])))

    def _erase_background(self):
        if self.src_image is None:
            messagebox.showwarning("No image", "Please open an image first."); return

        tol = self.tol_var.get() * 2.21  # scale 0-100 → 0-221 (max RGB distance ≈ 441)

        # Determine target colour
        if self.auto_corners_var.get():
            img = self.src_image.copy().convert("RGBA")
            corners = [
                img.getpixel((0, 0)),
                img.getpixel((img.width - 1, 0)),
                img.getpixel((0, img.height - 1)),
                img.getpixel((img.width - 1, img.height - 1)),
            ]
            avg = tuple(int(sum(c[i] for c in corners) / 4) for i in range(3))
            target = avg
            self._log(f"Auto corner colour: rgb{target}")
        elif self.picked_color:
            target = self.picked_color
        else:
            messagebox.showwarning("No colour", "Please pick a background colour first."); return

        self._log(f"Erasing background… tolerance={self.tol_var.get()}")
        threading.Thread(target=self._do_erase, args=(target, tol), daemon=True).start()

    def _do_erase(self, target: tuple, tol: float):
        img = self.src_image.copy().convert("RGBA")
        data = img.load()
        w, h = img.size
        for y in range(h):
            for x in range(w):
                r, g, b, a = data[x, y]
                if self._color_distance((r, g, b), target) <= tol:
                    data[x, y] = (r, g, b, 0)  # make transparent
        self.result_image = img
        self.after(0, self._display_image, img)
        self.after(0, self._log, "Background erased. Save or convert to ICO.")

    def _reset_to_original(self):
        if self.src_image is None: return
        self.result_image = self.src_image.copy()
        self._display_image(self.result_image)
        self._log("Reset to original.")

    def _save_ico(self):
        img = self.result_image or self.src_image
        if img is None:
            messagebox.showwarning("No image", "Please open an image first."); return

        sizes = [int(s) for s, v in self.size_vars.items() if v.get()]
        if not sizes:
            messagebox.showwarning("No sizes", "Select at least one ICO size."); return

        path = filedialog.asksaveasfilename(
            defaultextension=".ico",
            filetypes=[("ICO files", "*.ico"), ("All Files", "*.*")],
            title="Save ICO"
        )
        if not path: return
        try:
            base = img.convert("RGBA")
            resized = [base.resize((s, s), Image.Resampling.LANCZOS) for s in sizes]
            resized[0].save(path, format="ICO",
                            sizes=[(s, s) for s in sizes],
                            append_images=resized[1:])
            self._log(f"Saved ICO → {os.path.basename(path)}  sizes={sizes}")
            messagebox.showinfo("Saved", f"ICO saved:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _save_png(self):
        img = self.result_image or self.src_image
        if img is None:
            messagebox.showwarning("No image", "Please open an image first."); return
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("All Files", "*.*")],
            title="Save PNG"
        )
        if not path: return
        try:
            img.convert("RGBA").save(path, format="PNG")
            self._log(f"Saved PNG → {os.path.basename(path)}")
            messagebox.showinfo("Saved", f"PNG saved:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = GifOptimizerApp()
    app.mainloop()
