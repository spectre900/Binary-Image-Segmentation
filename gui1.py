import cv2
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import messagebox
import tkinter.filedialog as tkFileDialog

# This func is called whenever the 'Select an image' button is clicked
def select_image():
    global canvas
    global path

    canvas.delete("all")
    # open a file chooser dialog and allow the user to select an input image
    path = tkFileDialog.askopenfilename()

    # ensure a file path was selected
    if len(path) > 0 and (path[-4:] == ".jpg" or path[-4:] == ".png"):
        # load the image from disk
        image = cv2.imread(path)
        original_image = image.copy()

        # represents images in BGR order; however PIL represents
        # images in RGB order, so we need to swap the channels
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (600, 500))

        # convert the images to PIL format...
        image = Image.fromarray(image)

        # ...and then to ImageTk format
        image = ImageTk.PhotoImage(image)

        canvas.image = image
        canvas.create_image(0, 0, anchor=NW, image=image)
    else:
        messagebox.showinfo(
            "Warning", "Please choose an image! (It should be a .jpg or .png file)"
        )


# Submit the image for preprocessing if the image path is valid
def submit():
    global path
    global selectedImage
    if len(path) <= 0:
        messagebox.showinfo("Warning", "Please choose an image!")
    else:
        print(path)
        selectedImage = True
        messagebox.showinfo("Info", "Image sent for processing!")
        root.destroy()


# Exit window
def exit_window():
    global root
    root.destroy()


# Main functions
# Declaring root window
if __name__ == "__main__":
    root = Tk()
    root.title("Binary Image Segmentation using Max Flow Algorithms")
    root.config(bg="black")
    root.resizable(False, False)

    window_height = 700
    window_width = 1100

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))
    root.geometry(
        "{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate)
    )

    # Declaring variables
    path = ""
    selectedImage = False

    # create all of the main containers
    top_frame = Frame(root, bg="black", width=1090, height=50, pady=3)
    frame1 = Frame(root, bg="black", width=1090, height=80, padx=3, pady=3)
    frame2 = Frame(root, bg="brown", width=1090, height=510, pady=5, padx=5)
    frame3 = Frame(root, bg="black", width=1090, height=50, pady=3)
    frame4 = Frame(root, bg="black", width=1090, height=10, pady=3)

    # Assigning all frames in a grid layout on the root window
    top_frame.grid(row=1, column=1, padx=5, pady=5)
    frame1.grid(row=2, column=1, padx=5, pady=5)
    frame2.grid(row=3, column=1, padx=5, pady=5)
    frame3.grid(row=5, column=1, padx=5, pady=5)
    frame4.grid(row=6, column=1, padx=5, pady=5)

    # Title label
    title = Label(
        master=top_frame,
        text="BINARY IMAGE SEGMENTATION",
        font="Script 35",
        fg="#23ff0f",
        bg="black",
    )
    title.pack()  # Put the label into the window

    # Text label
    text1 = Label(
        master=frame1,
        text="This system uses Max Flow algorithms to perform Binary Segmentation of Images. Browse your image file and get started!",
        fg="white",
        bg="black",
        font="Script 10",
    )
    text1.pack()

    # Creating a canvas to display the image
    canvas = Canvas(master=frame2, width=600, height=500)
    canvas.pack()

    # Button to browse the image
    btn = Button(
        master=frame3,
        text="Select an image",
        command=select_image,
        font="Script 20",
        fg="blue",
    )
    btn.pack(side="left", padx=10, pady=10)

    # Button to submit the image
    btn = Button(
        master=frame3, text="Submit", command=submit, font="Script 20", fg="green"
    )
    btn.pack(side="left", padx=10, pady=10)

    # Button to exit window
    btn = Button(
        master=frame3, text="Exit", command=exit_window, font="Script 20", fg="red"
    )
    btn.pack(side="left", padx=10, pady=10)

    # Open the root window
    root.mainloop()
