""""""

import pathlib

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv

# matplotlib.use('Qt5Agg')


def read_density_from_vtu(mesh, density_field='density'):
    """Reads density data from a VTU file.

    Args:
        mesh (pyvista.UnstructuredGrid): Loaded VTU mesh.
        density_field (str): Name of the density field in the file.

    Returns:
        numpy.ndarray: Array of density values.
    """
    if density_field not in mesh.point_data and density_field not in mesh.cell_data:
        raise ValueError(f"'{density_field}' not found in point or cell data.")

    # Check both point_data and cell_data
    if density_field in mesh.point_data:
        return mesh.point_data[density_field]
    else:
        return mesh.cell_data[density_field]


if __name__ == "__main__":
    root = pathlib.Path("../../../../provided/ELLIS-ucns3d/RUN_EXAMPLES/2D/medium/")

    for fname in root.glob("OUT_*.vtu"):
        mesh = pv.read(fname)
        dens = read_density_from_vtu(mesh)
        np.save("medium.npy", data)
        print(dens)
        print(np.shape(dens))
