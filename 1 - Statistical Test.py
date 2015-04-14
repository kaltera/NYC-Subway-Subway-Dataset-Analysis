__author__ = 'ylucas'

import pandas
from scipy.stats import rankdata
from scipy.stats.mstats import count_tied_groups
import numpy as np
from numpy import ndarray
import numpy.ma as ma
from scipy.lib.six import iteritems
import scipy.special as special

# CSV File location
csv_file = "data.csv"
data = pandas.read_csv(csv_file)

# Create 2 dataframes for rainy and non-rainy days
x = data['ENTRIESn_hourly'][data['rain'] == 0]
y = data['ENTRIESn_hourly'][data['rain'] == 1]


# As there was an issue with the scipy.stats.mannwhitneyu(y,x) which gave a nan p-value, I had to copy/paste the
# calculating functions instead of using directly scipy.stats.mannwhitneyu(x,y)

use_continuity = True
x = ma.asarray(x).compressed().view(ndarray)
y = ma.asarray(y).compressed().view(ndarray)
ranks = rankdata(np.concatenate([x,y]))
(nx, ny) = (len(x), len(y))
nt = nx + ny
U = ranks[:nx].sum() - nx*(nx+1)/2.
U = max(U, nx*ny - U)
u = nx*ny - U
#
mu = (nx*ny)/2.
sigsq = (nt**3 - nt)/12.
ties = count_tied_groups(ranks)
sigsq -= np.sum(v*(k**3-k) for (k,v) in iteritems(ties))/12.
sigsq *= nx*ny/float(nt*(nt-1))

if use_continuity:
    z = (U - 1/2. - mu) / ma.sqrt(sigsq)
else:
    z = (U - mu) / ma.sqrt(sigsq)
prob = special.erfc(abs(z)/np.sqrt(2))

print "p-value : " + str(prob)
