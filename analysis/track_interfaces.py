import pathlib

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv

matplotlib.use('Qt5Agg')


def get_bubble_interface_position(mesh, field_name='volume_fraction', volfrac_cutoff=1e-6, symmetry_line=None, symmetry_line_tol=1e-4):
    """Get the upstream/downstream/jet position of the bubble for a given cycle.

    Args:
        mesh (pyvista.UnstructuredGrid): Loaded VTU mesh.
        field_name (str): Name of the scalar field to check.
    """
    if field_name not in mesh.cell_data:
        raise ValueError(f"'{field_name}' not found in cell data.")

    rho_values = mesh.cell_data[field_name]

    centroids = []
    for i, rho in enumerate(rho_values):
        if rho > volfrac_cutoff:
            centroids.append(mesh.cell_centers().points[i])
    centroids = np.asarray(centroids)

    if symmetry_line is None:
        symmetry_line = (mesh.bounds[2] + mesh.bounds[3]) / 2.0
    x_coords = centroids[:, 0]  # Extract x positions
    axial_centroid = centroids[np.abs(centroids[:, 1] - symmetry_line) < symmetry_line_tol]

    upstream = x_coords.min()
    downstream = x_coords.max()
    jet = axial_centroid.min()

    return upstream, downstream, jet


def extract_interface_positions(root):
    """Extract interface positions, as defined by Fig 15 of Tsoutsanis 2021."""

    data = []
    for fname in root.glob("OUT_*.vtu"):
        mesh = pv.read(fname)
        time = mesh.field_data['TimeValue'][0]
        upstream, downstream, jet = get_bubble_interface_position(mesh)
        data.append([time, upstream, downstream, jet])

    array = np.asarray(data)
    sorted_array = array[array[:, 0].argsort()]
    return sorted_array


def plot_interface_vs_time(data, label=""):
    """"""
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)
    ax.grid()
    ax.plot(data[:, 1], data[:, 0], label="Upstream")
    ax.plot(data[:, 2], data[:, 0], label="Downstream")
    ax.plot(data[:, 3], data[:, 0], label="Jet")

    ax.legend()
    # plt.show()
    fig.savefig(f"interfaces_{label}")


def main(res):
    """"""
    # root = pathlib.Path(f"/Users/ellis/Documents/msc_cfd/08_dissertation/provided/RUN_EXAMPLES/2D/{res}")
    root = pathlib.Path(f"/home/ellis/Documents/cfd_msc/08_dissertation/provided/ELLIS-ucns3d/RUN_EXAMPLES/2D/{res}/")
    data = extract_interface_positions(root)
    np.save(f"{res}.npy", data)
    # data = np.load(f"{res}.npy")
    plot_interface_vs_time(data, label=res)


if __name__ == "__main__":
    main("finex2")
    # main("medium")
