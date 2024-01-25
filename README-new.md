## Installation Instructions
These instructions are targeted at people running Windows machines.  Anyone running this on a Linux box will need to do things somewhat differently, but it's much easier to install the libraries that way.

1. Ensure Python 3 is installed.  If you already have Python 3 installed (version 3.6+) from something else, that's fine, just make a note of what python version it is (with `python --version`).  If you don't have Python 3 installed yet, you can [download Python 3.8 here](https://www.python.org/ftp/python/3.8.2/python-3.8.2.exe).  

2. Download the code from this repository into a folder, either through `git clone` or by downloading a zipped file of the archive (the button should be on the right, just below the description of the repository (and then unzip it into a folder).  Cloning makes for easier future updates with a single command, but just downloading the zip and unzipping is easier and requires less software.  

3. Open a command prompt window and navigate to the root folder of the project (the same folder with `README.md` and `requirements.txt`.

4. Download the python GDAL wheel [from this page](https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal).  You'll want `GDAL-3.0.4-cpNN-cpNNm-win_amd64.whl` where `NN` is your Python 3 version (38 for 3.8, and so on).  Move the downloaded file into the directory with the code.

5. Download the python Fiona wheel [from this page](https://www.lfd.uci.edu/~gohlke/pythonlibs/#fiona).  You'll want `Fiona-1.8.13-cpNN-cpNNm-win_amd64.whl` where `NN` is your Python 3 version (38 for 3.8, and so on).  Move the downloaded file into the directory with the code.

6. Create a Python 3 virtual environment to install all the libraries needed to run this software.  From the command prompt window in step 3, run `python -m venv venv`, this will create a folder named `venv` and make a self-contained python environment inside it.  If an error occurs, make sure the python version you're running is Python 3, you might need to manually use the correct python executable if you have multiple versions installed on your system at once (just don't uninstall older versions if they do exist, because you might break some other software by doing so).  

7. Activate the virtual environment with `venv\Scripts\activate`.  This should change your command prompt to say `(venv)` at the beginning of the line.  This forces the specific command prompt window you're using to use the copy of python in the `venv` folder instead of using the system-wide python install, letting you avoid messing up other programs when installing needed libraries for this software.  

8. Install the compiled wheels with `pip install GDAL-3.0.4-cpNN-cpNNm-win_amd64.whl` (and the same thing with Fiona); using the `Tab` key to auto-complete filenames helps here.  Just make sure you have the venv activated when running the command, to make sure they get installed to the virtual environment as-intended.

9. Once GDAL and Fiona are installed, install the rest of the dependencies with `pip install -r requirements.txt`.  This will install the rest of the libraries needed that are more cooperative with regards to being installed than GDAL and Fiona.  

Once those things are all done, the environment should be set up and ready to use.  

## Running the code

For running the code, you'll need to open a command prompt window to the correct folder and run `venv\Scripts\activate` to activate the virtual environemnt.  After that, you can use `python mcmc_runner.py` to run the code with whatever command-line arguments are needed.  To get a listing of all the command-line arguments, you can run `python mcmc_runner.py --help`.

Arguments can also be passed in via configuration file, using the `-c` or `--config` flag, see `example_settings.ini` for examples.  

Also, note that the "Creating initial partition" step can take some time.  It's currently configured with a 2-minute timeout (it will retry if it can't make a partition in two minutes).  For larger datasets, it's possible that it could timeout before completing partitioning; this can be tweaked by changing the timeout value (around line 70), but hopefully future versions will automatically calculate an appropriate timeout period based on the input dataset.  

If you kill the program while it is creating the initial partition, you'll need to kill it via Task Manager instead of the normal Ctrl+C.  This is because of how the threading is set up to handle timing out the partitioning process.  