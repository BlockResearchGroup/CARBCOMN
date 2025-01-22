from compas_ifc.model import Model
import os


HERE = os.path.dirname(os.path.abspath(__file__))

# Loading an IFC file and print summary
model = Model(os.path.join(HERE, "Duplex_A_20110907.ifc"))
model.print_summary()

# print the spatial hierarchy
model.print_spatial_hierarchy()

# Visualize the model
model.show()
