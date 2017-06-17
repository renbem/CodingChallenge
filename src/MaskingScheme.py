"""
\file MaskingScheme.py
\brief      Abstract class to define interface of a masking scheme used by
            the TrainingTesting class.

\author     Michael Ebner (michael.ebner.14@ucl.ac.uk)
\date       June 2017
"""

from abc import ABCMeta, abstractmethod


class MaskingScheme(object):
    __metaclass__ = ABCMeta

    def __init__(self, images_array=None, targets_array=None):
        """!
        Store information on given image and target data array where the target
        array includes labelling information.

        \param      images_array   Images data as numpy array
        \param      targets_array  Targets data as numpy array
        """
        self._images_array = images_array
        self._targets_array = targets_array

    def set_images_array(self, images_array):
        """!
        Sets the images array.

        \param      images_array  Images data as numpy array
        """
        self._images_array = images_array

    def set_targets_array(self, targets_array):
        """!
        Sets the targets array.

        \param      targets_array  Target data as numpy array
        """
        self._targets_array = targets_array

    @abstractmethod
    def estimate_optimal_parameter(self):
        pass

    @abstractmethod
    def get_mean_dice_score(self, parameter):
        pass
