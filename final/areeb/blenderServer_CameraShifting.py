# D. Kaputa
# Ravvenlabs

import bpy
import numpy as np
import socket
import struct
from mathutils import Euler, Vector
import math

counter = 1
conn = []
s = []
connected = False

# Initial stereo pose storage
initial_camL_loc = None
initial_camR_loc = None
initial_camL_rot = None
initial_camR_rot = None
initial_center = None

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


# --- Save initial camera setup ---
def save_initial_stereo_pose():
    global initial_camL_loc, initial_camR_loc
    global initial_camL_rot, initial_camR_rot
    global initial_center

    camL = bpy.data.objects.get("Camera")
    camR = bpy.data.objects.get("Camera.001")

    if camL is None or camR is None:
        print("Stereo cameras not found.")
        return False

    initial_camL_loc = camL.location.copy()
    initial_camR_loc = camR.location.copy()
    initial_camL_rot = camL.rotation_euler.copy()
    initial_camR_rot = camR.rotation_euler.copy()

    # Midpoint of the two cameras = orbit center
    initial_center = (initial_camL_loc + initial_camR_loc) / 2.0

    print("Initial stereo pose saved.")
    print(f"  Left location:  {initial_camL_loc}")
    print(f"  Right location: {initial_camR_loc}")
    print(f"  Left rotation:  {initial_camL_rot}")
    print(f"  Right rotation: {initial_camR_rot}")
    print(f"  Orbit center:   {initial_center}")

    return True


def reset_to_initial_stereo_pose():
    global initial_camL_loc, initial_camR_loc
    global initial_camL_rot, initial_camR_rot

    camL = bpy.data.objects.get("Camera")
    camR = bpy.data.objects.get("Camera.001")

    if camL is None or camR is None:
        print("Stereo cameras not found.")
        return False

    if initial_camL_loc is None or initial_camR_loc is None:
        ok = save_initial_stereo_pose()
        if not ok:
            return False

    camL.location = initial_camL_loc.copy()
    camR.location = initial_camR_loc.copy()
    camL.rotation_euler = initial_camL_rot.copy()
    camR.rotation_euler = initial_camR_rot.copy()

    print("Stereo rig reset to initial pose.")
    return True


# --- Stereo rig transform (MATLAB drives LEFT camera delta; Python reconstructs RIGHT camera) ---
def xform_stereo_rig(dx, dy, dz, pitch, roll, yaw):
    """
    MATLAB sends dx,dy,dz as the LEFT camera's offset from its initial position.
    This function:
      1) moves the left camera using that delta
      2) computes the right camera as the point mirrored across the saved center
      3) applies incoming rotation deltas relative to each camera's own initial rotation
    """
    global initial_camL_loc, initial_camR_loc
    global initial_camL_rot, initial_camR_rot
    global initial_center

    camL = bpy.data.objects.get("Camera")
    camR = bpy.data.objects.get("Camera.001")

    if camL is None or camR is None:
        print("Stereo cameras not found.")
        return

    if initial_camL_loc is None or initial_camR_loc is None:
        ok = save_initial_stereo_pose()
        if not ok:
            return

    delta_pos = Vector((dx, dy, dz))

    # LEFT camera follows MATLAB exactly
    camL.location = initial_camL_loc + delta_pos

    # RIGHT camera is mirrored through the orbit center
    # If center is C and left is L, then right = 2C - L
    camR.location = (2.0 * initial_center) - camL.location

    # Apply rotation deltas relative to each camera's own initial rotation
    pitchRad = math.radians(pitch)
    rollRad = math.radians(roll)
    yawRad = math.radians(yaw)

    camL.rotation_euler = Euler((
        initial_camL_rot.x + pitchRad,
        initial_camL_rot.y + rollRad,
        initial_camL_rot.z + yawRad
    ), 'XYZ')

    camR.rotation_euler = Euler((
        initial_camR_rot.x + pitchRad,
        initial_camR_rot.y + rollRad,
        initial_camR_rot.z + yawRad
    ), 'XYZ')


# --- Rendering ---
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


def get_object_location_by_name(object_name):
    obj = bpy.data.objects.get(object_name)
    if obj is None:
        return (float('nan'), float('nan'), float('nan'))
    return (obj.location.x, obj.location.y, obj.location.z)


# --- Networking loop ---
def handle_data():
    interval = 0.1

    data = conn.recv(32)
    if not data or len(data) < 32:
        return interval

    floats = struct.unpack('f' * 8, data)

    bpy.context.scene.render.resolution_x = int(floats[0])
    bpy.context.scene.render.resolution_y = int(floats[1])

    namebuf = conn.recv(1024)
    if not namebuf:
        return interval

    text = namebuf.split(b'\x00', 1)[0].decode("utf-8")

    xform_stereo_rig(
        floats[2], floats[3], floats[4],
        floats[5], floats[6], floats[7]
    )

    left_bytes = render_bytes_from_camera("Camera")
    right_bytes = render_bytes_from_camera("Camera.001")

    header = struct.pack('II', len(left_bytes), len(right_bytes))
    conn.sendall(header)
    conn.sendall(left_bytes)
    conn.sendall(right_bytes)

    loc = get_object_location_by_name(text)
    conn.sendall(struct.pack('fff', *loc))

    return interval


# --- UI Operators ---
class TEST_OT_saveInitialPose(bpy.types.Operator):
    bl_idname = "scene.save_initial_pose"
    bl_label = "Save Initial Pose"

    def execute(self, context):
        ok = save_initial_stereo_pose()
        if ok:
            self.report({'INFO'}, "Initial stereo pose saved.")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Could not save initial stereo pose.")
            return {'CANCELLED'}


class TEST_OT_resetInitialPose(bpy.types.Operator):
    bl_idname = "scene.reset_initial_pose"
    bl_label = "Reset Initial Pose"

    def execute(self, context):
        ok = reset_to_initial_stereo_pose()
        if ok:
            self.report({'INFO'}, "Stereo pose reset.")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Could not reset stereo pose.")
            return {'CANCELLED'}


class TEST_OT_startServer(bpy.types.Operator):
    bl_idname = "scene.start_server"
    bl_label = "Start Server"

    def execute(self, context):
        global s, conn, connected

        print("starting server")
        HOST = '127.0.0.1'
        PORT = 55001

        ok = save_initial_stereo_pose()
        if not ok:
            self.report({'ERROR'}, "Could not save initial stereo pose.")
            return {'CANCELLED'}

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
            conn.close()
            s.close()

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
        layout.operator("scene.save_initial_pose", text="Save Initial Pose")
        layout.operator("scene.reset_initial_pose", text="Reset Initial Pose")
        layout.operator("scene.start_server", text="Start Server")
        layout.operator("scene.stop_server", text="Stop Server")


def register():
    bpy.utils.register_class(TEST_OT_saveInitialPose)
    bpy.utils.register_class(TEST_OT_resetInitialPose)
    bpy.utils.register_class(TEST_OT_startServer)
    bpy.utils.register_class(TEST_OT_stopServer)
    bpy.utils.register_class(MatlabPanel)


def unregister():
    bpy.utils.unregister_class(MatlabPanel)
    bpy.utils.unregister_class(TEST_OT_stopServer)
    bpy.utils.unregister_class(TEST_OT_startServer)
    bpy.utils.unregister_class(TEST_OT_resetInitialPose)
    bpy.utils.unregister_class(TEST_OT_saveInitialPose)


if __name__ == "__main__":
    register()