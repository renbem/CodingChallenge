"""
\file Sample.py
\brief      Sample contains all images and associated targets belonging to a
            single subject
\author     Michael Ebner (michael.ebner.14@ucl.ac.uk)
\date       June 2017
"""

import os
import re
import pylab

import src.Target as Target
import src.Image as Image
import src.Exceptions as Exceptions


class Sample(object):
    """!
    Sample contains all images and associated targets belonging to a single
    subject
    """

    def __init__(self,
                 directory_dicoms,
                 directory_contours,
                 regular_expression_dicoms='([0-9]+)[.]dcm',
                 regular_expression_contours='IM[-][0-9]+[-]([0-9]+).*[.]txt'):
        """!
        \param      directory_dicoms           path to DICOM images of subject
        \param      directory_contours         path to contour images of
                                               subject
        \param      regular_expression_dicoms  define valid patterns for DICOM
                                               filenames
        \param      regular_expression_dicoms  define valid patterns for
                                               contour filenames
        """

        self._directory_dicoms = directory_dicoms
        self._directory_contours = directory_contours
        self._regular_expression_dicoms = regular_expression_dicoms
        self._regular_expression_contours = regular_expression_contours

        self._images = None
        self._targets = None

    def create_sample(self):
        """!
        Create a sample containing all images and targets belonging to same
        subject

        \post       list of images and targets is created
        """

        dictionary_dicoms = self._get_pattern_group_matches_in_directory(
            self._directory_dicoms, self._regular_expression_dicoms)

        dictionary_contours = self._get_pattern_group_matches_in_directory(
            self._directory_contours, self._regular_expression_contours)

        # list of triples (image_id, filename_dicom_image,
        # filename_contour_image)
        image_ids_and_dicom_contours_filenames = self._get_matching_files_and_ids(
            dictionary_dicoms, dictionary_contours)

        # Add image and target objects belonging to same subject sample
        N_images = len(image_ids_and_dicom_contours_filenames)
        self._images = [None] * N_images
        self._targets = [None] * N_images

        for i in range(0, len(image_ids_and_dicom_contours_filenames)):

            # Extract image id and absolute filenames for DICOM image and
            # contour file, respectively.
            image_id = image_ids_and_dicom_contours_filenames[i][0]
            filename_dicom = os.path.abspath(os.path.join(
                self._directory_dicoms, image_ids_and_dicom_contours_filenames[i][1]))
            filename_contours = os.path.abspath(os.path.join(
                self._directory_contours, image_ids_and_dicom_contours_filenames[i][2]))

            # Add image and target objects
            self._images[i] = Image.Image(image_id, filename_dicom)
            self._targets[i] = Target.Target(
                image_id, filename_contours, shape=self._images[i].get_data().shape)

    def get_images(self):
        """!
        Get images as list

        \return     list of Image objects
        """
        if self._images is None:
            raise Exceptions.ObjectNotCreated("create_sample")

        return self._images

    def get_targets(self):
        """!
        Get targets as list

        \return     list of Target objects
        """
        if self._targets is None:
            raise Exceptions.ObjectNotCreated("create_sample")

        return self._targets

    def show(self, mask=False, alpha=0.2):
        """!
        Show all image slices and masks (optional) of sample sequentially

        \param      mask   boolean value to show mask as well
        \param      alpha  scalar value in [0, 1] to define transparency of
                           mask
        """

        for i in range(0, len(self._images)):
            image_data = self._images[i].get_data()
            target_data = self._targets[i].get_data()

            pylab.imshow(image_data, cmap="Greys_r")
            if mask:
                pylab.imshow(target_data, cmap="bone", alpha=alpha)
            pylab.title("slice %d" % (self._images[i].get_id()))
            pylab.show(block=False)
            raw_input("Press the <ENTER> key to continue ...")

    def _get_pattern_group_matches_in_directory(self,
                                                directory,
                                                regular_expression):
        """!
        Gets the pattern group matches in directory.

        \param      directory           The directory
        \param      regular_expression  The regular expression

        \return     The pattern group matches in directory.
        """

        # Use dictionary to link slices (integer) with filenames (strings)
        p = re.compile(regular_expression)
        pattern_groups = {int(p.match(f).group(1)): p.match(
            f).group(0) for f in os.listdir(directory) if p.match(f)}

        return pattern_groups

    def _get_matching_files_and_ids(self,
                                    dictionary_dicoms,
                                    dictionary_contours):
        """!
        Gets the matching files and identifiers.

        \param      dictionary_dicoms    The dictionary dicoms
        \param      dictionary_contours  The dictionary contours

        \return     The matching files and identifiers.
        """
        image_ids_and_dicom_contours_filenames = \
            [(k, dictionary_dicoms[k], dictionary_contours[k])
             for k, v in dictionary_contours.iteritems() if k in dictionary_dicoms.keys()]

        image_ids_and_dicom_contours_filenames = sorted(
            image_ids_and_dicom_contours_filenames, key=lambda x: x[0])

        return image_ids_and_dicom_contours_filenames
