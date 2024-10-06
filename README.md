# Model Maker
This project/application is a tool to train ML models in form of a PyTorch file, using just a image dataset and Classification names.

## How to use:

**Setup **
Clone the Model Maker repository and:
In `main.py`, change line 49 and 52 to the actual repository path and name, which contains the `yolov5.zip` file

Run the `python main.py`

Open the webpage, of the flask application (`main.py`), and if signup, if already haven't previously, then proceed to login

After logging in, the option to upload a file and enter number of classes will appear:

** 1.Upload the dataset file(in zip format)
 2.Enter number of classes
 3.Enter the name of each class (the order in which the class names are entered should be the same as the order in which they are present in the `classes.txt` in the dataset)
 4.Upload**

The training page will appear, displaying the status, and will throw an error, if any occurs, such as:
Invalid dataset format
Invalid Classes (Classifications)

Once the training is completed, a download button will appear on the page

The completion of the training can be estimated through the 'epoch' status in the program command line, where the training will be completed at 99 epoch

## How to create a dataset
Gather images of the object you want to detect, at least 50-100 per classification, depending on the quality of the images an the type of object...some may even require larger datasets

Open labelImg, and set the label format to YOLO, change the save directory, and label the images, and save each image, after labelling

Now, the labels will be stored in `.txt` format and a `classes.txt` file will be created, containing the classification names

Copy all the `.txt` files into each subdirectory under a 'labels' directory
And all the images under each subdirectory in 'images' directory

### The structure will be:

 \data
	-\images
		-\training
		-\validation
	-\labels
		-\training
		-\validation 
  
Compress this 'data' directory to obtain a `data.zip` and upload this to the ModelMaker, as mentioned previously 

## Remember 
The number of classes entered in the ModelMaker should be equal to the number to classes in the `classes.txt`, and the Class names entered should be in the same order as in the `classes.txt` file
