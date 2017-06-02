#!/usr/bin/python

##
# \file foo.py
# \brief      
#
# \author     Michael Ebner (michael.ebner.14@ucl.ac.uk)
# \date       June 2017
#

## Import libraries
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import argparse
import pylab

import csv

## Import modules
import src.parsing as parsing
# import src.SimpleITKHelper as sitk
import src.utilities as utils
import src.Image as Image
import src.Target as Target

import src.Image2D as Image2D
import src.DataReader as DataReader

def get_parsed_input_line(
    verbose,
    subdirectory_contourfiles,
    subdirectory_dicoms,
    contours_type,
    ):

    parser = argparse.ArgumentParser(description=
        "Add my description here",
        prog="python reconstructStaticVolume.py",
        epilog="Author: Michael Ebner (michael.ebner.14@ucl.ac.uk)",
        )

    parser.add_argument('--dir-input', type=str, help="", required=True)
    parser.add_argument('--subdirectory-dicoms', type=str, help="Subdirectory within dir-input pointing to DICOM images [default: %s]" %(subdirectory_dicoms), required=False, default=subdirectory_dicoms)
    parser.add_argument('--subdirectory-contourfiles', type=str, help="Subdirectory within dir-input pointing to contour files [default: %s]" %(subdirectory_contourfiles), required=False, default=subdirectory_contourfiles)
    parser.add_argument('--contours-type', type=str, help="Chosen type of contour files [default: %s]" %(contours_type), required=False, default=contours_type)
    parser.add_argument('--csv-file', type=str, help="CSV-file with two columns 'patient-id' and 'original-id' to link up the appropriate DICOM and contour files", required=True)
    parser.add_argument('--verbose', type=bool, help="Turn on/off verbose output. [default: %s]" %(verbose), default=verbose)

    args = parser.parse_args()

    if args.verbose:
        print("Given Input")
        for arg in sorted(vars(args)):
            sys.stdout.write("-- %s: " %(arg))
            print(getattr(args, arg))

    return args

if __name__ == '__main__':

    slice_id = "59"
    slice_id = "68"
    slice_id = "79"
    
    patient_id = "SCD0000101"   #Dicoms
    original_id = "SC-HF-I-1"   #contours
    contour_type = "i-contours"
    csv_file = "link.csv"

    prefix_contours = "IM-0001-"
    suffix_contours =  "-icontour-manual"

    args = get_parsed_input_line(
        verbose=True,
        subdirectory_contourfiles="contourfiles",
        subdirectory_dicoms="dicoms",
        contours_type="i-contours",
        )

    dir_input_dicom = os.path.join(args.dir_input, 'dicoms')
    # dir_input_contourfiles = os.path.join(args.dir_input, 'contourfiles')

    # Read Samples
    directory_dicoms = os.path.join(args.dir_input, args.subdirectory_dicoms)
    directory_contourfiles = os.path.join(args.dir_input, args.subdirectory_contourfiles)
    
    data_reader = DataReader.DataReader(directory_dicoms=directory_dicoms, directory_contours=directory_contourfiles, csv_file=args.csv_file, contours_type=args.contours_type)
    data_reader.read_data()
    training_samples = data_reader.get_training_samples()

    sample = training_samples[0]
    for i in range(0, len(training_samples)):
        training_samples[i].show(1)

        

