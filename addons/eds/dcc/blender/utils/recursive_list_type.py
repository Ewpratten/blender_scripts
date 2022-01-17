
from typing import Generator


def get_all_armature_bones(armature_obj) -> Generator[list,None,None]:
    for bone in armature_obj.data.bones:
        yield bone

        if bone.children:
            for child in bone.children:
                yield from get_all_armature_bones(child)