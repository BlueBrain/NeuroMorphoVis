#!/computer/bbp-blender-development/nmv-blender-2.80/Blender-2.80.app/Contents/Resources/2.80/python/bin/python3.7m

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

x, y = np.random.randn(2, 1000).cumsum(axis=1)
ax = sns.lineplot(x=x, y=y, sort=False, lw=2, color="coral")

x, y = np.random.randn(2, 1000).cumsum(axis=1)
ax = sns.lineplot(x=x, y=y, sort=False, lw=1, color="red")


plt.savefig('/Users/abdellah/Desktop/nmv-release/neuron.pdf',
                    bbox_inches='tight')