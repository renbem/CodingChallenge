"""
\file TrainingTesting.py
\brief      Class used to train and testa masking scheme

\author     Michael Ebner (michael.ebner.14@ucl.ac.uk)
\date       June 2017
"""

import src.utilities as utils
import src.Exceptions as Exceptions


class TrainingTesting(object):
    """!
    Class used to train masking scheme and also to report its performance
    """

    def __init__(self, masking_scheme, database, fraction_training=0.7):
        """!
        Store training scheme, database and other information required to
        perform training and to assess the performance of the learned parameter

        \param      masking_scheme     masking scheme of type MaskingScheme
        \param      database           database as DataBase object
        \param      fraction_training  fraction of training, remainder for
                                       testing
        """

        self._masking_scheme = masking_scheme
        self._database = database
        self._fraction_training = fraction_training

        self._training_images_array, self._training_targets_array = None, None
        self._testing_images_array, self._testing_targets_array = None, None

    def randomly_split_into_training_and_testing_data(self):
        """!
        Randomly split data in database into training and testing data in
        proportions specified by fraction_training.
        
        \post       run_training/run_testing can be executed
        """

        N_samples = self._database.get_number_of_all_training_samples()

        batch_size = int(N_samples * self._fraction_training)
        self._database.set_batch_size(batch_size)

        [training_data_arrays,
            test_data_arrays] = self._database.get_random_batch_and_batch_complement()

        self._training_images_array, self._training_targets_array = training_data_arrays
        self._testing_images_array, self._testing_targets_array = test_data_arrays

        # utils.print_info("Number of total samples: %d" %(N_samples))
        # utils.print_info("Number of training samples: %d" %(self._training_images_array.shape[2]))
        # utils.print_info("Number of testing samples: %d" %(self._testing_images_array.shape[2]))

    def run_training(self):
        """!
        Perform training to obtain estimated optimal parameter for masking
        scheme

        \return     tuple (estimated_parameter, mean_dice_score) after training
        """

        if self._training_images_array is None:
            raise Exceptions.ObjectNotCreated("randomly_split_into_training_and_testing_data")

        # Feed masking scheme with images and targets array
        self._masking_scheme.set_images_array(self._training_images_array)
        self._masking_scheme.set_targets_array(self._training_targets_array)

        # Estimate parameter of masking scheme on given data
        estimated_parameter = self._masking_scheme.estimate_optimal_parameter()

        # Evaluate performance with estimated parameter
        dice_scores_mean = self._masking_scheme.get_mean_dice_score(
            estimated_parameter)

        return (estimated_parameter, dice_scores_mean)

    def run_testing(self, parameter):
        """
        Run testing with given parameter

        \param      parameter  Parameter for masking scheme
        
        \return     tuple (parameter, mean_dice_score) after testing
        """

        if self._testing_images_array is None:
            raise Exceptions.ObjectNotCreated("randomly_split_into_training_and_testing_data")

        # Feed masking scheme with images and targets array
        self._masking_scheme.set_images_array(self._testing_images_array)
        self._masking_scheme.set_targets_array(self._testing_targets_array)

        # Evaluate performance with estimated parameter
        dice_scores_mean = self._masking_scheme.get_mean_dice_score(parameter)

        return (parameter, dice_scores_mean)
