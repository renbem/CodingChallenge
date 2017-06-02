"""
\file Exceptions.py
\brief
\author     Michael Ebner (michael.ebner.14@ucl.ac.uk)
\date       June 2017
"""


class ObjectNotCreated(Exception):
    """!
    Error handling in case of an attempted object access which is not being
    created yet
    """

    def __init__(self, function_call):
        """!
        Store name of function which shall be executed to create desired
        object.

        \param      function_call  function call missing to create the object
        """
        self.function_call = function_call

    def __str__(self):
        error = "Object has not been created yet. Run '%s' first." % (
            self.function_call)
        return error


class CsvFileFlawed(Exception):
    """!
    Error handling in case given CSV file is flawed in whatever way
    """

    def __init__(self, message):
        """!
        Store error message

        \param      message  message to be stated in case of error
        """
        self.message = message

    def __str__(self):
        error = "Given CSV file is flawed. %s" % (self.message)
        return error


class FolderNotExistent(Exception):
    """!
    Error handling in case specified folder does not exist
    """

    def __init__(self, missing_folder):
        """!
        Store information on the missing folder

        \param      missing_folder  string of missing folder
        """
        self.missing_folder = missing_folder

    def __str__(self):
        error = "Folder '%s' does not exist" % (self.missing_folder)
        return error


class FileNotExistent(Exception):
    """!
    Error handling in case specified file does not exist
    """

    def __init__(self, missing_file):
        """!
        Store information on the missing file

        \param      missing_file  string of missing file
        """
        self.missing_file = missing_file

    def __str__(self):
        error = "File '%s' does not exist" % (self.missing_file)
        return error

class SampleNotValid(Exception):
    """!
    Error handling in case a valid sample cannot be created
    """

    def __str__(self):
        error = "Sample cannot be created since no pair of image and target could be established"
        return error
