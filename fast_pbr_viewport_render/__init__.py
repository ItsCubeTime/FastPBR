from __future__ import annotations
from typing import Any, Mapping, ValuesView
from typing import TYPE_CHECKING

from PIL import ImageChops

import bpy

import bpy
import subprocess
import sys

from bpy.types import MaterialSlot, PropertyGroup

bl_info = {
    "name": "Fast PBR Viewport Render",
    "blender": (3, 00, 0),
    "category": "Object",
}

def copyModifiers(copyAllModifiersAndThereSettingsFromObject: bpy.types.Object, copyTargetObjects: list(bpy.types.Object)):
    # copyAllModifiersAndThereSettingsFromObject = bpy.context.object
    # copyTargetObjects = [o for o in bpy.context.selected_objects
    #                     if o != copyAllModifiersAndThereSettingsFromObject and o.type == copyAllModifiersAndThereSettingsFromObject.type]

    for obj in copyTargetObjects:
        obj: bpy.types.Object
        # if hasattr(obj, 'name') and hasattr(copyAllModifiersAndThereSettingsFromObject, 'name') and hasattr(obj, 'material_slots') and hasattr(obj, 'modifiers'):
        if obj.type == 'MESH' and not obj == copyAllModifiersAndThereSettingsFromObject:
            # if obj.type == copyAllModifiersAndThereSettingsFromObject.type:
            # if obj.type == copyAllModifiersAndThereSettingsFromObject.type:

            for mSrc in copyAllModifiersAndThereSettingsFromObject.modifiers:
                mSrc: bpy.types.Modifier
                mDst: bpy.types.Modifier = obj.modifiers.get(mSrc.name, None)
                # if not mDst:
                #     mDst = obj.modifiers.new(mSrc.name, mSrc.type) # The if block is useful if you want to avoid duplicates, although 
                # this can also be a bad behaviour as if the user happen to have put an identical modifier somewhere in the middle of the stack
                # , the script will not add another one at the end of the stack - which in our case is often necessary.
                # print(f"@@@@@@@@@@@@@@@@@@@@@@@@@@@@ obj: {obj}")
                # print(f"@@@@@@@@@@@@@@@@@@@@@@@@@@@@ mSrc: {mSrc}")
                # print(f"@@@@@@@@@@@@@@@@@@@@@@@@@@@@ mSrc.name: {mSrc.name}")
                # print(f"@@@@@@@@@@@@@@@@@@@@@@@@@@@@ mSrc.type: {mSrc.type}")
                mDst = obj.modifiers.new(mSrc.name, mSrc.type)
                # print(f"@@@@@@@@@@@@@@@@@@@@@@@@@@@@ mDst: {mDst}")
                # collect names of writable properties
                properties = [p.identifier for p in mSrc.bl_rna.properties
                            if not p.is_readonly]

                # copy those properties
                for prop in properties:
                    # getattr(mSrc, prop)
                    setattr(mDst, prop, getattr(mSrc, prop))

# installPackage('PILLOW')
# installPackage('numpy')
__name__ # This is the name of the folder that the __init__.py is in. I think
addonName: str = bl_info["name"]
addonNameShort: str = "Fast PBR"

import importlib
def putTextInBox(text):
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = ['┌' + '─' * width + '┐']
    for s in lines:
        res.append('│' + (s + ' ' * width)[:width] + '│')
    res.append('└' + '─' * width + '┘')
    return '\n'.join(res)
def installPackage(package: str):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Running installPackage is a slow operation, therefore we want to make sure that we only run it when necessary, hence this function to speed up registration/activation time of the addon SIGNIFICANTLY (like by 5-10 seconds).
def attemptToImportModuleAndInstallItIfItIfTheCorespondingPackageDoesntExist(packageName, moduleName): 
    print("Attempting")
    try:
        importlib.import_module(moduleName)
        # from PIL import Image
    except Exception as error:
        print(putTextInBox(f"{addonName}Error: ---\n{error}\n---\nwhen attempting to import {moduleName}, we're assuming that you dont have {packageName} installed and will try to install it for you!"))
        installPackage(packageName)
        importlib.import_module(moduleName) # Doesnt actually work? 
ListOfModulesToAttemptToImportAndInstallItIfItIfTheCorespondingPackageDoesntExist = [['PILLOW', 'PIL'], ['numpy']]
attemptToImportModuleAndInstallItIfItIfTheCorespondingPackageDoesntExist('PILLOW', 'PIL')
import PIL
attemptToImportModuleAndInstallItIfItIfTheCorespondingPackageDoesntExist('numpy', 'numpy')
import numpy
# import pi
# attemptToImportModuleAndInstallItIfItIfTheCorespondingPackageDoesntExist('PILLOW', 'PIL')
# attemptToImportModuleAndInstallItIfItIfTheCorespondingPackageDoesntExist('numpy', 'numpy')
# from PIL import Images
# if TYPE_CHECKING: # Importing packages just for intellisense as our import function wont run through VS Codes intellisense engine.

# import numpy
# print(help(numpy))


# materialToReplaceTo = ""
# materialToReplaceFrom = ""

# bpy.ops.ed.undo_push()

# for object in bpy.context.scene.objects:
#     object: bpy.types.Object
#     for materialSlot in object.material_slots:
#         materialSlot: bpy.types.MaterialSlot
#         if materialSlot.material.name_full == materialToReplaceFrom:
#             materialSlot.material = bpy.data.materials.get(materialToReplaceTo)



# from "C:/Program Files/Blender Foundation/blender-3.0.0-alpha+master.2b64b4d90d67-windows.amd64-release/3.0/scripts/addons/fast_pbr_viewport_render/fileRenamer.py" import moveImages
import os
from .fileRenamer import *
import glob


pathToStoreImagesIn = "C:/FromFastPBR/"





classesToRegister = list()

settingsPropertyGroupParents = list()

renderPasses = list()

nameOfWorldUsedDuringPBRmapCreation = "FastPBRViewportRender"

disableRestore = True # Set to true for  debugging

# addonNameShort = "Fast PBR"
import pathlib
pathToAddonDirectory = str(pathlib.Path(__file__).parent.resolve())
nameOfAssetsFileWithoutPath = 'FastPBRAssets.blend'
pathToAssetsFile = pathToAddonDirectory + '/' + nameOfAssetsFileWithoutPath
# 

#############################
##### Utility functions #####
#############################
# @bookmark Utility functions
def appendAssetFromAssetsBlendFile(dataBlockToAppend: str, blendFileDataCategory: str):
    """
    dataBlockToAppend is the name of the object/material/whatever you want to append.
    blendFileDataCategory is the type of data you want to append, if you go into the outliner > display mode > Data API you will see all these categories. Example values: "Material", "Object", "Node Groups" (etc). For some reason, the "s" at the end of some categories displayed in that list is not supposed to be included, which is rather confusing :)
    """
    bpy.ops.wm.append(filename=dataBlockToAppend, directory=pathToAssetsFile + '\\' + blendFileDataCategory + '\\')
        
    print("filepath:", nameOfAssetsFileWithoutPath)
    print("directory:", pathToAssetsFile + '\\' + blendFileDataCategory)
    print("filename:", dataBlockToAppend)

def containsLowerCase(string):
    # string: str = ""
    for letter in string:
        if letter.islower():
            # print("aaa")
            return True
    return False

def PascalCaseTo_snake_case(string):
    # string = 


    string: str =  'A' + string.replace(" ", "_") + 'A'
    outputString: str = string.lower()

    firstRun = True
    for index in range(string.__len__()-1, -1, -1):
        letter = string[index]
        if not firstRun and index is not 1:
            nextLetter = string[index+1]
            previousLetter = string[index-1]
            if letter.isupper() and (nextLetter.islower() or previousLetter.islower()) and (index is not 0) and containsLowerCase(string[:index]):
                if not '_' in [letter, nextLetter, previousLetter] and not '.' in [letter, nextLetter, previousLetter]:
                    outputString = outputString[:index] + "_" + outputString[index:]
                    # print(index)
        else:
            firstRun = False
    
    

    outputString = outputString[1:-1]

    return outputString

# Takes something like: "FFFFFFast PBRViewportRenderRRRRRrRRR" and outputs: "FFFFFFast PBR Viewport Render RRRR Rr RRR"
# Doesnt generate double spaces if a space comes before a capital letter in the input string.
def insertSpaceAfterCapital(string):
    string: str = str(string)
    outputString = string
    for index in range(string.__len__()-1, -1, -1):
        letter = string[index]
            
        if letter.isupper():
            if index != 0 and index != string.__len__()-1:
                nextLetter = string[index+1]
                previousLetter = string[index-1]
                if previousLetter.islower() or nextLetter.islower() and containsLowerCase(string[:index]):
                    outputString = outputString[:index] + " " + outputString[index:]

    return outputString



############################
# End of Utility functions #
############################


####################
#### DECORATORS ####
####################
# @bookmark decorators

def registerClassGivebl_labelAndbl_idnameWithUnderscore(cls):
    cls.bl_idname = PascalCaseTo_snake_case(addonNameShort + "_" + cls.__name__)
    cls.bl_label = insertSpaceAfterCapital(cls.__name__)
    classesToRegister.append(cls)
    return cls

def registerClassGivebl_labelAndbl_idnameWithDot(cls):
    cls.bl_idname = PascalCaseTo_snake_case(addonNameShort + "." + cls.__name__)
    cls.bl_label = insertSpaceAfterCapital(cls.__name__)
    classesToRegister.append(cls)
    return cls

def settingsContainerDecorator(cls):
    # settingsPropertyGroupParents.append(cls)
    # # classesToRegister.append(cls.settings)
    # cls.settings = registerClassGivebl_labelAndbl_idnameWithUnderscore(cls.settings)
    # settingsPropertyGroupParents.append(cls)



    
    cls.settings.bl_label = insertSpaceAfterCapital(cls.__name__)
    cls.settings.bl_idname = PascalCaseTo_snake_case(addonNameShort + "_" + cls.__name__)
    cls.bl_label = insertSpaceAfterCapital(cls.__name__)
    cls.bl_idname = PascalCaseTo_snake_case(cls.__name__)
    classesToRegister.append(cls.settings)
    # classesToRegister.append(cls)
    settingsPropertyGroupParents.append(cls)
    return cls

def renderPassDecorator(cls):
    # class NewClass(cls):
    #     # print("helloFromRenderPassDecorator:", str(cls))  # For some reason, prints cant take place before the addon has been registered
    #     # If one uncomments the print, it wont ever show up in Blenders terminal
    #     renderPasses.append(cls)
    #     print(f"Awesomesauce: cls.__name__")
    #     classesToRegister.append(cls.settings)
        
    # return NewClass
        # print("helloFromRenderPassDecorator:", str(cls))  # For some reason, prints cant take place before the addon has been registered
        # If one uncomments the print, it wont ever show up in Blenders terminal


    cls.settings.bl_label = insertSpaceAfterCapital(cls.__name__)
    cls.settings.bl_idname = PascalCaseTo_snake_case(addonNameShort + "_" + cls.__name__)
    cls.bl_label = insertSpaceAfterCapital(cls.__name__)
    cls.bl_idname = PascalCaseTo_snake_case(cls.__name__)
    classesToRegister.append(cls.settings)
    classesToRegister.append(cls)
    settingsPropertyGroupParents.append(cls)
    renderPasses.append(cls)

    # cls = registerClassGivebl_labelAndbl_idnameWithUnderscore(cls)
    # cls = settingsContainerDecorator(cls)
    # renderPasses.append(cls)
    print(f"Awesomesauce: cls.__name__")
    return cls

def registerClassToBPYDecorator(cls):
    # class NewClass(cls):
    #     classesToRegister.append(cls)
    # return NewClass
    classesToRegister.append(cls)
    return cls
        
def registerOperatorsDecorator(cls):
    # class NewClass(cls):
    #     classesToRegister.append(cls)
    #     cls.bl_idname = PascalCaseTo_snake_case(addonNameShort + "." + cls.__name__)
    #     cls.bl_label = insertSpaceAfterCapital(cls.__name__)
    #     # cls.bl_label = "Fast PBR viewport render"         # Display name in the interface.
    #     # cls.bl_options = {'DEFAULT_CLOSED'}  # Enable undo for the operator.
    #     # cls.bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    # return NewClass


        # cls.bl_label = "Fast PBR viewport render"         # Display name in the interface.
        # cls.bl_options = {'DEFAULT_CLOSED'}  # Enable undo for the operator.
        # cls.bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    return registerClassGivebl_labelAndbl_idnameWithDot(cls)


#####################
# END OF DECORATORS #
#####################

#####################
# This example adds an object mode tool to the toolbar.
# This is just the circle-select and lasso tools tool.
# import bpy

# # from bpy.utils.toolsystem import ToolDef
# from bpy.types import WorkSpaceTool

# class MyTool(WorkSpaceTool):
#     bl_space_type='VIEW_3D'
#     bl_context_mode='OBJECT'

#     # The prefix of the idname should be your add-on name.
#     bl_idname = "my_template.my_circle_select"
#     bl_label = "My Circle Select"
#     bl_description = (
#         "This is a tooltip\n"
#         "with multiple lines"
#     )
#     bl_icon = "ops.generic.select_circle"
#     bl_widget = None
#     bl_keymap = (
#         ("view3d.select_circle", {"type": 'LEFTMOUSE', "value": 'PRESS'},
#          {"properties": [("wait_for_input", False)]}),
#         ("view3d.select_circle", {"type": 'LEFTMOUSE', "value": 'PRESS', "ctrl": True},
#          {"properties": [("mode", 'SUB'), ("wait_for_input", False)]}),
#     )

#     def draw_settings(context, layout, tool):
#         props = tool.operator_properties("view3d.select_circle")
#         layout.prop(props, "mode")
#         layout.prop(props, "radius")


# class MyOtherTool(WorkSpaceTool):
#     bl_space_type='VIEW_3D'
#     bl_context_mode='OBJECT'

#     bl_idname = "my_template.my_other_select"
#     bl_label = "My Lasso Tool Select"
#     bl_description = (
#         "This is a tooltip\n"
#         "with multiple lines"
#     )
#     bl_icon = "ops.generic.select_lasso"
#     bl_widget = None
#     bl_keymap = (
#         ("view3d.select_lasso", {"type": 'LEFTMOUSE', "value": 'PRESS'}, None),
#         ("view3d.select_lasso", {"type": 'LEFTMOUSE', "value": 'PRESS', "ctrl": True},
#          {"properties": [("mode", 'SUB')]}),
#     )

#     def draw_settings(context, layout, tool):
#         props = tool.operator_properties("view3d.select_lasso")
#         layout.prop(props, "mode")


# def register():


# def unregister():


# if __name__ == "__main__":
#     register()
###################

    # os.remove(file)
#import os
#import time

################
# UI OPERATORS #
################

# class SimpleOperator(bpy.types.Operator):
#     """Tooltip"""
#     bl_idname = "object.test"
#     bl_label = "Confirm"
#     confirm = bpy.props.EnumProperty(
#         name="Confirm",
#         items= [
#             ('yes',"Yes",''),
#             ('no',"No",''),
#         ],
#     )

#     def execute(self, context):
#         print(self.confirm)

#         return {'FINISHED'}
    
#     def invoke(self, context, event):
#         return context.window_manager.invoke_props_dialog(self)
#     def draw(self,context):
#         self.layout.prop(self, "confirm", expand=True)
        
# bpy.utils.register_class(SimpleOperator)



# bl_info = {
#     "name": "Multiple panel example",
#     "author": "Robert Guetzkow",
#     "version": (1, 0),
#     "blender": (2, 80, 0),
#     "location": "View3D > Sidebar > Example tab",
#     "description": "Example with multiple panels",
#     "warning": "",
#     "wiki_url": "",
#     "category": "3D View"}



# classesToRegister.append(classesToRegister.append(EXAMPLE_PT_panel_1))

#######################################################################################
# @bookmark retrieve settings

def retrieveSettings(cls):
    if TYPE_CHECKING: # TYPE_CHEKCING is only true when running through a language server.
        # Always False when the code is running in a real software.
        print("TYPE_CHEKCING IS RETURNING TRUE! IF YOURE ATTEMPTING TO RUN THE SOFTWARE, IT LIKELY WONT RUN AS LONG AS THIS IS THE CASE. Im using TYPE_CHEKCING to get some intellisense fixes, but it will as a result break the addon at runtime if TYPE_CHEKCING is true when its not supposed to.")
        return cls.settings
    else: # bpy.context.scene.fast_pbr_render_normal_pass_with_workbench
        # print("bpy.context.scene." + PascalCaseTo_snake_case(addonNameShort + "_" + cls.__name__))
        # returnValue: Any
        # exec(("returnValue = bpy.context.scene." + PascalCaseTo_snake_case(addonNameShort + "_" + cls.__name__)))
        lcls = locals()
        # exec( "returnValue = bpy.context.scene." + PascalCaseTo_snake_case(addonNameShort + "_" + cls.__name__), globals(), lcls )
        exec( f"""returnValue = bpy.context.scene.{PascalCaseTo_snake_case(addonNameShort + '_' + cls.bl_idname)}""", globals(), lcls )
        returnValue = lcls["returnValue"]
        # print(f"returnValue: {returnValue}")
        # print(f"""returnValue code as string: returnValue = bpy.context.scene.{PascalCaseTo_snake_case(addonNameShort + '_' + cls.bl_idname)}""")
        return returnValue

# Supposedly unused, but might be needed at some point in the future
def retrieveSettingsUsing__name__insteadOfbl_idname(cls):
    if TYPE_CHECKING: # TYPE_CHEKCING is only true when running through a language server.
        # Always False when the code is running in a real software.
        return cls.settings
    else: # bpy.context.scene.fast_pbr_render_normal_pass_with_workbench
        # print("bpy.context.scene." + PascalCaseTo_snake_case(addonNameShort + "_" + cls.__name__))
        # returnValue: Any
        # exec(("returnValue = bpy.context.scene." + PascalCaseTo_snake_case(addonNameShort + "_" + cls.__name__)))
        lcls = locals()
        # exec( "returnValue = bpy.context.scene." + PascalCaseTo_snake_case(addonNameShort + "_" + cls.__name__), globals(), lcls )
        exec( f"""returnValue = bpy.context.scene.{PascalCaseTo_snake_case(addonNameShort + '_' + cls.__name__)}""", globals(), lcls )
        returnValue = lcls["returnValue"]
        print(f"returnValue: {returnValue}")
        return returnValue

#######################################################################################
                        

 ########################################
 ###### PANEL AND UI REGISTRATION #######
 ########################################
# @bookmark panel and ui reg

class GRABDOC_OT_map_preview_warning(bpy.types.Operator):
    """Preview the selected material"""
    bl_idname = "grab_doc.preview_warning"
    bl_label = "    MATERIAL PREVIEW WARNING"
    bl_options = {'INTERNAL'}

    preview_type: bpy.types.EnumProperty(
        items=(
            ('normals', "", ""),
            ('curvature', "", ""),
            ('occlusion', "", ""),
            ('height', "", ""),
            ('alpha', "", ""),
            ('albedo',"",""),
            ('ID', "", "")
        ),
        options={'HIDDEN'}
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 550)

    def draw(self, context):
        layout = self.layout
        
        col = layout.column()
        col.separator()

        col.label(text = "Live Material Preview is a feature that allows you to view what your bake maps will look like")
        col.label(text = "in real-time. Consider this warning: This feature is strictly meant for viewing your materials &")
        col.label(text = "not for editing while inside a preview. Once finished previewing, please exit to avoid instability.")
        col.label(text = "")
        col.label(text = "Pressing 'OK' will dismiss this warning permanently for this project file.")

    def execute(self, context):
        context.scene.grabDoc.firstBakePreview = False

        bpy.ops.grab_doc.preview_map(preview_type = self.preview_type)
        return{'FINISHED'}

# @registerOperatorsDecorator
# class FastPBRViewportRender(bpy.types.Panel):
#     # self.__classess__.

#     bl_label = "Fast PBR Viewport Render"
#     bl_idname = "Fast_PBR_Viewport_Render"
#     bl_category = "Fast"
#     bl_space_type = "VIEW_3D"
#     bl_region_type = "UI"
#     bl_options = set()

#     def draw(self, context):
#         layout = self.layout
        # layout.operator("fast_pbr.fast_pbr_viewport_render")
#         layout.label(text="This is panel 1.")
        
        # layout.row().prop(bpy.context.scene.fast_pbr_render_normal_pass_with_workbench, "file_path")
        # row = self.layout.row().prop(retrieveSettings(RenderNormalPassWithWorkbench), "file_path")
        # row.separator(factor = .5)
        # row.prop(retrieveSettings(RenderNormalPassWithWorkbench), "second_file_path")

# @bookmark panel base class
class FastPanelBaseClass:
    bl_space_type = "VIEW_3D"
    # bl_region_type = "TOOLS" # This actually puts the panel
    # on the left side of the 3D viewport! Since the left panel is usually very
    # narrow however, I dont recommend putting it here.
    bl_region_type = "UI"
    bl_category = "Fast"
class FastToolBarPanelBaseClass:
    bl_space_type = "VIEW_3D"
    # bl_region_type = "TOOLS" # This actually puts the panel
    # on the left side of the 3D viewport! Since the left panel is usually very
    # narrow however, I dont recommend putting it here.


    bl_region_type = "HEADER"
    bl_category = "Fast"
    # bl_options = {"DEFAULT_CLOSED"}
import textwrap


# parent could be self.layout
# context is the second parameter in draw()
# text is the text you want to wrap
def label_multiline(text: str, context: bpy.types.Context, parent):
    textListSplitByNewLines = text.split('\n')

    for text in textListSplitByNewLines:
        chars = int(context.region.width / 7)   # 7 pix on 1 character
        wrapper = textwrap.TextWrapper(width=chars)
        text_lines = wrapper.wrap(text=text)
        for text_line in text_lines:
            parent.label(text=text_line)

def retrieveOperatorFromCls(cls):

    # if hasattr(cls, 'bl_idname'):
    #     return cls.bl_idname
    # return PascalCaseTo_snake_case(f"{addonNameShort}_{cls.__name__}")
    return cls.bl_idname

# @bookmark main panel

@registerOperatorsDecorator
class FastPBRViewportRender(FastPanelBaseClass, bpy.types.Panel):
    # bl_idname = "EXAMPLE_PT_panel_1"
    # bl_label = "Panel 1"

    def draw(self, context):
        # print("YOOOOOOOOOOOOOOOOOOOOOOOOOOOOO: " + retrieveOperatorFromCls(FastPBRViewportRender))
        self.layout.operator(retrieveOperatorFromCls(FastPBRViewportRender))
        self.layout.operator(retrieveOperatorFromCls(FastPBRRestoreSettings))
        self.layout.operator(retrieveOperatorFromCls(MatchViewportDisplayAndSurfaceBaseColor))
        # self.layout.row().prop(bpy.context.scene.fast_pbr_render_normal_pass_with_workbench, "file_path")
        # box = self.layout.box()
        # # box.separator_spacer = 0.1
        # box.label(text=f"Welcome to {addonNameShort}!")

        # box.row().prop(retrieveSettingsUsing__name__insteadOfbl_idname(RenderNormalPassWithWorkbench), "file_path")
        
        # self.layout.box()




@registerOperatorsDecorator
class WelcomeToFastPBRViewportRender(FastPanelBaseClass, bpy.types.Panel):
    bl_parent_id = FastPBRViewportRender.bl_idname

    def draw(self, context):
        # layout = self.layout
        # layout.label(text=f"{self.bl_label}First Sub Panel of Panel 1.")
        label_multiline(f"""This tool lets you automatically generate full sets of PBR images and export them using a naming standard of your choice.

The addon supports a wide range of PBR types & is easily configurable, in addition to this it works by rendering your viewport, therefore
rendering from a camera of your choice is as easy as looking through the camera and performing a render.
        
If you have any questions or have any ideas, you can reach me via Discord, danieljackson#0286 or by visiting our Github.""",context,self.layout)

class propertyClass():
    def __str__(self):
        return str(f'{self=}'.split('=')[0])
testVar = propertyClass()


# @registerOperatorsDecorator
# class Dynamic2StringListElement(bpy.types.UIList):
#     # bl_idname = "BAKELAB_MAP_UL_list"
#     def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
#         if self.layout_type in {'DEFAULT', 'COMPACT'}:
#             if item.type == 'CustomPass':
#                 layout.label(text = item.pass_name, icon = 'NONE')
#             else:
#                 layout.label(text = item.type, icon = 'NONE')
#         elif self.layout_type in {'GRID'}:
#             layout.alignment = 'CENTER'
#             layout.label(text = "", icon = 'TEXTURE')
#         layout.prop(item, 'enabled')



#####################
### DYAMIC UI LIST###
#####################
# @bookmark dynamic ui list
import bpy
# from bpy.props import StringProperty, IntProperty, CollectionProperty
# from bpy.types import PropertyGroup, UIList, Operator, Panel
# bl_info = {
#     "name": "Sinestesia UI List Example",
#     "blender": (3, 00, 0),
#     "category": "Object",
# }

@settingsContainerDecorator
class ListStringItem():
    
    class settings(bpy.types.PropertyGroup): # The data container for the values stored on each item in the list.
        """Group of properties representing an item in the list."""

        key: bpy.props.StringProperty(
            name="key",
            description="""This is the key that you put into the brackets to have it be replaced by the held value when generating the final path. Note that you are not supposed to enter the curly braces yourself here, you only put the braces when using the key in a path.
            
An example value could be 'textureSetName'""",
            default="textureSetName") = propertyClass()

        value: bpy.props.StringProperty(
            name="value",
            description="This is the value that the key gets replaced by. Example 'myFancyTextureSet'",
            default="MyFancyTextureSet") = propertyClass()


@registerOperatorsDecorator # Seems to work just fine with UILIST as well kek.
class DynamicListItemUI(bpy.types.UIList): # Draws all the items in the list, its the box that the list items are displayed within.
    """Demo UIList."""
    # bl_

    def draw_item(self, context, layout: bpy.types.Panel.layout, data, item: ListStringItem.settings, icon, active_data,
                  active_propname, index): # Draws the item itself
        # item = ListStringItem()
        # We could write some code to decide which icon to use here...
        # custom_icon = 'OBJECT_DATAMODE'
        custom_icon = 'NONE'

        # Make sure your code supports all 3 layout types
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # item: ListStringItem
            
        # row = layout.row()
            layout.label(text=item.key, icon = custom_icon) # @todo Check if its possible to make these modifiable with double click, like as if they were displayed as a prop directly.
            layout.label(text=item.value, icon = custom_icon)
            # layout.prop(retrieveSettings(GlobalSettings).file_path_replacement_keys_collection_property, item.key)
            # layout.label(text=item.value, icon = custom_icon)

            
            # cls.layout.prop(retrieveSettings(cls), f'{cls.settings.enable_pass=}'.split('=')[0].split('.')[-1], text = "")

            # layout.label(text=item.name, icon = custom_icon)
            # layout.label(text=item.random_prop, icon = custom_icon)

        elif self.layout_type in {'GRID'}: # Not sure when this is supposed to trigger?
            layout.alignment = 'CENTER' # When is the ui displayed in a grid lol?
            layout.label(text="", icon = custom_icon)

@registerOperatorsDecorator
class DynamicListNewItemOperator(bpy.types.Operator):
    """Add a new item to the list."""

    # bl_idname = "my_list.new_item"
    # bl_label = "Add a new item"

    def execute(self, context):
        retrieveSettings(GlobalSettings).file_path_replacement_keys_collection_property.add()

        return{'FINISHED'}


@registerOperatorsDecorator
class DynamicListDeleteOperator(bpy.types.Operator):
    """Delete the selected item from the list."""

    # bl_idname = "my_list.delete_item"
    # bl_label = "Deletes an item"

    @classmethod
    def poll(cls, context):
        return retrieveSettings(GlobalSettings).file_path_replacement_keys_collection_property

    def execute(self, context):
        # my_list = context.scene.my_list
        # index = context.scene.list_index
        my_list = retrieveSettings(GlobalSettings).file_path_replacement_keys_collection_property
        index = retrieveSettings(GlobalSettings).file_path_replacement_keys_index_selected_by_user

        my_list.remove(index)
        index = min(max(0, index - 1), len(my_list) - 1)

        return{'FINISHED'}

@registerOperatorsDecorator
class DynamicListMoveOperator(bpy.types.Operator):
    """Move an item in the list."""

    # bl_idname = "my_list.move_item"
    # bl_label = "Move an item in the list"

    direction: bpy.props.EnumProperty(items=(('UP', 'Up', ""),
                                              ('DOWN', 'Down', ""),))

    @classmethod
    def poll(cls, context):
        return retrieveSettings(GlobalSettings).file_path_replacement_keys_collection_property

    def move_index(self):
        """ Move index of an item render queue while clamping it. """

        index = retrieveSettings(GlobalSettings).file_path_replacement_keys_index_selected_by_user
        list_length = len(retrieveSettings(GlobalSettings).file_path_replacement_keys_collection_property) - 1  # (index starts at 0)
        new_index = index + (-1 if self.direction == 'UP' else 1)

        index = max(0, min(new_index, list_length))

    def execute(self, context):
        my_list = retrieveSettings(GlobalSettings).file_path_replacement_keys_collection_property
        index = retrieveSettings(GlobalSettings).file_path_replacement_keys_index_selected_by_user

        neighbor = index + (-1 if self.direction == 'UP' else 1)
        my_list.move(neighbor, index)
        self.move_index()

        return{'FINISHED'}

# @bookmark UI list panel

# class GlobalSettings():
#     pass




# def register():

#     bpy.utils.register_class(ListItem)
#     bpy.utils.register_class(MY_UL_List)
#     bpy.utils.register_class(LIST_OT_NewItem)
#     bpy.utils.register_class(LIST_OT_DeleteItem)
#     bpy.utils.register_class(LIST_OT_MoveItem)
#     bpy.utils.register_class(PT_ListExample)

    # bpy.types.Scene.my_list = CollectionProperty(type = ListItem)
    # bpy.types.Scene.list_index = IntProperty(name = "Index for my_list",
                                            #  default = 0)


# def unregister():

#     del bpy.types.Scene.my_list
#     del bpy.types.Scene.list_index

    # bpy.utils.unregister_class(ListItem)
    # bpy.utils.unregister_class(MY_UL_List)
    # bpy.utils.unregister_class(LIST_OT_NewItem)
    # bpy.utils.unregister_class(LIST_OT_DeleteItem)
    # bpy.utils.unregister_class(LIST_OT_MoveItem)
    # bpy.utils.unregister_class(PT_ListExample)


# if __name__ == "__main__":
#     register()

######### UI LIST EXAMPLE END


@registerOperatorsDecorator
class RenderPasses(FastPanelBaseClass, bpy.types.Panel):
    bl_parent_id = FastPBRViewportRender.bl_idname

    def draw(self, context):
        pass


# @bookmark GlobalSettings

# def getFutureClass(cls):
#     if TYPE_CHECKING:
#         return cls.settings

class texts():
    MoveAndRenameOperatorDescription = f'''Move and rename lets you move all the images from your source folder to your destination folder, specified by the respective fields. The source path supports variable/key insertion using the {{myVariable}} format, however unlike the destination path it ONLY supports user defined variables and a smaller subset of predefined variables. Variables like imageSizeShort or imageName are therefore not supported.

Supported predefined variables for the source path are:

fullPathToDesktop
fullPathToUserHomePath
    
The intended usecase for this feature is that if youre exporting images from a 3rd party software such as Photoshop, Houdini, Quixel Mixer or Adobe Substance (or any other software that exports images :P ) you can still use {addonName} to name the images by your personal or your projects naming standards with help of the addons file name/path generation.

For instance if you export some 4K images from Mixer to have something like the following paths:

"C:/FromMixer/albedo.png"
"C:/FromMixer/roughness.png"
"C:/FromMixer/metalness.png"
"C:/FromMixer/normal.png"
"C:/FromMixer/displacement.png"
"C:/FromMixer/ao.png"

You can use the following source:

"C:/FromMixer"

and target path:

"{{fullPathToDesktop}}/Art And Development/{{name}}/{{sourceDirectoryTopLevelFolderName}}{{imageSizeShort}}/{{name}}{{imageSizeShort}}_{{fileNameWithExtension}}"

You will have your images be moved and renamed to something like:

"C:/Users/Oliver/desktop/Art And Development/MyFancyTextureSet/FromMixer4K/MyFancyTextureSet4K_albedo.png"
"C:/Users/Oliver/desktop/Art And Development/MyFancyTextureSet/FromMixer4K/MyFancyTextureSet4K_roughness.png"
"C:/Users/Oliver/desktop/Art And Development/MyFancyTextureSet/FromMixer4K/MyFancyTextureSet4K_metalness.png"
"C:/Users/Oliver/desktop/Art And Development/MyFancyTextureSet/FromMixer4K/MyFancyTextureSet4K_normal.png"
"C:/Users/Oliver/desktop/Art And Development/MyFancyTextureSet/FromMixer4K/MyFancyTextureSet4K_displacement.png"
"C:/Users/Oliver/desktop/Art And Development/MyFancyTextureSet/FromMixer4K/MyFancyTextureSet4K_ao.png"

Magical right?

Note that the souce path should be pointing towards a folder, not a particular image! Moving individual images is unsupported currently, it always moves all images that it can find directly under the specified directory.
'''
    exportPathDescription = f"""The export path lets you choose the name
of the images as well as the full path those images goes inside upon export using
pre-defined variables that are auto-generated as well as variables that you define yourself.

There is a large set of predefined variables:
   
imageSizeShort
imageWidth
imageHeight
imageSizeInPixels
fileNameWithExtension
fileNameWithoutExtension
fileExtensionWithoutDot
fileWithPathAndExtension
sourceDirectoryTopLevelFolderName
sourceDirectory

fullPathToDesktop
fullPathToUserHomePath
   
In addition to these, you can define your own using the dynamic list below, but first, heres an example of what a file path could look like:
C:/testTarget/{{name}}/FromFastPBR/{{name}}{{imageSizeShort}}_{{fileNameWithExtension}}
Which would then turn into something like:
C:/testTarget/myFancyTextureSet/FromFastPBR/myFancyTextureSet4K_AO.png
"""
        
    


@settingsContainerDecorator
@registerOperatorsDecorator
class GlobalSettings(FastPanelBaseClass, bpy.types.Panel):
    bl_parent_id = FastPBRViewportRender.bl_idname
    # bl_options = {'HIDE_HEADER'}
    # bl_options = {}
    bl_order = 1000000  # Doesnt seem to work ;-;
    class settings(bpy.types.PropertyGroup): # CANNOT BE RENAMED
            # def __init_subclass__(cls, scm_type=None, name=None, **kwargs):
            #     print(f"initializing subclass: {cls}")
            #     classesToRegister.append(cls)
            export_source_path: bpy.props.StringProperty(name="Source Path",
                                        description=texts.MoveAndRenameOperatorDescription,
                                        default="",
                                        maxlen=1024,
                                        subtype="FILE_PATH")
            export_file_path: bpy.props.StringProperty(name="Destination path",
                                        description=texts.exportPathDescription,
                                        default="",
                                        maxlen=1024,
                                        subtype="FILE_PATH")
            second_file_path: bpy.props.StringProperty(name="File path", # Unused I think? Should be safe to remove if you feel brave
                                        description="Some elaborate description",
                                        default="",
                                        maxlen=1024,
                                        subtype="FILE_PATH")
            enable_pass: bpy.props.BoolProperty(name="Enable Pass", default=True) = propertyClass() # Also unused?
            file_path_replacement_keys_collection_property: bpy.props.CollectionProperty(type=ListStringItem.settings) = propertyClass()
            file_path_replacement_keys_index_selected_by_user: bpy.props.IntProperty(name = "Index Selected by the User.", default = 0) = propertyClass()
# def register():
    # bpy.types.Scene.my_list = CollectionProperty(type = ListItem)
    # bpy.types.Scene.list_index = IntProperty(name = "Index for my_list",
                                            #  default = 0)

    def draw(self, context):
        # layout = self.layout
        descriptiveText = f"""The export path lets you choose the name
of the images as well as the full path those images goes inside upon export using
pre-defined variables that are auto-generated as well as variables that you define yourself.

There is a large set of predefined variables:
   
imageSizeShort
imageWidth
imageHeight
imageSizeInPixels
fileNameWithExtension
fileNameWithoutExtension
fileExtension
fileWithPathAndExtension
   
In addition to these, you can define your own using the dynamic list below, but first, heres an example of what a file path could look like:
C:/testTarget/{{name}}/FromFastPBR/{{name}}{{imageSizeShort}}_{{fileNameWithExtension}}
Which would then turn into something like:
C:/testTarget/myFancyTextureSet/FromFastPBR/myFancyTextureSet4K_AO.png
"""


        box = self.layout.box()
        # box.row().prop(retrieveSettingsUsing__name__insteadOfbl_idname(RenderNormalPassWithWorkbench), "file_path")
        box.row().prop(retrieveSettings(self), "export_file_path")
        # label_multiline(descriptiveText, context, box)
        # box.row().template_list(Dynamic2StringListElement.bl_idname, "", context.scene)


@registerOperatorsDecorator
class CustomPathKeys(FastPanelBaseClass,bpy.types.Panel):
    """Demo panel for UI list Tutorial."""

    # bl_label = "UI_List Demo"
    # bl_idname = "SCENE_PT_LIST_DEMO"
    # bl_space_type = 'PROPERTIES'
    # bl_region_type = 'WINDOW'
    # bl_context = "scene"
    # bl_options = {'HIDE_HEADER'}
    # bl_options = {'DRAW_BOX', 'HIDE_HEADER'}
    # bl_parent_id = PascalCaseTo_snake_case(f"{addonNameShort}GlobalSettings")
    # bl_parent_id = PascalCaseTo_snake_case(f"{addonNameShort}ViewportRender")
    bl_parent_id = GlobalSettings.bl_idname
    
    # def draw_header(cls, context): # The draw header is the first line of the panel where the foldout arrow is.
    #     # layout = self.layout
    #     # cls.layout.prop(retrieveSettings(cls), f'{cls.settings.enable_pass=}'.split('=')[0].split('.')[-1], text = "")
    #     cls.layout.row().label("hi")

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        outerVerticalBox = layout.row().box()
        # print("LOOK MAN: " + str(retrieveSettings(GlobalSettings)))
        # # print("LOOK MAN: " + f'{GlobalSettings.settings.file_path_replacement_keys_collection_property=}'.split('=')[0].split('.')[-1])
        # print("LOOK MAN: " + f'{GlobalSettings.settings.file_path_replacement_keys_index_selected_by_user=}'.split('=')[0].split('.')[-1])
        outerVerticalBox.template_list(DynamicListItemUI.bl_idname, "wtf_is_this_for", retrieveSettings(GlobalSettings),
                          str(f'{GlobalSettings.settings.file_path_replacement_keys_collection_property=}'.split('=')[0].split('.')[-1]), retrieveSettings(GlobalSettings), str(f'{GlobalSettings.settings.file_path_replacement_keys_index_selected_by_user=}'.split('=')[0].split('.')[-1]))


        # cls.layout.prop(retrieveSettings(cls), f'{cls.settings.enable_pass=}'.split('=')[0].split('.')[-1])

        # row.template_list(MY_UL_List.bl_idname, "wtf_is_this_for", bpy.context.scene.fast_pbr_global_settings,
        #                   'file_path_replacement_keys_collection_property', bpy.context.scene.fast_pbr_global_settings, "file_path_replacement_keys_i

        # row.template_list(MY_UL_List.bl_idname, "wtf_is_this_for", bpy.context.scene.fast_pbr_global_settings,
        #                   'file_path_replacement_keys_collection_property', bpy.context.scene.fast_pbr_global_settings, "file_path_replacement_keys_index_selected_by_user")
        # BACKUP:
        # row.template_list(MY_UL_List.bl_idname, "wtf_is_this_for", retrieveSettings(GlobalSettings),
        #                   f'{GlobalSettings.settings.file_path_replacement_keys_collection_property=}'.split('=')[0], retrieveSettings(GlobalSettings), f'{GlobalSettings.settings.file_path_replacement_keys_index_selected_by_user=}'.split('=')[0])


        
        # self.layout.operator(retrieveOperatorFromCls(FastPBRViewportRender))

        # MEANT TO BE ACTIVE:
        # innerRow = row.box()
        innerHorizontalRow = outerVerticalBox.row()
        # row.operator(PascalCaseTo_snake_case(f"{addonNameShort}.{DynamicListNewItemOperator}"), text='NEW')
        innerHorizontalRow.operator(retrieveOperatorFromCls(DynamicListNewItemOperator), text='NEW')
        innerHorizontalRow.operator(retrieveOperatorFromCls(DynamicListDeleteOperator), text='REMOVE')
        innerHorizontalRow.operator(retrieveOperatorFromCls(DynamicListMoveOperator), text='UP').direction = 'UP'
        innerHorizontalRow.operator(retrieveOperatorFromCls(DynamicListMoveOperator), text='DOWN').direction = 'DOWN'

        if retrieveSettings(GlobalSettings).file_path_replacement_keys_collection_property:
            item = retrieveSettings(GlobalSettings).file_path_replacement_keys_collection_property[retrieveSettings(GlobalSettings).file_path_replacement_keys_index_selected_by_user]

            # outerVerticalBox = outerVerticalBox.row()
            # outerVerticalBox.prop(item, retrieveSettings(ListStringItem).key)
            outerVerticalBox.prop(item, "key")
            outerVerticalBox.prop(item, "value")

        # if retrieveSettings(GlobalSettings).file_path_replacement_keys_index_selected_by_user >= 0 and retrieveSettings(GlobalSettings).file_path_replacement_keys_collection_property:
        #     item = retrieveSettings(GlobalSettings).file_path_replacement_keys_collection_property[retrieveSettings(GlobalSettings).file_path_replacement_keys_index_selected_by_user]

        #     row = layout.row()
        #     row.prop(item, "name")
        #     row.prop(item, "random_prop")





        # layout = self.layout
        # box = self.layout.box()
#         box.row().prop(retrieveSettingsUsing__name__insteadOfbl_idname(RenderNormalPassWithWorkbench), "file_path")
#         label_multiline(f"""The export path lets you choose the name
# of the images as well as the full path those images goes inside upon export using
# pre-defined variables that are auto-generated as well as variables that you define yourself.

# Heres an example of what a file path could look like:

# """)
        # layout.label(text="Second Sub Panel of Panel 1.")



@registerOperatorsDecorator
class MoveAndRenameImages(bpy.types.Operator):
    bl_description =  texts.MoveAndRenameOperatorDescription
    def execute(self, context: bpy.types.Context):

        replacementDictionary = dict()

        for item in retrieveSettings(GlobalSettings).file_path_replacement_keys_collection_property:
            # print(str(item.value) + "item")
            replacementDictionary[item.key] = item.value

        print(f"""
replacementDictionary: {replacementDictionary}
pathToStoreImagesIn: {pathToStoreImagesIn}
retrieveSettings(GlobalSettings).export_file_path: {retrieveSettings(GlobalSettings).export_file_path}""")


        moveImages(retrieveSettings(GlobalSettings).export_source_path, retrieveSettings(GlobalSettings).export_file_path, replacementDictionary)
        # moveImages(retrieveSettings(GlobalSettings).export_source_path, retrieveSettings(GlobalSettings).export_file_path, dict(retrieveSettings(GlobalSettings).file_path_replacement_keys_collection_property))
        
        return {'FINISHED'}


def MoveAndRenameDecorator(cls: MoveAndRename):
    cls.bl_parent_id = FastPBRViewportRender.bl_idname

@MoveAndRenameDecorator
@registerOperatorsDecorator
class MoveAndRename(FastPanelBaseClass, bpy.types.Panel):
    # bl_parent_id = GlobalSettings.bl_idname # Moved into decorator
    def draw(self, context):
        box = self.layout.box()
        box.row().prop(retrieveSettings(GlobalSettings), "export_source_path")
        self.layout.row().operator(retrieveOperatorFromCls(MoveAndRenameImages))
# classesToRegister.append(classesToRegister.append(EXAMPLE_PT_panel_3))

# classesToRegister = (EXAMPLE_PT_panel_1, EXAMPLE_PT_panel_2, EXAMPLE_PT_panel_3)

        #         row = self.layout.row(align = True)
        # row.separator(factor = .5)
        # row.prop(grabDoc, 'exportNormals', text = "")

        # row.operator("grab_doc.preview_warning" if grabDoc.firstBakePreview else "grab_doc.preview_map", text = "Normals Preview").preview_type = 'normals'
        
        # row.operator("grab_doc.offline_render", text = "", icon = "RENDER_STILL").render_type = 'normals'
        # row.separator(factor = 1.3)
        # layout.row().prop(retrieveSettings(RenderNormalPassWithWorkbench), "second_file_path")



        # layout.row().prop(RenderNormalPassWithWorkbench.retrieveSettings(), "file_path")


        # layout.row().prop(context.scene.fast_pbr, "file_path")
        # layout.row().prop(getGlobalAddonProperties(), "target_directory")
        # layout.row().prop(context.preferences.addons[__name__].preferences, "file_path")



# class EXAMPLE_panel:
#     bl_space_type = "VIEW_3D"
#     bl_region_type = "UI"
#     bl_category = "Example Tab"
#     bl_options = {"DEFAULT_CLOSED"}

# @registerOperatorsDecorator
# class EXAMPLE_PT_panel_1(EXAMPLE_panel, bpy.types.Panel):
#     bl_idname = "EXAMPLE_PT_panel_1"
#     bl_label = "Panel 1"

#     def draw(self, context):
#         layout = self.layout
#         layout.label(text="This is the main panel.")
# @registerOperatorsDecorator
# class EXAMPLE_PT_panel_2(EXAMPLE_panel, bpy.types.Panel):
#     bl_parent_id = "EXAMPLE_PT_panel_1"
#     bl_label = "Panel 2"

#     def draw(self, context):
#         layout = self.layout
#         layout.label(text="First Sub Panel of Panel 1.")
# @registerOperatorsDecorator
# class EXAMPLE_PT_panel_3(EXAMPLE_panel, bpy.types.Panel):
#     bl_parent_id = "EXAMPLE_PT_panel_1"
#     bl_label = "Panel 3"







# if __name__ == "__main__":
#     register()


# PSUEDO CODE FOR A SETTINGS BACKUP/RESOTORE SYSTEM.

# myDictionary = {"test": bpy.context.world}

# @bookmark BACKUP RESTORE
class BackupPrepareAndRestore():

    show_overlaysBackup: bpy.types.Space
    activeWorldBackup: bpy.types.World
    render_passBackup = str
    shading_type: str = str()


    @classmethod
    def backupSettingsAndPrepareForRender(self):
        # myDictionary[bpy.context.world] = "someRandomWorldThatINeedDuringTheExecutionOfTheScript - but that I later on wanna bring back to previous state"
        
        self.show_overlaysBackup = bpy.context.space_data.overlay.show_overlays
        self.activeWorldBackup = bpy.context.scene.world
        
        self.render_passBackup = bpy.context.space_data.shading.render_pass

        self.shading_type = bpy.context.space_data.shading.type


        
        # bpy.context.world
        global test
        test = bpy.context



        bpy.ops.ed.undo_push()

    @classmethod
    def restoreSettings(self):
        disableRestore = False
        if not disableRestore:
            
            bpy.ops.ed.undo() # This restores any settings
            # in the file, however certain "settings" that
            # are frequently toggled such as "overlays" (visibility
            # of things like the 3D cursor & selected object outlines)
            # Do not get affected by the undo action!

            if bpy.context.scene.render.engine == 'BLENDER_EEVEE':        
                bpy.context.space_data.shading.render_pass = self.render_passBackup

            bpy.context.space_data.shading.type = self.shading_type

            # pass
            # for key in myDictionary:
            #     key = myDictionary[key]
            # bpy.context =  test
            bpy.context.space_data.overlay.show_overlays = self.show_overlaysBackup
            # bpy.context.scene.world =  bpy.data.worlds.get(self.activeWorldBackup.name_full)




# def prepareScene():
#     bpy.context.space_data.overlay.show_overlays = False

#     space_shading = {sett: getattr(bpy.context.space_data.display.shading, sett) for sett in dir(bpy.context.space_data.display.shading)}
# # blabla
#     for sett in space_shading:
#         try:
#              setattr(bpy.context.space_data.display.shading, sett, space_shading[sett])
#         except Exception as e:
#             pass



###################################################################################
######################### CLASSES FOR PASSES ######################################
###################################################################################
# bpy.types.collec
# @bookmark RenderPass base class



# @renderPassDecorator

# @renderPassDecorator
# class GlobalSettings():
#     class settings(bpy.types.PropertyGroup):
#         export_file_path: bpy.props.StringProperty(name="Export path",
#                                     description="The path that the images will be exported to, including the image name and file extension.",
#                                     default="",
#                                     maxlen=1024,
#                                     subtype="FILE_PATH")

class RenderPass(FastPanelBaseClass, bpy.types.Panel):
    bl_options = {'DRAW_BOX', 'DEFAULT_CLOSED'}
    # @registerOperatorsDecorator

    class settings(bpy.types.PropertyGroup): # CANNOT BE RENAMED
            # def __init_subclass__(cls, scm_type=None, name=None, **kwargs):
            #     print(f"initializing subclass: {cls}")
            #     classesToRegister.append(cls)
            file_path: bpy.props.StringProperty(name="File path",
                                        description="Some elaborate description",
                                        default="",
                                        maxlen=1024,
                                        subtype="FILE_PATH")
            second_file_path: bpy.props.StringProperty(name="File path",
                                        description="Some elaborate description",
                                        default="",
                                        maxlen=1024,
                                        subtype="FILE_PATH")
            enable_pass: bpy.props.BoolProperty(name="Enable Pass", default=True) = propertyClass()
            
            # myVar123: str = "MY VAR!!!"
    
    global classesToRegister
    classesToRegister.append(settings)        

    ##########
    ### UI ###
    ##########
    
    bl_label = '' # Set in decorator by class name
    bl_parent_id = RenderPasses.bl_idname # The parent ID is the panel name
    # bl_parent_id = PascalCaseTo_snake_case(f"{addonNameShort}_global_settings") # The parent ID is the panel name
    # that the coresponding panel will be in
    def draw_header(cls, context): # The draw header is the first line of the panel where the foldout arrow is.
        # layout = self.layout
        cls.layout.prop(retrieveSettings(cls), f'{cls.settings.enable_pass=}'.split('=')[0].split('.')[-1], text = "")
        # layout.label(text="My Select Panel")


    def draw(cls, context):
        # layout = self.layout
        # cls.layout.label(text=f"{cls.bl_label}First Sub Panel of Panel 1.")     
        # print("LOOK HERE ", f'{cls.settings.enable_pass=}'.split('=')[0].split('.')[-1])
        cls.layout.prop(retrieveSettings(cls), f'{cls.settings.enable_pass=}'.split('=')[0].split('.')[-1])
        cls.draw_pass_specific_ui_elements(context)


    def draw_pass_specific_ui_elements(cls, context):
        pass
                               
    ##########
    # UI END #
    ##########

    @classmethod
    def retrieveSettings(cls): # CANNOT BE RENAMED
        if TYPE_CHECKING: # TYPE_CHEKCING is only true when running through a language server.
            # Always False when the code is running in a real software.
            return cls.settings
        else: # bpy.context.scene.fast_pbr_render_normal_pass_with_workbench
            return print("bpy.context.scene." + PascalCaseTo_snake_case(addonNameShort + "_" + cls.__name__))
            return exec("bpy.context.scene." + PascalCaseTo_snake_case(addonNameShort + "_" + cls.__name__))
            # exec exectues a string as if it were written without the string
            # Here were using it to access classes dynamically at runtime.
            # Returns something like bpy.context.scene.fast_pbr.render_pass


    instances: list[RenderPass] = []

    passName = "UnnamedChannel" # Something simple, like "normal", "ao", "height", "matID" etc. Used for naming the files
    # Should be overriden by each pass "subclass", or the passes will end up overriding the same file upon creation!

    # @classmethod
    # def __init__(self):
    #     self.__class__.instances.append(self)
    @classmethod
    def prepare_to_render(self):
        pass

    @classmethod
    def render(self):
        bpy.ops.render.opengl()
        # bpy.ops.render.opengl(write_still = True, sequencer=False)
        # print("---------------------------------------------------rendering")

    @classmethod
    def save_to_disk(self):
        # print("-----------------------------------------------------saving")
        image = bpy.data.images.get("Render Result")
        # image.filepath = pathToStoreImagesIn
        # image.save_render(pathToStoreImagesIn, "test")
        # image.filepath_raw = 'C:\FastPBRViewportRender'
        # image.file_format = 'PNG'
        # pathToStoreImageInIncludingFileNameAndFileExtension = 'C:/FastPBRViewportRender/'
        pathToStoreImageInIncludingFileNameAndFileExtension = pathToStoreImagesIn
        pathToStoreImageInIncludingFileNameAndFileExtension = pathToStoreImageInIncludingFileNameAndFileExtension + self.passName + ".png"
        # bpy.context.scene.render.__format__
        # image = bpy.data.images.new("Sprite", alpha=True, width=16, height=16)
        # image.alpha_mode = 'STRAIGHT'
        # image.filepath_raw = "pathToStoreImageInIncludingFileNameAndFileExtension"
        # image.file_format = 'PNG'
        # image.save()

        # bpy.data.images['Render Result'].filepath_raw = pathToStoreImageInIncludingFileNameAndFileExtension
        # bpy.data.images['Render Result'].file_format = 'PNG'
        # bpy.data.images['Render Result'].save()
        image.save_render(pathToStoreImageInIncludingFileNameAndFileExtension)


        # image.save_render('C:\FastPBRViewportRender\mytexture.png')
        # bpy.ops.image.save_as(save_as_render=True, copy=True, filepath="//..\\..\\untitled321.png", relative_path=True, show_multiview=False, use_multiview=False)
        # bpy.ops.image. 

    @classmethod
    def perform_post_process(self):
        """Runs after save_to_disk"""
        pass

    @classmethod
    def prepare_render_and_save(self):
        self.prepare_to_render()
        if retrieveSettingsUsing__name__insteadOfbl_idname(self).enable_pass:
            self.render()
            self.save_to_disk()
            self.perform_post_process()
        
# classesToRegister.append(classesToRegister.append(RenderPass))
# @bookmark Normal pass


class RenderAppendedMaterialTypeRenderPass(RenderPass): # A base class for render passes that are supposed to render a specific material only
    f"""To use this class, assign the literal name of the material in our assets file that you want to render to the materialToRender variable.
    
    Children of this class are typically found towards the bottom of the render pass section as its rendered in Eeevee."""

    materialToRender = 'FastPBRNormal'
    """This is the literal name of the material in our assets file that you want to render!"""

    @classmethod
    def prepare_to_render(self):
        bpy.context.space_data.shading.render_pass = 'DIFFUSE_COLOR'
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'
        # bpy.context
        # bpy.context.scene.render.engine = 'RENDER'
        # Switch viewport view to rendered, rather than solid or wire or whatever.
        bpy.context.space_data.shading.type = 'RENDERED'

        

        print("File path:", pathlib.Path(__file__).parent.resolve())
        
        if bpy.data.materials.find(self.materialToRender) < 0:
            appendAssetFromAssetsBlendFile(self.materialToRender, 'Material')
        if bpy.data.objects.find(self.materialToRender) < 0:
            appendAssetFromAssetsBlendFile(self.materialToRender, 'Object')
            bpy.data.objects[self.materialToRender].visible_camera = False
            bpy.data.objects[self.materialToRender].hide_render = True
            bpy.data.objects[self.materialToRender].hide_viewport = True
            # Skipping to loop over collections to save some precious execution time of looping over collections. The block is otherwise perfectly functional
            # for collection in bpy.context.scene.collection:
            #     collection: bpy.types.Collection
            #     collection.objects.unlink(bpy.data.objects[self.materialToRender])
            # bpy.context.scene.collection.objects.unlink(bpy.data.objects[self.materialToRender])




        for object in bpy.data.objects:
            object: bpy.types.Object
            if hasattr(object.data, 'materials'):
                if object.material_slots.__len__() < 1:
                    # bpy.ops.object.material_slot_add() 
                    # object.material_slots[0].material[0] = bpy.data.materials.get(self.materialToRender)
                    object.data.materials.append(None)
                    # cube.material_slots[0].material = bpy.data.materials['Blue']
                for materialSlot in object.material_slots:
                    materialSlot: bpy.types.MaterialSlot
                    # materialSlot.link = 'FastPBRNormal'
                    materialSlot.material = bpy.data.materials.get(self.materialToRender)
        copyModifiers(bpy.data.objects[self.materialToRender], bpy.data.objects)
        # raise ValueError('A very specific bad thing happened.')

    @classmethod
    def perform_post_process(self):
        pathToStoreImageInIncludingFileNameAndFileExtension = pathToStoreImagesIn
        fileToPerformPostProcessOn = pathToStoreImageInIncludingFileNameAndFileExtension + self.passName + ".png"

        # print("hello from post process")
        # from PIL import Image
        # import numpy

        im = Image.open(fileToPerformPostProcessOn)
        im = im.convert('RGBA')

        data = numpy.array(im)   # "data" is a height x width x 4 numpy array
        red, green, blue, alpha = data.T # Temporarily unpack the bands for readability

        
        white_areas = (red < 3) & (blue < 3) & (green < 3) # Condition for writing
        data[..., :-1][white_areas.T] = (128, 128, 255) # Replace values that fullfill the condition with 128,128,255
        # white_areas = (red == 1) & (blue == 1) & (green == 1)
        # data[..., :-1][white_areas.T] = (128, 128, 255) # Transpose back needed
        im2 = Image.fromarray(data)
        im2 = im2.convert('RGB')
        im.close()
        im2.save(fileToPerformPostProcessOn)
        im2.close()
        # im2.show()
        # print("Second hello")

@renderPassDecorator
class RenderNormalPassWithWorkbench(RenderPass):
    passName = "normal" 


    @classmethod
    def prepare_to_render(self):


        # Output Properties > Output
        bpy.context.scene.render.image_settings.color_mode = 'RGB'
        bpy.context.scene.render.image_settings.file_format = 'PNG'
        bpy.context.scene.render.image_settings.color_depth = '8'
        bpy.context.scene.render.image_settings.compression = 60
        bpy.context.scene.render.use_overwrite = True



        
        # Worlds properties
        if not nameOfWorldUsedDuringPBRmapCreation in bpy.data.worlds:
            bpy.data.worlds.new(nameOfWorldUsedDuringPBRmapCreation)
            
        # bpy.data.worlds
        bpy.context.scene.world = bpy.data.worlds[nameOfWorldUsedDuringPBRmapCreation]
        bpy.context.scene.world.color = (0.215861, 0.215861, 1)
        
        # bpy.context.world = bpy.contex


        # Switch viewport view to rendered, rather than solid or wire or whatever.
        bpy.context.space_data.shading.type = 'RENDERED'

        # Hides things like the 3D cursor, object selection outlines (etc).
        bpy.context.space_data.overlay.show_overlays = False

        # Set the render engine to workbench rather than Eevee/Cycles
        bpy.context.scene.render.engine = 'BLENDER_WORKBENCH'

        # Render properties > Lighting
        bpy.context.scene.display.shading.light = 'MATCAP'
        bpy.context.scene.display.shading.studio_light = 'FastPBRNormalMatCap.exr'
        # bpy.context.scene.display.shading.studio_light = 'check_normal+y.exr'

        # Render properties > Color
        bpy.context.scene.display.shading.color_type = 'SINGLE'
        bpy.context.scene.display.shading.single_color = (1, 1, 1)

        # Render properties > Options
        bpy.context.scene.display.shading.show_backface_culling = False
        bpy.context.scene.display.shading.show_xray = False
        bpy.context.scene.display.shading.show_shadows = False
        bpy.context.scene.display.shading.show_cavity = False
        bpy.context.scene.display.shading.use_dof = False
        bpy.context.scene.display.shading.show_object_outline = False
        bpy.context.scene.display.shading.show_specular_highlight = True

        # Render properties > Color management
        bpy.context.scene.display_settings.display_device = 'None'
        bpy.context.scene.view_settings.view_transform = 'Standard'
        bpy.context.scene.view_settings.look = 'None'
        bpy.context.scene.view_settings.exposure = 0
        bpy.context.scene.view_settings.gamma = 1
        bpy.context.scene.sequencer_colorspace_settings.name = 'Raw'

    @classmethod
    def perform_post_process(cls):
        # return
        # Now we will invert the pixels where the normal map has rendered a face that is facing away from the camera.

        # This will let users simply not care about correcting there face normals before rendering, so even if it may
        # add 3-4 seconds worth of render time - its probably gonna save the user more time than if he had to ensure
        # his normals are correct.
        pathToStoreImageInIncludingFileNameAndFileExtension = pathToStoreImagesIn
        fileToPerformPostProcessOn = pathToStoreImageInIncludingFileNameAndFileExtension + cls.passName + ".png"
        
        from PIL import Image, ImageChops
        imageWithoutCull = Image.open(fileToPerformPostProcessOn).convert('RGB')
        # import numpy as np
        bpy.context.scene.display.shading.show_backface_culling = True
        cls.render()
        cls.passName = 'temp'
        cls.save_to_disk() # Save a 'temp' file to disk.
        normalWithBackfaceCulling = pathToStoreImageInIncludingFileNameAndFileExtension + cls.passName + ".png"
        imageWithCull = Image.open(normalWithBackfaceCulling).convert('RGB')
        # imageWithCull = Image.open('C:/Users/Oliver/Desktop/test/inversionTest/withCull.png').convert('RGB')
        # imageWithoutCull = Image.open('C:/Users/Oliver/Desktop/test/inversionTest/withoutCull.png').convert('RGB')
        # img1 = Image.open('C:/Users/Oliver/Desktop/test/untitled.png').convert('RGB')
        # img2 = Image.open('C:/Users/Oliver/Desktop/test/untitled3.png').convert('RGB')
        
        # # image3 = ImageChops.difference(image1, image2)
        
        # # image3.save('C:/Users/Oliver/Desktop/test/untitled3.png')
        
        
        # # from PIL import Image, ImageChops
        # print(img1)
        # # assign images
        # # img1 = Image.open("1img.jpg")
        # # img2 = Image.open("2img.jpg")
        # # image1.show()
        # # finding difference
        # # import numpy as np
        # # whiteImage = np.zeros([100,100,3],dtype=np.uint8)
        # # whiteImage.fill(255) # or img[:] = 255
        # whiteImage = Image.new('RGB', (1920, 1080), color = (1,1,1))
        # diff = ImageChops.add_modulo(ImageChops.difference(img1, img2).convert('RGB'), whiteImage).convert('L')
        # # ImageChops.hard_light
        # final = Image.composite(img2, img1, diff)
        # # showing the difference
        # ImageChops.hard_light
        
        # img1AsArray = numpy.asarray(img1)
        # img2AsArray = numpy.asarray(img2)
        
        # final = PIL.Image.fromarray(numpy.uint8((img1AsArray == img2AsArray)))
        
        
        # final.show()
        
        # import numpy as np
        print(imageWithoutCull.size)
        # img1 = Image.open('test.png')
        imageWithoutCull = imageWithoutCull.convert('RGBA')
        imageWithCull = imageWithCull.convert('RGBA')
        
        imageWithoutCullAsArray = numpy.array(imageWithoutCull)   # "data" is a height x width x 4 numpy array
        imageWithCullAsArray = numpy.array(imageWithCull)   # "data" is a height x width x 4 numpy array
        red1, green1, blue1, alpha1 = imageWithoutCullAsArray.T # Temporarily unpack the bands for readability
        red2, green2, blue2, alpha2 = imageWithCullAsArray.T # Temporarily unpack the bands for readability
        
        # Replace white with red... (leaves alpha values alone...)
        differences = (red1 == red2) & (blue1 == blue2) & (green1 == green2)
        # image1asArray = Image.new('RGBA', (1920, 1080), (0,0,0,0))
        imageWithoutCullAsArray[..., :-1][differences.T] = (0, 0, 0) # Transpose back needed
        imageWithoutCullAsArray[..., :-1][~ differences.T] = (255, 255, 255) # Transpose back needed
        
        diff = Image.fromarray(imageWithoutCullAsArray).convert('L')
        
        red, green, blue, alpha = imageWithoutCull.split()
        invertedImg1 = Image.merge('RGBA', (ImageChops.invert(red), ImageChops.invert(green), blue, alpha))
        
        imageWithoutCull = imageWithoutCull.convert('RGB')
        invertedImg1 = invertedImg1.convert('RGB')
        final = Image.composite(invertedImg1, imageWithoutCull, diff)
        imageWithoutCull.close()
        invertedImg1.close()
        diff.close()
        imageWithCull.close()
        final.save(fileToPerformPostProcessOn)
        final.close()
        
        # from PIL import Image
        # from PIL.ImageChops import invert
        
        # image = Image.open('test.tif')
        # red, green, blue = image.split()
        # image_with_inverted_green = Image.merge('RGB', (invert(red), invert(green), blue))
        # image_with_inverted_green.save('test_inverted_green.tif')
        
        # os.remove(normalWithBackfaceCulling)
        

        bpy.context.scene.display.shading.show_backface_culling = False


# @bookmark Curvature pass
@renderPassDecorator
class RenderCurvaturePassWithWorkbench(RenderPass):
    passName = "Curvature"

    @classmethod
    def prepare_to_render(self):
        # # Switch viewport view to rendered, rather than solid or wire or whatever.
        # bpy.context.space_data.shading.type = 'RENDERED'

        # # Hides things like the 3D cursor, object selection outlines (etc).
        # bpy.context.space_data.overlay.show_overlays = False

        # # Set the render engine to workbench rather than Eevee/Cycles
        # bpy.context.scene.render.engine = 'BLENDER_WORKBENCH'

        # bpy.data.worlds
        bpy.context.scene.world = bpy.data.worlds[nameOfWorldUsedDuringPBRmapCreation]
        bpy.context.scene.world.color = (0.5, 0.5, 0.5)

        # Render properties > Lighting
        bpy.context.scene.display.shading.light = 'FLAT'



        # Render properties > Color
        bpy.context.scene.display.shading.color_type = 'SINGLE'
        bpy.context.scene.display.shading.single_color = (0.5, 0.5, 0.5)
        bpy.context.scene.display.shading.cavity_valley_factor = 2.5
        bpy.context.scene.display.shading.cavity_ridge_factor = 2.5



        # # Render properties > Options
        bpy.context.scene.display.shading.show_cavity = True
        bpy.context.scene.display.shading.cavity_type = 'WORLD'
        # bpy.context.scene.display.shading.show_backface_culling = False
        # bpy.context.scene.display.shading.show_xray = False
        # bpy.context.scene.display.shading.show_shadows = False
        # bpy.context.scene.display.shading.show_cavity = True
        # bpy.context.scene.display.shading.use_dof = False
        # bpy.context.scene.display.shading.show_object_outline = False
        # bpy.context.scene.display.shading.show_specular_highlight = True
        
@renderPassDecorator
class RenderMatIDPassWithWorkbenchViewportDisplayCol(RenderPass):
    passName = "MatID"

    @classmethod
    def prepare_to_render(self):

        # # 3D Viewport > Viewport shading (top right) > Render Pass
        # bpy.context.space_data.shading.render_pass = 'DIFFUSE_COLOR'
        
        # # Render properties > Sampling
        # bpy.context.scene.eevee.taa_samples = 1

        # Render properties > Lighting
        bpy.context.scene.display.shading.color_type = 'MATERIAL'

        # Render properties > Color
        bpy.context.scene.display.shading.light = 'FLAT'

        # Render properties > Options
        bpy.context.scene.display.shading.show_cavity = False

        # for material in bpy.data.materials:
        #     material: bpy.types.Material
        #     material.diffuse_color =  material.node_tree.nodes
        #     bpy.data.materials["Material"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.8, 0.272124, 0.414903, 1)


# @bookmark AO pass
@renderPassDecorator
class RenderAOPassWithEevee(RenderPass):
    passName = "AO"

    @classmethod
    def prepare_to_render(self):
        # Render properties > Render Engine
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'

        # Render properties > Ambient Occlusion
        bpy.context.scene.eevee.use_gtao = True
        bpy.context.scene.eevee.gtao_distance = 7
        bpy.context.scene.eevee.gtao_factor = 1.3




        # 3D Viewport > Viewport shading (top right) > Render Pass
        bpy.context.space_data.shading.render_pass = 'AO'

        
        # Render properties > Sampling
        bpy.context.scene.eevee.taa_samples = 32

@renderPassDecorator
class RenderHeightPassWithEeveeMist(RenderPass):     
    passName = "Height"

    @classmethod
    def prepare_to_render(self):
        # Render properties > Render Engine
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'

        # 3D Viewport > Viewport shading (top right) > Render Pass
        bpy.context.space_data.shading.render_pass = 'MIST'
        
        # Render properties > Sampling
        bpy.context.scene.eevee.taa_samples = 1

@renderPassDecorator
class RenderMatIDPassWithEevee(RenderPass):
    passName = "MatID"

    @classmethod
    def prepare_to_render(self):

        # 3D Viewport > Viewport shading (top right) > Render Pass
        bpy.context.space_data.shading.render_pass = 'DIFFUSE_COLOR'
        
        # Render properties > Sampling
        bpy.context.scene.eevee.taa_samples = 1

# @bookmark Transparency pass

# Supports "Alpha hashed" & "alpha clipped", blend mode, however "alpha blend"
# will appear fully transparent, which might be undesired.
@renderPassDecorator
class RenderTransparencyPassWithEeveeEnvironmentPass(RenderPass):
    passName = "Transparency"
    
    # settings = dict()
    # settings["High quality transparency"] = False

    restoreDisplayDevice = ''
    restoreSequencer = ''


    @classmethod
    def prepare_to_render(self):

        # 3D Viewport > Viewport shading (top right) > Render Pass
        bpy.context.space_data.shading.render_pass = 'ENVIRONMENT'

        # Render properties > Sampling
        # if self.settings["High quality transparency"]:
        # bpy.context.scene.eevee.taa_samples = 256
        # else:
        bpy.context.scene.eevee.taa_samples = 1
        
        # Render properties > Color
        bpy.context.scene.display.shading.single_color = (999, 999, 999)

        self.restoreDisplayDevice = bpy.context.scene.display_settings.display_device
        bpy.context.scene.display_settings.display_device = 'None'

        self.restoreSequencer = bpy.context.scene.sequencer_colorspace_settings.name
        bpy.context.scene.sequencer_colorspace_settings.name = 'Raw'


    def perform_post_process(self):
        # Inverts the alpha pass so that white means visible and black means invisible.
        bpy.context.scene.display_settings.display_device = self.restoreDisplayDevice
        bpy.context.scene.sequencer_colorspace_settings.name = self.restoreSequencer

        pathToStoreImageInIncludingFileNameAndFileExtension = pathToStoreImagesIn
        fileToPerformPostProcessOn = pathToStoreImageInIncludingFileNameAndFileExtension + self.passName + ".png"
        imageToPerformPostProcessOn = Image.open(fileToPerformPostProcessOn)
        finalImage = ImageChops.invert(imageToPerformPostProcessOn)
        imageToPerformPostProcessOn.close()
        finalImage.save(fileToPerformPostProcessOn)



# def RenderNormalFromAppendedMaterialDecorator(cls: RenderAppendedMaterialTypeRenderPass):
#     retrieveSettings(cls).enable_pass = False

# @RenderNormalFromAppendedMaterialDecorator
# @renderPassDecorator
# class RenderNormalFromAppendedMaterial(RenderAppendedMaterialTypeRenderPass):
#     passName = "normal"
#     materialToRender = 'FastPBRNormal'
#     def draw_pass_specific_ui_elements(cls, context): 
#         label_multiline(f"""Compared to rendering the normal pass with workbench, this pass has the advantage of that it totally ignores whether faces are pointing the wrong direction or not, they will always appear like as if they were pointing towards the camera, or a direction that has a maximum of a 90 degree angle from the camera. A downside of this pass is that it might not be able to replace the material of all objects if you have objects from other files linked in your blend.""",context,cls.layout)
        

###################################################################################
######################### END OF PASSES SECTION ###################################
###################################################################################






# class CustomDrawOperator(bpy.types.Operator):
#     bl_idname = "object.custom_draw"
#     bl_label = "Simple Modal Operator"

#     filepath: bpy.props.StringProperty(subtype="FILE_PATH")

#     my_float: bpy.props.FloatProperty(name="Float")
#     my_bool: bpy.props.BoolProperty(name="Toggle Option")
#     my_string: bpy.props.StringProperty(name="String Value")

#     def execute(self, context):
#         print("Test", self)
#         return {'FINISHED'}

#     def invoke(self, context, event):
#         wm = context.window_manager.invoke_props_dialog(self)
#         return wm.invoke_props_dialog(self)

# bpy.types.

# def test123(cls):
#     print(cls + "AWESOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOME")

# @bookmark Operator Base Class
class OperatorBaseClass(bpy.types.Operator, object):
    __metaclass__ = registerOperatorsDecorator # This method runs when the class is created - Edit: Appears broken?
    # Currently still calling the function as a decorator on a per child-class basis!
    bl_idname = ""
    bl_label = ""         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.





# class test(PluginBase):
#     pass

@registerOperatorsDecorator
class FastPBRBackupSettings(OperatorBaseClass):
    def execute(self, context: bpy.types.Context) -> bpy.typing.Set[str]:
        BackupPrepareAndRestore.backupSettingsAndPrepareForRender()
        return {'FINISHED'}


@registerOperatorsDecorator
class FastPBRRestoreSettings(OperatorBaseClass):
    def execute(self, context: bpy.types.Context) -> bpy.typing.Set[str]:
        BackupPrepareAndRestore.restoreSettings()
        return {'FINISHED'}

# @bookmark MatchViewportDisplayAndSurfaceBaseColor Operator

replaceSelectedObjectMaterials = 'MaterialsOnSelectedObjectsOnly'
replaceScene = 'AllMaterialsInTheCurrentScene'
replaceAll = 'AllMaterialsInTheCurrentBlend'

@settingsContainerDecorator
class OperatorSettingsContainer():
    class settings(bpy.types.PropertyGroup):
            materials_to_replace: bpy.props.EnumProperty(name = "My Property", items={(replaceSelectedObjectMaterials,replaceSelectedObjectMaterials,replaceSelectedObjectMaterials), 
                                                                        (replaceScene,replaceScene,replaceScene), 
                                                                        (replaceAll,replaceAll,replaceAll)}, default = replaceSelectedObjectMaterials) = propertyClass()




@registerOperatorsDecorator
class MatchViewportDisplayAndSurfaceBaseColor(OperatorBaseClass):

    # class settings(bpy.types.PropertyGroup):
            # materials_to_replace: bpy.props.EnumProperty(name = "My Property", items={(replaceSelectedObjectMaterials,replaceSelectedObjectMaterials,replaceSelectedObjectMaterials), 
            #                                                             (replaceScene,replaceScene,replaceScene), 
            #                                                             (replaceAll,replaceAll,replaceAll)}, default = replaceSelectedObjectMaterials)
    
    
    
    # flag_prop: bpy.props.BoolProperty(name = "Use Int")
    # dependent_prop: bpy.props.EnumProperty(name = "My Property", items={(replaceSelectedObjectMaterials,replaceSelectedObjectMaterials,replaceSelectedObjectMaterials), 
    #                                                                     (replaceScene,replaceScene,replaceScene), 
    #                                                                     (replaceAll,replaceAll,replaceAll)}, default = 'Foo')
    
    def execute(self, context):
        msg = f"dependent_prop: {retrieveSettings(OperatorSettingsContainer).materials_to_replace}"
        self.report({'INFO'}, msg)
        print(msg)

        materialsToReplace: list(bpy.types.Material) = list()
        if retrieveSettings(OperatorSettingsContainer).materials_to_replace == replaceAll:
            materialsToReplace = bpy.data.materials
        elif retrieveSettings(OperatorSettingsContainer).materials_to_replace in (replaceSelectedObjectMaterials, replaceScene):
            if retrieveSettings(OperatorSettingsContainer).materials_to_replace == replaceSelectedObjectMaterials:
                objectsToLoop = bpy.context.selected_objects
            elif retrieveSettings(OperatorSettingsContainer).materials_to_replace == replaceScene:
                objectsToLoop = bpy.context.scene.objects

            for object in objectsToLoop:
                object: bpy.types.Object
                for materialSlot in object.material_slots:
                    materialSlot: bpy.types.MaterialSlot
                    materialsToReplace.append(materialSlot.material)
        # elif self.dependent_prop == self.replaceScene:
        for material in materialsToReplace:
            material: bpy.types.Material
            if material.use_nodes:
                if material.node_tree.nodes.find("Principled BSDF") > -1:
                    material.diffuse_color = material.node_tree.nodes["Principled BSDF"].inputs[0].default_value
# bpy.data.materials["!@darkGray"].node_tree.nodes["Principled BSDF"].inputs[0].default_value
        return {'FINISHED'}
    
    def draw(self, context):
        self.layout.use_property_split = True

        row = self.layout.row()
        # row.prop(self, "flag_prop")
        
        sub = row.row()
        # sub.enabled = self.flag_prop
        sub.prop(retrieveSettings(OperatorSettingsContainer), 'materials_to_replace', text="MaterialsToReplace")
        # sub.prop(retrieveSettings(OperatorSettingsContainer), OperatorSettingsContainer.settings.materials_to_replace.__name__, text="Materials to replace: ")
        # sub.prop(self, "materials_to_replace", text="Materials to replace: ")

# Backup:

# replaceSelectedObjectMaterials = 'MaterialsOnSelectedObjectsOnly'
# replaceScene = 'AllMaterialsInTheCurrentScene'
# replaceAll = 'AllMaterialsInTheCurrentBlend'

# @settingsContainerDecorator
# @registerOperatorsDecorator
# class MatchViewportDisplayAndSurfaceBaseColor(OperatorBaseClass):

#     class settings(bpy.types.PropertyGroup):
#             materials_to_replace: bpy.props.EnumProperty(name = "My Property", items={(replaceSelectedObjectMaterials,replaceSelectedObjectMaterials,replaceSelectedObjectMaterials), 
#                                                                         (replaceScene,replaceScene,replaceScene), 
#                                                                         (replaceAll,replaceAll,replaceAll)}, default = 'Foo')
    
    
    
#     # flag_prop: bpy.props.BoolProperty(name = "Use Int")
#     # dependent_prop: bpy.props.EnumProperty(name = "My Property", items={(replaceSelectedObjectMaterials,replaceSelectedObjectMaterials,replaceSelectedObjectMaterials), 
#     #                                                                     (replaceScene,replaceScene,replaceScene), 
#     #                                                                     (replaceAll,replaceAll,replaceAll)}, default = 'Foo')
    
#     def execute(self, context):
#         msg = f"dependent_prop: {self.dependent_prop}" if self.flag_prop else "Nothing to report"
#         self.report({'INFO'}, msg)
#         print(msg)

#         materialsToReplace: list(bpy.types.Material) = list()
#         if self.dependent_prop == self.replaceAll:
#             materialsToReplace = bpy.data.materials
#         elif self.dependent_prop in (self.replaceSelectedObjectMaterials, self.replaceScene):
#             if self.dependent_prop == self.replaceSelectedObjectMaterials:
#                 objectsToLoop = bpy.context.selected_objects
#             elif self.dependent_prop == self.replaceScene:
#                 objectsToLoop = bpy.context.scene.objects

#             for object in objectsToLoop:
#                 object: bpy.types.Object
#                 for materialSlot in object.material_slots:
#                     materialSlot: bpy.types.MaterialSlot
#                     materialsToReplace.append(materialSlot.material)
#         # elif self.dependent_prop == self.replaceScene:
#         for material in materialsToReplace:
#             material: bpy.types.Material
#             if material.use_nodes:
#                 if material.node_tree.nodes.find("Principled BSDF") > -1:
#                     material.diffuse_color = material.node_tree.nodes["Principled BSDF"].inputs[0].default_value
# # bpy.data.materials["!@darkGray"].node_tree.nodes["Principled BSDF"].inputs[0].default_value
#         return {'FINISHED'}
    
#     def draw(self, context):
#         self.layout.use_property_split = True

#         row = self.layout.row()
#         row.prop(self, "flag_prop")
        
#         sub = row.row()
#         # sub.enabled = self.flag_prop
#         sub.prop(self, "dependent_prop", text="Materials to replace: ")

#### backup end



    # def execute(self, context):        # execute() is called when running the operator.
    #     pass


# MENU REFERENCE:


# import bpy

# class VIEW3D_MT_menu(bpy.types.Menu):
#     bl_label = "Test"

#     def draw(self, context):
#         self.layout.operator("mesh.primitive_monkey_add")
#         self.layout.menu("OBJECT_MT_select_submenu")

# def addmenu_callback(self, context):
#     self.layout.menu("VIEW3D_MT_menu")


# def register():
#     bpy.utils.register_class(VIEW3D_MT_menu)
#     bpy.types.VIEW3D_MT_editor_menus.append(addmenu_callback)  

# def unregister():
#     bpy.types.VIEW3D_MT_editor_menus.remove(addmenu_callback)  
#     bpy.utils.unregister_class(VIEW3D_MT_menu)


# if __name__ == "__main__":
#     register()


# import bpy



# class SubMenu(bpy.types.Menu):
#     bl_idname = "OBJECT_MT_select_submenu"
#     bl_label = "Select"

#     def draw(self, context):
#         layout = self.layout

#         # layout.operator("object.select_all", text="Select/Deselect All").action = 'TOGGLE'
#         # layout.operator("object.select_all", text="Inverse").action = 'INVERT'
#         # layout.operator("object.select_random", text="Random")

#         # # access this operator as a submenu
#         # layout.operator_menu_enum("object.select_by_type", "type", text="Select All by Type...")

#         # layout.separator()

#         # # expand each operator option into this menu
#         # layout.operator_enum("object.lamp_add", "type")

#         # layout.separator()

#         # # use existing memu
#         self.layout.menu("VIEW3D_MT_transform")


# bpy.utils.register_class(SubMenu)

# # test call to display immediately.
# bpy.ops.wm.call_menu(name="OBJECT_MT_select_submenu")

# 

# bpy.types.VIEW3D_MT_editor_menus.append(addmenu_callback) 

# MENU REFERENCE END

###############################
# @bookmark Menus and headers #
###############################
# menusToRegister = dict()

# @registerOperatorsDecorator
# # class Fast(FastToolBarPanelBaseClass, bpy.types.Panel):
# class Fast(bpy.types.Menu):
#     menusAndHeadersToRegisterUnder = list()
#     menusAndHeadersToRegisterUnder.append('VIEW3D_MT_editor_menus')
#     # bl_space_type = "VIEW_3D"
#     # bl_region_type = "NAVIGATION_BAR"
#     # bl_category = "Object"
#     # bl_region_type = "TOOLS" # This actually puts the panel
#     # on the left side of the 3D viewport! Since the left panel is usually very
#     # narrow however, I dont recommend putting it here.
#     def draw(self, context: bpy.types.Context) -> None:
#         self.layout.row().prop(retrieveOperatorFromCls(MatchViewportDisplayAndSurfaceBaseColor))


# def registerMenusDecorator(cls: FastMenuBaseClass):
#     # registerOperatorsDecorator(cls)
#     registerClassGivebl_labelAndbl_idnameWithUnderscore(cls)
#     # menusToRegister.append((cls, cls.menusAndHeadersToRegisterUnder))
#     menusToRegister[cls] = cls.menusAndHeadersToRegisterUnder



# # def addmenu_callback(self, context):
# #     self.layout.menu("VIEW3D_MT_menu")



# class FastMenuBaseClass(bpy.types.Menu):
#     # pass
#     menusAndHeadersToRegisterUnder = list()
#     menusAndHeadersToRegisterUnder.append('VIEW3D_MT_editor_menus')
#     # menusAndHeadersToRegisterUnder.append(retrieveOperatorFromCls(Fast).replace('.', '_'))

# @registerMenusDecorator
# class Materials(FastMenuBaseClass):
#     def draw(self, context: bpy.types.Context) -> None:
#         self.layout.operator(retrieveOperatorFromCls(MatchViewportDisplayAndSurfaceBaseColor))

#################################
# # # Menus and headers END # # #
#################################

# @bookmark Fast PBR Viewport Render opeartor
@registerOperatorsDecorator
class FastPBRViewportRender(OperatorBaseClass):
    
    # print("Auto generated bl_idname based on the class name!!" + bl_idname)
    # bl_description = """fast pbr viewport render"""      # Use this as a tooltip for menu items and buttons.
    # bl_idname = "object.fast_pbr_viewport_render"        # Unique identifier for buttons and menu items to reference.
    # bl_idname = "fast_pbr.fast_pbr_viewport_render"        # Unique identifier for buttons and menu items to reference.
    # bl_label = "Fast PBR viewport render"         # Display name in the interface.
    # bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.



    def test(self):
        print("wot")
    def execute(self, context):        # execute() is called when running the operator.
        #os.system("cls")
        # The original script

        # print(context.window_manager.invoke_props_dialog(self.test))
        # for renderPassClass in 

        # renderNormalPassWithWorkbench = RenderNormalPassWithWorkbench()
        # renderNormalPassWithWorkbench.prepare_render_and_save()
        
        # print("HERE:",retrieveOperatorFromCls(FastPBRBackupSettings))
        BackupPrepareAndRestore.backupSettingsAndPrepareForRender()

        # bpy.ops.wm.append(
        #     filepath="cube.blend",
        #     directory="/home/lucas/Desktop/cube.blend\\Object\\",
        #     filename="Cube")
        
##################################################
        # import pathlib
        # pathToAddonDirectory = str(pathlib.Path(__file__).parent.resolve())
        # nameOfAssetsFileWithoutPath = 'FastPBRAssets.blend'
        # pathToAssetsFile = pathToAddonDirectory + '/' + nameOfAssetsFileWithoutPath
        # # 
        # def appendAssetFromAssetsBlendFile(dataBlockToAppend: str, blendFileDataCategory: str):
        #     """
        #     dataBlockToAppend is the name of the object/material/whatever you want to append.

        #     blendFileDataCategory is the type of data you want to append, if you go into the outliner > display mode > Data API you will see all these categories. Example values: "Material", "Object", "Node Groups" (etc). For some reason, the "s" at the end of some categories displayed in that list is not supposed to be included, which is rather confusing :)
        #     """
        #     bpy.ops.wm.append(filename=dataBlockToAppend, directory=pathToAssetsFile + '\\' + blendFileDataCategory + '\\')
                
        #     print("filepath:", nameOfAssetsFileWithoutPath)
        #     print("directory:", pathToAssetsFile + '\\' + blendFileDataCategory)
        #     print("filename:", dataBlockToAppend)
                    
        # pathToNormalAssetsFile = pathToAddonDirectory + '/' + 'FastPBRAssets.blend'
        # print("File path:", pathlib.Path(__file__).parent.resolve())
        
        # if bpy.data.materials.find('FastPBRNormal') < 0:
        #     appendAssetFromAssetsBlendFile('FastPBRNormal', 'Material')
        # for object in bpy.data.objects:
        #     object: bpy.types.Object
        #     for materialSlot in object.material_slots:
        #         materialSlot: bpy.types.MaterialSlot
        #         # materialSlot.link = 'FastPBRNormal'
        #         materialSlot.material = bpy.data.materials.get('FastPBRNormal')
                # materialSlot
################################################

        # print("File path:", pathlib.Path(__file__).parent.resolve())
        # bpy.ops.wm.append(
        #     filepath="cube.blend",
        #     directory=pathToAssetsFile,
        #     filename="Cube")
        # bpy.ops.wm.append(
        #     filepath="cube.blend",
        #     directory="C:/Program Files/Blender Foundation/blender-3.0.0-alpha+master.2b64b4d90d67-windows.amd64-release/3.0/scripts/addons/fast_pbr_viewport_render/FastPBRAssets.blend\\Object",
        #     filename="Cube")
        # return {'FINISHED'}     
        
        # print("IMPORTANTEEE" + getGlobalAddonProperties().target_directory)

        for renderPass in renderPasses:
            if not renderPass == RenderPass:
                renderPass: RenderPass
                
                renderPass.prepare_render_and_save()
                print(str(renderPass) + "Woohoo") # Success

            # renderPass.
        # print("Weird?")
        # for key, value in retrieveSettings(GlobalSettings).file_path_replacement_keys_collection_property:
        #     print(f"HEEEY, key: {key} value: {value}")  
        # for index in range(len(retrieveSettings(GlobalSettings).file_path_replacement_keys_collection_property)-1):
        #     print("Key: " + bpy.types.CollectionProperty().keys()[index]) 
        #     print("Value: " + bpy.types.CollectionProperty().get[index])

        replacementDictionary = dict()

        for item in retrieveSettings(GlobalSettings).file_path_replacement_keys_collection_property:
            # print(str(item.value) + "item")
            replacementDictionary[item.key] = item.value

        print(f"""
replacementDictionary: {replacementDictionary}
pathToStoreImagesIn: {pathToStoreImagesIn}
retrieveSettings(GlobalSettings).export_file_path: {retrieveSettings(GlobalSettings).export_file_path}""")

        moveImages(pathToStoreImagesIn, retrieveSettings(GlobalSettings).export_file_path, replacementDictionary)

        # os.system(f'explorer "{targetFolder}"')
        # print(f'FINAL CMD: explorer "{targetFolder}"')


        # moveImages(pathToStoreImagesIn, getGlobalAddonProperties().target_directory, replacementDictionary)

        BackupPrepareAndRestore.restoreSettings()

        # bpy.props.CollectionProperty
        # retrieveSettings(GlobalSettings).file_path_replacement_keys_collection_property


        # @todo Feed path replacement keys to moveImages. Figure out how to extract stuff from the damn collectionProperty.

#
        # for file in os.listdir(pathToStoreImagesIn):
        #     print(file)

        # test.prepare_render_and_save()


        #####################
        # Render normal map #
        #####################

        # bpy.context.scene.render.engine = 'BLENDER_WORKBENCH'
        # bpy.context.scene.display.shading.light = 'MATCAP'
        # bpy.context.scene.display.shading.studio_light = 'check_normal+y.exr'
        # bpy.context.scene.display.shading.color_type = 'SINGLE'

        # # Color   
        # bpy.context.scene.display.shading.single_color = (1, 1, 1)


        # # Options
        # bpy.context.scene.display.shading.show_object_outline = False
        # bpy.context.scene.display.shading.use_dof = False
        # bpy.context.scene.display.shading.show_cavity = False
        # bpy.context.scene.display.shading.show_shadows = False
        # bpy.context.scene.display.shading.show_xray = False
        # bpy.context.scene.display.shading.show_backface_culling = False

        
        # bpy.context.scene.display.shading.show_backface_culling = False





        # for area in bpy.context.screen.areas:
        #     if area.type == 'VIEW_3D':
        #         if bpy.context.active_object.mode == 'EDIT':
        #             area.spaces[0].shading.render_pass = 'NORMAL'
   #
  #  This loop was supposed to allow the user to select multiple objects and set the modifier collection based on 
   # what is set to the first newBoolean, however it seems layout.prop() cant delay the execution in the script
   # hence making this code run before the user have selected a collection. Not sure how to get by this.
    #    for object in bpy.context.selected_objects:
     #       newBoolean_ = object.modifiers.new(type='BOOLEAN', name='Boolean')
      #      newBoolean_.operand_type = 'COLLECTION'
       #     newBoolean_.solver = 'FAST'
        #    newBoolean_.collection = newBoolean.collection

        return {'FINISHED'}            # Lets Blender know the operator finished successfully.

# test = "wa"
# test.rfind()

# class CreateFastCollectionBoolean(bpy.types.Operator):
#     """Fast collection booleans"""      # Use this as a tooltip for menu items and buttons.
#     bl_idname = "object.create_fast_collection_boolean"        # Unique identifier for buttons and menu items to reference.
#     bl_label = "Create fast collection boolean"         # Display name in the interface.
#     bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

#     def execute(self, context):        # execute() is called when running the operator.
#         # for object in bpy.context.active_object.modifiers:
#         #     print("h")
#         #     object.name
#         # for property in bpy.context.active_object.modifiers[0].bl_rna.properties:
#         #     print(property)

#         # print(bpy.context.active_object.modifiers[0].type)


#         # for object in bpy.context.active_object.modifiers[0].name

    
#         collectionBooleansIndex = []
#         currentIndex = -1
#         modifier: bpy.types.Modifier
#         for modifier in bpy.context.active_object.modifiers:
#             currentIndex += 1
#             if modifier.type == "BOOLEAN":
#                 print("EQUALS BOOLEAN")
#             else:
#                 print("Not BOOLEAN")
#             print(modifier.type)
#             if modifier.operand_type == "COLLECTION":
#                 print("COLLECTION OPERAND TYPE")
#             else:
#                 print("Not COLLECTION OPERAND TYPE")


#             if modifier.type == "BOOLEAN" and modifier.operand_type == "COLLECTION":
#                 collectionBooleansIndex.append(currentIndex)

        


#         #os.system("cls")
#         # The original script
#         newBoolean = bpy.context.active_object.modifiers.new(type='BOOLEAN', name='Boolean')
#         newBoolean.operand_type = 'COLLECTION'
#         newBoolean.solver = 'FAST'
#         def draw_func(self, context):
#             self.layout.prop(newBoolean, "collection", text="")
#         bpy.context.window_manager.popup_menu(draw_func, title="Select cutter collection", icon='MOD_BOOLEAN')
#    #
#   #  This loop was supposed to allow the user to select multiple objects and set the modifier collection based on 
#    # what is set to the first newBoolean, however it seems layout.prop() cant delay the execution in the script
#    # hence making this code run before the user have selected a collection. Not sure how to get by this.
#     #    for object in bpy.context.selected_objects:
#      #       newBoolean_ = object.modifiers.new(type='BOOLEAN', name='Boolean')
#       #      newBoolean_.operand_type = 'COLLECTION'
#        #     newBoolean_.solver = 'FAST'
#         #    newBoolean_.collection = newBoolean.collection

#         return {'FINISHED'}            # Lets Blender know the operator finished successfully.

# @bookmark property group
# @registerClassToBPYDecorator
# @registerOperatorsDecorator

# @registerClassToBPYDecorator
# class PropertyGrouBaseClass(bpy.types.PropertyGroup,object):
#     __metaclass__ = registerClassToBPYDecorator


class PerSceneAddonProperties(bpy.types.PropertyGroup):
    file_path: bpy.props.StringProperty(name="File path",
                                        description="Some elaborate description",
                                        default="",
                                        maxlen=1024,
                                        subtype="FILE_PATH")

# @registerOperatorsDecorator # The decorator appears unable to register PropertyGroups for some reason!!
class FastPBR(PerSceneAddonProperties): 
    pass                        
classesToRegister.append(FastPBR)

def getNameOfVariable(variable):
    return f'{variable=}'.split('=')[0]
def getNameOfVariableAndReplaceUnderscoreWithSpace(variable):
    return getNameOfVariable(variable).replace("_", " ")

class GlobalAddonProperties():
    # target_directory: str = ""
    target_directory: bpy.props.StringProperty("Target Directory",
                                        description="Some elaborate description",
                                        default="",
                                        maxlen=2048,
                                        subtype="FILE_PATH")



class AddonPreferencesUI():
    def draw(self, context):
        self.layout.label(text=f"Welcome to {addonName}!")

def getGlobalAddonProperties():
    return bpy.context.preferences.addons[__name__].preferences

class FastPBRPreferences(bpy.types.AddonPreferences, GlobalAddonProperties, AddonPreferencesUI):
    bl_idname = __name__
    
classesToRegister.append(FastPBRPreferences)

# @bookmark register


# @TODO automatic system for menu registration
# # This loop generates addmenu callback functions necessary for BPY to register a menu to an existing menu or header.
# # These  functions are later fed inside register()
# for menuClass in menusToRegister:
#     exec(f'''def {retrieveOperatorFromCls(menuClass).replace('.', '_')}_addmenu(self, context):
#     self.layout.menu({retrieveOperatorFromCls(menuClass)})''')




def register():
    # bpy.utils.register_class(FastPBRViewportRender)
    os.system("cls")
    print(putTextInBox(f"Registering {addonName}"))
    # print("Globals:" + str(globals()))
    
    # print(__name__)
    alreadyRegistered = list()

    for cls in classesToRegister:
        if not cls in alreadyRegistered:
            alreadyRegistered.append(cls)
            print("Registering operator:", str(cls))
            bpy.utils.register_class(cls)

    # bpy.context.scene.fast_pbr.render_pass.file_path = RenderNormalPassWithWorkbench.settings.file_path


    # bpy.types.Scene.fast_pbr=bpy.types.PointerProperty(type=(RenderNormalPassWithWorkbench.settings))

    # bpy.types.Scene.fast_pbr = bpy.props.PointerProperty(type=FastPBR)

    for settingsPropertyGroupParent in settingsPropertyGroupParents:
        
        print(f'''Adding settingsPropertyGroup: "{settingsPropertyGroupParent.__name__}"  to the scene as "bpy.types.Scene.{PascalCaseTo_snake_case(addonNameShort + '_' + settingsPropertyGroupParent.__name__)}"''')
        # renderPass: RenderPass = RenderPass

        renderPassSettingsVariables = list()
        # for variableName in renderPass.settings.__dict__:
        # for variableName in dir(renderPass.settings):
        # for variableName in renderPass.settings.items(renderPass.settings):
        # for variableName in [attr for attr in dir(renderPass.settings) if not callable(getattr(renderPass.settings, attr)) and not attr.startswith("__")]:
        for variableName in settingsPropertyGroupParent.settings.__annotations__.keys():
            print("variableName: " + variableName)
            if not variableName[0] == '_':
                renderPassSettingsVariables.append(variableName)
        
        for variableName in renderPassSettingsVariables:
            # exec(f"bpy.context.scene.{PascalCaseTo_snake_case(addonNameShort + '.' + renderPass.__name__)}.{variableName} = {renderPass.__name__}.settings.{variableName}")
            # print(f"bpy.types.Scene.{PascalCaseTo_snake_case(addonNameShort + '_' + renderPass.__name__)} = {renderPass.__name__}.settings.{variableName}")
            # exec(f"bpy.types.Scene.{PascalCaseTo_snake_case(addonNameShort + '_' + renderPass.__name__)} = {renderPass.__name__}.settings.{variableName}")


            
            print(f"bpy.types.Scene.{PascalCaseTo_snake_case(addonNameShort + '_' + settingsPropertyGroupParent.__name__)} = bpy.props.PointerProperty(type={settingsPropertyGroupParent.__name__}.settings)")
            exec(f"bpy.types.Scene.{PascalCaseTo_snake_case(addonNameShort + '_' + settingsPropertyGroupParent.__name__)} = bpy.props.PointerProperty(type={settingsPropertyGroupParent.__name__}.settings)")
            # bpy.types.Scene.fast_pbr_render_normal_pass_with_workbench = bpy.props.PointerProperty(type=FastPBR)



            # exec(f"{renderPass.__name__}.retrieveSettings().{variableName} = {renderPass.__name__}.settings.{variableName}")

            # exec(f"""print("in my ass{renderPass.__name__}")""")
            # Emulates something like:
            # bpy.context.scene.fast_pbr.render_pass.file_path = renderPass.settings.file_path



    # bpy.utils.register_tool(MyTool, after={"builtin.scale_cage"}, separator=True, group=True)
    # bpy.utils.register_tool(MyOtherTool, after={MyTool.bl_idname})


    # Instead of:
    # bpy.types.Scene.fast_pbr = bpy.props.PointerProperty(type=FastPBR)
    # Is there something like:
    # createPropertyGroupObject("bpy.types.Scene.fast_pbr", bpy.props.PointerProperty(type=FastPBR)) # Psuedo code for doing the same thing.
    # Basically I want to be able to put it in a loop iterating over a list of classes.
    
    # @TODO automatic system for menu registration ###### Start
    # # Append menus to existing menus in the order that there cooresponding classes are declared in the addon.
    # print(f"menusToRegister: {menusToRegister}")
    # for menuClass in menusToRegister:
    #     print(f"menuClass: {menusToRegister}")
    #     print(f"menuClass: {menusToRegister}")
    #     for menuToRegisterMenuClassUnder in menusToRegister[menuClass]:
    #         print(f"menusToRegister[menuClass]: {menusToRegister[menuClass]}")
    #         print(f"menuToRegisterMenuClassUnder: {menuToRegisterMenuClassUnder}")
    #         menuToRegisterMenuClassUnder: str()
    #         exec(f"bpy.types.{menuToRegisterMenuClassUnder}.append({retrieveOperatorFromCls(menuClass).replace('.', '_')}_addmenu)")
    #     # bpy.types.VIEW3D_MT_editor_menus.append(addmenu_callback)
    ########### End



    print(putTextInBox(f"Registration complete"))





def unregister():
    # bpy.utils.unregister_class(FastPBRViewportRender)
    
    print(putTextInBox(f"Unregistering {addonName}"))


    alreadyRegistered = list()

    for cls in classesToRegister:
        if not cls in alreadyRegistered:
            alreadyRegistered.append(cls)
            print("Unregistering operator:", str(cls))
            bpy.utils.unregister_class(cls)

    # for cls in classesToRegister:
    #     print("Unregistering operator:", str(cls))
    #     bpy.utils.unregister_class(cls)

    # bpy.utils.unregister_tool(MyTool)
    # bpy.utils.unregister_tool(MyOtherTool)

    # bpy.utils.unregister_class(FastPBR) 
    # del bpy.types.Scene.fast_pbr


    # for settingsPropertyGroupParent in settingsPropertyGroupParents:
        
    #     print(f'''Removing settingsPropertyGroup: "{settingsPropertyGroupParent.__name__}" from the scene as "bpy.types.Scene.{PascalCaseTo_snake_case(addonNameShort + '_' + settingsPropertyGroupParent.__name__)}"''')

    #     renderPassSettingsVariables = list()
    #     for variableName in settingsPropertyGroupParent.settings.__annotations__.keys():
    #         print("variableName: " + variableName)
    #         if not variableName[0] == '_':
    #             renderPassSettingsVariables.append(variableName)
        
    #     for variableName in renderPassSettingsVariables:
    #         toExec = f"del bpy.types.Scene.{PascalCaseTo_snake_case(addonNameShort + '_' + settingsPropertyGroupParent.__name__)}"
    #         print("EXEC -> " + toExec)
    #         exec(toExec)



    print(putTextInBox(f"Unregistration complete"))







# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()