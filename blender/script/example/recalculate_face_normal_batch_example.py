import bpy
from pathlib import Path

context = bpy.context
scene = context.scene
viewlayer = context.view_layer

for i in range(1, 256, 1):
    if not Path(f'/Users/engineering/Desktop/mc/{i}.stl').expanduser().is_file():
        continue

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    bpy.ops.import_mesh.stl(
        filepath=f'/Users/engineering/Desktop/mc/{i}.stl',
        filter_glob='*.stl',
        files=[{'name': f'{i}.stl', 'name': f'{i}.stl'}],
        directory='/Users/engineering/Desktop/mc/'
    )

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.normals_make_consistent(inside=False)

    bpy.ops.object.mode_set(mode='OBJECT')
    obs = [o for o in scene.objects if o.type == 'MESH']
    bpy.ops.object.select_all(action='DESELECT')

    for ob in obs:
        viewlayer.objects.active = ob
        ob.select_set(True)
        stl_path = f'/Users/engineering/Desktop/mc/{i}_fixed.stl'
        bpy.ops.export_mesh.stl(
            filepath=str(stl_path),
            use_selection=True
        )
        ob.select_set(False)
