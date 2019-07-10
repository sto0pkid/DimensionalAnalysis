# Simple package for computation with dimensional quantities
Best for running within Jupyter Notebook to be able to make use of mathematical typesetting.

Currently requires SymPy and Jupyter but in the future these should be optional dependencies or even something entirely separate.

There are other Python packages for dimensional analysis out there (pint, scipy, sympy.physics.units, etc...) this project is mainly just for the learning experience unless it turns out to be useful.

## TODO:
* fine-grained expression manipulation (probably w/ SymPy)
* quantity conversions (minutes to seconds, etc..), 1 minute + 30 seconds
* prefixes: kilo, milli, centi, ...
* check consistency / completeness of units for each dimension
    * consistency: do all units normalize to the same value in terms of the base?
    * completeness: are all units able to be normalized to the base via the conversion ratios given?
* make sure the arithmetic is arbitrary-precision (probably w/ mpmath, apparently NumPy doesn't actually do arbitrary-precision)
* tracking significant figures
