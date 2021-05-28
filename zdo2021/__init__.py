 adresar = "mytest"
 startobr = 1
 pocetobr = 10
 vyska = 0 #nepracoval jsem s tim v algoritmu, predpokladam datasety s podobnymi vlastnosti (rozliseni, vzdalenost, velikost obr, barevne kanaly)
 sirka = 0 #nepracoval jsem s tim v algoritmu, predpokladam datasety s podobnymi vlastnosti (rozliseni, vzdalenost, velikost obr, barevne kanaly)
 barevne_kanaly = 3 #nepracoval jsem s tim v algoritmu, predpokladam datasety s podobnymi vlastnosti (rozliseni, vzdalenost, velikost obr, barevne kanaly)
 data = [pocetobr,vyska,sirka,barevne_kanaly]
 result = VarroaDetector.predict(startobr, adresar, data)
 print(result)
