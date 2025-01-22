from compas_model.models import Model
from compas_ifc.model import Model as IFCModel
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# Import the serialized compas model.
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


# Import the Concrete Receipe.
concrete_recipe = {
    "cement": {
        "type": "Portland",
        "amount_kg_per_m3": 350,
    },
    "aggregates": {
        "fine_aggregate_kg_per_m3": 600,
        "coarse_aggregate_kg_per_m3": 1200,
    },
    "water": {
        "amount_liters_per_m3": 200,
    },
    "additives": {
        "plasticizer_liters_per_m3": 1.5,
        "air_entrainer_liters_per_m3": 0.1,
    },
    "mixing_instructions": {
        "mix_order": [
            "Add cement and aggregates.",
            "Add water gradually while mixing.",
            "Add additives and mix until uniform.",
        ],
        "mix_duration_minutes": 5,
    },
}


# Insert elements into the IFC model
parent = ifc_model.building_storeys[0]
for element in model.elements():
    geometry = element.modelgeometry
    compas_cls = element.__class__.__name__
    ifc_cls = class_map[compas_cls]

    # Add the concrete recipe to all the BlockElement
    if compas_cls == "BlockElement":
        properties = {
            "Pset_ConcreteRecipe": concrete_recipe
        }
    else:
        properties = {}

    ifc_model.create(cls=ifc_cls, parent=parent, geometry=geometry, name=compas_cls, properties=properties)


# Visualize the IFC model
ifc_model.show()

# Save the IFC model to file
ifc_model.save(os.path.join(HERE, "barrel_vault_frame_with_psets.ifc"))
