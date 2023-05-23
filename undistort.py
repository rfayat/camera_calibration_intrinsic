"""Undistort a video from a calibration toml file.

Note
----
This will consume a LOT of RAM as we are storing both the initial and final
videos as numpy arrays. I did this because I know by experience that opencv
tends to generate segfaults when both a video reader and a video writer are
opened at the same time. 

Author: Romain FAYAT, May 2022
"""
import toml
from pathlib import Path
import cv2
import sys
import numpy as np
from tqdm import tqdm


def get_new_camera_matrix(matrix, dist, size):
    "Return the new camera parameters from intrinisc calibration."
    return cv2.getOptimalNewCameraMatrix(matrix, dist, size, 1, size)


def undistort(frame, matrix, dist, matrix_new, roi):
    "Undistort and crop a frame."
    dst = cv2.undistort(frame, matrix, dist, None, matrix_new)
    x, y, w, h = roi
    return dst[y:y+h, x:x+w]


def get_capture_width(capture):
    "Return the frame width of a capture object."
    return int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))


def get_capture_height(capture):
    "Return the frame height of a capture object."
    return int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))


def get_capture_nframes(capture):
    "Return the frame width of a capture object."
    return int(capture.get(cv2.CAP_PROP_FRAME_COUNT))


def preallocate_frame_stack(capture):
    "Return an array that can store an entire video."
    w = get_capture_width(capture)
    h = get_capture_height(capture)
    n = get_capture_nframes(capture)
    return np.empty((n, h, w, 3), dtype=np.uint8)


def read_all_frames(path_video):
    "Read all frames from a video and store them as a numpy array."
    capture = cv2.VideoCapture(str(path_video))
    frame_all = preallocate_frame_stack(capture)

    for i in tqdm(range(len(frame_all))):
        ret, frame = capture.read()  # Capture frame-by-frame
        if ret:
            frame_all[i] = frame.copy()
        else:  # Could not read the frame
            break

    capture.release()
    return frame_all


def write_all_frames(frame_all, path_video, fps=30):
    "Write an array of frames to a video."
    w, h = frame_all.shape[2], frame_all.shape[1]
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    writer = cv2.VideoWriter(str(path_video), fourcc, fps, (w, h))
    for frame in tqdm(frame_all):
        writer.write(frame)
    writer.release()
    return True
    

def undistort_frame_stack(frame_all, matrix, dist, matrix_new, roi):
    "Undistort an array of frames."
    _, _, w, h = roi
    frame_undistorted = np.zeros((len(frame_all), h, w, 3), dtype=np.uint8)

    for i, frame in tqdm(enumerate(frame_all), total=len(frame_all)):
        frame_undistorted[i] = undistort(frame, matrix, dist, matrix_new, roi)
        
    return frame_undistorted


if __name__ == "__main__":
    # Argument parsing:
    if len(sys.argv) < 3:
        raise ValueError("Need to pass calibration and input video.")
    path_calib = Path(sys.argv[1]).expanduser()
    if not path_calib.is_file():
        raise FileNotFoundError(f"Input calibration {path_calib} path does not exist or is a directory.")
    elif path_calib.suffix != ".toml":
        raise ValueError(f"Input calibration {path_calib} is not a toml file.")
    
    path_in = Path(sys.argv[2]).expanduser()
    if not path_in.is_file():
        raise FileNotFoundError(f"Input video {path_in} path does not exist or is a directory.")
    
    if len(sys.argv) > 3:
        path_out = Path(sys.argv[3]).expanduser().resolve()
        if path_out.exists():
            raise FileExistsError(f"Output file {path_out} already exists.")
    else:
        path_out = path_in.parent / (path_in.stem + "_undistorted.avi")

    print("Loading calibration")
    calib = toml.load(path_calib)
    matrix = np.array(calib["matrix"]).astype(float)
    dist = np.array(calib["dist"]).astype(float)
    size = tuple(calib["size"])

    print("Computing new distortion matrix")
    matrix_new, roi = get_new_camera_matrix(matrix, dist, size)

    print("Loading all frames")
    frame_all = read_all_frames(path_in)

    print("Undistorting frames")
    frame_undistorted = undistort_frame_stack(frame_all, matrix=matrix, dist=dist,
                                            matrix_new=matrix_new, roi=roi)
    print("Writing output video")
    write_all_frames(frame_undistorted, path_out, fps=30)
