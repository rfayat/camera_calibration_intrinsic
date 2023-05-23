"Save a camera's intrinsic properties as a toml from a calibration video."
from pathlib import Path
import sys
from utils import get_calibration_board, get_size
import toml
import cv2
import numpy as np


def detect_board(config, path_in):
    "Return the coordinates of a calibration board from a video file."
    board = get_calibration_board(config)
    detection = board.detect_video(str(path_in), progress=True)
    # all_obj, all_img = board.get_all_calibration_points(detection)
    size = get_size(path_in)
    return detection, size


def calibrate(detection, size, n_frame_max=100):
    "Perform the actual calibration from the detection."  
    all_obj, all_img = board.get_all_calibration_points(detection)
    
    # Use only frames with more than 7 detections
    mixed = [(o, i) for (o, i) in zip(all_obj, all_img) if len(o) >= 7]
    objp, imgp = zip(*mixed)
    
    # Select at most n_frame_max frames among them
    if len(objp) > n_frame_max:
        idx_selected = np.linspace(0, len(objp) - 1, n_frame_max, dtype=int)
        objp = tuple(objp[idx] for idx in idx_selected)
        imgp = tuple(imgp[idx] for idx in idx_selected)
    
    # Do the actual calibration
    ret, matrix, dist, rvecs, tvecs = cv2.calibrateCamera(objp, imgp, size, None, None)
    return dict(ret=ret, matrix=matrix, dist=dist, rvecs=rvecs, tvecs=tvecs, size=size)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("Need to pass input calibration video.")
    path_in = Path(sys.argv[1]).expanduser()
    if not path_in.is_file():
        raise FileNotFoundError(f"Input video {path_in} path does not exist or is a directory.")
    
    if len(sys.argv) > 2:
        path_out = Path(sys.argv[2]).expanduser().resolve()
        if path_out.exists():
            raise FileExistsError(f"Output file {path_out} already exists.")
    else:
        path_out = path_in.parent / (path_in.stem + "_calibration.toml")
       
    path_toml = Path(__file__).parent / "config.toml"
    config = toml.load(path_toml)
    board = get_calibration_board(config)
    print("Detecting Board")
    detection, size = detect_board(config, path_in)
    print("Running calibration")
    calibration = calibrate(detection, size, n_frame_max=100)
    
    # Save the calibration as a toml file
    with path_out.open("w") as f:
        toml.dump(calibration, f)
