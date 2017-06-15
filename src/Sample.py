"""
\file Sample.py
\brief      Sample contains all images and associated targets belonging to a
            data collection/acquisition/folder.

\details    A sample contains all the (2D) images which have a target (mask).

            To read the data and extract a sample, i.e. an object
            containing all 2D images with associated targets (masks) of
            a given data collection, the following data structure is assumed:

            The DICOM-folder contains
                - dFolder1: includes single DICOM files (*.dcm) of slices,
                            i.e. 2D images, with consecutive names for the
                            acquisitions, e.g. 1.dcm ... 200.dcm
                - ... dFolderN

            The contours-folder contains
                - cFolder1
                - ... cFolderN
            with each including 'i-contours' and 'o-contours' folder.
            The assumed filename convention for the contour-files (*.txt)
            in each of those folders is "IM-abc..z-0123-*.txt" with a,b,c,..,z
            denoting integers between 0 and 9.

            To link the respective DICOM-folders 'dFolder1' ... 'dFolderN'
            and contour-folders 'cFolder1' .... 'cFolderN' is provided
            by a CSV-file. There two column headers, assumed to be
            'patient_id' and 'original_id', establish the correct link
            between DICOM-folder ('patient_id') and contours-folder
            ('original_id').

            Example scripts can be found in the examples-folder which are
            based on the data in the test-folder.

\author     Michael Ebner (michael.ebner.14@ucl.ac.uk)
\date       June 2017
"""

import os
import re
import pylab

import src.TargetSingleClass as TargetSingleClass
import src.Target as Target
import src.Image as Image
import src.Exceptions as Exceptions
import src.utilities as utils


class Sample(object):
    """!
    Sample contains all images and associated targets belonging to a data
    collection/acquisition/folder.
    """

    def __init__(self,
                 directory_dicoms,
                 directory_contours_list,
                 regular_expression_dicoms='([0-9]+)[.]dcm',
                 regular_expression_contours='IM[-][0-9]+[-]([0-9]+)[-].*[.]txt'):
        """!
        Store paths and filenames required to create a sample
        
        \param      directory_dicoms           path to DICOM images of
                                               collection as string
        \param      directory_contours_list    list of strings specifying the
                                               paths to, possibly, multiple
                                               contour directories
        \param      regular_expression_dicoms  define regular expression
                                               pattern for valid DICOM
                                               filenames
        \param      regular_expression_dicoms  define regular expression
                                               pattern for valid contour
                                               filenames
        """

        self._directory_dicoms = directory_dicoms
        self._directory_contours_list = directory_contours_list
        self._regular_expression_dicoms = regular_expression_dicoms
        self._regular_expression_contours = regular_expression_contours

        self._images = None
        self._targets = None

    def create_sample(self):
        """!
        Create a sample containing all images and targets belonging to a data
        collection/acquisition/folder.

        \post       list of images and targets is created
        """

        # Check whether given input files and directories exist
        self._check_input_files()

        # Create dictionary linking DICOM images (slice id) with their
        # filenames
        dictionary_dicoms = self._get_pattern_group_matches_in_directory(
            self._directory_dicoms, self._regular_expression_dicoms)

        # Create list of dictionaries for all contour file inputs: Each
        # item links contour files (slice_id) with their filenames
        dictionary_contours_list = [self._get_pattern_group_matches_in_directory(
            c, self._regular_expression_contours) for c in self._directory_contours_list]

        # Get image ids/slice ids which are common for all contours and the
        # DICOM images
        image_ids = self._get_image_ids_of_matching_dicom_and_contour_files(
            dictionary_dicoms, dictionary_contours_list)
        N_images = len(image_ids)

        # Ensure that at least one valid image with mask is provided
        if N_images == 0:
            raise Exceptions.SampleNotValid()

        # Create a sample containing all image and target objects
        self._images = [None] * N_images
        self._targets = [None] * N_images

        for i in range(0, N_images):

            image_id = image_ids[i]

            # Create image using image id and absolute filename for DICOM
            self._images[i] = Image.Image(
                slice_id=image_id,
                filename=os.path.abspath(os.path.join(
                    self._directory_dicoms, dictionary_dicoms[image_id])))

            # Create list of targets using image id and absolute filename for contours
            targets_single_class_list = [
                TargetSingleClass.TargetSingleClass(
                    slice_id=image_id,
                    filename=os.path.abspath(os.path.join(
                        self._directory_contours_list[j],
                        dictionary_contours_list[j][image_id])),
                    shape=self._images[i].get_data().shape)
                for j in range(0, len(self._directory_contours_list))
            ]

            # Create a target holding all specified contours.
            self._targets[i] = Target.Target(targets_single_class_list)


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

    def show(self, mask=False, alpha=0.4):
        """!
        Show all image slices and masks (optional) of sample sequentially

        \param      mask   boolean value to show mask as well
        \param      alpha  scalar value in [0, 1] to define transparency of
                           mask
        """

        for i in range(0, len(self._images)):
            image_data = self._images[i].get_data()
            target_data = self._targets[i].get_data()

            if mask:
                utils.show_image(image_data, target_data=target_data,
                                 title=self._images[i].get_id(), alpha=alpha)
            else:
                utils.show_image(image_data, title=self._images[i].get_id())

            utils.pause()

    def _get_pattern_group_matches_in_directory(self,
                                                directory,
                                                regular_expression):
        """!
        Gets a dictionary linking image identifier with associated filename.

        \details    Create a dictionary to link image identifier/slice number
                    with image file, e.g. 
                    dictionary = {
                        1   :   "1.dcm",
                        ...
                        N   :   "N.dcm",
                    }

        \param      directory           path to directory with DICOM/contour
                                        files
        \param      regular_expression  String of regular expression defining
                                        the valid filenames

        \return     dictionary linking image id with filename.
        """

        # Use dictionary to link slices (integer) with filenames (strings)
        p = re.compile(regular_expression)
        pattern_groups = {int(p.match(f).group(1)): p.match(
            f).group(0) for f in os.listdir(directory) if p.match(f)}

        return pattern_groups

    def _get_image_ids_of_matching_dicom_and_contour_files(self, dictionary_dicoms,
                                                           dictionary_contours_list):

        # Get list of lists with all image ids for all dicom and contour files
        image_ids_list = [dictionary_dicoms.keys()]
        [ image_ids_list.append(dictionary_contours_list[i].keys()) for i in range(0, len(dictionary_contours_list)) ]

        # Get image ids which exist for all contours and DICOM files
        image_ids = reduce(set.intersection, map(set, image_ids_list))

        # Return sorted list of indices
        image_ids = sorted(image_ids)

        return image_ids

    def _check_input_files(self):
        """!
        Check whether given paths and filenames exist and raise an error
        if not
        """

        if not utils.directory_exists(self._directory_dicoms):
            raise Exceptions.FolderNotExistent(self._directory_dicoms)

        if type(self._directory_contours_list) is not list:
            raise Exceptions.ObjectIsNotList(self._directory_contours_list)

        for c in self._directory_contours_list:
            if not utils.directory_exists(c):
                raise Exceptions.FolderNotExistent(c)
