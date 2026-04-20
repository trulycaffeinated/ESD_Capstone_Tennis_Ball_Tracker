# D. Kaputa
# Ravvenlabs

import bpy
import numpy as np
import socket
import struct
from mathutils import Euler
import math

conn = None
s = None
connected = False

# --- Compositor setup ---
bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree
links = tree.links

for n in tree.nodes:
    tree.nodes.remove(n)

rl = tree.nodes.new('CompositorNodeRLayers')
rl.location = 185, 285

v = tree.nodes.new('CompositorNodeViewer')
v.location = 750, 210
v.use_alpha = False

links.new(rl.outputs[0], v.inputs[0])


# --- Robust socket receive ---
def recv_exact(sock, n):
    buf = b''
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise RuntimeError(f"Socket closed while receiving {n} bytes")
        buf += chunk
    return buf


# --- Object transform (ball shifting behavior) ---
def xform_object_by_name(object_name, x, y, z, pitch, roll, yaw):
    if object_name in bpy.data.objects:
        obj = bpy.data.objects[object_name]
        obj.location = (x, y, z)

        pitch_rad = math.radians(pitch)
        roll_rad  = math.radians(roll)
        yaw_rad   = math.radians(yaw)

        obj.rotation_euler = Euler((pitch_rad, roll_rad, yaw_rad), 'XYZ')
    else:
        print(f"Object '{object_name}' not found.")


# --- Color conversion / rendering ---
def from_linear(linear):
    srgb = linear.copy()
    less = linear <= 0.0031308
    srgb[less] = linear[less] * 12.92
    srgb[~less] = 1.055 * np.power(linear[~less], 1.0 / 2.4) - 0.055
    return srgb * 255.0


def render_bytes_from_camera(cam_name):
    scene = bpy.context.scene
    cam = bpy.data.objects.get(cam_name)
    if cam is None:
        raise RuntimeError(f"Camera '{cam_name}' not found.")

    scene.camera = cam
    bpy.ops.render.render()

    pixels = bpy.data.images['Viewer Node'].pixels[:]
    arr = np.array(pixels, dtype=np.float32)
    rgba = np.uint8(from_linear(arr))

    return rgba.tobytes()


# --- Scene info helpers ---
def get_object_location_by_name(object_name):
    obj = bpy.data.objects.get(object_name)
    if obj is None:
        return (float('nan'), float('nan'), float('nan'))
    return (obj.location.x, obj.location.y, obj.location.z)


def get_camera_pose_matrix_by_name(camera_name):
    cam = bpy.data.objects.get(camera_name)
    if cam is None:
        nan3 = (float('nan'), float('nan'), float('nan'))
        nan9 = (float('nan'),) * 9
        return nan3, nan9

    loc = (cam.location.x, cam.location.y, cam.location.z)
    R = cam.matrix_world.to_3x3()

    rot9 = (
        R[0][0], R[0][1], R[0][2],
        R[1][0], R[1][1], R[1][2],
        R[2][0], R[2][1], R[2][2],
    )

    return loc, rot9


# --- Networking loop ---
def handle_data():
    interval = 0.1

    try:
        # Receive 8 floats = width, height, x, y, z, pitch, roll, yaw
        data = recv_exact(conn, 32)
        floats = struct.unpack('f' * 8, data)

        bpy.context.scene.render.resolution_x = int(floats[0])
        bpy.context.scene.render.resolution_y = int(floats[1])

        # Receive object name
        namebuf = recv_exact(conn, 1024)
        text = namebuf.split(b'\x00', 1)[0].decode("utf-8")

        # Move object (ball), NOT cameras
        xform_object_by_name(
            text,
            floats[2], floats[3], floats[4],
            floats[5], floats[6], floats[7]
        )

        # Render stereo images
        left_bytes = render_bytes_from_camera("Camera")
        right_bytes = render_bytes_from_camera("Camera.001")

        # Send image sizes
        header = struct.pack('II', len(left_bytes), len(right_bytes))
        conn.sendall(header)

        # Send image payloads
        conn.sendall(left_bytes)
        conn.sendall(right_bytes)

        # Send object location
        obj_loc = get_object_location_by_name(text)
        conn.sendall(struct.pack('fff', *obj_loc))

        # Send camera poses: location + 3x3 world rotation matrix
        camL_loc, camL_rot9 = get_camera_pose_matrix_by_name("Camera")
        camR_loc, camR_rot9 = get_camera_pose_matrix_by_name("Camera.001")

        conn.sendall(struct.pack('fff', *camL_loc))
        conn.sendall(struct.pack('fffffffff', *camL_rot9))

        conn.sendall(struct.pack('fff', *camR_loc))
        conn.sendall(struct.pack('fffffffff', *camR_rot9))

    except Exception as e:
        print(f"handle_data error: {e}")

    return interval


# --- UI Operators ---
class TEST_OT_startServer(bpy.types.Operator):
    bl_idname = "scene.start_server"
    bl_label = "Start Server"

    def execute(self, context):
        global s, conn, connected

        print("starting server")
        HOST = '127.0.0.1'
        PORT = 55001

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen()

        print("Waiting for MATLAB client connection...")
        conn, addr = s.accept()
        print(f"Connected by {addr}")

        conn.settimeout(20)
        connected = True

        bpy.app.timers.register(handle_data)
        return {'FINISHED'}


class TEST_OT_stopServer(bpy.types.Operator):
    bl_idname = "scene.stop_server"
    bl_label = "Stop Server"

    def execute(self, context):
        global conn, s, connected

        print("stopping server")

        if connected:
            try:
                conn.close()
            except:
                pass
            try:
                s.close()
            except:
                pass

        if bpy.app.timers.is_registered(handle_data):
            bpy.app.timers.unregister(handle_data)

        connected = False
        return {'FINISHED'}


# --- UI Panel ---
class MatlabPanel(bpy.types.Panel):
    bl_label = "Matlab Server"
    bl_idname = "PT_MatlabPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Matlab Server"

    def draw(self, context):
        layout = self.layout
        layout.operator("scene.start_server", text="Start Server")
        layout.operator("scene.stop_server", text="Stop Server")


def register():
    bpy.utils.register_class(TEST_OT_startServer)
    bpy.utils.register_class(TEST_OT_stopServer)
    bpy.utils.register_class(MatlabPanel)


def unregister():
    bpy.utils.unregister_class(MatlabPanel)
    bpy.utils.unregister_class(TEST_OT_stopServer)
    bpy.utils.unregister_class(TEST_OT_startServer)


if __name__ == "__main__":
    register()