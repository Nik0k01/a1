# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 19:26:57 2023

@author: Nik0
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
a_file = open("wyniki.txt", 'w')

# Elbowl 13 - czerwony - łaczy sie z niebieskim
data1 = pd.read_excel('a1.xlsx', sheet_name=0, index_col=0, 
                      names=['Press. drop', 'Flow'])
data1 = data1.drop(2)
# Trójnik TR9, spadek cisnienia 45-46, przeplywomierz 43
data2 = pd.read_excel('a1.xlsx', sheet_name=1, index_col=0, 
                      names=['Press. drop', 'Flow'])
# Trójnik TR9, spadek cisnienia 54-46, przeplywomierz 50
data3 =  pd.read_excel('a1.xlsx', sheet_name=2, index_col=0, 
                      names=['Press. drop', 'Flow'])
# do not include 1st and 9th row
data3 = data3.drop([1, 9])


data1['Flow'] = data1['Flow'] / 3600
data2['Flow'] = data2['Flow'] / 3600
data3['Flow'] = data3['Flow'] / 3600


plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": "Helvetica",
})
plt.figure(1, figsize=(8, 5), dpi=120, )
plt.plot(data1.iloc[:, 1], data1.iloc[:, 0], 'r-.*',
         data2.iloc[:, 1], data2.iloc[:, 0], 'g--*',
         data3.iloc[:, 1], data3.iloc[:, 0], 'b:*') 
plt.xlabel(r'$\dot{V}$ [m$^3$/s]')
plt.ylabel(r'$\Delta P$ [Pa]')
plt.title("Spadki na różnych kształtkach")
plt.annotate("TR9 54-56", xy=(0.06, 45), xytext=(0.07, 45))
plt.annotate("TR9 45-46", xy=(0.06, 30), xytext=(0.065, 30))
plt.annotate("K13", xy=(0.08, 15), xytext=(0.08, 18))
plt.savefig('spadki_ksztaltki.png')

polies = []
for data in [data1, data2, data3]:
    polies.append(np.polynomial.Polynomial.fit(data.iloc[:, 1],
                                               data.iloc[:, 0], 2))
    
poly1, poly2, poly3 = polies   
a = poly1.linspace(n=100, domain=(0, 0.12))
b = poly2.linspace(n=100, domain=(0, 0.12))
c = poly3.linspace(n=100, domain=(0, 0.12))
plt.plot(a[0], a[1], 'r',
         b[0], b[1], 'g',
         c[0], c[1], 'b')

# Flow velocity
data1['vel'] = np.sqrt(data1['Flow'] * 4 / np.pi / 0.1 ** 2)
data2['vel'] = np.sqrt(data2['Flow'] * 4 / np.pi / 0.135 ** 2)
data3['vel'] = np.sqrt(data3['Flow'] * 4 / np.pi / 0.135 ** 2)

# Local pressure dropp coef
data1['zeta'] = data1['Press. drop'] * 2 / data1['vel'] ** 2 / 1.2
data2['zeta'] = data2['Press. drop'] * 2 / data2['vel'] ** 2 / 1.2
data3['zeta'] = data3['Press. drop'] * 2 / data3['vel'] ** 2 / 1.2


plt.figure(2, figsize=(8, 5), dpi=120)
plt.plot(data1.iloc[:, 1], data1.iloc[:, 3], 'r-.*',
         data2.iloc[:, 1], data2.iloc[:, 3], 'g--*',
         data3.iloc[:, 1], data3.iloc[:, 3], 'b:*') 
plt.xlabel(r'$\dot{V}$ [m$^3$/s]')
plt.ylabel(r'$\zeta$ [-]')
plt.title("Współczynnik strat miejscowych na różnych kształtkach")
plt.annotate("TR9 54-56", xy=(0.06, 13), xytext=(0.07, 13))
plt.annotate("TR9 45-46", xy=(0.06, 10), xytext=(0.065, 9))
plt.annotate("K13", xy=(0.08, 4), xytext=(0.08, 3))
plt.savefig('wsp_zeta_ksztaltki.png')


polies = []
for data in [data1, data2, data3]:
    polies.append(np.polynomial.Polynomial.fit(data.iloc[:, 1],
                                               data.iloc[:, 3], 2))

zeta1, zeta2, zeta3 = polies 
a = zeta1.linspace(n=100, domain=(0.01, 0.12))
b = zeta2.linspace(n=100, domain=(0.01, 0.12))
c = zeta3.linspace(n=100, domain=(0.01, 0.10))
plt.plot(a[0], a[1], 'r',
         b[0], b[1], 'g',
         c[0], c[1], 'b')

# Opory liniowe przepływu przez ruociag
# L1 łaczy sie z zielonym
flows = np.linspace(0.01, 0.2)
vels1 = np.sqrt(flows * 4 / np.pi / 0.135 ** 2)
L1 = pd.DataFrame({'Flow' : flows, 'vel' : vels1, 
                   'Re' : vels1 * 0.135 / 1.516e-5})
L1['lambda'] = 0.3164 / L1['Re'] ** 0.25
# Opory liniowe gornego rurociagu
L1['Press. drop'] = L1['lambda'] * 10 / 0.135 * L1['vel'] ** 2 / 2 * 1.2

ziel = zeta2.linspace(n=50, domain=(0.01, 0.2)) 
czerw = zeta1.linspace(n=50, domain=(0.01, 0.2))
nieb = zeta3.linspace(n=50, domain=(0.01, 0.2))

# Spadek cisnienia na trojniku na gorze
p_drop_troj_u = vels1 ** 2 / 2 * 1.19 * ziel[1]
# Wykres spadkow cisnienia gornego rurociagu

plt.figure(3, figsize=(8, 5), dpi=120)
plt.plot(L1['Flow'], L1['Press. drop'],
         ziel[0], ziel[1])

# Sumaryczny spadek na gornym rurociagu
press_drop_tot_u = L1['Press. drop'] + p_drop_troj_u

plt.plot(L1['Flow'], press_drop_tot_u, '-.')
plt.xlabel(r'$\dot{V}$ [m$^3$/s]')
plt.ylabel(r'$\Delta P$ [Pa]')
plt.title("Charakterystyka rurociagu górnego")
legend = ['L1', 'Trojnik', 'Suma']
plt.legend(legend)
plt.savefig('rury_gora.png')

# Second pipeline
# L2 łaczy sie z czerwonym i niebieskim
vels2 = np.sqrt(flows * 4 / np.pi / 0.1 ** 2)
L2 = pd.DataFrame({'Flow' : flows, 'vel' : vels2, 
                   'Re' : vels2 * 0.1 / 1.516e-5})
L2['lambda'] = 0.3164 / L2['Re'] ** 0.25
# Opory liniowe dolnego rurociagu
L2['Press. drop'] = L2['lambda'] * 15 / 0.1 * L2['vel'] ** 2 / 2 * 1.2

# Spadek cisnienia na kolanie
p_drop_kol = vels2 ** 2 / 2 * 1.19 * czerw[1]
# Spadek cisnienia na trojniku na dole
p_drop_troj_b = vels2 ** 2 / 2 * 1.19 * nieb[1]

# Wykres spadkow cisnienia w dolnym rurociagu
plt.figure(4, figsize=(8, 5), dpi=120)
plt.plot(L2['Flow'], L2['Press. drop'],
         czerw[0], p_drop_kol,
         nieb[0], p_drop_troj_b)

# Sumaryczny spadek na dolnym rurociagu
press_drop_tot_b = L2['Press. drop'] + p_drop_kol + p_drop_troj_b

# Wielomiany żeby łatwo dodać 
poly_L1 = np.polynomial.Polynomial.fit(press_drop_tot_u,
                                           L1['Flow'], 2)
poly_L2 = np.polynomial.Polynomial.fit(press_drop_tot_b,
                                           L1['Flow'], 3)
# Charakterystyka zastepcza
przeplyw = poly_L1.linspace(domain=(29, 230))[1] + poly_L2.linspace(domain=(29, 230))[1]
przeplyw = np.append(L1['Flow'][:16], przeplyw)
spadki = np.append(press_drop_tot_u[:16], poly_L1.linspace(domain=(29, 230))[0])

for data in [data1, data2, data3]:
    polies.append(np.polynomial.Polynomial.fit(data.iloc[:, 1],
                                               data.iloc[:, 3], 2))        
    
plt.plot(L2['Flow'], press_drop_tot_b, '-.')
plt.xlabel(r'$\dot{V}$ [m$^3$/s]')
plt.ylabel(r'$\Delta P$ [Pa]')
plt.title("Charakterystyka rurociagu dolnego")
legend = ['L2', 'Kolanko', 'Trojnik', 'Suma']
plt.legend(legend)
plt.savefig('rury_dol.png')


plt.figure(5, figsize=(8, 5), dpi=120)
plt.plot(L2['Flow'][:29], press_drop_tot_b[:29],
         L1['Flow'], press_drop_tot_u,
         przeplyw, spadki)
plt.axhline(y=31, color='r', linestyle='-.')
plt.legend(["Dolny", "Górny", "Ekwiwalentny"])
plt.xlabel(r'$\dot{V}$ [m$^3$/s]')
plt.ylabel(r'$\Delta P$ [Pa]')
plt.title("Charakterystyka zastepcza rurociagów równoległych")
plt.savefig('zastepcza_rowno.png')

# Ostatni odcinek rurociagu 
length_3 = 10
diam_3 = 0.15
flows_3 = przeplyw
vels_3 = np.sqrt(flows_3 * 4 / np.pi / diam_3 ** 2)
L3 = pd.DataFrame({'Flow' : flows_3, 'vel' : vels_3, 
                   'Re' : vels_3 * diam_3 / 1.516e-5})

L3['lambda'] = 0.3164 / L3['Re'] ** 0.25
# Opory liniowe ostatniego rurociagu
L3['Press. drop'] = L3['lambda'] * length_3 / diam_3 * L3['vel'] ** 2 / 2 * 1.2
plt.figure(6, figsize=(8, 5), dpi=120)
plt.plot(przeplyw, spadki,
         L3['Flow'], L3['Press. drop'],
         przeplyw, spadki + L3['Press. drop'])
plt.xlabel(r'$\dot{V}$ [m$^3$/s]')
plt.ylabel(r'$\Delta P$ [Pa]')
plt.title("Całkowita charakterystyka rurociagu")
plt.legend([r'$L_1 + L_2$', r'$L_3$', r'$L_3 + L_2 + L_1$'])
plt.savefig('zastepcza_wszystko.png')

print('Rurociag L1\n', L1, file=a_file)
print('\nRurociag L2\n', L2, file=a_file)
print('\nSpadki gorny\n', press_drop_tot_u, file=a_file)
print('\nSpadki dolny\n', press_drop_tot_b, file=a_file)
print('\nSpadki zastepczy rownolegle', spadki, file=a_file)
print('\nSpadki zastepczy wszystko', spadki + L3['Press. drop'], file=a_file)
a_file.close()


