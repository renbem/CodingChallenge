"""
\file Image.py
\brief      Class to define an image for a training sample
\author     Michael Ebner (michael.ebner.14@ucl.ac.uk)
\date       June 2017
"""

import src.parsing as parsing
from src.Slice import Slice


class Image(Slice):
    """!
    Class to define an image for a training sample
    \date       2017-06-02 19:24:19+0100
    """

    def __init__(self, slice_id, filename_absolute):
        """"!
        Store the slice_id and absolute filename provided in the parameters

        \param      slice_id           integer value referring to the image
                                       number
        \param      filename_absolute  absolute path to filename
        """
        Slice.__init__(self, slice_id=slice_id,
                       filename_absolute=filename_absolute)

    def get_data(self):
        """!
        Gets the slice image data.

        \return     numpy array of image data.
        """
        image = parsing.parse_dicom_file(self._filename_absolute)
        return image['pixel_data']
