# Webcam Motion Recorder with Google Drive Upload

A lightweight Python project that captures webcam video, detects motion, records motion events, and uploads captured clips to Google Drive.

## Project Files

- `WebCam2.py` - main application script
- `client_secrets.json` - Google Drive API client configuration
- `recordings/` - automatically created folder for saved video clips

## Features

- Real-time webcam video capture using OpenCV
- Motion detection using background subtraction and contour thresholding
- Automatic recording when motion is detected
- Continue recording for a fixed duration after motion stops
- Save AVI videos locally in `recordings/`
- Upload saved videos to Google Drive using PyDrive

## Requirements

- Python 3.8+
- OpenCV (`opencv-python`)
- NumPy
- PyDrive

## Setup

1. Clone or copy the repository into your workspace.
2. Place your Google Drive API client secret file as `client_secrets.json` in the project folder.
3. Install dependencies:

```bash
pip install opencv-python numpy PyDrive
```

4. If needed, update the path to `client_secrets.json` in `WebCam2.py`:

```python
gauth.LoadClientConfigFile("C:/Users/rohit/Documents/SEM---3-2/py_project/client_secrets.json")
```

## Usage

Run the script from the project folder:

```bash
python WebCam2.py
```

While the application runs:

- It displays a live webcam window titled `Motion Detector`
- Motion overlays are shown on detected regions
- Recorded clips are saved to `recordings/`
- Each saved clip is uploaded to Google Drive automatically
- Press `q` to quit

## Notes

- The default recording duration is 20 seconds after motion stops.
- The video resolution is set to 1280x720.
- The output codec is MJPG and clips are saved as `.avi` files.
- The current script uses a hardcoded absolute path for the Google API client config file.

## Troubleshooting

- If the webcam feed does not appear, check that your webcam is accessible and not used by another application.
- If Google Drive authentication fails, verify `client_secrets.json` and your API credentials.
- If upload fails, make sure you have network access and valid Drive permissions.

## License

Add your preferred license here.
