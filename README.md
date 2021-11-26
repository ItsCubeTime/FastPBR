![fastPBRBanner](https://user-images.githubusercontent.com/20190653/143656184-ede0ab79-f67a-499b-858c-92e593377941.jpg)
# FastPBR
Fast PBR Viewport Render is a tool that lets you fetch curvature, AO, normal maps, transparency, matID and height from the camera youre currently looking through or directly from your viewport. It uses Blenders "Render viewport" operator which renders pretty much exactly what you see on screen or what the camera you are looking through currently has within frame. Therefore its extremely flexible as "what you see is what you get" and as you can use it ANYWHERE to render ANY sort of geometry or scene. It works by modifying your render settings and renderer (it uses Eevee and workbench for maximum performance), it can render out several 4K maps in the matter of seconds, making it versatile and useable for projects where you need to do a lot of rendering (and hence cant afford any time lost for waiting). It also comes equipped with a flexible, configurable and automatic file naming and folder hierarchy system that lets you move and name your images wherever you want based on custom &amp; automatically generated variables that describes your images.

# Quick demo video

https://user-images.githubusercontent.com/20190653/136704470-e3d3a362-9d9f-48e7-8a6a-69f4d155d6db.mp4
The resulting image created in the video ended up looking like so once combined with some smart materials in "Quixel Mixer" afterwards:
https://user-images.githubusercontent.com/20190653/136704479-869414bf-1a4b-440c-bd17-36b90903a5ad.jpg


# Install instructions

1. [Download](https://github.com/ItsCubeTime/FastPBR/releases) and install the addon .zip file like usual (via Top Panel > Edit > Preferences > Add-ons > Install > select the zip).

2. You should now see the dedicated "Fast PBR Viewpot Render" panel in In "your 3D viewport > Left side Bar/foldout panel (N is the default hotkey to open/close) > Fast > Fast PBR".

4. Optional step if your normal matcap doesnt install automatically: Download the FastPBRNormalMatCap.exr attached in any of the [releases](https://github.com/ItsCubeTime/FastPBR/releases) (as of 1.2.1 and up the exr file is bundled as a part of the zip file for convenience) and install it as a matCap in Blender (& make sure you dont rename it, the script utelizes the matcap to generate the normal maps):
![image](https://user-images.githubusercontent.com/20190653/136703921-1df20cef-71d8-4ca2-af3f-72d43ecad2f3.png)

# Usage

1. Choose a destination path, note that this path has to include the file name itself and the file extension. Only png is supposed at the time being, so make sure that it ends with png.
2. Configure the render passes you would like to use by toggling the checkboxes, more settings might become available in there foldout panels on a later time.
3. Choose the resolution by setting your camera resolution like usual in Properties > Output Properties.
4. Save your file for safety (The addon modifies your render settings and later reverts them, but if the script fails to reach the end due to a fatal error (which could occur if the Blender version you're using is not 100% compatable) it might not get a chance to restore the settings. If that happens however, you should be able to hit ctrl Z on your keyboard to revert the settings yourself as the addon automatically sets up a restore state to go back to.
5. Hit the top button "Fast PBR Viewport Render" to render out your maps, once the operation is complete you will see a pop-up message appear at your cursor as well as that Windows file explorer will automatically open up the directory that the images has been created in for you.

To find out more about each button and property in the UI, you can hover over it to get a short decsription:
![image](https://user-images.githubusercontent.com/20190653/136705600-442c0aa1-3f48-4595-860d-9d6a7ec426e6.png)

# Overview
![image](https://user-images.githubusercontent.com/20190653/143656380-2e4c28b8-c64d-47ba-bd23-d3e613b3d0ec.png)
# Contributing

Anyone is welcome to contribute, the addon is 100% pure Python 3.

# Troubleshooting

If you encounter any issues, dont hesitate to open up an issue ticket here on Github and I will do my best to assist. <3 Also dont shy away from digging in the code yourself if you believe you can figure out whats happening in the event of an unexpected Python error or any sort of unexpected behaviour.

Also make sure to read the below section "Known issues"

# Known issues

1. The transparency pass is inverted - still wip.
2. The height doesnt utelize the full 0-1 range as its utelizing Eevees mist, also wip.

# Things I want to add

1. Support for normal maps that are texture based.
2. Support for baking geometry with inverted normals without it affecting the result of the baked texture emitted by Fast PBR.
3. Better height maps.
4. A grid visualizer that lets you preview how large a pixel will be on the final image before performing a render.
5. Got a sick idea? Dont hesitate to let me know about it!

# Contact

You can reach me by either opening an issue or discussion here on Github, or sending a dm to me over Discord: danieljackson#0286

# Intended workflow

The addon had its initial development in the process of the making of a video game "We Might Die" (an upcoming title as of writing this), we needed A LOT of textures baked from geometry for hard surface details for sci-fi ship interiors. The workflow is that you model/sculpt/generate geometry of any kind (the addon supports any sort of geometry thats visible in workbench & Eevee) in Blender or your software of choice, generate the maps and then add image based microdetails and materials in a texturing software of choice, such as Quixel Mixer.

The addon is also capable of renaming images emitted by another software and doing the naming for you with naming standards of choice.

Its recommended that you keep your images to the power of 2 (so 512, 1024, 2048, 4096 (etc)) and perfectly square as that will yield best performance when using it in most modern renderers as of today.

## Thanks for checking out my repo!
