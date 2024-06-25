import tkinter as tk
import random
import time
import json
import threading
import math

class SortVisualizer:
    def __init__(self, root, num_bars, speed, width, height, sort_type, show_config, display_method):
        self.root = root
        self.num_bars = num_bars
        self.speed = speed
        self.width = width
        self.height = height
        self.sort_type = sort_type
        self.show_config = show_config
        self.display_method = display_method

        self.root.title(f"{sort_type} Sort Visualization")
        self.root.geometry(f"{self.width}x{self.height}")

        self.canvas = tk.Canvas(self.root, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.shuffling_label = tk.Label(self.root, text="Shuffling", fg="white", bg="gray", font=("Arial", 16))
        self.shuffling_label.place(relx=0.5, rely=0.5, anchor="center")
        self.shuffling_label.lower()

        self.config_label = tk.Label(self.root, text="", fg="white", bg="black", font=("Arial", 12), anchor="nw", justify="left")
        self.config_label.place(relx=0.01, rely=0.01, anchor="nw")


        self.array = list(range(1, self.num_bars + 1))
        random.shuffle(self.array)  # Ensure array is shuffled initially
        self.colors = self.generate_rainbow_colors(len(self.array))
        self.draw_bars()

        self.sorting = False
        self.start_time = None

        if self.show_config:
            self.display_config()

    def generate_rainbow_colors(self, n):
        colors = []
        for i in range(n):
            hue = i / n
            color = self.hsv_to_rgb(hue, 1.0, 1.0)
            colors.append(color)
        return colors

    def hsv_to_rgb(self, h, s, v):
        if s == 0.0: return v, v, v
        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        i %= 6
        if i == 0: return v, t, p
        if i == 1: return q, v, p
        if i == 2: return p, v, t
        if i == 3: return p, q, v
        if i == 4: return t, p, v
        if i == 5: return v, p, q

    def rgb_to_hex(self, r, g, b):
        return "#{:02x}{:02x}{:02x}".format(int(r * 255), int(g * 255), int(b * 255))

    def draw_bars(self):
        self.canvas.delete("all")
        if self.display_method == "Bars":
            self.draw_bars_display()
        elif self.display_method == "Spiral":
            self.draw_spiral_display()
        elif self.display_method == "Circle":
            self.draw_circle_display()
        self.root.update_idletasks()

    def draw_bars_display(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        bar_width = width / len(self.array)
        for i, val in enumerate(self.array):
            x0 = i * bar_width
            y0 = height - (val * height / self.num_bars)
            x1 = (i + 1) * bar_width
            y1 = height
            color = self.rgb_to_hex(*self.colors[val - 1])  # Use the value for color indexing
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

    def draw_spiral_display(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        radius = min(width, height) / 2.5
        cx, cy = width / 2, height / 2
        angle_step = 360 / len(self.array)
        for i, val in enumerate(self.array):
            angle = math.radians(i * angle_step)
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            x_inner = cx + (radius * val / self.num_bars) * math.cos(angle)
            y_inner = cy + (radius * val / self.num_bars) * math.sin(angle)
            color = self.rgb_to_hex(*self.colors[val - 1])  # Use the value for color indexing
            self.canvas.create_line(cx, cy, x_inner, y_inner, fill=color, width=2)

    def draw_circle_display(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        radius = min(width, height) / 2.5
        cx, cy = width / 2, height / 2
        angle_step = 2 * math.pi / len(self.array)
        for i, val in enumerate(self.array):
            start_angle = i * angle_step
            end_angle = (i + 1) * angle_step
            x_start = cx + radius * math.cos(start_angle)
            y_start = cy + radius * math.sin(start_angle)
            x_end = cx + radius * math.cos(end_angle)
            y_end = cy + radius * math.sin(end_angle)
            color = self.rgb_to_hex(*self.colors[val - 1])  # Use the value for color indexing
            self.canvas.create_polygon(cx, cy, x_start, y_start, x_end, y_end, fill=color, outline="")


    def display_config(self):
        config_text = (
            f"Width: {self.width}\n"
            f"Height: {self.height}\n"
            f"Number of Bars: {self.num_bars}\n"
            f"Speed: {self.speed}\n"
            f"Sort Type: {self.sort_type}\n"
            f"Display Method: {self.display_method}"
        )
        self.config_label.config(text=config_text)

    def bubble_sort(self):
        n = len(self.array)
        for i in range(n):
            for j in range(0, n - i - 1):
                if self.array[j] > self.array[j + 1]:
                    self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]
                    self.draw_bars()
                    time.sleep(self.speed)
        self.draw_bars()

    def merge_sort(self, arr, left, right):
        if left < right:
            mid = (left + right) // 2
            self.merge_sort(arr, left, mid)
            self.merge_sort(arr, mid + 1, right)
            self.merge(arr, left, mid, right)
            self.draw_bars()
            time.sleep(self.speed)

    def merge(self, arr, left, mid, right):
        left_copy = arr[left:mid + 1]
        right_copy = arr[mid + 1:right + 1]

        left_copy_index = 0
        right_copy_index = 0
        sorted_index = left

        while left_copy_index < len(left_copy) and right_copy_index < len(right_copy):
            if left_copy[left_copy_index] <= right_copy[right_copy_index]:
                arr[sorted_index] = left_copy[left_copy_index]
                left_copy_index += 1
            else:
                arr[sorted_index] = right_copy[right_copy_index]
                right_copy_index += 1
            sorted_index += 1

        while left_copy_index < len(left_copy):
            arr[sorted_index] = left_copy[left_copy_index]
            left_copy_index += 1
            sorted_index += 1

        while right_copy_index < len(right_copy):
            arr[sorted_index] = right_copy[right_copy_index]
            right_copy_index += 1
            sorted_index += 1

    def insertion_sort(self):
        for i in range(1, len(self.array)):
            key = self.array[i]
            j = i - 1
            while j >= 0 and key < self.array[j]:
                self.array[j + 1] = self.array[j]
                j -= 1
                self.draw_bars()
                time.sleep(self.speed)
            self.array[j + 1] = key
            self.draw_bars()
            time.sleep(self.speed)

    def quick_sort(self, arr, low, high):
        if low < high:
            pi = self.partition(arr, low, high)
            self.quick_sort(arr, low, pi - 1)
            self.quick_sort(arr, pi + 1, high)

    def partition(self, arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                self.draw_bars()
                time.sleep(self.speed)
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        self.draw_bars()
        time.sleep(self.speed)
        return i + 1

    def animate_shuffle(self):
        self.shuffling_label.lift()
        self.shuffling_label.config(text="Shuffling", bg="gray", fg="white")  # Ensure text is set
        random.shuffle(self.array)
        for i in range(len(self.array)):
            j = random.randint(0, len(self.array) - 1)
            self.array[i], self.array[j] = self.array[j], self.array[i]
            self.draw_bars()
            time.sleep(self.speed / 2)
        self.shuffling_label.lower()

    def shuffle_and_sort(self):
        while True:  # Infinite loop for continuous shuffling and sorting
            self.animate_shuffle()
            self.start_time = time.time()
            self.sorting = True

            if self.sort_type == "Bubble":
                self.bubble_sort()
            elif self.sort_type == "Merge":
                self.merge_sort(self.array, 0, len(self.array) - 1)
            elif self.sort_type == "Insertion":
                self.insertion_sort()
            elif self.sort_type == "Quick":
                self.quick_sort(self.array, 0, len(self.array) - 1)

            self.sorting = False

            time.sleep(2)  # Wait for 2 seconds before shuffling again


class MenuScreen:
    CONFIG_FILE = "config.txt"
    SORT_TYPES = ["Bubble", "Merge", "Insertion", "Quick"]
    DISPLAY_METHODS = ["Bars", "Spiral", "Circle"]

    def __init__(self, root):
        self.root = root
        self.root.title("Sort Visualization Config")
        self.load_config()

        tk.Label(root, text="Screen Width:").pack()
        self.width_entry = tk.Entry(root)
        self.width_entry.pack()
        self.width_entry.insert(0, self.width)

        tk.Label(root, text="Screen Height:").pack()
        self.height_entry = tk.Entry(root)
        self.height_entry.pack()
        self.height_entry.insert(0, self.height)

        tk.Label(root, text="Number of Bars:").pack()
        self.bars_entry = tk.Entry(root)
        self.bars_entry.pack()
        self.bars_entry.insert(0, self.num_bars)

        tk.Label(root, text="Speed (in seconds):").pack()
        self.speed_entry = tk.Entry(root)
        self.speed_entry.pack()
        self.speed_entry.insert(0, self.speed)

        tk.Label(root, text="Sort Type:").pack()
        self.sort_type_var = tk.StringVar(root)
        self.sort_type_var.set(self.sort_type)
        self.sort_type_menu = tk.OptionMenu(root, self.sort_type_var, *self.SORT_TYPES)
        self.sort_type_menu.pack()

        tk.Label(root, text="Display Method:").pack()
        self.display_method_var = tk.StringVar(root)
        self.display_method_var.set(self.display_method)
        self.display_method_menu = tk.OptionMenu(root, self.display_method_var, *self.DISPLAY_METHODS)
        self.display_method_menu.pack()

        self.show_config_var = tk.BooleanVar(root)
        self.show_config_var.set(self.show_config)
        tk.Checkbutton(root, text="Show Config in Display", variable=self.show_config_var).pack()

        tk.Button(root, text="Start", command=self.start_visualization).pack()

    def load_config(self):
        try:
            with open(self.CONFIG_FILE, "r") as file:
                config = json.load(file)
            self.width = config.get("width", 800)
            self.height = config.get("height", 400)
            self.num_bars = config.get("num_bars", 50)
            self.speed = config.get("speed", 0.05)
            self.sort_type = config.get("sort_type", "Bubble")
            self.show_config = config.get("show_config", True)
            self.display_method = config.get("display_method", "Bars")
        except FileNotFoundError:
            self.width = 800
            self.height = 400
            self.num_bars = 50
            self.speed = 0.05
            self.sort_type = "Bubble"
            self.show_config = True
            self.display_method = "Bars"

    def save_config(self):
        config = {
            "width": int(self.width_entry.get()),
            "height": int(self.height_entry.get()),
            "num_bars": int(self.bars_entry.get()),
            "speed": float(self.speed_entry.get()),
            "sort_type": self.sort_type_var.get(),
            "show_config": self.show_config_var.get(),
            "display_method": self.display_method_var.get()
        }
        with open(self.CONFIG_FILE, "w") as file:
            json.dump(config, file)

    def start_visualization(self):
        self.save_config()

        width = int(self.width_entry.get())
        height = int(self.height_entry.get())
        num_bars = int(self.bars_entry.get())
        speed = float(self.speed_entry.get())
        sort_type = self.sort_type_var.get()
        show_config = self.show_config_var.get()
        display_method = self.display_method_var.get()

        self.root.destroy()

        visualization_root = tk.Tk()
        visualizer = SortVisualizer(visualization_root, num_bars, speed, width, height, sort_type, show_config, display_method)
        visualization_root.after(1000, visualizer.shuffle_and_sort)
        visualization_root.mainloop()

def main():
    root = tk.Tk()
    menu = MenuScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()
