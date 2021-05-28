import numpy as np
# moduly v lokálním adresáři musí být v pythonu 3 importovány s tečkou
from . import podpurne_funkce
. import cv2
. import numpy as np
. import matplotlib.pyplot as plt
. import skimage
from skimage . import data
from skimage.morphology . import label
from skimage.color . import rgb2gray
from skimage . import data
from skimage.filters.  import gaussian
from skimage.segmentation . import active_contour
. import skimage.segmentation
. import scipy
. import numpy as np
. import matplotlib.pyplot as plt
. import scipy
from scipy . import ndimage

class VarroaDetector():
   def varoadetektor(adresa):
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
        imgv = cv2.imread(adresa) 

        # stupne sedi:
        img = rgb2gray(imgv)

        # prahovani:
        imthr = img < prah 

        # vyplni diry - kvuli lesku klestiku:
        imthr = ndimage.binary_fill_holes(imthr) 

        # label (vyselektovani jednotlivych objektu)
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

        return varoa

    def predict(startobr, adresar, data):
        pocetobr = data[0]
        vyska = data[1]
        sirka = data[2]
        barevne_kanaly= data[3]
        shapeoutput = []
        varoa = -1
        pocetobrsvarroa = 0 # na kolika obrazcich je varroa
        jevarroa = 0 #je v datasetu varroa?
        for x in range(startobr,startobr+pocetobr): 
            a = str(x)
            adresa = adresar + "/" + a + ".jpg"        
            varroa = varoadetektor(adresa)
            if varroa == 1:
                pocetobrsvarroa += 1
        if pocetobrsvarroa > (pocetobr/2): #je v datasetu varroa? vic nez 50% fotek detekovalo varoa?
            jevarroa = 1

        shapeoutput = [pocetobr, vyska, sirka]
        return shapeoutput, jevarroa, pocetobrsvarroa
    
   
        
           
