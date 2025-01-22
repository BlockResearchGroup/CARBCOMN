import compas
from compas_rhino import conversions
from compas_rhino import objects

# monkey = compas.json_load("/Users/vanmelet/monkey.json")

guid = objects.select_curve()
obj = objects.find_object(guid)
curve = conversions.curve_to_compas(obj)

session = {
    # "monkey": monkey,
    "curve": curve,
}

compas.json_dump(session, "/Users/vanmelet/knitcandela.json")
