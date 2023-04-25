"Simplified version of anipose's calibrate scripts for intrinsic properties."
from pathlib import Path
import sys
from utils import get_calibration_board
import toml


def detect_board(config, path_in):
    "Return the coordinates of a calibration board from a video file."
    board = get_calibration_board(config)
    detection = None
    return detection


def calibrate(config, detection, path_out):
    "Intrinsic parameters calibration from board detection."
    board = get_calibration_board(config)


if __name__ == "__main__":
    if len(sys.argv) < 1:
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
    detection = detect_board(config, path_in)
    calibration = calibrate(config, detection, path_out)
    # Save the calibration as a toml file
    