import pathlib

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv

matplotlib.use('Qt5Agg')


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


def get_bubble_interface_position(mesh, field_name='volume_fraction'):
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
        if rho > 0.0:
            centroids.append(mesh.cell_centers().points[i])
    centroids = np.asarray(centroids)

    ycentre = (mesh.bounds[2] + mesh.bounds[3]) / 2.0
    x_coords = centroids[:, 0]  # Extract x positions
    axial_centroid = centroids[np.abs(centroids[:, 1] - ycentre) < 0.01]

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


if __name__ == "__main__":
    root = pathlib.Path("../../../../provided/ELLIS-ucns3d/RUN_EXAMPLES/2D/medium/")
    data = extract_interface_positions(root)
    np.save("medium.npy", data)
    # data = np.load("medium.npy")

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)
    ax.grid()
    # ax.plot(data[:, 0], data[:, 1], label="Upstream")
    # ax.plot(data[:, 0], data[:, 2], label="Downstream")
    # ax.plot(data[:, 0], data[:, 3], label="Jet")
    ax.plot(data[:, 1], data[:, 0], label="Upstream")
    ax.plot(data[:, 2], data[:, 0], label="Downstream")
    ax.plot(data[:, 3], data[:, 0], label="Jet")

    ax.legend()
    plt.show()
    fig.savefig("interfaces")