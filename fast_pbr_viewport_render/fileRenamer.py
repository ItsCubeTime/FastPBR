import shutil
import os
import glob
print()

from PIL import Image

import time

# shutil.
def is_locked(filepath):
    locked = None
    file_object = None
    if os.path.exists(filepath):
        try:
            buffer_size = 8
            # Opening file in append mode and read the first 8 characters.
            file_object = open(filepath, 'a', buffer_size)
            if file_object:
                locked = False
        except IOError as message:
            locked = True
        finally:
            if file_object:
                file_object.close()
    return locked

import errno, os

# Sadly, Python fails to provide the following magic number for us.
ERROR_INVALID_NAME = 123

def is_pathname_valid(pathname: str) -> bool:
    '''
    `True` if the passed pathname is a valid pathname for the current OS;
    `False` otherwise.
    '''
    # If this pathname is either not a string or is but is empty, this pathname
    # is invalid.
    try:
        if not isinstance(pathname, str) or not pathname:
            return False

        # Strip this pathname's Windows-specific drive specifier (e.g., `C:\`)
        # if any. Since Windows prohibits path components from containing `:`
        # characters, failing to strip this `:`-suffixed prefix would
        # erroneously invalidate all valid absolute Windows pathnames.
        _, pathname = os.path.splitdrive(pathname)

        # Directory guaranteed to exist. If the current OS is Windows, this is
        # the drive to which Windows was installed (e.g., the "%HOMEDRIVE%"
        # environment variable); else, the typical root directory.
        root_dirname = os.environ.get('HOMEDRIVE', 'C:') \
            if os.sys.platform == 'win32' else os.path.sep
        assert os.path.isdir(root_dirname)   # ...Murphy and her ironclad Law

        # Append a path separator to this directory if needed.
        root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep

        # Test whether each path component split from this pathname is valid or
        # not, ignoring non-existent and non-readable path components.
        for pathname_part in pathname.split(os.path.sep):
            try:
                os.lstat(root_dirname + pathname_part)
            # If an OS-specific exception is raised, its error code
            # indicates whether this pathname is valid or not. Unless this
            # is the case, this exception implies an ignorable kernel or
            # filesystem complaint (e.g., path not found or inaccessible).
            #
            # Only the following exceptions indicate invalid pathnames:
            #
            # * Instances of the Windows-specific "WindowsError" class
            #   defining the "winerror" attribute whose value is
            #   "ERROR_INVALID_NAME". Under Windows, "winerror" is more
            #   fine-grained and hence useful than the generic "errno"
            #   attribute. When a too-long pathname is passed, for example,
            #   "errno" is "ENOENT" (i.e., no such file or directory) rather
            #   than "ENAMETOOLONG" (i.e., file name too long).
            # * Instances of the cross-platform "OSError" class defining the
            #   generic "errno" attribute whose value is either:
            #   * Under most POSIX-compatible OSes, "ENAMETOOLONG".
            #   * Under some edge-case OSes (e.g., SunOS, *BSD), "ERANGE".
            except OSError as exc:
                if hasattr(exc, 'winerror'):
                    if exc.winerror == ERROR_INVALID_NAME:
                        return False
                elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                    return False
    # If a "TypeError" exception was raised, it almost certainly has the
    # error message "embedded NUL character" indicating an invalid pathname.
    except TypeError as exc:
        return False
    # If no exception was raised, all path components and hence this
    # pathname itself are valid. (Praise be to the curmudgeonly python.)
    else:
        return True
    # If any other exception was raised, this is an unrelated fatal issue
    # (e.g., a bug). Permit this exception to unwind the call stack.
    #
    # Did we mention this should be shipped with Python already?

def wait_for_file(filepath):
    wait_time = 1
    while is_locked(filepath):
        print("File lock detected!")
        time.sleep(wait_time)
import bpy
def moveImages(sourceDirectory, targetDirectory, replacementDictionary, removeOriginalFiles = True):
    # sourceDirectory = "C:\FastPBRViewportRender"

    fullPathToDesktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') 
    fullPathToUserHomePath = os.path.join(os.path.expanduser('~')) 

    
    replacementDictionary["fullPathToDesktop"] = fullPathToDesktop
    replacementDictionary["fullPathToUserHomePath"] = fullPathToUserHomePath





    if isinstance(replacementDictionary, bpy.types.CollectionProperty):
        print("ReplacementDictionary is of type CollectionProperty")
        
        replacementDictionaryTemp = dict()
        for item in replacementDictionary:
            # replacementDictionaryTemp[str(key)] = str(replacementDictionary[key])
            replacementDictionaryTemp[item.key] = item.value
        replacementDictionary = replacementDictionaryTemp
        print(replacementDictionary)


    sourceDirectory = sourceDirectory.replace('\\', '/')
    if not sourceDirectory[-1] == '/':
        sourceDirectory = sourceDirectory + '/'


    # replacementDictionary = {"name": "myFancyName", "var1Key": "var1Value"}


    # targetDirectory = r"C:/testTarget/{name}/FromFastPBR/{name}{imageSizeShort}_{fileNameWithExtension}"
    targetDirectory = targetDirectory.replace('\\', '/')
    sourceDirectory = sourceDirectory.replace('\\', '/')
    # if not targetDirectory[-1] == '/':
    #     targetDirectory = targetDirectory + '/'

    from os import walk

    # f = []
    # for (dirpath, dirnames, filenames) in walk(directory):
    #     print(f"dirpath: {dirpath} dirnames: {dirnames} filenames: {filenames} ")



    # f = []

    # walkOut = walk(directory)
    # for i in range(5):
    #     # print(walk(directory)[0])
    #     print(walkOut[0])
    #     # print(f"dirpath: {dirpath} dirnames: {dirnames} filenames: {filenames} ")


    sourceDirectory

    for replaceFromWithoutBrackets in replacementDictionary:
        replaceFrom = '{' + replaceFromWithoutBrackets + '}'
        replaceTo = replacementDictionary[replaceFromWithoutBrackets]
        while replaceFrom in sourceDirectory:
            sourceDirectory = sourceDirectory.replace(replaceFrom, str(replaceTo))

    if not os.path.exists(sourceDirectory):
        os.makedirs(sourceDirectory)

    # if sourceDirectory[-1] == '/':
    #     sourceDirectory = sourceDirectory [:-1]

    files = os.listdir(sourceDirectory)
    didWeFindAnyFilesInSourceDir = False
    print(f"files: {files}")
    for fileNameWithExtension in files:
        didWeFindAnyFilesInSourceDir = True
        print("fileNameWithExtension: " + fileNameWithExtension)

        fileNameWithoutExtension = fileNameWithExtension.split('.')[0]
        fileExtensionWithoutDot = fileNameWithExtension.split('.')[1]
        fileWithPathAndExtension = sourceDirectory + fileNameWithExtension
        wait_for_file(fileWithPathAndExtension)
        try:
            im = Image.open(fileWithPathAndExtension)
        except IOError as ErrorMessage:
            print(f"""
    fastPBR: We believe we just detected non-image in the directory that we're moving the images from
    Skipping this file (or possibly directory) and moving on to the next:
        {fileWithPathAndExtension}
    Error message by PIL:
        {ErrorMessage}
    
    Otherwise the images might be broken. PIL cannot open them non the less.""")
            continue

        imageWidth, imageHeight = im.size
        imageSizeInPixels = 0
        if imageWidth > imageHeight:
            imageSizeInPixels = imageWidth
        else:
            imageSizeInPixels = imageHeight
        im.close()

        imageSizeShort = ''
        if imageSizeInPixels == 65536: # No, this is not excessive at all
            imageSizeShort = '64K'
        if imageSizeInPixels == 32768:
            imageSizeShort = '32K'
        if imageSizeInPixels == 16384:
            imageSizeShort = '16K'
        if imageSizeInPixels == 8192:
            imageSizeShort = '8K'
        if imageSizeInPixels == 4096:
            imageSizeShort = '4K'
        elif imageSizeInPixels == 2048:
            imageSizeShort = '2K'
        elif imageSizeInPixels == 1024:
            imageSizeShort = '1K'
        else:
            imageSizeShort = str(imageSizeInPixels) + 'PX'

        targetDirectory: str
        sourceDirectory: str

        if sourceDirectory[-1] == '/':
            sourceDirectoryWithoutEndingSlash = sourceDirectory[:-1]
        else:
            sourceDirectoryWithoutEndingSlash = sourceDirectory
        
        sourceDirectoryTopLevelFolderName = sourceDirectoryWithoutEndingSlash[sourceDirectoryWithoutEndingSlash.rfind('/'):]


        replacementDictionary["imageSizeShort"] = imageSizeShort
        replacementDictionary["imageWidth"] = imageWidth
        replacementDictionary["imageHeight"] = imageHeight
        replacementDictionary["imageSizeInPixels"] = imageSizeInPixels
        replacementDictionary["fileNameWithExtension"] = fileNameWithExtension
        replacementDictionary["fileNameWithoutExtension"] = fileNameWithoutExtension
        replacementDictionary["fileExtensionWithoutDot"] = fileExtensionWithoutDot
        replacementDictionary["fileWithPathAndExtension"] = fileWithPathAndExtension
        replacementDictionary["sourceDirectoryTopLevelFolderName"] = sourceDirectoryTopLevelFolderName
        replacementDictionary["sourceDirectory"] = sourceDirectory





        preparedTargetDirectoryAndFileNameWithExtension = targetDirectory
        # preparedTargetDirectoryAndFileNameWithExtension = targetDirectory + '/' + 

        for replaceFromWithoutBrackets in replacementDictionary:
            replaceFrom = '{' + replaceFromWithoutBrackets + '}'
            replaceTo = replacementDictionary[replaceFromWithoutBrackets]
            while replaceFrom in preparedTargetDirectoryAndFileNameWithExtension:
                preparedTargetDirectoryAndFileNameWithExtension = preparedTargetDirectoryAndFileNameWithExtension.replace(replaceFrom, str(replaceTo))
                # print(targetDirectory, "--", replaceFrom, "--", replaceTo)
        if not targetDirectory.__contains__('.'):
            ShowMessageBox("The target directory must include the file name and its extension!", "Fast PBR", 'ERROR')
            return {'FINISHED'}


        print(f"""{fileNameWithExtension}:
        fileNameWithoutExtension: {fileNameWithoutExtension}
        fileExtension: {fileExtensionWithoutDot}
        fileWithPathAndExtension: {fileWithPathAndExtension}
        preparedTargetDirectory: {preparedTargetDirectoryAndFileNameWithExtension}
        sourceDirectoryTopLevelFolderName: {sourceDirectoryTopLevelFolderName}
        sourceDirectory: {sourceDirectory}""")
        # print()
        preparedTargetDirectoryAndFileNameWithExtension: str
        # preparedTargetDirectoryWithoutFile = '/'.join(preparedTargetDirectoryAndFileNameWithExtension.split('/')[0:-1])
        preparedTargetDirectoryWithoutFile = preparedTargetDirectoryAndFileNameWithExtension[:preparedTargetDirectoryAndFileNameWithExtension.rfind('/')]
        # if not is_pathname_valid(preparedTargetDirectoryAndFileNameWithExtension):
        #     print("The destination path appears to be invalid:\n  " + str(preparedTargetDirectoryAndFileNameWithExtension))
        #     return
        if not os.path.exists(preparedTargetDirectoryWithoutFile):
            os.makedirs(preparedTargetDirectoryWithoutFile)
        shutil.copy2(fileWithPathAndExtension, preparedTargetDirectoryAndFileNameWithExtension)


        if removeOriginalFiles:
            os.remove(fileWithPathAndExtension)
    if not didWeFindAnyFilesInSourceDir:
        ErrorMsg = f'''There are no images in your source path! The source path we tried reading was: "{sourceDirectory}"'''
        ShowMessageBox(ErrorMsg, "Error", 'ERROR')
        return {'FINISHED'}
    else: 
        ShowMessageBox("Your images are now in the destination folder!", "Fast PBR", 'INFO')

    pathForExplorer = preparedTargetDirectoryWithoutFile.replace('/', '\\')
    os.system(f'explorer "{pathForExplorer}"')
    print(f'Opening explorer -> explorer "{pathForExplorer}"')
    
    return {'FINISHED'}
    # os.rename(r'C:\Users\Administrator.SHAREPOINTSKY\Desktop\Work\name.txt',r'C:\Users\Administrator.SHAREPOINTSKY\Desktop\Newfolder\details.txt' )

def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)
        
        print(message)
        return {'FINISHED'}

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

# moveImages("C:\FastPBRViewportRender", r"C:/testTarget/{name}/FromFastPBR/{name}{imageSizeShort}_{fileNameWithExtension}")




    # break
# for file in directory
#     shutil.move(file, '/home/user/Documents/useful_name.txt')