"""
\file TestUserBehaviour.py
\brief Test potentially problematic behaviour of user

\author     Michael Ebner (michael.ebner.14@ucl.ac.uk)
\date       June 2017
"""

import unittest
import sys
import os

from definitions import dir_test_data
from definitions import dir_test_data_final_data

import src.Image as Image
import src.Target as Target
import src.DataReader as DataReader
import src.Exceptions as Exceptions


class TestUserBehaviour(unittest.TestCase):

    def test_data_reader_read_data_not_called(self):
        """
        Attempt to access samples without having read input
        """
        directory_contours = os.path.join(
            dir_test_data_final_data, "contourfiles")
        directory_dicoms = os.path.join(
            dir_test_data_final_data, "dicoms")
        csv_file = os.path.join(dir_test_data_final_data, "link.csv")

        data_reader = DataReader.DataReader(
            directory_dicoms=directory_dicoms,
            directory_contours=directory_contours,
            csv_file=csv_file,
            contours_type="i-contours")
        # data_reader.read_data()

        self.assertRaises(Exceptions.ObjectNotCreated,
                          lambda: data_reader.get_samples())
