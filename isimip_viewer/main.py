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
    parser.add_argument('--vmin', default=240)
    parser.add_argument('--vmax', default=320)
    parser.add_argument('--cmap', default='coolwarm')

    args = parser.parse_args()
    path = Path(args.file).expanduser()

    with Dataset(path) as ds:
        x = ds.variables['lon'][:]
        y = ds.variables['lat'][:]
        z = ds[args.var][args.time, :, :]

        if args.flip:
            z = np.flip(z, 0)

        plt.imshow(z, extent=[x[0], x[-1], y[0], y[-1]], aspect='auto',
                   vmin=args.vmin, vmax=args.vmax, cmap=args.cmap)
        plt.title(args.var)
        plt.colorbar()
        plt.tight_layout()
        plt.gcf().set_size_inches(8, 8)
        plt.show()
