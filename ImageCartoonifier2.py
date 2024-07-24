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
top.title('Cartoonify An Image!!')
top.configure(background='white')
label = Label(top, background='#CDCDCD', font=('calibri', 20, 'bold'))


def upload():
    ImagePath = easygui.fileopenbox()
    cartoonify(ImagePath)


def color_quantization(img, k):
    # Defining input data for clustering
    data = np.float32(img).reshape((-1, 3))
    # Defining criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    # Applying cv2.kmeans function
    ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    result = center[label.flatten()]
    result = result.reshape(img.shape)
    return result


def cartoonify(ImagePath):
    # read the image
    orgImage = cv2.imread(ImagePath)
    orgImage = cv2.cvtColor(orgImage, cv2.COLOR_BGR2RGB)
    # print(image)  # image is stored in form of numbers

    # confirm that image is chosen
    if orgImage is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()

    image1 = orgImage
    # plt.imshow(Image1, cmap='gray')

    # converting an image to grayscale
    gray_scale_image = cv2.cvtColor(orgImage, cv2.COLOR_BGR2GRAY)
    # plt.imshow(Image2, cmap='gray')

    # applying median blur to smoothen an image
    smooth_gray_scale = cv2.medianBlur(gray_scale_image, 5)
    image2 = smooth_gray_scale
    # plt.imshow(Image3, cmap='gray')

    # retrieving the edges for cartoon effect
    # by using thresholding technique
    edges = cv2.adaptiveThreshold(smooth_gray_scale, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 6)
    image3 = edges

    # plt.imshow(Image3, cmap='gray')

    # Applying Color_Quantization
    quantized_image = color_quantization(orgImage, 25)
    # plt.imshow(quantized_image, cmap='gray')
    image4 = quantized_image

    # Applying Median_blur
    blurred = cv2.medianBlur(quantized_image, 5)
    # plt.imshow(blurred, cmap='gray')
    image5 = blurred

    # masking edged image with our "Quantized_Image" image
    cartoon_image_2 = cv2.bitwise_and(blurred, blurred, mask=edges)
    # plt.imshow(cartoon_image_2, cmap='gray')
    image6 = cartoon_image_2

    # Plotting the whole transition
    images = [image1, image2, image3, image4, image5, image6]

    fig, axes = plt.subplots(3, 2, figsize=(8, 8), subplot_kw={'xticks': [], 'yticks': []},
                             gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

    save1 = Button(top, text="Save cartoon image", command=lambda: save(image6, ImagePath), padx=30, pady=5)
    save1.configure(background='#364156', foreground='white', font=('calibri', 14, 'bold'))
    save1.pack(side=TOP, pady=50)

    plt.show()


def save(image6, ImagePath):
    # saving an image using imwrite()
    new_name = "cartoonifiedImage2"
    path1 = os.path.dirname(ImagePath)
    extension = os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, new_name + extension)
    cv2.imwrite(path, cv2.cvtColor(image6, cv2.COLOR_RGB2BGR))
    I = "Image saved by name " + new_name + " at " + path
    tk.messagebox.showinfo(title=None, message=I)
    print(path1)


upload = Button(top, text="Cartoonify an Image", command=upload, padx=10, pady=5)
upload.configure(background='#364156', foreground='white', font=('calibri', 12, 'bold'))
upload.pack(side=TOP, pady=50)

top.mainloop()
