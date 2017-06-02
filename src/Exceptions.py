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

        \param      function_call  The object name
        """
        self.value = function_call

    def __str__(self):
        message = "Object has not been created yet. Run '%s' first." % (
            self.value)
        return message
