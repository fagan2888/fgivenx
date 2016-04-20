#!/usr/bin/python
import numpy
from fgivenx.contours import Contours
from fgivenx.data_storage import FunctionalPosterior

# setup
# -----
xmin = -5                                    # minimum of x range
xmax = 5                                     # maximum of x range
nsamp = 500                                  # number of samples to use
chains_file = 'chains/test.txt'              # posterior files
paramnames_file = 'chains/test.paramnames'   # paramnames  file

def f(x, theta):
    """ Simple y = m x + c """
    m, c = theta

    return m * x + c

choices = [['m_' + str(i), 'c_' + str(i)] for i in range(1,11)]


# Computing contours
# ------------------
# load the posteriors from file
posterior = FunctionalPosterior(chains_file,paramnames_file).trim_samples(nsamp)

for i, chosen_parameters in enumerate(choices):
    # Generate some functional posteriors
    posterior.set_function(f, chosen_parameters)

    # Compute the contours and save
    contours = Contours(posterior,[xmin, xmax])
    contours.save('contours/posterior' + str(i) + '.pkl')
