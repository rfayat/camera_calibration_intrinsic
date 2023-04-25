"Generate a Charuco calibration board using aniposelib and save it on the Desktop."
import toml
from pathlib import Path
import cv2
from utils import get_calibration_board


def get_calibration_board_image(config):
    board = get_calibration_board(config)
    numx, numy = board.get_size()
    size = numx * 200, numy * 200
    img = board.draw(size)
    return img


if __name__ == "__main__":
    path_toml = Path(__file__).parent / "config.toml"
    config = toml.load(path_toml)
    img = get_calibration_board_image(config)

    path_out = Path("~/Desktop").expanduser()
    cv2.imwrite(str(path_out / "calibration_board.png"), img)
    
