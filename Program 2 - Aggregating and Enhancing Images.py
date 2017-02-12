"""
Created on Thu Nov 10 12:43:08 2016
@author: jamesfuller
"""
import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2

import scipy.ndimage as ndimage
import numpy
from PIL import Image
import os.path
import scipy 
"""
Error Catching list
- Image loads incorrectly, raise warning
- Check img is 3-d, or code can deal with 1,2-d images. For newImg[x,y] = img[x,y,1]
- Way to to deal with molecule on edge of image (LLcorner)
- 
"""

"""
Next steps
- make code be able to deal with multiple images in a foler
- LED array, capturing images
- Produce an initial image of blurriness to compare with final image
"""

""" 
Possible
- Multiple colours
E:\Stochastic Imaging Project\ImageBin

"""
filepath = raw_input("Input your filepath:")
#James's filepath: /Users/jamesfuller/Desktop/Project/final/images/


if filepath == '':
    filepath = 'E:\Stochastic Imaging Project\ImageBin\\' 
    #default filepath for Windows computer
    
print('Using Filepath - ', filepath)

def _convert_video_to_images(videoName):
    #Function that converts inputted video to image of each frame
    #Uses module cv2 which is only installed on James' Mac (hard to install)
    cap = cv2.VideoCapture(videoName)
    #select video to be used
    count = 0
    #set frame count = 0
    
    while(cap.isOpened()):
        ret, frame = cap.read()
        #capture frame
    
        name = "images/frame%d.jpg"%count
        #name file to be saved
        cv2.imwrite(name, frame)
        #save file
        count = count + 1
        #iterate count
        if count == 151:
        #able to change variable knowing 20 fps to set time of recording
            break
    
    cap.release()
    cv2.destroyAllWindows()
    return

def _image_to_molecule_locations(

    imageIn, 
    #The image in 2d array form     
    xyShape,
    #Shape of calibration stack used to localise particles in image    
    numSTD=10,
    #Default = 4
    #'numSTD' is the number of standard deviations of brightness a particle must 
    #rise above the image mean to be considered a particle    
    numSTD_changed=None,
    #Default = none    
    ):
    
    """    
    Given a 2d array 'imageIn', finds the bright (or changed) regions    
    of the image that we think are single particles.    
    'xyShape' is a 2-tuple giving the XY shape of the calibration    
    stack used to localize particles in the image. 'numSTD' is the    
    number of standard deviations of brightness a particle must rise    
    above the image mean to be considered a particle. 'showSteps'    
    displays some of the particle selection process, and can be useful    
    for debugging and choosing other parameters.                
    """                                   
    """Groundwork:"""
    
    calibrationShape = scipy.asarray(xyShape)
    #Set array of calibration shape as defined above
    #user defined as size of shape round molecule
    
    imageIn = scipy.asarray(imageIn)
    #Set image in as an array                           
    locs, avg, std, thresh = [], [], [], []
    
    avg.append(imageIn.mean()) #Image average over 3 frames
    std.append(imageIn.std()) #Image standard deviation over 3 frames    
    thresh.append(imageIn > (avg[-1] + numSTD*std[-1])) #Brightness threshold    
    locs.append([])

    """Zero the image, except for the bright or changed spots:"""   
    peaksImage = imageIn * thresh[-1] 
    #print(peaksImage)
    """Chop out the bright spots one at a time:"""   
    while peaksImage.max() > 0:
        #Rest of image is zeroed so this will only be bright spots    
        peakLocation = scipy.unravel_index(    
            peaksImage.argmax(),    
            peaksImage.shape)
        #get location of peak found   
        """The lower left corner of the chop region:"""    
        LLcorner = scipy.asarray(peakLocation - calibrationShape//2) 
        #// = integer division
        appendMolecule = True

        """Don't include molecules that touch the image edge:"""

        if (LLcorner <= 0).any():    
            appendMolecule = False    
            LLcorner = LLcorner * (LLcorner >= 0)
        #Reset lower left corner if less than 0
        if ((LLcorner + calibrationShape) >= imageIn.shape).any():
            appendMolecule = False
        #if right corner greater than image then ignore molecule                
        molX = slice(LLcorner[0],(LLcorner[0] + calibrationShape[0]))
        #set x-distance for molecule
        molY = slice(LLcorner[1],(LLcorner[1] + calibrationShape[1]))
        #set y-distance for molecule   
        if appendMolecule:    
            locs[-1].append((molX, molY))
            #print(molX,molY)
            #set values into locations array                
            
            
        """Zero out the chopped region:"""    
        peaksImage[molX, molY] = 0
        #zero bright spot to continue on with process
        
   # print(molX,molY)
    brights = locs[0]    
    return (brights)
    
_convert_video_to_images("cross20fr.mp4")
#input name of video to be analysed
              
if os.path.exists(filepath):    
    maxPixels = [] #list of points of maxima for final image
    initialPixels = [] # possibly create initial image to compare
    iterationCount = 0
    for imgName in os.listdir(filepath): 
        if not imgName.startswith('.'): # ignore hidden files
            iterationCount += 1
            try:    
                im = Image.open(filepath+imgName) #open frame
                im = im.crop((600,300,1112,812)) #crop set around light sources manually
                im.save(filepath+imgName) #save crop
                img = ndimage.imread(filepath+imgName) #open file in greyscale form
                impixels = im.load() #load pixel values from image
                newImg = numpy.zeros((512,512)) #create recreation image
                print('CHECK1: Image',iterationCount,'has been loaded correctly')
            
                img = ndimage.gaussian_laplace(img, sigma=3.2)
                #Apply gaussian laplace function to image
            
                for x in range(512):
                    for y in range(512):
                        newImg[x, y] = img[x,y,1]
                #apply each pixel value to 1-d  image
                                      
                brights = _image_to_molecule_locations(imageIn=newImg, xyShape=[50,50])
                #call function to find bright spots         
            
                im = Image.open(filepath+imgName)
                im = im.convert('L') #Convert image to greyscale
            
                for loc in brights: #for each bright spot
                    im2 = im.crop(((loc[1].start), (loc[0].start), (loc[1].stop), (loc[0].stop)))
                    #crop each image around bright spot 50px x 50px
                    minima, maxima = im2.getextrema()
                    #find maximum pixel value
                
                    for width in range(im2.size[0]):
                        for height in range(im2.size[1]):
                            if im2.getpixel((width, height)) == maxima:
                                maxPixels.append(((width + loc[1].start), (height + loc[0].start)))
                    #find location of max pixel value in bright spot image
                
                # plot final sharp image if it is last iteration
                if iterationCount == int(len(os.listdir(filepath)))-1: 
                    finalImg = Image.new('RGBA', (1920,1080), "black") #create final image
                    new_colour = (255,0,0,1) #red 
                    for each in maxPixels:
                        newX = each[0] + 600 
                        #apply x difference to recreate 1920x1080 input image size
                        newY = each[1] + 300
                        #apply y difference to recreate 1920x1080 input image size
                        finalImg.putpixel((newX, newY),new_colour) 
                        #Changes Pixel Colour to red
            
            except FileNotFoundError:
                print("ERROR: Image does not exist in location - ", filepath)
                #catch error statement

    finalImg.show() #show recreated image
    finalImg.save("finalImageCross10std.png") #save recreated image as png
else:
    print('ERROR: Filepath does not exist - ', filepath)
#catch error statement