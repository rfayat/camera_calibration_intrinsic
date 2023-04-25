"Utils functions, mainly from anipose."
from aniposelib.boards import Checkerboard, CharucoBoard


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
                             calib['board_square_side_length'],
                             manually_verify=False)
    else:
        raise ValueError("board_type should be one of "
                         "'aruco', 'charuco', or 'checkerboard' not '{}'".format(
                             board_type))

    return board
