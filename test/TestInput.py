"""
\file TestInput.py
\brief Unit tests to check given inputs

\author     Michael Ebner (michael.ebner.14@ucl.ac.uk)
\date       June 2017
"""

import unittest
import sys
import os

from definitions import dir_test
from definitions import dir_test_final_data

import src.Image as Image
import src.Target as Target
import src.DataReader as DataReader


class TestInput(unittest.TestCase):

    def test_image_exists(self):
        """
        Image does not exist and shall throw an error
        """
        self.assertRaises(NameError, lambda: Image.Image(1, "x.dcm"))

    def test_data_reader_input_does_not_exist_1(self):
        """
        Input data is not correct. DICOM directory is incorrect
        """
        directory_contours = os.path.join(
            dir_test_final_data, "contourfiles")
        directory_dicoms = os.path.join(
            dir_test_final_data, "XXX", "s")
        csv_file = os.path.join(dir_test_final_data, "link.csv")

        data_reader = DataReader.DataReader(
            directory_dicoms=directory_dicoms,
            directory_contours=directory_contours,
            csv_file=csv_file,
            contours_type="i-contours")

        self.assertRaises(NameError, lambda: data_reader.read_data())

    def test_data_reader_input_does_not_exist_2(self):
        """
        Input data is not correct. Contour files directory is incorrect
        """
        directory_contours = os.path.join(
            dir_test_final_data, "XXX")
        directory_dicoms = os.path.join(
            dir_test_final_data, "dicoms")
        csv_file = os.path.join(dir_test_final_data, "link.csv")

        data_reader = DataReader.DataReader(
            directory_dicoms=directory_dicoms,
            directory_contours=directory_contours,
            csv_file=csv_file,
            contours_type="i-contours")

        self.assertRaises(NameError, lambda: data_reader.read_data())

    def test_data_reader_input_does_exist(self):
        """
        Input data is given. Thus, file reading shall work flawlessly
        """
        directory_contours = os.path.join(
            dir_test_final_data, "contourfiles")
        directory_dicoms = os.path.join(
            dir_test_final_data, "dicoms")
        csv_file = os.path.join(dir_test_final_data, "link.csv")

        data_reader = DataReader.DataReader(
            directory_dicoms=directory_dicoms,
            directory_contours=directory_contours,
            csv_file=csv_file,
            contours_type="i-contours")
        data_reader.read_data()
