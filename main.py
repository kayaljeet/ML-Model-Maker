import os
import zipfile
import shutil
import subprocess
from flask import Flask, render_template, request, send_from_directory, jsonify, session, redirect
import threading
import uuid

app = Flask(__name__)
app.secret_key = os.urandom(24)


def initial_setup():
    repo_path = 'yolov5train'

    # Check if the 'yolov5train' directory already exists
    if os.path.exists(repo_path):
        return 1
    else:
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


initial_setup()


def setup_environment(unique_training_dir):
    repo_path = os.path.join(unique_training_dir, 'yolov5train')
    shutil.copytree('yolov5train', repo_path)


def delete_client_session():
    global current_status
    session_id = session.get('session_id')
    if session_id:
        session_folder = os.path.join('client_sessions', session_id)
        shutil.rmtree(session_folder)
        current_status = "Session Deleted"


unique_training_dir = ''  # Global variable to hold the training directory


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('start_pressed') == 'true':
            session['session_id'] = str(uuid.uuid4())  # Store session ID in the user's session

            session_folder = os.path.join('client_sessions', session['session_id'])
            os.makedirs(session_folder, exist_ok=True)

            setup_thread = threading.Thread(target=setup_environment, args=(session_folder,))
            setup_thread.start()

            return render_template('index.html')  # Redirect to 'index.html' after starting the session

    return render_template('session.html')  # Render the session.html template


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'num_classes' not in request.form or 'class_name' not in request.form:
        return "Incomplete form data"

    file = request.files['file']
    num_classes = int(request.form['num_classes'])
    class_names = request.form.getlist('class_name')

    if file.filename == '':
        return "No selected file"

    if 'session_id' not in session:
        return "No active session"

    session_id = session['session_id']
    session_folder = os.path.join('client_sessions', session_id)

    download_folder = os.path.join(session_folder, 'yolov5train/yolov5/runs/train/exp/weights')
    app.config['DOWNLOAD_FOLDER'] = download_folder

    temp_folder = os.path.join(session_folder, 'temp_upload')
    temp_path = os.path.join(temp_folder, file.filename)
    os.makedirs(temp_folder, exist_ok=True)
    file.save(temp_path)

    dataset_path = os.path.abspath(os.path.join(session_folder, 'yolov5train/yolov5', 'dataset.yaml'))
    with open(dataset_path, 'w') as yaml_file:
        yaml_file.write("train: ../data/images/training/\n")
        yaml_file.write("val: ../data/images/validation/\n")
        yaml_file.write(f"\nnc: {num_classes}\n\n")
        yaml_file.write(f"names: {str(class_names)}\n")

    # Extracting the first directory to 'data'
    with zipfile.ZipFile(temp_path, 'r') as zip_ref:
        first_item = zip_ref.namelist()[0]  # Get the name of the first item in the archive
        zip_ref.extractall(os.path.abspath(os.path.join(session_folder, 'yolov5train')))
        extracted_path = os.path.join(session_folder, 'yolov5train', first_item)
        # Rename the extracted item to 'data'
        os.rename(extracted_path, os.path.join(session_folder, 'yolov5train', 'data'))

    folder_path = os.path.join(session_folder, 'temp_upload')
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

    repo_path = os.path.join(session_folder, 'yolov5train')
    folder_to_delete = '__MACOSX'
    folder_path = os.path.join(repo_path, folder_to_delete)
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

    train_script_path = os.path.join(repo_path, 'yolov5/train.py')
    dataset_path = os.path.join(repo_path, 'yolov5/dataset.yaml')
    weights_path = os.path.join(repo_path, 'yolov5s.pt')

    train_command = f"python3 {train_script_path} --img 416 --batch 16 --epochs 100 --data {dataset_path} --weights {weights_path}"

    def run_training():
        global current_status
        try:
            current_status = "Training"
            # subprocess.run(train_command, shell=True, check=True)
            print('Training done')
            current_status = "Finished Training"
        except subprocess.CalledProcessError as e:
            current_status = 'Error'
            delete_client_session()

    train_thread = threading.Thread(target=run_training)
    train_thread.start()

    return render_template('training.html')
import os
import zipfile
import shutil
import subprocess
from flask import Flask, render_template, request, send_from_directory, jsonify, session, redirect
import threading
import uuid

app = Flask(__name__)
app.secret_key = os.urandom(24)


def initial_setup():
    repo_path = 'yolov5train'

    # Check if the 'yolov5train' directory already exists
    if os.path.exists(repo_path):
        return 1
    else:
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


initial_setup()


def setup_environment(unique_training_dir):
    repo_path = os.path.join(unique_training_dir, 'yolov5train')
    shutil.copytree('yolov5train', repo_path)


def delete_client_session():
    global current_status
    session_id = session.get('session_id')
    if session_id:
        session_folder = os.path.join('client_sessions', session_id)
        shutil.rmtree(session_folder)
        current_status = "Session Deleted"


unique_training_dir = ''  # Global variable to hold the training directory


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('start_pressed') == 'true':
            session['session_id'] = str(uuid.uuid4())  # Store session ID in the user's session

            session_folder = os.path.join('client_sessions', session['session_id'])
            os.makedirs(session_folder, exist_ok=True)

            setup_thread = threading.Thread(target=setup_environment, args=(session_folder,))
            setup_thread.start()

            return render_template('index.html')  # Redirect to 'index.html' after starting the session

    return render_template('session.html')  # Render the session.html template


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'num_classes' not in request.form or 'class_name' not in request.form:
        return "Incomplete form data"

    file = request.files['file']
    num_classes = int(request.form['num_classes'])
    class_names = request.form.getlist('class_name')

    if file.filename == '':
        return "No selected file"

    if 'session_id' not in session:
        return "No active session"

    session_id = session['session_id']
    session_folder = os.path.join('client_sessions', session_id)

    download_folder = os.path.join(session_folder, 'yolov5train/yolov5/runs/train/exp/weights')
    app.config['DOWNLOAD_FOLDER'] = download_folder

    temp_folder = os.path.join(session_folder, 'temp_upload')
    temp_path = os.path.join(temp_folder, file.filename)
    os.makedirs(temp_folder, exist_ok=True)
    file.save(temp_path)

    dataset_path = os.path.abspath(os.path.join(session_folder, 'yolov5train/yolov5', 'dataset.yaml'))
    with open(dataset_path, 'w') as yaml_file:
        yaml_file.write("train: ../data/images/training/\n")
        yaml_file.write("val: ../data/images/validation/\n")
        yaml_file.write(f"\nnc: {num_classes}\n\n")
        yaml_file.write(f"names: {str(class_names)}\n")

    # Extracting the first directory to 'data'
    with zipfile.ZipFile(temp_path, 'r') as zip_ref:
        first_item = zip_ref.namelist()[0]  # Get the name of the first item in the archive
        zip_ref.extractall(os.path.abspath(os.path.join(session_folder, 'yolov5train')))
        extracted_path = os.path.join(session_folder, 'yolov5train', first_item)
        # Rename the extracted item to 'data'
        os.rename(extracted_path, os.path.join(session_folder, 'yolov5train', 'data'))

    folder_path = os.path.join(session_folder, 'temp_upload')
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

    repo_path = os.path.join(session_folder, 'yolov5train')
    folder_to_delete = '__MACOSX'
    folder_path = os.path.join(repo_path, folder_to_delete)
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

    train_script_path = os.path.join(repo_path, 'yolov5/train.py')
    dataset_path = os.path.join(repo_path, 'yolov5/dataset.yaml')
    weights_path = os.path.join(repo_path, 'yolov5s.pt')

    train_command = f"python3 {train_script_path} --img 416 --batch 16 --epochs 100 --data {dataset_path} --weights {weights_path}"

    def run_training():
        global current_status
        try:
            current_status = "Training"
            # subprocess.run(train_command, shell=True, check=True)
            print('Training done')
            current_status = "Finished Training"
        except subprocess.CalledProcessError as e:
            current_status = 'Error'
            delete_client_session()

    train_thread = threading.Thread(target=run_training)
    train_thread.start()

    return render_template('training.html')


@app.route('/training')
def training_page():
    return render_template('training.html')


current_status = "Not Training"


@app.route('/training_status', methods=['GET'])
def get_training_status():
    global current_status
    return jsonify({'status': current_status})


@app.route('/download/best.pt')
def download_file():
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], 'best.pt')


if __name__ == '__main__':
    app.run(debug=True)


@app.route('/training')
def training_page():
    return render_template('training.html')


current_status = "Not Training"


@app.route('/training_status', methods=['GET'])
def get_training_status():
    global current_status
    return jsonify({'status': current_status})


@app.route('/download/best.pt')
def download_file():
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], 'best.pt')


if __name__ == '__main__':
    app.run(debug=True)
