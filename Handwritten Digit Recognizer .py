# ===============================================#
#       Handwritten Digit Recognizer (ML)      #
#----------------------------------------------#
#                             #
#   Demonstrates a Support Vector Machine (SVM)  #
#         for image classification.            #
# ===============================================#

# Import necessary packages
import tkinter as tk
from tkinter import Canvas, Label, Button, Frame
import numpy as np
from sklearn import datasets, svm
from PIL import Image, ImageOps
import io

'''
-------------------------
Part 1: Machine Learning
-------------------------
- Load the dataset.
- Create and train the Support Vector Machine (SVM) classifier.
'''
print("Preparing the ML model...")

# Load the digits dataset from scikit-learn
digits = datasets.load_digits()

# Create the Support Vector Machine (SVM) classifier
# 'gamma' is a model parameter, and 'C' is a regularization parameter.
model = svm.SVC(gamma=0.001, C=100.)

# Train the model on the entire dataset
# model.fit() teaches the classifier the relationship between the images and their labels.
model.fit(digits.data, digits.target)

print("Model is trained and ready!")


'''
-------------------------
Part 2: GUI Application
-------------------------
- Create a Tkinter window with a canvas for drawing.
- Functions to handle drawing, image processing, prediction, and clearing.
'''
class DigitRecognizerApp:
    def __init__(self, root, model):
        self.root = root
        self.model = model
        self.root.title("Digit Recognizer")
        self.root.configure(bg="#2c3e50")

        # --- Member Variables ---
        self.last_x, self.last_y = None, None
        self.canvas_width = 280  # 10x the size of MNIST images (28x28)
        self.canvas_height = 280
        self.pen_size = 12

        # --- UI Elements ---
        # Frame for the canvas
        canvas_frame = Frame(root, bg="#2c3e50", padx=10, pady=10)
        canvas_frame.pack(side=tk.TOP)

        # Main drawing canvas
        self.canvas = Canvas(canvas_frame, width=self.canvas_width, height=self.canvas_height, bg="white", cursor="cross")
        self.canvas.pack()
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset_coords)

        # Frame for controls
        control_frame = Frame(root, bg="#2c3e50", pady=10)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Prediction label
        self.pred_label = Label(control_frame, text="Draw a digit...", font=('Helvetica', 20, 'bold'), fg="#ecf0f1", bg="#2c3e50")
        self.pred_label.pack(pady=(0, 10))

        # Button container
        button_container = Frame(control_frame, bg="#2c3e50")
        button_container.pack()

        # Predict button
        self.predict_btn = Button(button_container, text="Predict", command=self.predict_digit, font=('Helvetica', 14, 'bold'), bg="#2980b9", fg="white", relief="flat", padx=10)
        self.predict_btn.pack(side=tk.LEFT, padx=5)

        # Clear button
        self.clear_btn = Button(button_container, text="Clear", command=self.clear_canvas, font=('Helvetica', 14, 'bold'), bg="#c0392b", fg="white", relief="flat", padx=10)
        self.clear_btn.pack(side=tk.LEFT, padx=5)

    def paint(self, event):
        """Draws on the canvas."""
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                   width=self.pen_size, fill='black',
                                   capstyle=tk.ROUND, smooth=tk.TRUE)
        self.last_x = event.x
        self.last_y = event.y

    def reset_coords(self, event):
        """Resets coordinates when the mouse is released."""
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        """Clears the canvas and the prediction label."""
        self.canvas.delete("all")
        self.pred_label.config(text="Draw a digit...")

    def preprocess_image(self):
        """
        Processes the canvas drawing to match the format of the MNIST dataset.
        1. Saves canvas content as an in-memory image.
        2. Resizes the image to 8x8 pixels.
        3. Converts to grayscale.
        4. Inverts colors (model expects white digit on black background).
        5. Flattens the 8x8 image into a 1D array of 64 pixels.
        """
        # Save the canvas content to a PostScript file in memory
        ps = self.canvas.postscript(colormode='color')
        # Use PIL to open the PostScript image
        img = Image.open(io.BytesIO(ps.encode('utf-8')))
        
        # Invert colors (from black-on-white to white-on-black)
        img = ImageOps.invert(img.convert('L'))
        
        # Resize to 8x8, which is the size of the images in scikit-learn's digits dataset
        img = img.resize((8, 8), Image.LANCZOS)
        
        # Convert image data to a numpy array
        img_array = np.array(img)
        
        # Flatten the 8x8 array into a 1D array of 64 elements
        img_flat = img_array.reshape(1, -1)
        
        # Normalize the pixel values to be in the range the model expects
        # The scikit-learn dataset has pixel values from 0 to 16
        img_flat = (img_flat / 255.0) * 16
        
        return img_flat

    def predict_digit(self):
        """Predicts the digit drawn on the canvas."""
        try:
            # Preprocess the drawing
            processed_image = self.preprocess_image()
            
            # Use the trained model to make a prediction
            prediction = self.model.predict(processed_image)
            
            # Update the label with the result
            self.pred_label.config(text=f"Prediction: {prediction[0]} ✔️")
        except Exception as e:
            self.pred_label.config(text="Error in prediction!")
            print(f"An error occurred: {e}")

'''
-------------------------
Part 3: Main Execution
-------------------------
'''
if __name__ == "__main__":
    root = tk.Tk()
    app = DigitRecognizerApp(root, model)
    root.mainloop()