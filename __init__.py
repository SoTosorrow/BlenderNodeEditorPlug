# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import bpy
import os
import sys
import importlib
from itertools import groupby


bl_info = {
    "name" : "PearlNode",
    "author" : "Cuimi",
    "description" : "",
    "blender" : (3, 00, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "DevelopMent",
    "category" : "Test",
    "doc_url" : "",
    "tracker_url" : "https://github.com/SoTosorrow/BlenderNodeEditor",
}



'''
from . import node_system
from . import node_category
from . import node_socket
from . import node_operator

from . import node_node_input
from . import node_node_function
from . import node_node_output
from . import node_node_convert
from . import node_node_mesh

def register():
    node_system.register()
    node_socket.register()
    node_category.register()
    node_operator.register()

    node_node_input.register()
    node_node_function.register()
    node_node_output.register()
    node_node_convert.register()
    node_node_mesh.register()
    print("Pearl Node On")

def unregister():
    node_system.unregister()
    node_socket.unregister()
    node_category.unregister()
    node_operator.unregister()

    node_node_input.unregister()
    node_node_function.unregister()
    node_node_output.unregister()
    node_node_convert.unregister()
    node_node_mesh.unregister()
    print("Pearl Node Off")
'''





# get folder name
__folder_name__ = __name__
__dict__ = {}
addon_dir = os.path.dirname(__file__)

# get all .py file path
py_paths = [os.path.join(root, f) for root, dirs, files in os.walk(addon_dir) for f in files if
            f.endswith('.py') and f != '__init__.py']

for path in py_paths:
    name = os.path.basename(path)[:-3]
    correct_path = path.replace('\\', '/')
    # split path with folder name
    dir_list = [list(g) for k, g in groupby(correct_path.split('/'), lambda x: x == __folder_name__) if
                not k]
    # combine path and make dict like this: 'name:folder.name'
    if 'preset' not in dir_list[-1]:
        r_name_raw = __folder_name__ + '.' + '.'.join(dir_list[-1])
        __dict__[name] = r_name_raw[:-3]

# auto reload
for name in __dict__.values():
    if name in sys.modules:
        importlib.reload(sys.modules[name])
    else:
        globals()[name] = importlib.import_module(name)
        setattr(globals()[name], 'modules', __dict__)
        


def register():
    for name in __dict__.values():
        if name in sys.modules and hasattr(sys.modules[name], 'register'):
            try:
                sys.modules[name].register()
            except ValueError:  # open template file may cause this problem
                pass
    print("Pearl Node On")


def unregister():
    for name in __dict__.values():
        if name in sys.modules and hasattr(sys.modules[name], 'unregister'):
            sys.modules[name].unregister()
    print("Pearl Node Off")
