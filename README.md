# Coding Challenge

This code was developed as part of an application process. Therefore,
only limited information can be provided here.

## Installation

This code requires the following Python packages 
* `numpy
* `pandas
* `Pillow
* `pydicom
* `SimpleITK`

The versions used for testing the code can be installed with `pip` by running
* `pip install -r requirements.txt`

For the visualization of 3D data objects, [ITK-SNAP](http://www.itksnap.org/pmwiki/pmwiki.php) for the was used. In case you want to make use of this feature, make sure ITK-SNAP is installed and can be accessed via `itksnap` from the command line.

## Code Documentation
A documentation for the Python source-files can be generated in case [Doxygen](http://www.doxygen.org) is installed. Within the root folder run
* `cd doc/py`
* `doxygen doxyfile`
* `open html/index.html`

## Example usage
Two example scripts are provided in the folder `examples` which shall illustrate the use of the code.

## License
This code was developed for a particular purpose. However, in case you find it
useful, feel free to work with it. 
This framework is licensed under the [MIT license ![MIT](https://raw.githubusercontent.com/legacy-icons/license-icons/master/dist/32x32/mit.png)](http://opensource.org/licenses/MIT)