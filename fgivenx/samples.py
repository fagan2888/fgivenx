import numpy
import tqdm


def trim_samples(samples, weights, nsamp=0):
    """ Make samples equally weighted, and trim if desired.

    Parameters
    ----------
    samples: numpy.array
        See argument of fgivenx.compute_contours for more detail.

    weights: numpy.array
        See argument of fgivenx.compute_contours for more detail.

    nsamps: int
        Number of samples to trim to. If <=0 do nothing.
    """

    n = len(weights)
    weights /= weights.max()
    choices = numpy.random.rand(n) < weights

    new_samples = samples[choices]

    if nsamp > 0:
        new_samples = numpy.random.choice(new_samples)

    return new_samples


def compute_samples(f, x, samples):
    """ Apply f(x,theta) to x array and theta in samples.

    Parameters
    ----------
    See arguments of fgivenx.compute_contours

    Returns
    -------
    An array of samples at each x. shape=(len(x),len(samples),)
    """
    return numpy.array([
                        f(x, theta) for theta in tqdm.tqdm(samples)
                        ]).transpose()


def samples_from_getdist_chains(file_root, params):
    """ Extract samples and weights from getdist chains.

    Parameters
    ----------
    file_root: str
        Root name for getdist chains files. This script requires
        - file_root.txt
        - file_root.paramnames

    params: list(str)
        Names of parameters to be supplied to second argument of f(x|theta).

    Returns
    -------
    samples: numpy.array
        2D Array of samples. samples.shape=(# of samples, len(params),)

    weights: numpy.array
        Array of weights. samples.shape = (len(params),)
    """

    # Get the full data
    data = numpy.loadtxt(file_root + '.txt')
    weights = data[:, 0]

    # Get the paramnames
    paramnames = numpy.loadtxt(file_root + '.paramnames', dtype=str)
    if len(paramnames.shape) is 2:
        paramnames = paramnames[:, 0]

    # Get the relevant samples
    indices = [2+list(paramnames).index(p) for p in params]
    samples = data[:, indices]

    return samples, weights

