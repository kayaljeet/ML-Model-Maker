# Model Maker

This project/application is a tool to train ML models in the form of a PyTorch file, using just an image dataset and classification names.

## How to Use

### Setup

1. Clone the Model Maker repository.
2. In `main.py`, change lines 49 and 52 to the actual repository path and name, which contains the `yolov5.zip` file.
3. Run the application using the command:
   ```bash
   python main.py
   ```
4. Open the webpage of the Flask application (`main.py`). If you haven't signed up yet, proceed to sign up and then log in.

5. After logging in, the option to upload a file and enter the number of classes will appear.

### Upload Process

1. Upload the dataset file (in zip format).
2. Enter the number of classes.
3. Enter the name of each class. (The order of class names should match the order in the `classes.txt` file in the dataset.)
4. Click **Upload**.

The training page will appear, displaying the status. An error will be thrown if any issues occur, such as:
- Invalid dataset format
- Invalid classes (classifications)

Once the training is completed, a download button will appear on the page. 

You can estimate the completion of the training through the 'epoch' status in the program command line, where training will be completed at 99 epochs.

## How to Create a Dataset

1. Gather images of the object you want to detect, with at least 50-100 images per classification, depending on the quality of the images and the type of object. Some objects may even require larger datasets.

2. Open **labelImg**, set the label format to YOLO, change the save directory, and label the images. Save each image after labeling.

3. The labels will be stored in `.txt` format, and a `classes.txt` file will be created containing the classification names.

4. Copy all the `.txt` files into each subdirectory under a 'labels' directory, and place all the images under each subdirectory in an 'images' directory.

### The Structure Should Be:

```
data/
    ├── images/
    │   ├── training/
    │   └── validation/
    └── labels/
        ├── training/
        └── validation/
```

Compress this 'data' directory to obtain a `data.zip` file and upload this to the Model Maker, as mentioned previously.

## Remember

The number of classes entered in the Model Maker should be equal to the number of classes in the `classes.txt` file, and the class names entered should be in the same order as in the `classes.txt` file.
