import os
import zipfile
import shutil
import subprocess
from flask import Flask, render_template, request, send_from_directory, jsonify
import threading


app = Flask(__name__)

# Clone the repository and unzip the 'yolov5' file
def setup_environment():
    repo_path = 'yolov5train'

    # Check if the 'yolov5train' directory already exists
    if os.path.exists(repo_path):
        # If it exists, delete the existing directory
        shutil.rmtree(repo_path)

    # Clone the repository
    subprocess.run(['git', 'clone', 'https://github.com/kayaljeet/yolov5train.git'])

    # Unzip the 'yolov5' file
    shutil.unpack_archive(os.path.join(repo_path, 'yolov5.zip'), repo_path)

    # Delete specific file if it exists
    file_to_delete = 'yolov5.zip'
    file_path = os.path.join(repo_path, file_to_delete)
    if os.path.exists(file_path):
        os.remove(file_path)

    # Delete specific folder if it exists
    folder_to_delete = '__MACOSX'
    folder_path = os.path.join(repo_path, folder_to_delete)
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

    # Install requirements
    requirements_path = os.path.join(repo_path, 'yolov5', 'requirements.txt')
    subprocess.run(['pip3', 'install', '-r', requirements_path])

    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context

# Run the setup function when the app starts
setup_environment()

# Specify the download folder
download_folder = 'yolov5train/yolov5/runs/train/exp/weights/best.pt'
yolov5_train_folder = 'yolov5train'
yolov5_dataset_folder = os.path.join(yolov5_train_folder, 'yolov5')

# Set the path for the download folder
app.config['DOWNLOAD_FOLDER'] = download_folder

# Ensure the download folder exists
os.makedirs(download_folder, exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    # Save the uploaded file to the temporary upload folder
    temp_folder = 'temp_upload'
    temp_path = os.path.join(temp_folder, file.filename)
    os.makedirs(temp_folder, exist_ok=True)
    file.save(temp_path)

    # Get additional information from the form
    num_classes = int(request.form['num_classes'])  # Convert to an integer
    class_names = request.form.getlist('class_name')  # Use getlist to get multiple values

    # Save dataset.yaml in the yolov5 dataset folder
    dataset_path = os.path.abspath(os.path.join(yolov5_dataset_folder, 'dataset.yaml'))
    with open(dataset_path, 'w') as yaml_file:
        yaml_file.write("train: ../data/images/training/\n")
        yaml_file.write("val: ../data/images/validation/\n")
        yaml_file.write(f"\nnc: {num_classes}\n\n")
        yaml_file.write(f"names: {str(class_names)}\n")

    # Unzip the uploaded file to yolov5train
    with zipfile.ZipFile(temp_path, 'r') as zip_ref:
        zip_ref.extractall(os.path.abspath(yolov5_train_folder))

    # Delete specific folder if it exists
    repo_path = 'yolov5train'
    folder_to_delete = '__MACOSX'
    folder_path = os.path.join(repo_path, folder_to_delete)
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

    # After processing the uploaded file and creating the dataset.yaml, start training
    train_command = "python3 yolov5/train.py --img 416 --batch 16 --epochs 100 --data yolov5/dataset.yaml --weights yolov5s.pt"
    os.chdir('yolov5train')

    def run_training():
        global current_status
        try:
            current_status = "Training"  # Update status when training starts
            subprocess.run(train_command, shell=True, check=True)
            current_status = "Finished Training"  # Update status when training finishes
        except subprocess.CalledProcessError as e:
            current_status = 'Error'  # Update status if there's an error during training

    train_thread = threading.Thread(target=run_training)
    train_thread.start()

    return render_template('training.html')


@app.route('/training')
def training_page():
    return render_template('training.html')

current_status = "Not Training"  # Initialize with default value

@app.route('/training_status', methods=['GET'])
def get_training_status():
    global current_status
    return jsonify({'status': current_status})


@app.route('/download/best.py')
def download_file():
    # Provide a link to download the fixed file 'best.py' from the download folder
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], 'best.py')


if __name__ == '__main__':
    app.run(debug=True)
