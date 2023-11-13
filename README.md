First Install picamera2

sudo apt install -y python3-picamera2

After create a venv that can access the base python

python -m venv --system-site-packages .env

Then activate the venv

source .env/bin/activate

Then install the requirements

pip install -r requirements.txt

Then run the script