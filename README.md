# Camera calibration intrinsic
Code for estimating a camera's intrinisic properties and using it to undistort videos using aniposelib and opencv.

For the board detection, will simply rewamp the parts of code of [anipose](https://anipose.readthedocs.io) (Karashchuk et al., *Cell Reports*, 2021, doi:[10.1016/j.celrep.2021.109730](https://doi.org/10.1016/j.celrep.2021.109730)) that takes care it.

The calibration estimate and undistortion are wrappers of the opencv functions designed for this purpose, the full pipeline we use is detailed [here](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html).

Example result, note that the curved aluminum bars in the original frame (left) are straight after the processing (right):
![before_after](example_calibration.png)


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

## Processing pipeline
### Grab the camera properties (calibration)
Here we simplify the [anipose calibration script](https://github.com/lambdaloop/anipose/blob/dbebebba1e438f563f373245c2e546ece118fc65/anipose/calibrate.py) for detecting the boards and combine it with bits of opencv code for the actual calibration part.


You'll need to record a calibration video using the calibration board generated at the previous step. Try to cover the full field of view of the camera and to show the board with diffent orientations. An example calibration video is available [here](https://drive.google.com/file/d/1GYCKgIv4uGF9z4vxeVpEbppbzZ-rK6Z1/view).

```bash
$ python -m calibrate path/to/calibration_video.avi path/to/output/calibration.toml
```

**Warning** Make sure that the config.toml file in your local repository folder matches the one you used to generate the board.
### Process a video (undistortion)
We can now simply use the precomputed camera distortion parameters to undistort a video: 

```bash
$ python -m undistort path/to/calibration.toml path/to/distorted_video.avi path/to/output.avi
```
**Warning** This will consume a lot of RAM for large videos (cf [undistort.py](./undistort.py) documentation).
## TODO for polishing
- [ ] Download links to video examples
- [ ] Argument parsers for the scripts using argparse
- [ ] Gif on the readme