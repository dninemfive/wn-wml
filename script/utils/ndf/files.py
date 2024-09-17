from ndf_parse.model import List, ListRow
import os
import shutil
import utils.ndf
import utils.ndf.ensure as ensure
import utils.ndf.make as make

def add_image(ndf_file: List,
              src_file_path: str,
              mod_output_path: str,
              folder_relative_to_gamedata: str,
              image_name: str,
              texture_bank_name: str,
              component_state: str = "~/ComponentState/Normal") -> str:
    destination_folder = os.path.join(mod_output_path, "GameData", folder_relative_to_gamedata)
    os.makedirs(destination_folder)
    dst_image_filename = f'{image_name}{os.path.splitext(src_file_path)[1]}'
    shutil.copyfile(src_file_path, os.path.join(destination_folder, dst_image_filename))
    texture_obj = utils.ndf.objects.make_obj('TUIResourceTexture_Common',
                           FileName=f'"GameData:/{folder_relative_to_gamedata}/{dst_image_filename}"')
    ndf_file.add(ListRow(texture_obj, namespace=image_name))
    ndf_file.by_name(texture_bank_name).value\
            .by_member("Textures").value\
            .add(key=f'"{image_name}"',
                 value=make.map(ensure.maprow(component_state, f"~/{image_name}")))
    return f'"{image_name}"'