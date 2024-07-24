import cv2  # for image processing
import easygui  # to open the filebox
import numpy as np  # to store image
import imageio  # to read image stored at particular path
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image, ImagePath

top = tk.Tk()
top.geometry('400x400')
top.title('Cartoonify Your Image!')
top.configure(background='white')
label = Label(top, background='#CDCDCD', font=('calibri', 20, 'bold'))


def upload():
    ImagePath = easygui.fileopenbox()
    cartoonify(ImagePath)


def cartoonify(ImagePath):
    # read the image
    orgImage = cv2.imread(ImagePath)
    orgImage = cv2.cvtColor(orgImage, cv2.COLOR_BGR2RGB)
    # print(image)  # image is stored in form of numbers

    # confirm that image is chosen
    if orgImage is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()

    Image1 = orgImage
    # plt.imshow(Image1, cmap='gray')

    # converting an image to grayscale
    gray_scale_image = cv2.cvtColor(orgImage, cv2.COLOR_BGR2GRAY)
    Image2 = gray_scale_image
    # plt.imshow(Image2, cmap='gray')

    # applying median blur to smoothen an image
    smooth_gray_scale = cv2.medianBlur(gray_scale_image, 5)
    Image3 = smooth_gray_scale
    # plt.imshow(Image3, cmap='gray')

    # retrieving the edges for cartoon effect
    # by using thresholding technique
    edges = cv2.adaptiveThreshold(smooth_gray_scale, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 5)
    Image4 = edges
    # plt.imshow(Image4, cmap='gray')

    # applying bilateral filter to remove noise
    # and keep edge sharp as required
    color_image = cv2.bilateralFilter(orgImage, d=9, sigmaColor=200, sigmaSpace=200)
    Image5 = color_image
    # plt.imshow(Image5, cmap='gray')

    # masking edged image with our "BEAUTIFY" image
    cartoon_image = cv2.bitwise_and(color_image, color_image, mask=edges)
    Image6 = cartoon_image
    # plt.imshow(Image6, cmap='gray')

    # Plotting the whole transition
    images = [Image1, Image2, Image3, Image4, Image5, Image6]

    fig, axes = plt.subplots(3, 2, figsize=(8, 8), subplot_kw={'xticks': [], 'yticks': []},
                             gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

    save1 = Button(top, text="Save cartoon image", command=lambda: save(Image6, ImagePath), padx=30, pady=5)
    save1.configure(background='#364156', foreground='white', font=('calibri', 12, 'bold'))
    save1.pack(side=TOP, pady=50)

    plt.show()


def save(Image6, ImagePath):
    # saving an image using imwrite()
    new_name = "cartoonifiedImage"
    path1 = os.path.dirname(ImagePath)
    extension = os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, new_name + extension)
    cv2.imwrite(path, cv2.cvtColor(Image6, cv2.COLOR_RGB2BGR))
    I = "Image saved by name " + new_name + " at " + path
    tk.messagebox.showinfo(title=None, message=I)
    print(path1)


upload = Button(top, text="Cartoonify an Image", command=upload, padx=10, pady=5)
upload.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
upload.pack(side=TOP, pady=50)

top.mainloop()
