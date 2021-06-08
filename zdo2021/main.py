import cv2
import numpy as np
import matplotlib.pyplot as plt
import skimage
from skimage import data
from skimage.morphology import label
from skimage.color import rgb2gray
from skimage import data
from skimage.filters import gaussian
from skimage.segmentation import active_contour
import skimage.segmentation
import scipy
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import ndimage

class VarroaDetector():    

    def predict(self, data):
      #Parametry ze zjistovaci mnoziny (20 klestiku):
        #Prah (klestici vyrazne tmavsi nez zbyla cast)
        prah = 0.2
        #Velikost 
        # rozsah area varoa:
        areamin = 100
        areamax = 200
        #Elipticky-tvar:
        # rozdil konvexni obalky s obsahem:
        rkonvexmax = 0.1
        # rozsah nekompaktnosti:
        maxnekompakt = 21
        minnekompakt = 13
        # rozsah pomeru os:
        maxpomer = 1.6
        minpomer = 1.2      
        
        # nacteni obrazku:
        imgv = cv2.imread(data)   ##---------------- ?
        # stupne sedi:
        img = rgb2gray(imgv)
        # prahovani:
        imthr = img < prah 
        # vyplni diry - kvuli lesku klestiku:
        imthr = ndimage.binary_fill_holes(imthr) 
        # label (vyselektovani jednotlivych obektu)
        imlabel = label(imthr, background=0)
        # pocet prvku
        #pocetvstupnichprvku = np.max(imlabel) 
        #print(pocetvstupnichprvku)
        #zjistovani charakteristik:
        props = skimage.measure.regionprops(imlabel)


        pocetdetekovanych = 0 #pocet detekovanych
        varoa = 0 #detekovana varroa?

        #projit vsechny objekty:
        for i in range(len(props)):   

                convexarea = props[i].convex_area    # plocha konvexni obalky 
                area = props[i].area    # plocha 
                rozdilkonvexarea = (convexarea - area)/((convexarea+area)/2) # rozdil konvexni obalky a area       
                perimeter = props[i].perimeter       # obvod   
                nekompaktnost = (perimeter*perimeter)/area     # vypocet nekompaktnosti
                major = props[i].major_axis_length # hlavni osa
                minor =props[i].minor_axis_length # vedlejsi osa
                if minor == 0: # nedelit nulou
                    minor = 0.0000001 
                pomeros = major/minor # pomer os       


                if area < areamax and area > areamin:  # splnuje velikost   
                    if rozdilkonvexarea < rkonvexmax: # splnuje dalsi vlastnosti eliptickeho tvaru
                        if nekompaktnost < maxnekompakt and nekompaktnost > minnekompakt:
                            if pomeros < maxpomer and pomeros > minpomer:                        
                                pocetdetekovanych +=1
                                ci = props[i].image                                                                  

        #print(pocetdetekovanych)   
        if pocetdetekovanych > 0:
            varoa = 1

        return varoa  ##---------------- ?
      
      
           
        
         
        
