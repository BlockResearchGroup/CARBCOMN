from compas_ifc.model import Model
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# Loading an IFC file and print summary
model = Model(os.path.join(HERE, "Duplex_A_20110907.ifc"))

# Find individual elements
slabs = model.get_entities_by_type("IfcSlab")
slab = slabs[0]


# Print attributes and Psets of the element
# print(slab.attributes)
slab.print_attributes()


# print(slab.property_sets)
slab.print_properties()


# Visualize the element
slab.show()
