import pathlib

import compas
from compas.datastructures import Mesh
from compas_gmsh.models import MeshModel
from compas_viewer import Viewer
from compas_viewer.config import Config

# ==============================================================================
# Define the data files
# ==============================================================================

here = pathlib.Path(__file__).parent
sessionpath = here / "data" / "session.json"

# ==============================================================================
# Import the session
# ==============================================================================

session = compas.json_load(sessionpath)

# ==============================================================================
# Load the cablemesh from the work session
# ==============================================================================

cablemesh = session["cablemesh"]

# ==============================================================================
# Mesh Model
# ==============================================================================

# Create a model directly from the STEP file
filepath = str(here / "data" / "waffle.stp")
model = MeshModel.from_step(filepath)

# Set the maximum mesh size
model.options.mesh.meshsize_max = 100

# ==============================================================================
# Surface Mesh
# ==============================================================================

# Generate and optimize a mesh
model.generate_mesh(2)
# model.optimize_mesh(niter=10)

# Convert to a COMPAS mesh
meshmodel = model.mesh_to_compas()

# ==============================================================================
# volumetric Mesh
# ==============================================================================

# ==============================================================================
# Export
# ==============================================================================

# compas.json_dump(session, sessionpath)

# ==============================================================================
# Viz
# ==============================================================================

config = Config()
config.renderer.show_gridz = False
config.camera.target = [0, 0, 2000]
config.camera.position = [3000, -7000, 3000]
config.camera.near = 1e0
config.camera.far = 1e5
config.camera.pandelta = 100
config.renderer.gridsize = (20000, 20, 20000, 20)

viewer = Viewer(config=config)

viewer.scene.add(meshmodel)
# viewer.scene.add(tetmesh)

viewer.show()
