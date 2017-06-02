"""
\file DataReader.py
\brief      Class to read data to create and return all samples specified by a
            CSV-file

\details    To read the data and extract the samples, i.e. the object 
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
import pandas
import numpy as np

import src.utilities as utils
import src.Sample as Sample
import src.Exceptions as Exceptions


class DataReader(object):
    """!
    Class to read data to create and return all samples specified by a
    CSV-file
    """

    def __init__(self,
                 directory_dicoms,
                 directory_contours,
                 csv_file,
                 contours_type,
                 header_dicoms="patient_id",
                 header_contours="original_id"):
        """!
        Store paths and filenames required to create samples comprising
        images and targets

        \param      directory_dicoms    path to DICOM directory including a
                                        collection of 2D DICOM images
        \param      directory_contours  path to contours directory including a
                                        collection of contour text files
        \param      csv_file            path to CSV-filename
        \param      contours_type       string describing the subdirectory in
                                        the contours directory, i.e. either
                                        "i-contours" or "o-contours"
        \param      header_dicoms       string of column header referring to
                                        the DICOM folders in CSV-file
        \param      header_contours      string of column header referring to
                                        the contour folders in CSV-file
        """

        self._directory_dicoms = directory_dicoms
        self._directory_contours = directory_contours
        self._csv_file = csv_file
        self._contours_type = contours_type
        self._header_dicoms = header_dicoms
        self._header_contours = header_contours

        self._samples = None

    def read_data(self):
        """!
        Reads the specified data and creates all samples with each sample
        containing the individual DICOM images and targets (masks).

        \post       created samples can be obtained via \p get_training_samples
        """

        # Check whether given input files and directories exist
        self._check_input_files()

        # Read CSV information
        data_frame = pandas.read_csv(self._csv_file)

        # Extract IDs from CSV-file pointing to DICOM filenames
        try:
            dicom_ids = data_frame[self._header_dicoms].tolist()
        except KeyError:
            raise NameError(
                "CSV-file does not contain the header '%s' to specify the DICOM files" % (
                    self._header_dicoms))

        # Extract IDs from CSV-file pointing to contour filenames
        try:
            contourfile_ids = data_frame[self._header_contours].tolist()
        except KeyError:
            raise NameError(
                "CSV-file does not contain the header '%s' to specify the contour files" % (self._header_contours))

        # Ensure same number of DICOM and contour files specified in CSV-file
        if np.nan in dicom_ids or np.nan in contourfile_ids:
            raise Exceptions.CsvFileFlawed(
                "Different length of input columns.")

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

    def get_samples(self):
        """!
        Gets the all created samples.

        \return     list of samples which each sample holding all 2D images and
                    targets associated to the same acquisition/folder.
        """
        if self._samples is None:
            raise Exceptions.ObjectNotCreated("read_data")
        return self._samples

    def _check_input_files(self):
        """!
        Check whether given paths and filenames exist and raise an error
        if not
        """

        if not utils.directory_exists(self._directory_dicoms):
            raise Exceptions.FolderNotExistent(self._directory_dicoms)

        if not utils.directory_exists(self._directory_contours):
            raise Exceptions.FolderNotExistent(self._directory_contours)

        if not utils.file_exists(self._csv_file):
            raise Exceptions.FileNotExistent(self._csv_file)
