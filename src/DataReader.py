"""
\file DataReader.py
\brief      Class to read data to create and return all samples specified by a
            CSV-file

\author     Michael Ebner (michael.ebner.14@ucl.ac.uk)
\date       June 2017
"""

import os
import pandas

import src.utilities as utils
import src.Sample as Sample
import src.Exceptions as Exceptions


class DataReader(object):
    """!
    Class to read data to create and return all samples specified by a CSV-file
    """

    def __init__(self,
                 directory_dicoms,
                 directory_contours,
                 csv_file,
                 contours_type,
                 header_dicoms='patient_id',
                 header_contourfiles='original_id'):
        """!
        Store paths and filenames required to create samples comprising images
        and targets
        """

        self._directory_dicoms = directory_dicoms
        self._directory_contours = directory_contours
        self._csv_file = csv_file
        self._contours_type = contours_type
        self._header_dicoms = header_dicoms
        self._header_contourfiles = header_contourfiles

        self._samples = None

    def read_data(self):
        """!
        Reads the specified data and creates all samples with each sample
        containing the individual DICOM images and targets (masks).
        \post created samples can be obtained via \p get_training_samples
        """

        # Check whether input files exist
        self._check_input_files()

        # Read CSV information
        data_frame = pandas.read_csv(self._csv_file)

        # Extract IDs from CSV-file pointing to DICOM filenames
        try:
            dicom_ids = data_frame[self._header_dicoms]
        except KeyError:
            raise NameError(
                "CSV-file does not contain the header '%s' to specify the DICOM files" % (
                    self._header_dicoms))

        # Extract IDs from CSV-file pointing to contour filenames
        try:
            contourfile_ids = data_frame[self._header_contourfiles]
        except KeyError:
            raise NameError(
                "CSV-file does not contain the header '%s' to specify the contour files" % (self._header_contourfiles))

        # Ensure same number of DICOM and contour files specified in CSV-file
        if len(dicom_ids) != len(contourfile_ids):
            raise ValueError(
                "Different number of DICOM and contour files specified in CSV-file.")

        # Create samples containing an image and target
        self._samples = []
        for i in range(0, len(dicom_ids)):

            # Get directory for samples
            directory_dicoms_images = os.path.join(
                self._directory_dicoms, dicom_ids[i])
            directory_countourfile_images = os.path.join(
                self._directory_contours,
                contourfile_ids[i], self._contours_type)

            # Create sample based on valid image slices
            sample = Sample.Sample(
                directory_dicoms_images, directory_countourfile_images)
            sample.create_sample()

            self._samples.append(sample)

    def get_training_samples(self):
        """!
        Gets the all created training samples.

        \return     list of training samples containing images and targets.
        """
        if self._samples is None:
            raise Exceptions.ObjectNotCreated("read_data")
        return self._samples

    def _check_input_files(self):
        """!
        Check whether given paths and filenames do exist and raise an error
        if not
        """

        if not utils.directory_exists(self._directory_dicoms):
            raise NameError("Directory %s does not exist" %
                            (self._directory_dicoms))

        if not utils.directory_exists(self._directory_contours):
            raise NameError("Directory %s does not exist" %
                            (self._directory_contours))

        if not utils.file_exists(self._csv_file):
            raise NameError("File %s does not exist" % (self._csv_file))
