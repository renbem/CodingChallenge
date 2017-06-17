# Coding Challenge

This code was developed as part of an application process. Therefore,
only limited information shall be provided here.

## Installation

This code requires the following Python packages 
* `numpy`
* `pandas`
* `Pillow`
* `pydicom`
* `SimpleITK`

The versions used for testing the code can be installed with `pip` by running
* `pip install -r requirements.txt`

[ITK-SNAP](http://www.itksnap.org/pmwiki/pmwiki.php) is used for the visualization of 3D data objects. In case you want to make use of this feature, please make sure ITK-SNAP is installed and can be accessed via `itksnap` from the command line.

## Code Documentation
A documentation for the Python source-files can be generated in case [Doxygen](http://www.doxygen.org) is installed. Within the root folder run
* `cd doc/py`
* `doxygen doxyfile`
* `open html/index.html`

## Example usage
Several example scripts are provided in the folder `examples` which shall illustrate the use of the code.  These include
* `python examples/showIContours.py`: Show image and overlaid i-contours slice by slice for each sample
* `python examples/showcaseTrainingPipeline.py`: Showcase how to use training pipeline and visualize the obtained training data in 3D
* `python examples/showIOContours.py`: Show image and overlaid i- and o-contours slice by slice for each sample
* `python examples/showcaseTrainingTesting.py`: Showcase how to use coding framework for training and testing a simple masking scheme based on thresholding.
* `python examples/analyseImages.py`: Script to analyse the image regions masked by i- and o-contours

within the root directory. To check the provided unit tests, execute
* `python test/runTests.py`


## License
This code was developed for a particular purpose. However, in case you find it
useful, feel free to work with it. 
This framework is licensed under the [MIT license ![MIT](https://raw.githubusercontent.com/legacy-icons/license-icons/master/dist/32x32/mit.png)](http://opensource.org/licenses/MIT)