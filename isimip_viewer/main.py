import argparse

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('var')
    parser.add_argument('--flip', action='store_true', default=False)
    parser.add_argument('--time', default=0)
    parser.add_argument('--vmin')
    parser.add_argument('--vmax')
    parser.add_argument('--cmap', default='viridis')

    args = parser.parse_args()
    path = Path(args.file).expanduser()

    with Dataset(path) as ds:
        x = ds.variables['lon'][:]
        y = ds.variables['lat'][:]
        z = ds[args.var][args.time, :, :]

        if args.flip:
            z = np.flip(z, 0)

        kwargs = {
            'extent': [x[0], x[-1], y[0], y[-1]],
            'aspect': 'auto',
            'cmap': args.cmap
        }
        if args.vmin:
            kwargs['vmin'] = args.vmin
        if args.vmax:
            kwargs['vmax'] = args.vmax

        plt.imshow(z, **kwargs)
        plt.title(args.var)
        plt.colorbar()
        plt.tight_layout()
        plt.gcf().set_size_inches(8, 8)
        plt.show()
