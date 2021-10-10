# Quick demo video
https://youtu.be/H1a0zsd9-6Y

# FastPBR
Fast PBR Viewport Render is a tool that lets you fetch curvature, AO, normal maps, transparency, matID and height from the camera youre currently looking through or directly from your viewport. It uses Blenders "Render viewport" operator which renders pretty much exactly what you see on screen or what the camera you are looking through currently has within frame. Therefore its extremely flexible as "what you see is what you get" and as you can use it ANYWHERE to render ANY sort of geometry or scene. It works by modifying your render settings and renderer (it uses Eevee and workbench for maximum performance), it can render out several 4K maps in the matter of seconds, making it versatile and useable for projects where you need to do a lot of rendering (and hence cant afford any time lost for waiting). It also comes equipped with a flexible, configurable and automatic file naming and folder hierarchy system that lets you move and name your images wherever you want based on custom &amp; automatically generated variables that describes your images.


# Install instructions.

1. Download the FastPBRNormalMatCap.exr attached in any of the releases:
![image](https://user-images.githubusercontent.com/20190653/136703921-1df20cef-71d8-4ca2-af3f-72d43ecad2f3.png)

2. Download the addon .zip file like usual (via Top Panel > Edit > Preferences > Add-ons > Install > select the zip).

3. You should now see the dedicated "Fast PBR Viewpot Render" panel in In "your 3D viewport > Left side Bar/foldout panel (N is the default hotkey to open/close) > Fast > Fast PBR".

# Usage

1. Choose a destination path, note that this path has to include the file name itself and the file extension. Only png is supposed at the time being, so make sure that it ends with png.
2. Configure the render passes you would like to use by toggling the checkboxes, more settings might become available in there foldout panels on a later time.
3. Choose the resolution by setting your camera resolution like usual in Properties > Output Properties.
4. Save your file for safety (The addon modifies your render settings and later reverts them, but if the script fails to reach the end due to a fatal error (which could occur if the Blender version you're using is not 100% compatable) it might not get a chance to restore the settings. If that happens however, you should be able to hit ctrl Z on your keyboard to revert the settings yourself as the addon automatically sets up a restore state to go back to.
5. Hit the top button "Fast PBR Viewport Render" to render out your maps, once the operation is complete you will see a pop-up message appear at your cursor as well as that Windows file explorer will automatically open up the directory that the images has been created in for you.


# Contributing

Anyone is welcome to contribute, the addon is 100% pure Python 3.

# Troubleshooting

If you encounter any issues, dont hesitate to open up an issue ticket here on Github and I will do my best to assist. <3 Also dont shy away from digging in the code yourself if you believe you can figure out whats happening in the event of an unexpected Python error or any sort of unexpected behaviour.

## Thanks for checking out my repo!
