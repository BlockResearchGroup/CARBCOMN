from compas_ifc.model import Model as IFCModel
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# Import the IFC model from file
ifc_model = IFCModel(os.path.join(HERE, "barrel_vault_frame_with_psets.ifc"))

# Get the first BlockElement
block = ifc_model.get_entities_by_name("BlockElement")[0]

# Check the property sets
block.print_properties(max_depth=5)

# Validate the property sets using the json schema
block.validate_properties({
    "Pset_ConcreteRecipe": os.path.join(HERE, "recipe_schema.json")
})
