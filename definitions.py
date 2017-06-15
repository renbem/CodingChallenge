import os

dir_root = os.path.abspath(os.path.dirname(__file__))
dir_test_data = os.path.join(dir_root, 'test', 'test_data')
dir_test_data_final_data = os.path.join(dir_test_data, 'final_data')

info = {
    "name": "Coding Challenge",
    "repository": {
        "type": "git",
        "url": "https://github.com/renbem/CodingChallenge.git"
    },
    "authors": "Michael Ebner (michael.ebner.14@ucl.ac.uk)",
    "dependencies": {
        "python": "{0}/requirements.txt".format(dir_root)
    }
}
