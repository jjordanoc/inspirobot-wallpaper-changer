import os, sys, time, shutil, requests, ctypes
import winreg as reg
import tkinter as tk
from ttkthemes import ThemedTk
from PIL import Image


# Get path to inner .exe files
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Default constant values
MONITOR_RESOLUTION = 1920, 1080
UPDATE_TIME = 60
CURR_DIR = os.getcwd()

# Create new window
window = ThemedTk(theme="arc")
window.title("InspiroBot Wallpapers")
icon_path = resource_path("app.ico")
window.iconbitmap(icon_path)
window.resizable(False, False)

# Main menu
def main():
    # Set update time and start change
    def start():
        time = time_ent.get()
        if time:
            global UPDATE_TIME
            UPDATE_TIME = int(time)
            change()

    # Update time input field
    time_lbl = tk.ttk.Label(text="Update time in seconds:")
    time_lbl.grid(row=0, padx=100, pady=10)
    time_ent = tk.ttk.Entry()
    time_ent.grid(row=1, padx=100, pady=7.5)

    # Create start button, onclick execute start()
    start_btn = tk.ttk.Button(text="Start", command=start)
    start_btn.grid(row=2, padx=100, pady=15)

    # Keep the window open
    window.mainloop()

# Infinite change loop
def change():
    # Destroy window, keep executing while loop on background
    window.destroy()
    while True:
        try:
            # URL of inspiro bot API
            URL = "https://www.inspirobot.me/api?generate=true"

            # API request
            res = requests.get(url = URL, stream=True)
            data = res.content
            img_url = data.decode("utf-8")

            # Request image and save it as a file
            res = requests.get(url=img_url, stream=True)
            with open('quote.jpg', 'wb') as outfile:
                shutil.copyfileobj(res.raw, outfile)

            # Resize image using PIL
            img = Image.open("quote.jpg")
            img_resized = img.resize(MONITOR_RESOLUTION, Image.ANTIALIAS)
            img_resized.save("quote.jpg", "JPEG")

            # Set desktop wallpaper
            img_path = os.path.join(CURR_DIR, "quote.jpg")
            SPI_SETDESKWALLPAPER = 20
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, img_path, 0)
            time.sleep(1)
            os.remove(img_path)
            time.sleep(UPDATE_TIME)

        except:
            continue

# Execute main application
if __name__ == "__main__":
    main()
