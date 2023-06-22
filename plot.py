import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import patches
import os
from PIL import Image
import numpy as np

def filterFiles(directoryPath, extension):
    # Filter files with the selected extension in the directory
    relevant_path = directoryPath
    included_extensions = [extension]
    file_names = [file1 for file1 in os.listdir(relevant_path) if any(file1.endswith(ext) for ext in included_extensions)]
    numberOfFiles = len(file_names)
    listParams = [file_names, numberOfFiles]
    return listParams

[image_names, numberOfFiles] = filterFiles("astra-fass/training", "jpg")    

trainRCNN = pd.read_csv('test.csv', sep=",", header=None)
trainRCNN.columns = ['filename', 'cell_type', 'xmin', 'xmax', 'ymin', 'ymax']
trainRCNN.head()

for imageFileName in image_names:    
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    plt.axis('off')

    image_path = 'astra-fass/training/' + imageFileName

    # Use PIL to load the image
    img = Image.open(image_path)

    # Check image orientation and rotate if necessary
    if hasattr(img, "_getexif") and img._getexif() is not None:
        exif = dict(img._getexif().items())
        orientation = exif.get(274)
        if orientation == 3:
            img = img.rotate(180, expand=True)
        elif orientation == 6:
            img = img.rotate(270, expand=True)
        elif orientation == 8:
            img = img.rotate(90, expand=True)

    # Convert image to numpy array
    image = np.array(img)

    # Plot the image
    plt.imshow(image)

    for _,row in trainRCNN[trainRCNN.filename == imageFileName].iterrows():
        xmin = float(row.xmin)
        xmax = float(row.xmax)
        ymin = float(row.ymin)
        ymax = float(row.ymax)
        
        width = xmax - xmin
        height = ymax - ymin
        ClassName= row.cell_type
        
        if row.cell_type == 'fass':
            ax.annotate('fass', xy=(xmax-40,ymin+20))
            rect = patches.Rectangle((xmin,ymin), width, height, edgecolor = 'r', facecolor = 'none')
        elif row.cell_type == 'astra':
            ax.annotate('astra', xy=(xmax-40,ymin+20))
            rect = patches.Rectangle((xmin,ymin), width, height, edgecolor = 'b', facecolor = 'none')
       
        else:
            print("nothing")
    
        ax.add_patch(rect)   
        if not os.path.exists("imagesBox"):
            os.makedirs("imagesBox")

        fig.savefig('imagesBox/' + imageFileName, dpi=90, bbox_inches='tight')
    plt.close()
    print("ImageName: " + imageFileName + " is saved in imagesBox folder")

print("PLOTBOX COMPLETED!")
