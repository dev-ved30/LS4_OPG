# Installing ls4_sim

## Prerequisites

While you can install `ls4_sim` on your laptop, it can take a day or more to run a one-year simulation. Accordingly you may prefer to install it on a remote server.

Since `ls4_sim` has several dependencies, we strongly recommend installing in a [conda environment](http://conda.pydata.org/docs/using/envs.html).

`ls4_sim` requires python 3.6 or later.

Packages needed:

* numpy
* scipy
* pandas
* [sqlalchemy](http://www.sqlalchemy.org/)
* [astropy](http://www.astropy.org/)
* [astroplan](http://www.astropy.org/)
* [scikit-learn](http://scikit-learn.org/)
* [xgboost](https://xgboost.readthedocs.io/)
* [transitions](https://github.com/tyarkoni/transitions)
* [gurobi](http://www.gurobi.com/)
* optional, for profiling: [pyinstrument](https://github.com/joerick/pyinstrument)

Note that Gurobi is commercial software, but [academic licenses](http://www.gurobi.com/academia/for-universities) are available. 
Install Gurobi via conda:

    conda config --add channels http://conda.anaconda.org/gurobi
    conda install gurobi

And activate it with your license:

    grbgetkey YOUR-LICENSE-KEY

In the future we plan to provide appropriate recipes for installing these libraries in one go.

## Installing

`ls4_sim` is easiest to install directly from the source tree:

    pip install -e .
