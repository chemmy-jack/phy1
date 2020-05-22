# GlowScript version of Jupyter demo program Color-RGB-HSV
showrgb = wtext(pos=scene.title_anchor, text="RGB display")

C = ['Red', 'Green', 'Blue']
sliders = []
wts = []

def set_background(sl):
    wts[sl.id].text = '{:1.3f}'.format(sl.value)
    rgb = vector(sliders[0].value, sliders[1].value, sliders[2].value)
    scene.background = rgb
    # For readability, limit precision of display of quantities to 3 figures
    showrgb.text = "{:1.3f}, {:1.3f}, {:1.3f}".format(rgb.x, rgb.y, rgb.z)

for i in range(3): # Create the 3 RGB and 3 HSV sliders
    sliders.append(slider(length=300, left=10, min=0, max=1, bind=set_background, id=i))
    scene.append_to_caption('    '+C[i]+' ') # Display slider name
    wts.append(wtext(text='0.000'))
    scene.append_to_caption('\n\n')
sliders[0].value = 0.796
sliders[1].value = 1
sliders[2].value = 0.693

