# Camera calibration intrinsic
Code for calibrating intrinisic properties from a camera using aniposelib.

We will simply rewamp the parts of code of [anipose](https://anipose.readthedocs.io) (Karashchuk et al., *Cell Reports*, 2021, doi: [10.1016/j.celrep.2021.109730](https://doi.org/10.1016/j.celrep.2021.109730)) that takes care of this part.



## Installation

Clone the repository and install the requirements:

```bash
$ git clone https://github.com/rfayat/camera_calibration_intrinsic
$ cd camera_calibration_intrinsic
$ pip install -r requirements.txt
```

## Generating the calibration board

### Configuration file
Parameters for the size, type of board, number of rows and columns in stored in the [config.toml](./config.toml) file which can be edited.

See [anipose documentation](https://anipose.readthedocs.io/en/latest/params.html#parameters-for-calibration) on the content of this configuration file. 

### Saving the board as a png

From the `camera_calibration_intrinsic` folder, simply run the [generate_board.py](./generate_board.py) script:

```bash
$ python -m generate_board
```

The calibration board is saved in the Desktop folder (this can be edited in the script).


## Actual calibration
TODO, grab the intrinsic calibration part from [anipose calibration script](https://github.com/lambdaloop/anipose/blob/dbebebba1e438f563f373245c2e546ece118fc65/anipose/calibrate.py).
