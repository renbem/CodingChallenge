#!/usr/bin/python

##
# \file analyseImages.py
# \brief      Script to analyse the given image regions masked by i- and
#             o-contours.
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
                          subdirectory_dicoms, contours_type):
    """
    Gets the parsed input line.

    \param      verbose                boolean for verbose output
    \param      directory_input        path to root directory of input files
    \param      subdirectory_contours  subdirectory of contours within root directory
    \param      subdirectory_dicoms    subdirectory of dicoms within root directory
    \param      contours_type          string to specify type of contours

    \return     The parsed input line.
    """

    parser = argparse.ArgumentParser(description="Analyse given image regions "
                                     "masked by i - and o-contours",
                                     prog="python showSamples.py",
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
    database = DataBase.DataBase(samples)
    database.build_training_database()

    # [images_array, targets_array] = database.get_random_batch()
    [images_array, targets_array] = database.get_batch_for_all_samples()

    # Show 3D images and targets as masks via ITK-SNAP
    utils.show_image_data(images_array, targets_array, title="ground-truth")

    utils.print_title("Statistics: Blood Pool vs Heart Muscle [mean (std)]")

    # "Ground-Truth" labelling of blood pool (given by i-contours)
    data_blood_pool = images_array[np.where(targets_array == 2)]

    # "Ground-Truth" labelling of heart muscle (between o- and i-contours)
    data_heart_muscle = images_array[np.where(targets_array == 1)]
    pval = stats.ttest_ind(data_blood_pool, data_heart_muscle)
    alpha = 0.05
    utils.print_info("Sample size: %d 2D images" % (images_array.shape[2]))
    print("Blood Pool: %.3f (%.3f)" %
          (data_blood_pool.mean(), data_blood_pool.std()))
    print("Heart Muscle: %.3f (%.3f)" %
          (data_heart_muscle.mean(), data_heart_muscle.std()))
    if pval[1] < alpha:
        print("Blood pool and heart muscle mean intensities are statistically significant (p < %g)" % (alpha))
    else:
        print("Mean of blood pool and hear muscle intensities are NOT statistically different (p > %g)" % (alpha))

    utils.show_box_plot(
        data=[data_blood_pool, data_heart_muscle],
        x_labels=["Blood Pool", "Heart Muscle"],
        y_label="Image Intensity",
        fig_number=1,
        # save_to_filename=os.path.join(dir_figures, "BoxPlot.pdf")
    )

    utils.print_title("Estimate optimal threshold for entire sample")
    # Create masking scheme used for predicting blood pool masks
    thresholds_list = range(0, 500)
    threshold_masking_scheme = ThresholdMaskingScheme.ThresholdMaskingScheme(
        images_array=images_array,
        targets_array=targets_array,
        thresholds_list=thresholds_list)

    dice_scores_means = threshold_masking_scheme.evaluate_masking_scheme_by_threshold_sweeping()
    utils.show_plot_dice_scores_over_thresholds(
        x=thresholds_list,
        y=dice_scores_means,
        x_label="Intensity Threshold",
        y_label="Dice Score",
        fig_number=2,
        # save_to_filename=os.path.join(dir_figures, "DiceScores.pdf")
    )

    # Generate segmentation for "optimal" (based on Dice) threshold
    optimal_threshold = thresholds_list[np.argmax(dice_scores_means)]
    target_array_estimate = threshold_masking_scheme.get_target_array_estimate(
        optimal_threshold)

    # Visualize i-contours for both "ground-truth" and estimate
    targets_array[np.where(targets_array == 1)] = 0
    utils.show_image_data(images_array, targets_array, title="i-contours")

    utils.show_image_data(
        images_array, target_array_estimate*2, title="i-contours-estimate")

    dice_scores_per_slice = [utils.dice_score(targets_array[:, :, i].astype(
        bool), target_array_estimate[:, :, i].astype(bool)) for i in range(0, targets_array.shape[2])]

    utils.show_plot_dice_scores_over_samples(
        y=dice_scores_per_slice,
        threshold=optimal_threshold,
        y_label="Dice Score",
        fig_number=3,
        # save_to_filename=os.path.join(dir_figures, "DiceScoresOverSample.pdf")
    )

    utils.print_info("Dice scores for 'optimal' threshold choice: %.3f (%.3f)" %(np.mean(dice_scores_per_slice), np.std(dice_scores_per_slice)))
    i_slice = 20
    utils.show_image(images_array[:, :, i_slice], 
        target_data=target_array_estimate[:, :, i_slice], 
        title="Dice = %.3f" % (dice_scores_per_slice[i_slice]))
