"""
\file TestInput.py
\brief Unit tests to check given inputs

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
import src.Sample as Sample
import src.DataReader as DataReader
import src.Exceptions as Exceptions


class TestInput(unittest.TestCase):

    def test_image_exists(self):
        """
        Image does not exist and shall throw an error
        """
        self.assertRaises(Exceptions.FileNotExistent, lambda: Image.Image(1, "x.dcm"))

    def test_data_reader_input_does_not_exist_1(self):
        """
        Input data is not correct. DICOM directory is incorrect
        """
        directory_contours = os.path.join(
            dir_test_data_final_data, "contourfiles")
        directory_dicoms = os.path.join(
            dir_test_data_final_data, "XXX", "s")
        csv_file = os.path.join(dir_test_data_final_data, "link.csv")

        data_reader = DataReader.DataReader(
            directory_dicoms=directory_dicoms,
            directory_contours=directory_contours,
            csv_file=csv_file,
            contours_type="i-contours")

        self.assertRaises(Exceptions.FolderNotExistent, lambda: data_reader.read_data())

    def test_data_reader_input_does_not_exist_2(self):
        """
        Input data is not correct. Contour files directory is incorrect
        """
        directory_contours = os.path.join(
            dir_test_data_final_data, "XXX")
        directory_dicoms = os.path.join(
            dir_test_data_final_data, "dicoms")
        csv_file = os.path.join(dir_test_data_final_data, "link.csv")

        data_reader = DataReader.DataReader(
            directory_dicoms=directory_dicoms,
            directory_contours=directory_contours,
            csv_file=csv_file,
            contours_type="i-contours")

        self.assertRaises(Exceptions.FolderNotExistent, lambda: data_reader.read_data())

    def test_data_reader_input_does_not_exist_3(self):
        """
        Input data is not correct. CSV file does not exist
        """
        directory_contours = os.path.join(
            dir_test_data_final_data, "contourfiles")
        directory_dicoms = os.path.join(
            dir_test_data_final_data, "dicoms")
        csv_file = os.path.join(dir_test_data_final_data, "XX.csv")

        data_reader = DataReader.DataReader(
            directory_dicoms=directory_dicoms,
            directory_contours=directory_contours,
            csv_file=csv_file,
            contours_type="i-contours")

        self.assertRaises(Exceptions.FileNotExistent, lambda: data_reader.read_data())

    def test_data_reader_input_does_exist(self):
        """
        Input data is given. Thus, file reading shall work flawlessly
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
        data_reader.read_data()

    def test_flawed_csv_file(self):
        """
        patient_id does not equal original_id in csv file
        """
        directory_contours = os.path.join(
            dir_test_data_final_data, "contourfiles")
        directory_dicoms = os.path.join(
            dir_test_data_final_data, "dicoms")
        csv_file = os.path.join(dir_test_data, "flawed_1.csv")

        data_reader = DataReader.DataReader(
            directory_dicoms=directory_dicoms,
            directory_contours=directory_contours,
            csv_file=csv_file,
            contours_type="i-contours")

        self.assertRaises(Exceptions.CsvFileFlawed,
                          lambda: data_reader.read_data())


    def test_sample_input_1(self):
        """
        Provided data folder only contains one valid pair of image and target,
        i.e. associated to 48.dcm. Corrupted files similar to it are provided,
        like r48.dcm and 48..dcm.
        """
        directory_contours = os.path.join(
            dir_test_data, "flawed_data", "contourfiles")
        directory_dicoms = os.path.join(
            dir_test_data, "flawed_data", "dicoms")
        csv_file = os.path.join(dir_test_data, "flawed_data", "link1.csv")

        data_reader = DataReader.DataReader(
            directory_dicoms=directory_dicoms,
            directory_contours=directory_contours,
            csv_file=csv_file,
            contours_type="i-contours")

        data_reader.read_data()
        samples = data_reader.get_samples()
        images = samples[0].get_images()

        self.assertEqual(len(images), 1)

    def test_sample_input_2(self):
        """
        Provided data folder does not contain any valid combination of image
        and target.
        """
        directory_contours = os.path.join(
            dir_test_data, "flawed_data", "contourfiles")
        directory_dicoms = os.path.join(
            dir_test_data, "flawed_data", "dicoms")
        csv_file = os.path.join(dir_test_data, "flawed_data", "link2.csv")

        data_reader = DataReader.DataReader(
            directory_dicoms=directory_dicoms,
            directory_contours=directory_contours,
            csv_file=csv_file,
            contours_type="i-contours")

        self.assertRaises(Exceptions.SampleNotValid,
            lambda: data_reader.read_data())

    def test_sample_input_3(self):
        """
        Contours input must be a list
        """
        directory_contours = os.path.join(
            dir_test_data, "flawed_data", "contourfiles", "SC-HF-I-1", "i-contours")
        directory_dicoms = os.path.join(
            dir_test_data, "flawed_data", "dicoms")
        sample = Sample.Sample(directory_dicoms, directory_contours)

        self.assertRaises(Exceptions.ObjectIsNotList, lambda: sample.create_sample())

    def test_multiple_contours(self):
        """
        Verify that numbers of matching contours given i-contours and 
        o-contours are correct
        """
        directory_contours = os.path.join(
            dir_test_data, "flawed_data", "contourfiles")
        directory_dicoms = os.path.join(
            dir_test_data, "flawed_data", "dicoms")
        csv_file = os.path.join(dir_test_data, "flawed_data", "link3.csv")
        
        data_reader = DataReader.DataReader(
            directory_dicoms=directory_dicoms,
            directory_contours=directory_contours,
            csv_file=csv_file,
            contours_type="i-contours o-contours")

        data_reader.read_data()
        samples = data_reader.get_samples()
        images = samples[0].get_images()

        self.assertEqual(len(images), 1)