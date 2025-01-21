import compas
import compas_dr
import compas_fd
import compas_ifc
import compas_model
import compas_notebook
import compas_occ
import compas_tna
import compas_viewer


def check_version(package, version):
    return f"{version} => {package.__version__}  {'OK' if package.__version__ == version else 'ERROR'}"


print(f"compas          : {check_version(compas, '2.8.1')}")
print(f"compas_dr       : {check_version(compas_dr, '0.3.1')}")
print(f"compas_fd       : {check_version(compas_fd, '0.5.4')}")
print(f"compas_ifc      : {check_version(compas_ifc, '1.4.1')}")
print(f"compas_model    : {check_version(compas_model, '0.4.5')}")
print(f"compas_notebook : {check_version(compas_notebook, '0.8.1')}")
print(f"compas_occ      : {check_version(compas_occ, '1.2.1')}")
print(f"compas_tna      : {check_version(compas_tna, '0.5.2')}")
print(f"compas_viewer   : {check_version(compas_viewer, '1.3.0')}")
