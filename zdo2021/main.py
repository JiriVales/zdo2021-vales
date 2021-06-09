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
    def __init__(self):
        pass

    def predict(self, data):
        """
        :param data: np.ndarray with shape [pocet_obrazku, vyska, sirka, barevne_kanaly]
        :return: shape [pocet_obrazku, vyska, sirka], 0 - nic, 1 - varroa destructor
        """
        
        pocetobrazku = data.shape[0]
        vyska = data.shape[1]
        sirka = data.shape[2]
        kanaly = data.shape[3]
        
      
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
        
          
        
        result = []
        
     
        
        for i in range(pocetobrazku):
         
            # nacteni obrazku:
            aktualniobrazek = data[i] 
            # stupne sedi:
            img = skimage.color.rgb2gray(aktualniobrazek)        
           
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
            spatnedetekovane = []

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
                                else:
                                    spatnedetekovane.append(props[i].label)
                            else:
                                spatnedetekovane.append(props[i].label)    
                        else:
                            spatnedetekovane.append(props[i].label)
                    else:
                        spatnedetekovane.append(props[i].label)

            #print(pocetdetekovanych)   
            if pocetdetekovanych > 0:
                varroa = 1
             
            #vymazat spatne            
            imlabel[np.isin(imlabel, spatnedetekovane)] = 0

            # vysledny obrazek
            vyslednyobr =  imthr < imlabel

            # obrazek hotov, vloz ho mezi vysledky
            result.append(vyslednyobr)
        
        # obrazek hotov, vloz ho mezi vysledky
        navratovahodnota = np.array(result)
        
        
        return navratovahodnota

           
      
      
           
        
         
        
