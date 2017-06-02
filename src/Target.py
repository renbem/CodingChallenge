"""
\file Target.py
\brief      Class to define a target (mask) for a training sample
\author     Michael Ebner (michael.ebner.14@ucl.ac.uk)
\date       June 2017
"""

import src.parsing as parsing
from src.Slice import Slice


class Target(Slice):
    """
    Class to define a target (mask) for a training sample
    """

    def __init__(self, slice_id, filename_absolute, shape):
        """!
        Class to define a target (mask) for a training sample
        """

        Slice.__init__(self, slice_id=slice_id,
                       filename_absolute=filename_absolute)
        self._shape = shape

    def get_data(self):
        """!
        Gets the target image data.

        \return     numpy boolean array of target (mask) data.
        """
        coordinates = parsing.parse_contour_file(self._filename_absolute)
        return parsing.poly_to_mask(coordinates, *self._shape)
