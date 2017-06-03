"""
\file utilities.py
\brief      Collection of utility functions acting as facilitator for several
            tasks

\author     Michael Ebner (michael.ebner.14@ucl.ac.uk)
\date       June 2017
"""

import os
import sys
import pylab
import numpy as np
import SimpleITK as sitk


def file_exists(file_path):
    """!
    Check whether file exists to given file_path

    \param      file_path  path to file whose existence to be checked

    \return     true if the file exists, otherwise false.
    """
    return True if os.path.isfile(file_path) else False


def directory_exists(directory_path):
    """!
    Check whether directory exists to given directory path

    \param      directory_path  path to directory whose existence to be checked

    \return     true if the file exists, otherwise false.
    """
    return True if os.path.isdir(directory_path) else False


def pause():
    """
    Pause current execution and wait for user response
    """
    program_pause = raw_input(
        "Press the <ENTER> key to continue or hit <C> to quit: ")

    if program_pause in ["c", "C"]:
        sys.exit()

def show_image(image_data, target_data=None, title=None, alpha=0.4):
        pylab.imshow(image_data, cmap="Greys_r")
        
        if target_data is not None:
            pylab.imshow(target_data, cmap="bone", alpha=alpha)
        
        if title is not None:
            pylab.title(title)
        
        pylab.show(block=False)

def print_title(title, symbol="*", counts=3):
    """
    Print title in predefined format
    """
    print_line_separator(symbol=symbol)
    print(counts*symbol + " " + title + " " + counts*symbol)


def print_debug_info(text, newline=True, prefix="--- "):
    """
    Print debug info in predefined format
    """
    if newline:
        print(prefix + text)
    else:
        sys.stdout.write(prefix + text)


def print_line_separator(add_newline=True, symbol="*", length=99):
    """
    Print line as separator
    """
    if add_newline:
        print("\n")
    print(symbol*length)

def show_image_data(image_data, target_data=None, title=None, dir_tmp="/tmp/"):

        image_sitk = sitk.GetImageFromArray(image_data)
        target_sitk = sitk.GetImageFromArray(target_data.astype(np.uint8))

        title = str(title)

        sitk.WriteImage(image_sitk, dir_tmp + title + ".nii.gz")
        sitk.WriteImage(target_sitk, dir_tmp + title + "_mask.nii.gz")

        cmd = "itksnap "
        cmd += "-g " + dir_tmp + title + ".nii.gz "
        cmd += "-s " + dir_tmp + title + "_mask.nii.gz "

        os.system(cmd)