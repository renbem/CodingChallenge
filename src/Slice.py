##
# \file Slice.py
# \brief      Abstract class to define a 2D image, i.e. a slice, to be used for
#             both images and targets
#
# \author     Michael Ebner (michael.ebner.14@ucl.ac.uk)
# \date       June 2017
#

from abc import ABCMeta, abstractmethod

import src.parsing as parsing
import src.utilities as utils
import src.Exceptions as Exceptions
import pylab


class Slice(object):
    """!
    Abstract class to define a 2D image, i.e. slice, to be used for both
    images and targets
    """
    __metaclass__ = ABCMeta

    def __init__(self, slice_id, filename):
        """!
        Store the slice_id and absolute filename provided in the parameters
        
        \param      slice_id  integer value referring to the image number
        \param      filename  absolute path to filename
        """
        self._slice_id = slice_id
        self._filename = filename

        if not utils.file_exists(self._filename):
            raise Exceptions.FileNotExistent(self._filename)

    @abstractmethod
    def get_data(self):
        """!
        Gets the slice image data.

        \return     numpy array of slice data.
        """
        pass

    def get_id(self):
        """!
        Gets the slice identifier referring to image number.

        \return     integer value of image number.
        """
        return self._slice_id

    def get_filename(self):
        """!
        \return     filename string
        """
        return self._filename

    def show(self):
        """!
        Show 2D slice
        """
        pylab.imshow(self.get_data(), cmap="Greys_r")
        pylab.title("slice %d" % (self._slice_id))
        pylab.show(block=False)
