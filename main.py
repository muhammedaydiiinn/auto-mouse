import time
import threading
import tkinter as tk
import pyautogui


class ChromeCleanerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chrome Geçmiş Öneri Temizleyici")
        self.root.geometry("470x470")

        self.running = False
        self.stop_event = threading.Event()

        screen_w, screen_h = pyautogui.size()

        self.search_x = tk.IntVar(value=screen_w // 2)
        self.search_y = tk.IntVar(value=90)

        self.delete_x = tk.IntVar(value=screen_w - 60)
        self.delete_y = tk.IntVar(value=90)

        self.hover_offset = tk.IntVar(value=35)
        self.delete_per_round = tk.IntVar(value=8)
        self.round_count = tk.IntVar(value=5)

        self.start_delay = tk.IntVar(value=8)
        self.after_search_wait = tk.DoubleVar(value=0.6)
        self.click_delay = tk.DoubleVar(value=0.45)

        self.build_ui(screen_w, screen_h)

    def build_ui(self, screen_w, screen_h):
        tk.Label(
            self.root,
            text=f"Ekran boyutu: {screen_w} x {screen_h}"
        ).pack(pady=5)

        tk.Label(
            self.root,
            text=(
                "Önce arama çubuğu konumunu, sonra X silme konumunu kaydet.\n"
                "Başlatınca pencere küçülür, sen Chrome'a geçersin."
            ),
            wraplength=430
        ).pack(pady=5)

        frame = tk.Frame(self.root)
        frame.pack(pady=8)

        self.add_row(frame, "Arama X:", self.search_x, 0)
        self.add_row(frame, "Arama Y:", self.search_y, 1)
        self.add_row(frame, "Silme X:", self.delete_x, 2)
        self.add_row(frame, "Silme Y:", self.delete_y, 3)
        self.add_row(frame, "Hover mesafesi:", self.hover_offset, 4)
        self.add_row(frame, "Tur başına silme:", self.delete_per_round, 5)
        self.add_row(frame, "Tur sayısı:", self.round_count, 6)
        self.add_row(frame, "Başlama süresi sn:", self.start_delay, 7)
        self.add_row(frame, "Arama sonrası bekleme:", self.after_search_wait, 8)
        self.add_row(frame, "Tık arası bekleme:", self.click_delay, 9)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="3 sn sonra arama çubuğunu kaydet",
            command=self.capture_search_delayed,
            width=30
        ).grid(row=0, column=0, padx=5, pady=4)

        tk.Button(
            btn_frame,
            text="3 sn sonra silme X'i kaydet",
            command=self.capture_delete_delayed,
            width=30
        ).grid(row=1, column=0, padx=5, pady=4)

        tk.Button(
            btn_frame,
            text="Arama test git",
            command=self.test_search,
            width=18
        ).grid(row=0, column=1, padx=5, pady=4)

        tk.Button(
            btn_frame,
            text="Silme test git",
            command=self.test_delete,
            width=18
        ).grid(row=1, column=1, padx=5, pady=4)

        tk.Button(
            btn_frame,
            text="Başlat",
            command=self.start_delayed,
            width=18
        ).grid(row=2, column=0, padx=5, pady=8)

        tk.Button(
            btn_frame,
            text="Durdur",
            command=self.stop_clicking,
            width=18
        ).grid(row=2, column=1, padx=5, pady=8)

        self.status = tk.Label(
            self.root,
            text="Hazır",
            fg="blue",
            wraplength=430
        )
        self.status.pack(pady=10)

        tk.Label(
            self.root,
            text="Acil durdurma: Mouse'u ekranın sol üst köşesine götür.",
            fg="red",
            wraplength=430
        ).pack(pady=5)

    def add_row(self, parent, label, variable, row):
        tk.Label(parent, text=label).grid(row=row, column=0, sticky="e", padx=5, pady=3)
        tk.Entry(parent, textvariable=variable, width=12).grid(row=row, column=1, padx=5, pady=3)

    def capture_search_delayed(self):
        self.status.config(
            text="3 saniye içinde Chrome'a geç, mouse'u arama çubuğunun üstüne götür."
        )

        def worker():
            time.sleep(3)
            pos = pyautogui.position()
            self.root.after(0, lambda: self.save_search(pos.x, pos.y))

        threading.Thread(target=worker, daemon=True).start()

    def capture_delete_delayed(self):
        self.status.config(
            text="3 saniye içinde Chrome'a geç, mouse'u X silme simgesinin üstüne götür."
        )

        def worker():
            time.sleep(3)
            pos = pyautogui.position()
            self.root.after(0, lambda: self.save_delete(pos.x, pos.y))

        threading.Thread(target=worker, daemon=True).start()

    def save_search(self, x, y):
        self.search_x.set(x)
        self.search_y.set(y)
        self.status.config(text=f"Arama çubuğu kaydedildi: x={x}, y={y}")

    def save_delete(self, x, y):
        self.delete_x.set(x)
        self.delete_y.set(y)
        self.status.config(text=f"Silme X kaydedildi: x={x}, y={y}")

    def test_search(self):
        x = self.search_x.get()
        y = self.search_y.get()

        def worker():
            time.sleep(1)
            pyautogui.moveTo(x, y, duration=0.3)
            self.root.after(0, lambda: self.status.config(text="Arama test tamam."))

        threading.Thread(target=worker, daemon=True).start()

    def test_delete(self):
        x = self.delete_x.get()
        y = self.delete_y.get()

        def worker():
            time.sleep(1)
            pyautogui.moveTo(x, y, duration=0.3)
            self.root.after(0, lambda: self.status.config(text="Silme test tamam."))

        threading.Thread(target=worker, daemon=True).start()

    def start_delayed(self):
        if self.running:
            return

        self.running = True
        self.stop_event.clear()

        delay = self.start_delay.get()

        self.status.config(
            text=f"{delay} saniye içinde Chrome'a geç. Süre bitince otomatik başlayacak."
        )

        self.root.iconify()

        def worker():
            time.sleep(delay)
            self.clean_loop()

        threading.Thread(target=worker, daemon=True).start()

    def stop_clicking(self):
        self.stop_event.set()
        self.running = False
        self.status.config(text="Durduruldu.")

    def clean_loop(self):
        pyautogui.FAILSAFE = True

        search_x = self.search_x.get()
        search_y = self.search_y.get()

        delete_x = self.delete_x.get()
        delete_y = self.delete_y.get()

        hover_offset = self.hover_offset.get()
        delete_per_round = self.delete_per_round.get()
        round_count = self.round_count.get()

        after_search_wait = self.after_search_wait.get()
        click_delay = self.click_delay.get()

        total_clicks = 0

        try:
            for round_no in range(1, round_count + 1):
                if self.stop_event.is_set():
                    break

                # 1. Arama çubuğuna tıkla
                pyautogui.click(search_x, search_y)
                time.sleep(after_search_wait)

                # 2. Bu turda 8 tane sil
                for i in range(delete_per_round):
                    if self.stop_event.is_set():
                        break

                    # Önce X'in çıkması için satırın üstüne gel
                    pyautogui.moveTo(delete_x - hover_offset, delete_y, duration=0.05)
                    time.sleep(0.15)

                    # Sonra X'e tıkla
                    pyautogui.click(delete_x, delete_y)

                    total_clicks += 1

                    self.root.after(
                        0,
                        lambda r=round_no, c=total_clicks: self.status.config(
                            text=f"Çalışıyor... Tur: {r}, toplam silme tıklaması: {c}"
                        )
                    )

                    time.sleep(click_delay)

                # 3. Liste temizlendikten sonra tekrar arama çubuğuna tıkla
                pyautogui.click(search_x, search_y)
                time.sleep(0.4)

        except pyautogui.FailSafeException:
            self.root.after(
                0,
                lambda: self.status.config(
                    text="Fail-safe çalıştı. Mouse sol üst köşeye gittiği için durdu."
                )
            )

        except Exception as e:
            self.root.after(
                0,
                lambda err=e: self.status.config(text=f"Hata: {err}")
            )

        self.running = False
        self.stop_event.set()

        self.root.after(0, self.root.deiconify)
        self.root.after(
            0,
            lambda: self.status.config(
                text=f"Bitti. Toplam silme tıklaması: {total_clicks}"
            )
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = ChromeCleanerGUI(root)
    root.mainloop()