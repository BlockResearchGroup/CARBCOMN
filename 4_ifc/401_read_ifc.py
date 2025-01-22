from compas_ifc.model import Model


# Loading an IFC file and print summary
model = Model("Duplex_A_20110907.ifc")
model.print_summary()

# print the spatial hierarchy
model.print_spatial_hierarchy()

# Visualize the model
model.show()
