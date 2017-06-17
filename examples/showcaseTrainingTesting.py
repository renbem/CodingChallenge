#!/usr/bin/python

##
# \file showcaseTrainingTesting.py
# \brief      Show how to use the code for training and testing a masking
#             scheme.
#
# \author     Michael Ebner (michael.ebner.14@ucl.ac.uk)
# \date       June 2017
#

# Import libraries
import os
import sys
import argparse
import numpy as np
from scipy import stats

from definitions import dir_test_data_final_data
from definitions import dir_figures

import src.DataReader as DataReader
import src.DataBase as DataBase
import src.utilities as utils
import src.ThresholdMaskingScheme as ThresholdMaskingScheme
import src.TrainingTesting as TrainingTesting


def get_parsed_input_line(verbose, directory_input, csv_file, subdirectory_contours,
                          subdirectory_dicoms, contours_type, N_repetitions, fraction_training):
    """
    Gets the parsed input line.

    \param      verbose                boolean for verbose output
    \param      directory_input        path to root directory of input files
    \param      subdirectory_contours  subdirectory of contours within root directory
    \param      subdirectory_dicoms    subdirectory of dicoms within root directory
    \param      contours_type          string to specify type of contours

    \return     The parsed input line.
    """

    parser = argparse.ArgumentParser(description="Show how to use the code for "
                                     "training and testing a masking scheme.",
                                     prog="python showcaseTrainingTesting.py",
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
    parser.add_argument('--fraction-training', type=float, required=False,
                        help="Fraction in [0, 1] specifying the proportion of samples in the read database used for training. Remaining samples will be used for testing. [default: %s]" % (
                            fraction_training),
                        default=fraction_training)
    parser.add_argument('--N-repetitions', type=int, required=False,
                        help="Number of repetitions to randomly draw training samples, estimate optimal parameter of masking scheme and run testing with it. [default: %s]" % (
                            N_repetitions),
                        default=N_repetitions)
    parser.add_argument('--verbose', type=bool, required=False,
                        help="Turn on/off verbose output. [default: %s]" % (
                            verbose),
                        default=verbose)

    args = parser.parse_args()

    if args.verbose:
        print("Given Input")
        for arg in sorted(vars(args)):
            utils.print_info("%s: " % (arg), newline=False)
            print(getattr(args, arg))

    return args

if __name__ == '__main__':

    args = get_parsed_input_line(
        verbose=True,
        directory_input=dir_test_data_final_data,
        # csv_file=os.path.join(dir_test_data_final_data, "link.csv"),
        csv_file=os.path.join(dir_test_data_final_data, "link_reduced.csv"),
        subdirectory_contours="contourfiles",
        subdirectory_dicoms="dicoms",
        contours_type="i-contours o-contours",
        fraction_training=0.8,
        N_repetitions=10,
    )

    # Read data
    directory_dicoms = os.path.join(
        args.directory_input, args.subdirectory_dicoms)
    directory_contourfiles = os.path.join(
        args.directory_input, args.subdirectory_contours)

    data_reader = DataReader.DataReader(
        directory_dicoms=directory_dicoms, directory_contours=directory_contourfiles, csv_file=args.csv_file, contours_type=args.contours_type)
    data_reader.read_data()
    samples = data_reader.get_samples()

    # Create data base to manage training samples
    database = DataBase.DataBase(samples, seed=1)
    database.build_training_database()

    # Create masking scheme used for predicting blood pool masks
    thresholds_list = range(0, 500, 1)
    threshold_masking_scheme = ThresholdMaskingScheme.ThresholdMaskingScheme(
        thresholds_list=thresholds_list)

    # Create training and testing object
    training_testing = TrainingTesting.TrainingTesting(
        masking_scheme=threshold_masking_scheme,
        database=database,
        fraction_training=args.fraction_training)

    #
    results = np.zeros((args.N_repetitions, 3))

    for i in range(0, args.N_repetitions):
        utils.print_title("Training-Testing-Cycle %d/%d" %
                          (i+1, args.N_repetitions))

        training_testing.randomly_split_into_training_and_testing_data()

        print("Result Training:")
        (estimated_parameter, dice_scores_mean_training) = training_testing.run_training()
        utils.print_info("Optimal Threshold = %d" % (estimated_parameter))
        utils.print_info("Dice Score = %.3f" % (dice_scores_mean_training))

        print("Result Testing (using 'optimal threshold'):")
        _, dice_scores_mean_testing = training_testing.run_testing(
            estimated_parameter)
        utils.print_info("Dice Score = %.3f" % (dice_scores_mean_testing))

        results[i, 0] = estimated_parameter
        results[i, 1] = dice_scores_mean_training
        results[i, 2] = dice_scores_mean_testing

    utils.print_title("Summary:")
    utils.print_info("Mean training Dice score: %.3f" %(results[:,1].mean()))
    utils.print_info("Mean test Dice score: %.3f" %(results[:,2].mean()))
