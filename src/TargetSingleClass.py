"""
\file TargetSingleClass.py
\brief      Class to define a target (mask) for a training sample. Only one
            single class can be described.
\author     Michael Ebner (michael.ebner.14@ucl.ac.uk)
\date       June 2017
"""

import src.parsing as parsing
from src.Slice import Slice


class TargetSingleClass(Slice):
    """
    Class to define a target (mask) for a training sample. Only one
    single class can be described.
    """

    def __init__(self, slice_id, filename, shape):
        """!
        Class to define a target (mask) for a training sample
        """

        Slice.__init__(self, slice_id=slice_id, filename=filename)
        self._shape = shape

    def get_data(self):
        """!
        Gets the target image data.

        \details    Read data array whenever required to keep memory usage low

        \return     numpy boolean array of target (mask) data.
        """
        
        coordinates = parsing.parse_contour_file(self._filename)
        return parsing.poly_to_mask(coordinates, *self._shape)
