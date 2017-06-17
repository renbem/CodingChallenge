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
import matplotlib.pyplot as plt


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
    """!
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
    """!
    Print title in predefined format
    """
    print_line_separator(symbol=symbol)
    print(counts*symbol + " " + title + " " + counts*symbol)


def print_info(text, newline=True, prefix="--- "):
    """!
    Print debug info in predefined format
    """
    if newline:
        print(prefix + text)
    else:
        sys.stdout.write(prefix + text)


def print_line_separator(add_newline=True, symbol="*", length=99):
    """!
    Print line as separator
    """
    if add_newline:
        print("\n")
    print(symbol*length)


def show_image_data(image_data, target_data=None, title=None, dir_tmp="/tmp/"):
    """!
    Visualize image and target/mask data via ITK-SNAP
    """
    image_sitk = sitk.GetImageFromArray(image_data)
    target_sitk = sitk.GetImageFromArray(target_data.astype(np.uint8))

    title = str(title)

    sitk.WriteImage(image_sitk, dir_tmp + title + ".nii.gz")
    sitk.WriteImage(target_sitk, dir_tmp + title + "_mask.nii.gz")

    cmd = "itksnap "
    cmd += "-g " + dir_tmp + title + ".nii.gz "
    cmd += "-s " + dir_tmp + title + "_mask.nii.gz "

    os.system(cmd)


def get_image_and_target_data_array_from_sample(sample):

    images = sample.get_images()
    targets = sample.get_targets()
    N_slices = len(images)

    image_data_array = images[0].get_data()
    image_data_array_dtype = image_data_array.dtype
    target_data_array_dtype = targets[0].get_data().dtype
    shape = image_data_array.shape

    images_data_array = np.zeros(
        (shape[0], shape[1], N_slices), dtype=image_data_array_dtype)
    targets_data_array = np.zeros(
        (shape[0], shape[1], N_slices), dtype=target_data_array_dtype)

    for i in range(0, N_slices):
        images_data_array[:, :, i] = images[i].get_data()
        targets_data_array[:, :, i] = targets[i].get_data()

    return images_data_array, targets_data_array


def show_plot_dice_scores_over_thresholds(x, y, x_label="", y_label="", fig_number=None, save_to_filename=None):
    """!
    Plot curves
    """
    dice_max_index = np.argmax(y)

    fig = plt.figure(fig_number)
    fig.clf()
    ax = fig.add_subplot(111)

    plt.plot(x, y)
    # plt.plot(x[dice_max_index], y[dice_max_index], marker="o")
    plt.plot(np.ones(2)*x[dice_max_index], [0, 1], linestyle="--")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    ax.set_xlim([0, np.max(x)])
    ax.set_ylim([0, 1])
    plt.title("Maximum Mean Dice Score = %.3f @ Intensity Threshold = %d" %
              (y[dice_max_index], x[dice_max_index]))
    plt.show(block=False)

    if save_to_filename is not None:
        fig.savefig(save_to_filename)
        print_info("Figure is saved to %s" % (save_to_filename))


def show_plot_dice_scores_over_samples(y, threshold, y_label="", fig_number=None, save_to_filename=None):

    mean_value = np.mean(y)

    fig = plt.figure(fig_number)
    fig.clf()
    ax = fig.add_subplot(111)
    plt.plot(sorted(y), marker="o")
    x_limits = ax.get_xlim()
    plt.plot(x_limits, [mean_value, mean_value], linestyle="--")
    plt.xlabel("Image (sorted according to Dice score)")
    plt.ylabel(y_label)
    plt.title("Image Dice Scores for Intensity Threshold = %d" %(threshold))
    ax.set_xlim(x_limits)
    ax.set_ylim([0, 1])
    plt.show(block=False)

    if save_to_filename is not None:
        fig.savefig(save_to_filename)
        print_info("Figure is saved to %s" % (save_to_filename))


def show_box_plot(data, x_labels=None, y_label=None, fig_number=None, save_to_filename=None):
    """!
    Show box plot
    """
    fig = plt.figure(fig_number)
    fig.clf()
    ax = fig.add_subplot(111)

    plt.boxplot(data)
    plt.setp(ax, xticklabels=x_labels)
    plt.ylabel(y_label)

    plt.show(block=False)

    if save_to_filename is not None:
        fig.savefig(save_to_filename)
        print_info("Figure is saved to %s" % (save_to_filename))


def dice_score(image_0, image_1):
    """!
    Compute Dice score given two image data arrays

    \param      image_0  Image as numpy data array
    \param      image_1  Image as numpy data array

    \return     Dice score
    """
    if image_0.shape != image_1.shape:
        raise Exceptions.ShapeMismatch()

    numerator = 2 * np.sum(image_0 * image_1)
    denominator = np.sum(image_0 > 0) + np.sum(image_1 > 0)

    return numerator / float(denominator)
