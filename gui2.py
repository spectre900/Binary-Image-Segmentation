import cv2
from tkinter import *
from PIL import ImageTk
from PIL import Image as PIL_Image


def displayImage(image, title, description, frame):

    frame1 = Frame(master=frame, pady=10, bg="black")
    frame1.pack()
    titleLabel = Label(
        master=frame1, text=title, font="Script 20", fg="orange", bg="black"
    )
    titleLabel.pack(side=LEFT, padx=10)

    frame2 = Frame(master=frame, pady=20, bg="black")
    frame2.pack()
    canvas = Canvas(master=frame2, width=600, height=500)
    canvas.pack()

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (600, 500))
    image = PIL_Image.fromarray(image)
    image = ImageTk.PhotoImage(image)
    canvas.image = image
    canvas.create_image(0, 0, anchor=NW, image=image)

    if description != "":
        frame3 = Frame(master=frame, pady=20, bg="black")
        frame3.pack()
        descLabel = Label(
            master=frame3, text=description, font="Script 20", fg="white", bg="black"
        )
        descLabel.pack()


def displayOutputInCanvas():
    frame1 = Frame(master=master_frame, width=1530, pady=10, bg="black")
    frame1.pack()
    title = Label(
        master=frame1,
        text="BINARY IMAGE SEGMENTATION",
        font="Script 35",
        fg="#23ff0f",
        bg="black",
    )
    title.pack()

    imageList = [
        cv2.imread("./Results/image.jpg"),
        cv2.imread("./Results/fordFulkerson.jpg"),
        cv2.imread("./Results/edmondKarp.jpg"),
        cv2.imread("./Results/scaling.jpg"),
        cv2.imread("./Results/dinic.jpg"),
        cv2.imread("./Results/image.jpg"),
    ]

    titleList = [
        "Original Image",
        "Ford Fulkerson",
        "Edmond Karp",
        "Scaling",
        "Dinic",
        "Comparison of Runtimes",
    ]

    descList = [""]

    file = open("./Results/results.txt", "r")
    for line in file:
        line = line.split("\n")[0]
        descList.append("Execution Time: " + line + " Seconds")

    descList.append("")

    displayImage(imageList[0], titleList[0], descList[0], master_frame)

    frame2 = Frame(master=master_frame, width=1530, pady=20, bg="black")
    frame2.pack()
    subtitle1 = Label(
        master=frame2, text="RESULTS", font="Script 25", fg="#23ff0f", bg="black"
    )
    subtitle1.pack(side=LEFT, padx=10)

    frame3 = Frame(master=master_frame, pady=20, bg="black")
    frame3.pack()

    for i in range(2):
        for j in range(2):
            frame = Frame(master=frame3, bg="black")
            frame.grid(row=i, column=j, padx=20, pady=20, sticky="nsew")

            idx = 2 * i + j + 1
            displayImage(imageList[idx], titleList[idx], descList[idx], frame)

    displayImage(imageList[5], titleList[5], descList[5], master_frame)

    frame9 = Frame(master=master_frame, width=1530, pady=10, bg="black")
    frame9.pack()


def main():
    # Arguments
    displayOutputInCanvas()


# Configuring the scroll bar widget and canvas widget
def scrollbar_function(event):
    canvas.configure(scrollregion=canvas.bbox("all"), width=1530, height=795)


if __name__ == "__main__":
    # Declaring root window and specifying its attributes
    root = Tk()
    root.title("Virtual Memory Management - Results")
    root.resizable(False, False)
    root.config(bg="black")

    # Defining attributes of root window
    root.resizable(False, False)
    window_height = 800
    window_width = 1550

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))

    root.geometry(
        "{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate)
    )

    # Creating a main frame inside the root window
    main_frame = Frame(root, relief=GROOVE, bd=1, bg="black")
    main_frame.place(x=0, y=0)  # Placing the frame at (10, 10)

    # Creating a canvas inside main_frame
    canvas = Canvas(main_frame, bg="black")
    master_frame = Frame(
        canvas, bg="black", padx=10, pady=10
    )  # Creating master_frame inside the canvas

    # Inserting  and configuring scrollbar widget
    myscrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=myscrollbar.set)

    myscrollbar.pack(side="right", fill="y")
    canvas.pack(side="left")
    canvas.create_window((0, 0), window=master_frame, anchor="nw")
    master_frame.bind("<Configure>", scrollbar_function)

    main()

    # Open the root window and loop
    root.mainloop()
