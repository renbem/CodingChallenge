"""
\file utilities.py
\brief      Collection of utility functions acting as facilitator for several
            tasks

\pre        Requires ITK-SNAP (\p www.itksnap.org) for some functions
\author     Michael Ebner (michael.ebner.14@ucl.ac.uk)
\date       June 2017
"""

import os
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


def show_image(data_array, mask_array=None, title=None):
    """
    Visualize a 2D/3D data array and its mask_array.

    \param      data_array  numpy array of image data
    \param      mask_array  numpy array of mask data
    \param      title       string of title to be shown in figure
    """

    dimension = len(data_array.shape)

    if dimension is 2:
        if mask_array is None:
            pylab.imshow(data_array, cmap="Greys_r")
            # pylab.imshow(mask_array, cmap="bone", alpha=0.4)
            pylab.show(block=False)
        else:
            show_sitk_image(data_array, mask_array=mask_array,
                            filename=str(title))

    else:
        show_sitk_image(data_array, mask_array=mask_array, filename=str(title))


def show_sitk_image(data_array,
                    mask_array=None,
                    filename=None,
                    dir_tmp="/tmp/",
                    suffix_mask="_mask"):
    """!
    Visualizes the 2D/3D data array and its mask via ITK-SNAP.
    \pre        ITK-SNAP (\p www.itksnap.org) needs to be installed and
                executable via 'itksnap'
    
    \param      data_array  numpy array of image data
    \param      mask_array  numpy array of mask data
    \param      filename    string of filename
    \param      dir_tmp     string of directory to write temporary files to
                            open ITK-SNAP
    """

    image_sitk = sitk.GetImageFromArray(data_array)
    sitk.WriteImage(image_sitk, dir_tmp + filename + ".nii.gz")

    if mask_array is not None:
        mask_sitk = sitk.GetImageFromArray(mask_array.astype(np.int8))
        sitk.WriteImage(mask_sitk, dir_tmp + filename +
                        suffix_mask + ".nii.gz")

    cmd = "itksnap "
    cmd += "-g " + dir_tmp + filename + ".nii.gz "

    if mask_array is not None:
        cmd += "-s " + dir_tmp + filename + suffix_mask + ".nii.gz"

    os.system(cmd)
