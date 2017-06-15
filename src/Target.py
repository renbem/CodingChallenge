"""
\file Target.py
\brief      Class to define a target (mask) for a training sample.

Multiple classes/contours can be described by combining the information of
several single class targets. The data array specified by multiple contours is
given by the array obtained by adding all single contour masks.

\author     Michael Ebner (michael.ebner.14@ucl.ac.uk)
\date       June 2017
"""

import numpy as np
import pylab
import src.parsing as parsing
from src.Slice import Slice


class Target(object):
    """
    Class to define a target (mask) for a training sample. Multiple
    classes/contours can be described by combining the information of several
    single class targets.
    """

    def __init__(self, single_targets_list):
        """!
        Class to define a target (mask) for a training sample

        \param      single_targets_list  List of TargetSingleClass objects
        """
        self._single_targets_list = single_targets_list
        self._slice_id = single_targets_list[0].get_id()

    def get_data(self):
        """!
        Gets the target image data as integer numpy array to accommodate
        different classes.

        The data array specified by multiple contours is given by the array
        obtained by adding all single contour masks.

        \details    Read data array whenever required to keep memory usage low

        \return     numpy integer array of target (mask) data.
        """

        # Read data/mask specified by first contour
        data_array = self._single_targets_list[0].get_data().astype(np.uint8)

        # Add data/masks specified by subsequent contours
        for i in range(1, len(self._single_targets_list)):
            data_array += self._single_targets_list[
                i].get_data().astype(np.uint8)

        return data_array

    def show(self):
        """!
        Show 2D slice
        """
        pylab.imshow(self.get_data(), cmap="Greys_r")
        pylab.title("slice %d" % (self._slice_id))
        pylab.show(block=False)
