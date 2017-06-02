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

    \param      file_path  path to file whose existence you want to check

    \return     true if the file exists, otherwise returns false.
    """
    return True if os.path.isfile(file_path) else False


def directory_exists(directory_path):
    """!
    Check whether directory exists to given directory path

    \param      directory_path  The directory_path

    \return     { description_of_the_return_value }
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
