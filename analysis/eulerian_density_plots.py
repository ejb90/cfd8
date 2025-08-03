""""""

import pathlib

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv

matplotlib.use('Qt5Agg')


def query_cell_data(mesh, point, quantity_name, tolerance=1e-6):
    """
    Query a quantity from a cell based on a point coordinate using PyVista.

    Parameters:
    -----------
    mesh (pyvista.DataSet):     The PyVista mesh/dataset containing the data
    point (list):               3D coordinates [x, y, z] of the query point
    quantity_name (str):        Name of the cell data array to query
    tolerance (float):          Tolerance for point location (default: 1e-6)

    Returns:
        float, None:
    """

    # Ensure point is a numpy array with shape (1, 3) for PyVista
    point = np.array(point).reshape(1, 3)

    # Check if the quantity exists in cell data
    if quantity_name not in mesh.cell_data:
        raise ValueError(f"Quantity '{quantity_name}' not found in cell data. "
                        f"Available quantities: {list(mesh.cell_data.keys())}")

    # Find the cell containing the point
    cell_id = mesh.find_containing_cell(point[0])

    # If point is not found in any cell, return None
    if cell_id == -1 or cell_id >= mesh.n_cells:
        return None

    # Return the quantity value from the cell
    return mesh.cell_data[quantity_name][cell_id]



if __name__ == "__main__":
    res = "medium"
    # root = pathlib.Path(f"/home/ellis/Documents/cfd_msc/08_dissertation/provided/ELLIS-ucns3d/RUN_EXAMPLES/2D/{res}/")
    # root = pathlib.Path(f"/home/ellis/Documents/cfd_msc/08_dissertation/tests/UCNS3D/try4/try4")
    root = pathlib.Path("/home/ellis/Documents/cfd_msc/08_dissertation/tests/UCNS3D/try5/try1")
    fname = root / "OUT_0.vtu"


    from datetime import datetime, timezone
    mtime = fname.stat().st_mtime

    # Convert to UTC datetime
    dt_utc = datetime.fromtimestamp(mtime, tz=timezone.utc)
    print(dt_utc)

    mesh = pv.read(fname)
    x = query_cell_data(mesh, (-0.05, 0.05, 0.0), "density")
    print(x)
    x = query_cell_data(mesh, (-0.2, 0.05, 0.0), "density")
    print(x)
    x = query_cell_data(mesh, (0.2, 0.05, 0.0), "density")
    print(x)