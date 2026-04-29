import tkinter as tk
from tkinter import ttk
import pygame
import sys
import os
import json
import subprocess          
import re

try:
    import tkvideo
    tkvideo_available = True
except ImportError:
    tkvideo_available = False
try:
    from PIL import Image, ImageTk
    pil_available = True
except ImportError:
    pil_available = False

pygame.init()
pygame.mixer.init()

# ----------------------------------------------------------------------------
# COSTANTI DI STILE
# ----------------------------------------------------------------------------
BG_COLOR    = "#1a0f00"
BTN_COLOR_1 = "#c8a96e"
BTN_COLOR_2 = "#7a4520"
BTN_TEXT    = "#f5e6c8"
BTN_HOVER   = "#e8c47a"
TITLE_COLOR = "#f5d78e"
TEXT_COLOR  = "#d4b896"

FONT_TITLE = ("Georgia", 32, "bold")
FONT_BTN   = ("Georgia", 14, "bold")
FONT_LABEL = ("Georgia", 13)
FONT_SMALL = ("Georgia", 11)

# ── Percorsi personalizzabili ─────────────────────────────────────────────────

VIDEO_FILE       = "assets_gioconave/wmremove-transformed.mp4"      # Lascia "" se non hai un video: userà l'animazione
SHOP_SCRIPT      = "shop.py"               # Script del negozio da aprire dopo la transizione
IMAGE_FOLDER     = "assets_gioconave/video in fotogrammi"  # Cartella con le immagini della slideshow
FRAME_DELAY_MS   = 10 # Millisecondi tra un fotogramma e il successivo
# ─────────────────────────────────────────────────────────────────────────────

# Slideshow tuning
SLIDESHOW_FILL = "cover"  # 'cover' to fill window (crop), 'contain' to fit with letterbox
SLIDESHOW_CROSSFADE = True
CROSSFADE_MS = 125
CROSSFADE_STEPS = 2

initial_volume = 100

def load_settings():
    default = {
        "volume_musica": 100,
        "effetti_sonori": True,
        "difficolta": "normale",
        "qualita_grafica": "alta",
        "lingua": "italiano"
    }
    if os.path.exists("config.json"):
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default

def save_settings(s):
    try:
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(s, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Errore salvataggio: {e}")


def natural_sort_key(s):
    parts = re.split(r'(\d+)', s)
    return [int(p) if p.isdigit() else p.lower() for p in parts]


def resize_and_crop(img, size):
    """Resize image to fill size (cover) and center-crop to exact size."""
    desired_w, desired_h = size
    w, h = img.size
    if w == 0 or h == 0:
        return img.resize((desired_w, desired_h), Image.LANCZOS)

    if SLIDESHOW_FILL == 'cover':
        scale = max(desired_w / w, desired_h / h)
    else:
        scale = min(desired_w / w, desired_h / h)

    new_w = max(1, int(w * scale + 0.5))
    new_h = max(1, int(h * scale + 0.5))
    img = img.resize((new_w, new_h), Image.LANCZOS)

    if SLIDESHOW_FILL == 'cover':
        left = (new_w - desired_w) // 2
        top = (new_h - desired_h) // 2
        img = img.crop((left, top, left + desired_w, top + desired_h))
    else:
        # contain: paste onto background to avoid stretching
        bg = Image.new('RGB', (desired_w, desired_h), BG_COLOR)
        left = (desired_w - new_w) // 2
        top = (desired_h - new_h) // 2
        if img.mode != 'RGB':
            img = img.convert('RGB')
        bg.paste(img, (left, top))
        img = bg

    if img.mode != 'RGB':
        img = img.convert('RGB')
    return img

settings = load_settings()

WIN_W, WIN_H = 1000, 592
sfx_on  = settings.get("effetti_sonori", True)
volume  = settings.get("volume_musica", 100)
root         = None
canvas       = None
main_frame   = None
settings_frame = None
vol_label    = None
bg_img       = None


# ----------------------------------------------------------------------------
# NAVIGAZIONE
# ----------------------------------------------------------------------------
def show_main_menu():
    settings_frame.place_forget()
    canvas.itemconfig("main", state="normal")

def show_shop():
    canvas.itemconfig("main", state="hidden")

def show_settings_menu():
    canvas.itemconfig("main", state="hidden")
    settings_frame.place(relx=0.5, rely=0.5, anchor="center")

def go_to_settings():
    show_settings_menu()

def go_to_shop():
    show_shop()

def go_to_main_menu():
    show_main_menu()


# ----------------------------------------------------------------------------
# HOVER BOTTONI FRAME
# ----------------------------------------------------------------------------
def on_btn_enter(e, btn):
    btn.configure(bg=BTN_HOVER, fg=BG_COLOR)

def on_btn_leave(e, btn):
    btn.configure(bg=BTN_COLOR_2, fg=BTN_TEXT)


# ----------------------------------------------------------------------------
# GIOCA → video → shop
# ----------------------------------------------------------------------------
def go_to_game():
    """
    Mostra una slideshow di immagini (se presenti) e poi apre lo shop.
    Se non ci sono immagini, mantiene il fallback alla riproduzione video/esecuzione esterna.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))

    print("go_to_game called")
    # Prova prima la slideshow di immagini (cartella IMAGE_FOLDER)
    frames_dir = os.path.join(script_dir, IMAGE_FOLDER)
    if pil_available and os.path.isdir(frames_dir):
        img_files = sorted([f for f in os.listdir(frames_dir)
                            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))],
                           key=natural_sort_key)
        print(f"Trovati {len(img_files)} file immagine in {frames_dir}")
        if img_files:
            pil_frames = []
            for fn in img_files:
                try:
                    img_path = os.path.join(frames_dir, fn)
                    img = Image.open(img_path)
                    img = resize_and_crop(img, (WIN_W, WIN_H))
                    pil_frames.append(img)
                except Exception as ex:
                    print(f"Errore caricando immagine {fn}: {ex}")

            print(f"Frame PIL caricati: {len(pil_frames)}")
            if not pil_frames:
                print("Nessun frame valido caricato dalla cartella, uso fallback video.")
            else:
                # Preconverti in PhotoImage per prestazioni
                photo_frames = [ImageTk.PhotoImage(p) for p in pil_frames]

                # Precompute crossfade blends per coppia di frame per evitare blocchi
                root._slideshow_blends = []
                if SLIDESHOW_CROSSFADE and len(pil_frames) > 1:
                    steps = max(1, CROSSFADE_STEPS)
                    try:
                        for idx in range(len(pil_frames) - 1):
                            a = pil_frames[idx]
                            b = pil_frames[idx + 1]
                            blended = []
                            for s in range(1, steps + 1):
                                alpha = s / steps
                                try:
                                    img_blend = Image.blend(a, b, alpha)
                                except Exception:
                                    img_blend = b
                                blended.append(ImageTk.PhotoImage(img_blend))
                            root._slideshow_blends.append(blended)
                    except Exception as ex:
                        print(f"Errore precomputing blend frames: {ex}")
                        root._slideshow_blends = []

                canvas.itemconfig("main", state="hidden")
                settings_frame.place_forget()

                slide_label = tk.Label(root, bg=BG_COLOR)
                # Inserisco il label dentro il canvas per garantire la visibilità sopra gli altri elementi
                slide_window = canvas.create_window(0, 0, anchor="nw", window=slide_label, width=WIN_W, height=WIN_H)

                # Mantieni i riferimenti per evitare garbage-collection
                root._slideshow_pil = pil_frames
                root._slideshow_frames = photo_frames

                def show_frame(i=0):
                    if i >= len(photo_frames):
                        try:
                            slide_label.destroy()
                        except Exception:
                            pass
                        try:
                            canvas.delete(slide_window)
                        except Exception:
                            pass
                        shop_path = os.path.join(script_dir, SHOP_SCRIPT)
                        if os.path.exists(shop_path):
                            try:
                                subprocess.Popen([sys.executable, shop_path])
                            except Exception as ex:
                                print(f"Errore avviando shop: {ex}")
                        quit_app()
                        return

                    # mostra il frame corrente
                    slide_label.configure(image=photo_frames[i])
                    slide_label.image = photo_frames[i]

                    # Se abilitate le dissolvenze e c'è un frame successivo, esegui crossfade usando frame precomputati
                    if SLIDESHOW_CROSSFADE and i + 1 < len(photo_frames):
                        hold_time = max(0, FRAME_DELAY_MS - CROSSFADE_MS)

                        def start_crossfade():
                            if hasattr(root, '_slideshow_blends') and i < len(root._slideshow_blends):
                                blended = root._slideshow_blends[i]
                            else:
                                blended = [photo_frames[i + 1]]

                            # mantieni riferimenti temporanei sulla label
                            slide_label._blend_frames = blended

                            steps_local = max(1, len(blended))
                            per_step_local = max(1, CROSSFADE_MS // steps_local)

                            def do_blend(idx=0):
                                if idx >= len(blended):
                                    try:
                                        del slide_label._blend_frames
                                    except Exception:
                                        pass
                                    show_frame(i + 1)
                                    return
                                slide_label.configure(image=blended[idx])
                                slide_label.image = blended[idx]
                                root.after(per_step_local, lambda: do_blend(idx + 1))

                            do_blend(0)

                        root.after(hold_time, start_crossfade)
                    else:
                        root.after(FRAME_DELAY_MS, lambda: show_frame(i + 1))

                show_frame(0)
                return

    # Se non ci sono immagini, torna al comportamento precedente (video / fallback)
    if tkvideo_available and VIDEO_FILE:
        video_path = os.path.join(script_dir, VIDEO_FILE)
        if os.path.exists(video_path):
            try:
                # Nasconde il menu principale
                canvas.itemconfig("main", state="hidden")
                settings_frame.place_forget()

                # Prova a riprodurre con tkvideo se presente
                try:
                    video_label = tkvideo.Label(root, video_path, size=(WIN_W, WIN_H))
                    video_label.pack(fill="both", expand=True)
                    video_label.play()
                except Exception as ex:
                    print(f"Errore avviando tkvideo: {ex}")
                    # Fallback: apri con player esterno
                    root.withdraw()
                    try:
                        if sys.platform == "win32":
                            os.startfile(video_path)
                        else:
                            opener = "open" if sys.platform == "darwin" else "xdg-open"
                            subprocess.Popen([opener, video_path])
                    except Exception as ex2:
                        print(f"Errore aprendo il video: {ex2}")

                # Bottone per saltare il video
                def after_video():
                    try:
                        video_label.destroy()
                    except Exception:
                        pass
                    try:
                        skip_btn.destroy()
                    except Exception:
                        pass
                    shop_path = os.path.join(script_dir, SHOP_SCRIPT)
                    if os.path.exists(shop_path):
                        try:
                            subprocess.Popen([sys.executable, shop_path])
                        except Exception as ex:
                            print(f"Errore avviando shop: {ex}")
                    quit_app()

                skip_btn = tk.Button(root, text="Salta", command=after_video)
                skip_btn.place(relx=0.98, rely=0.98, anchor="se")
            except Exception as ex:
                print(f"Errore durante riproduzione video: {ex}")
                root.withdraw()
                try:
                    if sys.platform == "win32":
                        os.startfile(video_path)
                    else:
                        opener = "open" if sys.platform == "darwin" else "xdg-open"
                        subprocess.Popen([opener, video_path])
                except Exception as ex2:
                    print(f"Errore aprendo il video: {ex2}")
                shop_path = os.path.join(script_dir, SHOP_SCRIPT)
                if os.path.exists(shop_path):
                    try:
                        subprocess.Popen([sys.executable, shop_path])
                    except Exception as ex:
                        print(f"Errore avviando shop: {ex}")
                quit_app()
        else:
            print(f"Video non trovato: {video_path}")
            shop_path = os.path.join(script_dir, SHOP_SCRIPT)
            if os.path.exists(shop_path):
                try:
                    subprocess.Popen([sys.executable, shop_path])
                except Exception as ex:
                    print(f"Errore avviando shop: {ex}")
            quit_app()
    else:
        # Fallback: comportamento originale
        root.withdraw()
        if VIDEO_FILE:
            video_path = os.path.join(script_dir, VIDEO_FILE)
            if os.path.exists(video_path):
                try:
                    if sys.platform == "win32":
                        os.startfile(video_path)
                    else:
                        opener = "open" if sys.platform == "darwin" else "xdg-open"
                        subprocess.Popen([opener, video_path])
                except Exception as ex:
                    print(f"Errore aprendo il video: {ex}")
            else:
                print(f"Video non trovato: {video_path}")
        shop_path = os.path.join(script_dir, SHOP_SCRIPT)
        if os.path.exists(shop_path):
            try:
                subprocess.Popen([sys.executable, shop_path])
            except Exception as ex:
                print(f"Errore avviando shop: {ex}")
        quit_app()


# ----------------------------------------------------------------------------
# USCITA
# ----------------------------------------------------------------------------
def exit_app():
    root.after(120, quit_app)

def quit_app():
    pygame.quit()
    root.destroy()
    sys.exit()


# ----------------------------------------------------------------------------
# AUDIO
# ----------------------------------------------------------------------------
def on_volume_change(val):
    v = int(float(val))
    vol_label.configure(text=f"{v}%")
    settings["volume_musica"] = v
    save_settings(settings)

def toggle_sfx():
    global sfx_on
    sfx_on = not sfx_on
    if sfx_on:
        pygame.mixer.unpause()
    else:
        pygame.mixer.pause()
    settings["effetti_sonori"] = sfx_on
    save_settings(settings)


# ----------------------------------------------------------------------------
# ASSETS
# ----------------------------------------------------------------------------
def load_assets():
    global bg_img
    bg_path = "assets_gioconave/wmremove-transformed.png"
    if pil_available and os.path.exists(bg_path):
        img = Image.open(bg_path).resize((WIN_W, WIN_H), Image.LANCZOS)
        bg_img = ImageTk.PhotoImage(img)


# ----------------------------------------------------------------------------
# HELPER UI
# ----------------------------------------------------------------------------
def create_separator(parent):
    line = tk.Frame(parent, height=1, bg=BTN_COLOR_2, width=320)
    line.pack(pady=6)

def create_menu_btn(parent, text, command):
    btn = tk.Button(
        parent, text=text, font=FONT_BTN,
        fg=BTN_TEXT, bg=BTN_COLOR_2,
        activebackground=BTN_COLOR_1, activeforeground=BG_COLOR,
        width=22, height=1, relief="flat", borderwidth=0,
        cursor="hand2", command=command,
    )
    btn.pack(pady=6, ipadx=10, ipady=8)
    btn.bind("<Enter>", lambda e, b=btn: on_btn_enter(e, b))
    btn.bind("<Leave>", lambda e, b=btn: on_btn_leave(e, b))
    return btn

def create_canvas_button(x, y, text, command):
    rect = canvas.create_rectangle(
        x - 110, y - 15, x + 110, y + 15,
        fill=BTN_COLOR_2, outline=BTN_COLOR_1, width=2, tags="main"
    )
    txt = canvas.create_text(
        x, y, text=text, font=FONT_BTN,
        fill=BTN_TEXT, anchor="center", tags="main"
    )

    def on_enter(e):
        canvas.itemconfig(rect, fill=BTN_HOVER, outline=BTN_HOVER)
        canvas.itemconfig(txt, fill=BG_COLOR)

    def on_leave(e):
        canvas.itemconfig(rect, fill=BTN_COLOR_2, outline=BTN_COLOR_1)
        canvas.itemconfig(txt, fill=BTN_TEXT)

    def on_click(e):
        command()

    for item in [rect, txt]:
        canvas.tag_bind(item, "<Enter>", on_enter)
        canvas.tag_bind(item, "<Leave>", on_leave)
        canvas.tag_bind(item, "<Button-1>", on_click)


# ----------------------------------------------------------------------------
# BUILD MENU PRINCIPALE
# ----------------------------------------------------------------------------
def build_main_menu():
    btn_y = 210
    for testo, funzione in [
        ("GIOCA",        go_to_game),
        ("IMPOSTAZIONI", go_to_settings),
        ("ESCI",         exit_app),
    ]:
        create_canvas_button(WIN_W // 2, btn_y, testo, funzione)
        btn_y += 60


# ----------------------------------------------------------------------------
# BUILD IMPOSTAZIONI
# ----------------------------------------------------------------------------
def build_settings_menu():
    global vol_label, sfx_btn
    f = settings_frame

    tk.Label(f, text="IMPOSTAZIONI", font=FONT_TITLE,
             fg=TITLE_COLOR, bg=BG_COLOR).pack(pady=(40, 10))
    create_separator(f)
    tk.Label(f, text="", bg=BG_COLOR).pack()

    row_vol = tk.Frame(f, bg=BG_COLOR)
    row_vol.pack(pady=8)
    tk.Label(row_vol, text="Volume Musica", font=FONT_LABEL,
             fg=TEXT_COLOR, bg=BG_COLOR, width=16, anchor="e").grid(row=0, column=0, padx=8)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Gold.Horizontal.TScale",
                    troughcolor="#3d2b10", background=BG_COLOR,
                    sliderlength=18, sliderrelief="flat")

    vol_var = tk.IntVar(value=volume)
    slider = ttk.Scale(row_vol, from_=0, to=100, orient="horizontal", length=200,
                       variable=vol_var, style="Gold.Horizontal.TScale",
                       command=on_volume_change)
    slider.grid(row=0, column=1, padx=8)

    vol_label = tk.Label(row_vol, text=f"{volume}%", font=FONT_LABEL,
                         fg=BTN_TEXT, bg=BG_COLOR, width=5)
    vol_label.grid(row=0, column=2, padx=4)

    row_sfx = tk.Frame(f, bg=BG_COLOR)
    row_sfx.pack(pady=8)
    tk.Label(row_sfx, text="Effetti Sonori", font=FONT_LABEL,
             fg=TEXT_COLOR, bg=BG_COLOR, width=16, anchor="e").grid(row=0, column=0, padx=8)

    sfx_btn = tk.Button(row_sfx,
                        text="ON" if sfx_on else "OFF", font=FONT_BTN,
                        fg=BTN_TEXT,
                        bg="#2e6e2e" if sfx_on else "#6e2e2e",
                        activebackground=BTN_COLOR_1, activeforeground=BG_COLOR,
                        width=6, relief="flat", command=toggle_sfx, cursor="hand2")
    sfx_btn.grid(row=0, column=1, padx=8)

    create_separator(f)
    tk.Frame(f, bg=BG_COLOR).pack(pady=10)
    tk.Label(f, text="", bg=BG_COLOR).pack()
    create_menu_btn(f, "TORNA AL MENU", go_to_main_menu)


# ----------------------------------------------------------------------------
# BUILD UI GENERALE
# ----------------------------------------------------------------------------
def build_ui():
    global canvas, settings_frame
    canvas = tk.Canvas(root, width=WIN_W, height=WIN_H,
                       highlightthickness=0, bg=BG_COLOR)
    canvas.pack(fill="both", expand=True)

    if bg_img:
        canvas.create_image(0, 0, anchor="nw", image=bg_img)

    canvas.create_rectangle(0, 0, WIN_W, WIN_H,
                             fill=BG_COLOR, stipple="gray75", outline="")

    settings_frame = tk.Frame(canvas, bg=BG_COLOR, highlightthickness=0)

    build_main_menu()
    build_settings_menu()
    show_main_menu()


def setup_window():
    root.geometry(f"{WIN_W}x{WIN_H}")
    root.resizable(False, False)
    root.configure(bg=BG_COLOR)
    root.update_idletasks()
    x = (root.winfo_screenwidth()  - WIN_W) // 2
    y = (root.winfo_screenheight() - WIN_H) // 2
    root.geometry(f"{WIN_W}x{WIN_H}+{x}+{y}")


# ----------------------------------------------------------------------------
# AVVIO
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    setup_window()
    load_assets()
    build_ui()
    root.mainloop()