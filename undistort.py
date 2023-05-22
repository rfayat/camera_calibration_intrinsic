"""Undistort a video from a calibration toml file.

Author: Romain FAYAT, May 2022
"""
import toml
from pathlib import Path
import cv2


def get_new_camera_matrix(matrix, dist, size):
    "Return the new camera parameters from intrinisc calibration."
    return cv2.getOptimalNewCameraMatrix(matrix, dist, size, 1, size)


def undistort(frame, matrix, dist, matrix_new, roi):
    "Undistort and crop a frame."
    dst = cv2.undistort(frame, matrix, dist, None, matrix_new)
    x, y, w, h = roi
    return dst[y:y+h, x:x+w]


# TODO: Read the toml and process the video
matrix_new, roi = get_new_camera_matrix(matrix, dist, size)
