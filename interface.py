import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import time
import matriks

selected_output_folder = None
is_running = False

def select_output_folder():
    global selected_output_folder
    folder = filedialog.askdirectory()
    if folder:
        selected_output_folder = folder
        output_label.config(text=f"Seçilen klasör: {folder}")

def run_scrapy_and_excel():
    global is_running
    try:
        is_running = True
        start_loading_animation()

        output_file_path = os.path.join(selected_output_folder, "price_matrix.xlsx")
        # matriks.run_all(output_file_path)

        is_running = False
        loading_label.config(text="")

        if os.path.exists(output_file_path):
            messagebox.showinfo("Başarılı", f"Bot tamamlandı!\nÇıktı dosyası:\n{output_file_path}")
        else:
            messagebox.showerror("Hata", f"Çıktı dosyası bulunamadı:\n{output_file_path}")
    except Exception as e:
        is_running = False
        loading_label.config(text="")
        messagebox.showerror("Hata", f"Hata oluştu:\n{e}")

def run_matriks_script():
    if not selected_output_folder:
        messagebox.showerror("Hata", "Lütfen bir çıktı klasörü seçin.")
        return

    # IMPORTANT: run directly in the main thread using `after()`
    root.after(100, run_scrapy_and_excel)

def start_loading_animation():
    def animate():
        dot_count = 0
        while is_running:
            dots = '.' * (dot_count % 4)
            loading_label.config(text=f"Yükleniyor{dots}")
            dot_count += 1
            time.sleep(0.5)
    threading.Thread(target=animate, daemon=True).start()

# GUI
root = tk.Tk()
root.title("Fiyat Karşılaştırma Botu")
root.geometry("400x250")

select_button = tk.Button(root, text="Çıktı klasörünü seç", command=select_output_folder)
select_button.pack(pady=10)

output_label = tk.Label(root, text="Henüz klasör seçilmedi.")
output_label.pack(pady=5)

run_button = tk.Button(root, text="Botu Çalıştır", command=run_matriks_script, bg="#4CAF50", fg="white")
run_button.pack(pady=20)

loading_label = tk.Label(root, text="", font=("Arial", 12), fg="gray")
loading_label.pack(pady=10)

root.mainloop()
