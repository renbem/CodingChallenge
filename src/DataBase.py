"""
\file DataBase.py
\brief      Class providing access to training samples

\author     Michael Ebner (michael.ebner.14@ucl.ac.uk)
\date       June 2017
"""

import random
import numpy as np
import SimpleITK as sitk
import src.TrainingSample as TrainingSample


class DataBase(object):
    """!
    Interface to data used for training
    """

    def __init__(self, samples, batch_size=8, seed=None):
        """!
        Store all samples and default values for batch size and seed for
        training sample retrieval

        \param      samples     list of Sample objects
        \param      batch_size  integer value to define batch size
        \param      seed        integer value to reproduce randomness
        """

        self._samples = samples
        self._batch_size = batch_size

        self._training_samples = None
        self._N_samples = None

        self._cursor = 0  # used for cycling over dataset to load batches

        image_data = self._samples[0].get_images()[0].get_data()
        self._shape = image_data.shape
        self._image_data_type = image_data.dtype

        # Set seed for reproducible random results
        np.random.seed(seed)

    def build_training_database(self):
        """!
        Builds a training database from the given samples.
        """
        self._training_samples = [TrainingSample.TrainingSample(i, t) for s in range(0, len(
            self._samples)) for (i, t) in zip(self._samples[s].get_images(), self._samples[s].get_targets())]

        self._N_samples = len(self._training_samples)

    def get_number_of_all_training_samples(self):
        """!
        Gets the number of all stored training samples

        \return integer value of available training samples
        """
        if self._N_samples is None:
            raise Exceptions.ObjectNotCreated(
                "create_training_sample_database")
        return self._N_samples

    def get_all_training_samples(self):
        """!
        Gets all stored training samples.

        \return     list of all training samples as objects of TrainingSample.
        """
        if self._training_samples is None:
            raise Exceptions.ObjectNotCreated(
                "create_training_sample_database")
        return self._training_samples

    def get_next_batch(self):
        """
        ! Gets the next batch of size batch_size.
        
        \details    returns one 3D numpy array for images and one 3D numpy
                    array for targets of a the next single batch, i.e. stacking
                    of respective arrays together. For each numpy array holds
                    array.shape[2] = batch_size (or smaller if end of data is
                    about to be reached). In case all data has been 
                    None, None is returned.
        
        \post       cursor is increased by batch size
        
        \return     Pair images_numpy_array, targets_numpy_array of next batch
                    with.
        """
        i_0 = self._cursor
        i_max = np.min([self._N_samples, i_0 + self._batch_size])

        self._cursor += self._batch_size

        return self._get_numpy_arrays_of_batch(np.arange(i_0, i_max))


    def restart_cursor(self):
        """!
        Restart cursor in case all batches have been returned already.
        """
        self._cursor = 0

    def get_random_batch(self):
        """!
        Gets random batch of size batch_size

        \return     Pair images_numpy_array, targets_numpy_array of random
                    batch
        """
        indices_all = np.arange(0, self._N_samples)

        indices = np.random.choice(indices_all, self._batch_size)

        return self._get_numpy_arrays_of_batch(indices)

    def _get_numpy_arrays_of_batch(self, indices):
        """!
        Returns a pair of 3D numpy arrays from the training samples specified
        by the indices.

        \details    Return one for image arrays and one for target arrays with
                    numpy_array.shape[2] = len(indices).

        \param      indices  list of indices to indicate training samples to
                             pick from

        \return     Pair images_numpy_array, targets_numpy_array
        """

        N_indices = len(indices)
        if N_indices == 0:
            return None, None

        # Allocate memory
        images_array = np.zeros(
            (self._shape[0], self._shape[1], N_indices), dtype=self._image_data_type)
        targets_array = np.zeros(
            (self._shape[0], self._shape[1], N_indices), dtype=bool)

        # Fill numpy arrays
        for i in range(0, N_indices):
            images_array[:, :, i] = self._training_samples[
                indices[i]].get_image_data()
            targets_array[:, :, i] = self._training_samples[
                indices[i]].get_target_data()

        return images_array, targets_array
