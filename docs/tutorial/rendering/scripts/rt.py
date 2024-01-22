"""Camera.

Concepts:
    - Ray tracing
"""

import sapien
import numpy as np
from PIL import Image, ImageColor
from sapien.utils.viewer import Viewer
from transforms3d.euler import mat2euler


def main():
    sapien.render.set_camera_shader_dir("rt")
    sapien.render.set_viewer_shader_dir("rt")
    sapien.render.set_ray_tracing_samples_per_pixel(4)  # change to 256 for less noise
    sapien.render.set_ray_tracing_denoiser("none") # change to "optix" or "oidn"

    scene = sapien.Scene()
    scene.set_timestep(1 / 100.0)

    loader = scene.create_urdf_loader()
    loader.fix_root_link = True
    urdf_path = "../assets/179/mobility.urdf"
    asset = loader.load(urdf_path)
    assert asset, "URDF not loaded."

    scene.set_ambient_light([0.5, 0.5, 0.5])
    scene.add_directional_light([0, 1, -1], [0.5, 0.5, 0.5], shadow=True)
    scene.add_point_light([1, 2, 2], [1, 1, 1], shadow=True)
    scene.add_point_light([1, -2, 2], [1, 1, 1], shadow=True)
    scene.add_point_light([-1, 0, 1], [1, 1, 1], shadow=True)

    # ---------------------------------------------------------------------------- #
    # Camera
    # ---------------------------------------------------------------------------- #
    near, far = 0.1, 100
    width, height = 640, 480
    camera_mount_actor = scene.create_actor_builder().build_kinematic()
    camera = scene.add_mounted_camera(
        name="camera",
        mount=camera_mount_actor,
        pose=sapien.Pose(),  # relative to the mounted actor
        width=width,
        height=height,
        fovy=np.deg2rad(35),
        near=near,
        far=far,
    )

    print("Intrinsic matrix\n", camera.get_intrinsic_matrix())

    # Compute the camera pose by specifying forward(x), left(y) and up(z)
    cam_pos = np.array([-2, -2, 3])
    forward = -cam_pos / np.linalg.norm(cam_pos)
    left = np.cross([0, 0, 1], forward)
    left = left / np.linalg.norm(left)
    up = np.cross(forward, left)
    mat44 = np.eye(4)
    mat44[:3, :3] = np.stack([forward, left, up], axis=1)
    mat44[:3, 3] = cam_pos
    camera_mount_actor.set_pose(sapien.Pose(mat44))

    scene.step()  # make everything set
    scene.update_render()
    camera.take_picture()

    # ---------------------------------------------------------------------------- #
    # RGBA
    # ---------------------------------------------------------------------------- #
    rgba = camera.get_picture("Color")  # [H, W, 4]
    # An alias is also provided
    # rgba = camera.get_color_rgba()  # [H, W, 4]
    rgba_img = (rgba * 255).clip(0, 255).astype("uint8")
    rgba_pil = Image.fromarray(rgba_img)
    rgba_pil.save("rt_color.png")


if __name__ == "__main__":
    main()
