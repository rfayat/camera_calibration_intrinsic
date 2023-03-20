"Generate a Charuco calibration board using aniposelib."
from aniposelib.boards import Checkerboard, CharucoBoard
import toml
from pathlib import Path
import cv2


def get_calibration_board(config):

    calib = config['calibration']
    board_size = calib['board_size']
    board_type = calib['board_type'].lower()

    if board_type == 'aruco':
        raise NotImplementedError(
            "aruco board is not implemented with the current pipeline")
    elif board_type == 'charuco':
        board = CharucoBoard(
            board_size[0], board_size[1],
            calib['board_square_side_length'],
            calib['board_marker_length'],
            calib['board_marker_bits'],
            calib['board_marker_dict_number'],
            manually_verify=False)

    elif board_type == 'checkerboard':
        board = Checkerboard(board_size[0], board_size[1],
                             calib['board_square_side_length'], manually_verify=manually_verify)
    else:
        raise ValueError("board_type should be one of "
                         "'aruco', 'charuco', or 'checkerboard' not '{}'".format(
                             board_type))

    return board


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
    