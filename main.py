# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 19:26:57 2023

@author: Nik0
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Elbowl 13 - czerwony - łączy się z niebieskim
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
# Usun punkt 10 ze wzgledu na znaczną rozbieżnosc zeta
data3 = data3.drop(10)

data1['Flow'] = data1['Flow'] / 3600
data2['Flow'] = data2['Flow'] / 3600
data3['Flow'] = data3['Flow'] / 3600


plt.rcParams['text.usetex'] = True
plt.figure(1, figsize=(8, 5), dpi=120, )
plt.plot(data1.iloc[:, 1], data1.iloc[:, 0], 'r-.*',
         data2.iloc[:, 1], data2.iloc[:, 0], 'g--*',
         data3.iloc[:, 1], data3.iloc[:, 0], 'b:*') 
plt.xlabel(r'$\dot{V}$ [m$^3$/s]')
plt.ylabel(r'$\Delta P$ [Pa]')
plt.annotate("TR9 54-56", xy=(0.06, 45), xytext=(0.07, 45))
plt.annotate("TR9 45-46", xy=(0.06, 30), xytext=(0.065, 30))
plt.annotate("K13", xy=(0.08, 15), xytext=(0.08, 18))

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
plt.annotate("TR9 54-56", xy=(0.06, 13), xytext=(0.07, 13))
plt.annotate("TR9 45-46", xy=(0.06, 10), xytext=(0.065, 9))
plt.annotate("K13", xy=(0.08, 4), xytext=(0.08, 3))

polies = []
for data in [data1, data2, data3]:
    polies.append(np.polynomial.Polynomial.fit(data.iloc[:, 1],
                                               data.iloc[:, 3], 2))

zeta1, zeta2, zeta3 = polies 
a = zeta1.linspace(n=100, domain=(0.01, 0.12))
b = zeta2.linspace(n=100, domain=(0.01, 0.12))
c = zeta3.linspace(n=100, domain=(0.03, 0.10))
plt.plot(a[0], a[1], 'r',
         b[0], b[1], 'g',
         c[0], c[1], 'b')

# Opory liniowe przepływu przez ruociąg
# L1 łączy się z zielonym
flows = np.linspace(0.04, 0.1)
vels1 = np.sqrt(flows * 4 / np.pi / 0.135 ** 2)
L1 = pd.DataFrame({'Flow' : flows, 'vel' : vels1, 
                   'Re' : vels1 * 0.135 / 1.516e-5})
L1['lambda'] = 0.3164 / L1['Re'] ** 0.25
L1['Press. drop'] = L1['lambda'] * 10 / 0.135 * L1['vel'] ** 2 / 2 * 1.2
ziel = zeta2.linspace(n=50, domain=(0.04, 0.1))
czerw = zeta1.linspace(n=50, domain=(0.04, 0.1))
nieb = zeta3.linspace(n=50, domain=(0.04, 0.1))
# Wykres spadkow cisnienia gornego rurociagu
plt.figure(3, figsize=(8, 5), dpi=120)
plt.plot(L1['Flow'], L1['Press. drop'],
         ziel[0], ziel[1])
press_drop_tot_u = L1['Press. drop'] + ziel[1]
plt.plot(L1['Flow'], press_drop_tot_u, '-.')
plt.xlabel(r'$\dot{V}$ [m$^3$/s]')
plt.ylabel(r'$\Delta P$ [Pa]')
legend = ['L1', 'Trojnik', 'Suma']
plt.legend(legend)


# Second pipeline
# L2 łączy się z czerwonym i niebieskim
vels2 = np.sqrt(flows * 4 / np.pi / 0.1 ** 2)
L2 = pd.DataFrame({'Flow' : flows, 'vel' : vels2, 
                   'Re' : vels2 * 0.1 / 1.516e-5})
L2['lambda'] = 0.3164 / L2['Re'] ** 0.25
L2['Press. drop'] = L2['lambda'] * 15 / 0.1 * L2['vel'] ** 2 / 2 * 1.2
# Wykres spadkow cisnienia w dolnym rurociagu
plt.figure(4, figsize=(8, 5), dpi=120)
plt.plot(L2['Flow'], L2['Press. drop'],
         czerw[0], czerw[1],
         nieb[0], nieb[1])
press_drop_tot_b = L2['Press. drop'] + czerw[1] + nieb[1]
plt.plot(L2['Flow'], press_drop_tot_b, '-.')
plt.xlabel(r'$\dot{V}$ [m$^3$/s]')
plt.ylabel(r'$\Delta P$ [Pa]')
legend = ['L2', 'Kolanko', 'Trojnik', 'Suma']
plt.legend(legend)

