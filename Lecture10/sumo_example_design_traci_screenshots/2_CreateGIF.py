# PYTHON IMPORTS
import os
import PIL.Image



# METHODS
def render_gif_animation(lst_image_files, target_file: str, speed:int=100, first_last_slow:bool=True):
    """
    This function reads static images from a list of image files, and stores 
    all of them in an GIF animation.
    
    Parameters
    ----------
    lst_image_files: List[str]
        A list with image files that shall be connected to a GIF animation.
    target_file : str
        The target file to store the GIF into.
    speed : int
        Optional, Default: 100. The time per image. The slower the faster the animation.
    first_last_slow : bool
        Optional, Default : True. This will repeat the first and the last 
        image for ten times, so the animation does not directly run.
        
    Returns
    -------
    None
    """
    frames = []
    if first_last_slow:
        for x in range(0,10):
            image = PIL.Image.open(lst_image_files[0])
            image = image.crop((int(image.size[0]/2-image.size[1]/2), 0, int(image.size[0]/2+image.size[1]/2), image.size[1]))
            frames.append(image)
    for file in lst_image_files:
        image = PIL.Image.open(file)
        image = image.crop((int(image.size[0]/2-image.size[1]/2), 0, int(image.size[0]/2+image.size[1]/2), image.size[1]))
        frames.append(image)
        print(file)
    if first_last_slow:
        for x in range(0,10):
            frames.append(frames[-1])
    frames[0].save(target_file, format='GIF',
                    append_images=frames[1:],
                    save_all=True,
                    duration=speed, loop=0)


# CREATE GIF
screenshot_folder = "screenshots"

files = os.listdir(screenshot_folder)
files = [screenshot_folder+"/"+f for f in files]

files2 = []
for i in range(0, len(files), 2):
    files2.append(files[i])
files = files2.copy()

render_gif_animation(files, "Test.gif", speed=50, first_last_slow=True)
