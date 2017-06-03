"""
\file TrainingSample.py
"""

import src.Target as Target
import src.Image as Image
import src.utilities as utils

class TrainingSample(object):
    """!
    Training sample contains exactly one pair of 2D image and target.
    """
    
    def __init__(self, image, target):
        """!
        Set Image and Target object

        \param      image   Image object of image
        \param      target  Target object of target associated to image
        """

        self._image = image
        self._target = target
        

    def get_image_data(self):
        """!
        Return image data array

        \return numpy array of image data
        """
        return self._image.get_data()

    def get_target_data(self):
        """!
        Return target data array

        \return boolean numpy array of target data
        """
        return self._target.get_data()

    def show(self, mask=False, alpha=0.4):
        """!
        Show image slices and masks (optional) of the sample

        \param      mask   boolean value to show mask as well
        \param      alpha  scalar value in [0, 1] to define transparency of
                           mask
        """

        image_data = self._image.get_data()
        target_data = self._target.get_data()

        if mask:
            utils.show_image(image_data, target_data=target_data,
                             title=self._image.get_id(), alpha=alpha)
        else:
            utils.show_image(image_data, title=self._image.get_id())
