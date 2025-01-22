from compas_model.models import Model
from compas_ifc.model import Model as IFCModel
import os

HERE = os.path.dirname(os.path.abspath(__file__))

model: Model = Model.from_json(os.path.join(HERE, "barrel_vault_frame.json"))

# Create an empty IFC model using template
ifc_model = IFCModel.template()


# Create a map between COMPAS model classes and IFC classes
class_map = {
    "BlockElement": "IfcBuildingElementProxy",
    "BeamTProfileElement": "IfcBeam",
    "ColumnSquareElement": "IfcColumn",
    "CableElement": "IfcReinforcingBar",
}

# Insert elements into the IFC model
parent = ifc_model.building_storeys[0]
for element in model.elements():
    geometry = element.modelgeometry
    compas_cls = element.__class__.__name__
    ifc_cls = class_map[compas_cls]
    ifc_model.create(cls=ifc_cls, parent=parent, geometry=geometry, name=compas_cls)


# Visualize the IFC model
ifc_model.show()

# Save the IFC model to file
ifc_model.save(os.path.join(HERE, "barrel_vault_frame.ifc"))
