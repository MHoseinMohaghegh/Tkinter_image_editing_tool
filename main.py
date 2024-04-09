import tkinter as tk
from tkinter import filedialog
from tkinter import colorchooser
from PIL import Image, ImageOps, ImageTk, ImageFilter
from tkinter import ttk

# Global variables for pen color, pen size, and file path
pen_color = 'black'
pen_size = 5
file_path = ''

# Function to add an image to the canvas
def add_image():
    global file_path, canvas_image
    file_path = filedialog.askopenfilename()
    canvas_image = Image.open(file_path)
    width, height = int(canvas_image.width / 2), int(canvas_image.height / 2)
    canvas_image = canvas_image.resize((width, height), resample=Image.LANCZOS)
    canvas.config(width=canvas_image.width, height=canvas_image.height)
    canvas_image = ImageTk.PhotoImage(canvas_image)
    canvas.image = canvas_image
    canvas.create_image(0, 0, image=canvas_image, anchor='nw')

# Function to change the pen size
def change_size(size):
    global pen_size
    pen_size = size

# Function to change the pen color
def change_color():
    global pen_color
    pen_color = colorchooser.askcolor(title='Select Pen Color')[1]

# Function to draw on the canvas
def draw(event):
    x1, y1 = (event.x - pen_size), (event.y - pen_size)
    x2, y2 = (event.x + pen_size), (event.y + pen_size)
    canvas.create_oval(x1, y1, x2, y2, fill=pen_color, outline='')

# Function to clear the canvas
def clear_canvas():
    canvas.delete('all')
    canvas.create_image(0, 0, image=canvas.image, anchor='nw')

# Function to save the canvas as an image
def save():
    global canvas_image
    if canvas_image:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
        )
        canvas.postscript(file=file_path + ".eps", colormode="color")
        img = Image.open(file_path + ".eps")
        img.save(file_path, "png")
        img.close()

# Function to apply image filters
def apply_filter(filter):
    global file_path, canvas_image
    if canvas_image:
        canvas.delete("all")  # Clear canvas
        canvas_image = None    # Close the existing PhotoImage
    if file_path:
        image = Image.open(file_path)
        width, height = int(image.width / 2), int(image.height / 2)
        image = image.resize((width, height), resample=Image.LANCZOS)
        if filter == 'Black and White':
            image = ImageOps.grayscale(image)
        elif filter == 'Blur':
            image = image.filter(ImageFilter.BLUR)
        elif filter == 'Sharpen':
            image = image.filter(ImageFilter.SHARPEN)
        elif filter == 'Smooth':
            image = image.filter(ImageFilter.SMOOTH)
        elif filter == 'Emboss':
            image = image.filter(ImageFilter.EMBOSS)
        canvas.config(width=image.width, height=image.height)
        canvas_image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, image=canvas_image, anchor='nw')

# Tkinter window setup
window = tk.Tk()
window.geometry('1000x600')
window.title('Image Drawing Tool')
window.config(bg='white')

# Left frame for buttons and controls
left_frame = tk.Frame(window, width=200, height=600, bg='white')
left_frame.pack(side='left', fill='y')

# Button to add an image
image_button = tk.Button(left_frame, text='Add Image', command=add_image)
image_button.pack(pady=15)

# Canvas for drawing
canvas = tk.Canvas(window, width=750, height=600)
canvas.pack()

# Button to change pen color
color_button = tk.Button(left_frame, text='Change Pen Color', command=change_color, bg='white')
color_button.pack(pady=5)

# Frame for pen size options
pen_size_frame = tk.Frame(left_frame, bg='white')
pen_size_frame.pack(pady=5)

# Radio buttons for pen size options
pen_size1 = tk.Radiobutton(pen_size_frame, text='Small', value=3, bg='white', command=lambda: change_size(3))
pen_size1.pack(side='left')
pen_size2 = tk.Radiobutton(pen_size_frame, text='Medium', value=5, bg='white', command=lambda: change_size(5))
pen_size2.pack(side='left')
pen_size2.select()
pen_size3 = tk.Radiobutton(pen_size_frame, text='Large', value=7, bg='white', command=lambda: change_size(7))
pen_size3.pack(side='left')

# Button to clear the canvas
clear_button = tk.Button(left_frame, text='Clear', command=clear_canvas, bg='#FF9797')
clear_button.pack(pady=10)

# Label and combobox for selecting filters
filter_label = tk.Label(left_frame, text='Select Filter', bg='white')
filter_label.pack()
filter_combobox = ttk.Combobox(left_frame, values=['Black and White', 'Blur', 'Emboss', 'Sharpen', 'Smooth'])
filter_combobox.pack()

# Binding filter selection event to apply_filter function
filter_combobox.bind('<<ComboboxSelected>>', lambda event: apply_filter(filter_combobox.get()))

# Binding mouse motion event to draw function
canvas.bind('<B1-Motion>', draw)

# Button to save the canvas as an image
save_button = tk.Button(left_frame, text='Save', command=save, bg='white')
save_button.pack()

# Start the Tkinter main loop
window.mainloop()
