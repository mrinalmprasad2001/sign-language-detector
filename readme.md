### Pre Requisites

Install Python in your system (make sure to enable installing pip during python installation).

### Project Requirements installation

Open windows terminal inside the directory `Hand Tracking`.

Run the commands:
- `pip install virtualenv` (Installing virtualenv).
- `python -m venv venv` (Creating virtual enviroment).
- `venv\Scripts\activate` (Activating virtual enviornment).
- `pip install -r requirements.txt` (Installing project requirements).

### Running the project
Open windows terminal inside the directory `Hand Tracking`.

If the enviornment is not activated, Run the command `.\venv\Scripts\activate`.

#### For collecting data
- `python collect_data.py` (Collecting data from USB webcam).
- Show the hand in the camera view.
- Press keys (A-Z) after showing the corresponding letter's hand sign.
- The images will be saved in the directory called `Data`.

#### Training the data
- Go to `https://teachablemachine.withgoogle.com/train`.
- Select Image Project -> Standard Image Model
- Rename `Class 1` to `A` and upload all the files in `Data/A`.
- Similarly, add classes and rename them to corresponding alphabets `(Class 2 - B, Class 3 -> C,...)`.
- Click on `Train Model`.
- After completion click on `Export Model`.
- In the upcoming tab, Select `Tensorflow` tab.
- Select `Keras` model and click `Download my model.`
- Extract the contents of the zip file inside the projects `Model` folder.

#### Sign language tracking
- `python result.py`.
- Show the hand in the camera view.
