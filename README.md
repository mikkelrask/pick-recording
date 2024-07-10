# List video files to open in mpv
This script lists all files of specified filetypes in a directory and allows the user to select a timestamp. All files matching the selected timestamp will open simultaneously in a video player (mpv).

It is primarily used to pick surveillance recordings and play multiple camera angles side by side from the timestamp of the recordings.

![pick-recording running in kitty](./screenshot.png)

## How to use pick-recording
To use this script, download it, install its dependencies, and make any necessary modifications to suit your needs.

### Clone the Repository
Navigate to where you want to store the script, and clone the repository:
```sh
cd /where/you/want/to/store/
git clone git@github.com:mikkelrask/pick-recording.git
```
Since the script is only one file, you can also download it directly with wget if you don't use git:
```sh
wget -cq --show-progress https://raw.githubusercontent.com/mikkelrask/pick-recording/main/App.py -o ~/pick-recording
```
The above command will download the file to your home directory and name it pick-recording.

### Install Requirements

The script uses the [**pick**](https://pypi.org/project/pick) module to list the timestamps and allow you to navigate with arrow keys or vim keys (hkjl), selecting your pick with the enter/return key.

#### Install pick with pip
I recommend installing pick globally on your system for ease of execution:
```sh
pip install pick
```
If you prefer not to install pick globally, create a virtual environment:
```sh
cd /path/to/pick-recording/
python3 -m venv .
source bin/activate
pip install pick
```
Each time you want to use the script, you will need to reactivate the virtual environment with the `source bin/activate` command from the same directory.

#### Install mpv
You also need to have `mpv` installed for the actual video playback. It's a tiny cross platform video player, and is bundled in most standard package manager repos. See [mpv.io/installation](https://mpv.io/installation/) for info. 

## Change to your needs
Make changes as needed — the script is specific to my use case but should be easily modifiable with basic Python/programming knowledge. For example, these lines (20 and 21) specify where the recordings are stored and their file types:
```py
directory = Path("Change this value to where you recordings are")
file_types = [".mp4"] # change this value as needed, or add more seperated by commas
```
### File name sanitizing
In the `clean_files` function, parts of the filenames specific to my use case are removed _(e.g., `TOP_VIEW`, `BOTTOM_VIEW`, and the file type `.mp4`)_. You can add your own regex patterns or modify the existing ones in the pattern variable on line 36:
```py
pattern = re.compile(r"(-?my-regex-?)|(\.mp4)|(YOUR-REGEX-HERE)")
```

### Timestamps
The timestamps in the filenames are expected in the `ddmmYYYYHHMMSS` format by default, which is then formatted to `dd/mm/YYYY HH:MM:SS` by the `format_timestamps` function. Adjust this as needed for your use case and filenames.  

See the [`date` manual](https://man7.org/linux/man-pages/man1/date.1.html) for more information. 

## Running the script
Invoke the script with Python from your terminal emulator, or double-click the file in your file explorer _(making it executable first if necessary)_
### With python
```sh
python3 App.py
```
### Make script executable (optional)
To run `pick-recording` by double-clicking it in a file explore, first make it executable with `chmod`:
```sh
chmod +x pick-recording
```

## Suggest changes
Suggestions and contributions are always welcome. Although the script is tailored to my use case, it is intended to be easily modifiable. If you have any suggestions, let me know, or fork the repository, implement your changes, and create a PR.