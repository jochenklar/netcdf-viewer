NetCDF viewer
=============

Setup
-----

```bash
pip install git+https://github.com/jochenklar/netcdf-viewer  # from GitHub
pip install .                                                # from this repo
pip install -e .                                             # from this repo, editable
```

or using `pipx`:

```bash
pipx install git+https://github.com/jochenklar/netcdf-viewer  # from GitHub
pipx install .                                                # from this repo
```


Usage
-----

```bash
netcdf-viewer path/to/netcdf-file.nc
```

The interactive plot is available in the browser at http://localhost:8050.
