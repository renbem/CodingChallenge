#!/usr/bin/python

##
# \file showcaseTrainingPipeline.py
# \brief      Showcase how to use training pipeline.
#
# \details    By executing 'python examples/showcaseTrainingPipeline.py'
#             provided test data is read and visualized sequentially. This code
#             can be run by specifying the respective arguments. More
#             information via 'python examples/showcaseTrainingPipeline.py -h'.
#
# \pre        Requires the installation of ITK-SNAP (\p www.itksnap.org) for
#             visualization.
# \author     Michael Ebner (michael.ebner.14@ucl.ac.uk)
# \date       June 2017
#

# Import libraries
import os
import sys
import argparse

from definitions import dir_test_data_final_data

import src.DataReader as DataReader
import src.DataBase as DataBase
import src.utilities as utils


def get_parsed_input_line(verbose, directory_input, csv_file, subdirectory_contours,
                          subdirectory_dicoms, contours_type):
    """!
    Gets the parsed input line.

    \param      verbose                boolean for verbose output
    \param      directory_input        path to root directory of input files
    \param      subdirectory_contours  subdirectory of contours within root directory
    \param      subdirectory_dicoms    subdirectory of dicoms within root directory
    \param      contours_type          string to specify type of contours

    \return     The parsed input line.
    """

    parser = argparse.ArgumentParser(description="Read and visualize generated "
                                     "batches via ITK-SNAP."
                                     "Executing 'python showcaseTrainingPipeline.py' "
                                     "visualizes the data provided in the "
                                     "test folder. Changing the respective "
                                     "variables allows the use of this "
                                     "script on any other data.",
                                     prog="python showcaseTrainingPipeline.py",
                                     epilog="Author: Michael Ebner"
                                     "(michael.ebner.14@ucl.ac.uk)",
                                     )

    parser.add_argument('--directory-input', required=False, type=str,
                        help="Specify input directory for all files/folders. [default: %s]" % (
                            directory_input),
                        default=directory_input)
    parser.add_argument('--csv-file', required=False, type=str,
                        help="CSV-file with two columns 'patient-id' and 'original-id' to link up the appropriate DICOM and contour files [default: %s]" % (
                            csv_file),
                        default=csv_file)
    parser.add_argument('--subdirectory-dicoms', required=False, type=str,
                        help="Subdirectory within input directory pointing to DICOM images [default: %s]" % (
                            subdirectory_dicoms),
                        default=subdirectory_dicoms)
    parser.add_argument('--subdirectory-contours', required=False, type=str,
                        help="Subdirectory within input directory pointing to contour files [default: %s]" % (
                            subdirectory_contours),
                        default=subdirectory_contours)
    parser.add_argument('--contours-type', required=False, type=str,
                        help="Chosen type of contour files. Several contours can be read by using white spaces for separation. Thus, valid inputs are, e.g., 'i-contours', 'o-contours', 'i-contours o-contours' etc. [default: %s]" % (
                            contours_type),
                        default=contours_type)
    parser.add_argument('--verbose', type=bool, required=False,
                        help="Turn on/off verbose output. [default: %s]" % (
                            verbose),
                        default=verbose)

    args = parser.parse_args()

    if args.verbose:
        print("Given Input")
        for arg in sorted(vars(args)):
            utils.print_info("%s: " %(arg), newline=False)
            print(getattr(args, arg))

    return args

if __name__ == '__main__':

    args = get_parsed_input_line(
        verbose=True,
        directory_input=dir_test_data_final_data,
        csv_file=os.path.join(dir_test_data_final_data, "link.csv"),
        subdirectory_contours="contourfiles",
        subdirectory_dicoms="dicoms",
        contours_type="i-contours",
    )

    # Read data
    directory_dicoms = os.path.join(
        args.directory_input, args.subdirectory_dicoms)
    directory_contourfiles = os.path.join(
        args.directory_input, args.subdirectory_contours)

    data_reader = DataReader.DataReader(
        directory_dicoms=directory_dicoms, directory_contours=directory_contourfiles, csv_file=args.csv_file, contours_type=args.contours_type)
    data_reader.read_data()

    # Create data base to manage training samples
    database = DataBase.DataBase(data_reader.get_samples(), batch_size=8, seed=None)
    database.build_training_database()
    
    # Show images with associated mask of each sample sequentially
    count = 1
    while (count < 5):        
        
        # Variant A: Get next batch of length batch_size
        images_array, targets_array = database.get_next_batch()
        
        # Variant B: Get random batch of length batch_size
        # images_array, targets_array = database.get_random_batch()
        
        if images_array is None:
            break
        
        utils.print_title("Batch %d" %(count))

        ## Show 3D images and targets as masks via ITK-SNAP
        utils.show_image_data(images_array, targets_array)
        
        utils.pause()
        count += 1

