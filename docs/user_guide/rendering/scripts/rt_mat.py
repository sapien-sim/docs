# By Jet <i@jetd.me>
#
import sapien
import numpy as np
import transforms3d.euler
from sapien.core import Pose
import PIL.Image as im


def main():
    ray_tracing = True

    if ray_tracing:
        sapien.render.set_camera_shader_dir("rt")
        sapien.render.set_viewer_shader_dir("rt")
        sapien.render.set_ray_tracing_samples_per_pixel(64)
        sapien.render.set_ray_tracing_denoiser("optix")

    scene = sapien.Scene()

    camera_mount = scene.create_actor_builder().build_kinematic()
    camera = scene.add_mounted_camera(
        name="camera",
        mount=camera_mount,
        pose=sapien.Pose(),  # relative to the mounted actor
        width=1280,
        height=720,
        fovy=np.deg2rad(45),
        near=0.1,
        far=100,
    )

    camera_mount.set_pose(
        Pose([-0.28, -0.28, 0.46], [0.8876263, -0.135299, 0.3266407, 0.2951603])
    )

    ground_material = sapien.render.RenderMaterial()
    ground_material.base_color = np.array([202, 164, 114, 256]) / 256
    ground_material.specular = 0.5
    scene.add_ground(0, render_material=ground_material)
    scene.set_timestep(1 / 240)

    scene.set_ambient_light([0.3, 0.3, 0.3])
    scene.add_directional_light(
        [0, 0.5, -1],
        color=[3.0, 3.0, 3.0],
        shadow=True,
        shadow_scale=2.0,
        shadow_map_size=4096,  # these are only needed for rasterization
    )

    builder = scene.create_actor_builder()
    material = sapien.render.RenderMaterial()
    material.base_color = [0.2, 0.2, 0.8, 1.0]
    material.roughness = 0.5
    material.metallic = 0.0
    builder.add_sphere_visual(radius=0.06, material=material)
    builder.add_sphere_collision(radius=0.06)
    sphere1 = builder.build()
    sphere1.set_pose(Pose(p=[-0.05, 0.05, 0.06]))

    builder = scene.create_actor_builder()
    material = sapien.render.RenderMaterial()
    material.ior = 1.2
    material.transmission = 1.0
    material.base_color = [1.0, 1.0, 1.0, 1.0]
    material.roughness = 0.15
    material.metallic = 0.0
    builder.add_sphere_visual(radius=0.07, material=material)
    builder.add_sphere_collision(radius=0.07)
    sphere2 = builder.build()
    sphere2.set_pose(Pose(p=[0.05, -0.05, 0.07]))

    builder = scene.create_actor_builder()
    material = sapien.render.RenderMaterial()
    material.base_color = [0.8, 0.7, 0.1, 1.0]
    material.roughness = 0.01
    material.metallic = 1.0
    builder.add_capsule_visual(radius=0.02, half_length=0.1, material=material)
    builder.add_capsule_collision(radius=0.02, half_length=0.1)
    cap = builder.build()
    cap.set_pose(
        Pose(p=[0.15, -0.01, 0.01], q=transforms3d.euler.euler2quat(0, 0, -0.7))
    )

    builder = scene.create_actor_builder()
    material = sapien.render.RenderMaterial()
    material.base_color = [0.8, 0.2, 0.2, 1.0]
    material.roughness = 0.005
    material.metallic = 1.0
    builder.add_box_visual(half_size=[0.09, 0.09, 0.09], material=material)
    builder.add_box_collision(half_size=[0.09, 0.09, 0.09])
    box = builder.build()
    box.set_pose(Pose(p=[0.05, 0.17, 0.09]))

    builder = scene.create_actor_builder()
    material = sapien.render.RenderMaterial()
    material.base_color = [0.9, 0.6, 0.5, 1.0]
    material.roughness = 0.0
    material.metallic = 1.0
    builder.add_visual_from_file(
        "../assets/objects/suzanne.dae", scale=[0.1, 0.1, 0.1], material=material
    )
    builder.add_box_collision(half_size=[0.1, 0.1, 0.1])
    box = builder.build()
    box.set_pose(Pose(p=[0.15, -0.25, 0.1], q=transforms3d.euler.euler2quat(0, 0, -1)))

    scene.step()
    scene.update_render()
    camera.take_picture()

    rgb = camera.get_picture("Color")
    rgb = im.fromarray((rgb * 255).astype(np.uint8))
    rgb.save(f'mat_{"rt" if ray_tracing else "rast"}.png')
    rgb.show()


main()
