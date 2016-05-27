#!/usr/bin/python
#
# Uso: $ ./plot_pnboia.py Brecife_argos.csv
#
# aula12: 24/05/2016

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import date

f_in = str(sys.argv[1])
print "Processando arquivo: " + f_in

# awk: seleciona colunas (NR>1: ignora primeira linha)
awkCommand = "awk -F, \'NR > 1 {print $2, $3, $4, $5, $6, $7, $8, $34, $35}\' "+f_in+" > arq.txt" 
os.system(awkCommand)
fname=os.path.splitext(f_in)[0]

data = np.loadtxt("arq.txt", float, delimiter="  ")

# retira os -99999
data[data==data.min()] = np.nan;
temp = data[:,8]
pres = data[:,7]

# datas
dtime = np.zeros(temp.shape[0], int);
dateList = []
for i in np.arange(dtime.shape[0]):
    dtime[i] = date.toordinal(date(int(data[i,0]),int(data[i,1]),int(data[i,2])))
    dateList.append(date.fromordinal(dtime[i]))

datemin=dateList[0]
datemax=dateList[-1]

# "limpeza" 1 
temp1 = np.empty_like(temp)
pres1 = np.empty_like(pres)
temp1[:] = temp;
pres1[:] = pres;

caca = np.logical_or(temp < 15, temp > 35)
temp1[caca] = np.nan;
caca = np.logical_or(pres < 950, pres > 1050)
pres1[caca] = np.nan;

# "limpeza" 2: limpa por "janelas" 
k=0
temp2 = np.empty_like(temp1)
temp2[:] = temp1;
desvio = np.nanstd(temp2)
desviop = np.nanstd(pres1)
janela = 50
for i in np.arange(0,temp1.size,janela):
    media = np.nanmean(temp1[k:i-1])
    mediap = np.nanmean(pres1[k:i-1])
    for j in np.arange(k,i,1):
        dif = np.abs(temp1[j] - media)
        difp = np.abs(pres1[j] - mediap)
        if dif > desvio:
            temp2[j] = np.nan
        if difp > desviop:
            pres1[j] = np.nan
    k = i

# plot
plt.figure(figsize=(11,9),dpi=90)
plt.subplot(411)
plt.plot(dateList, temp,'b',markersize=1, markeredgecolor='b',label='original')
plt.plot(dateList, temp1,'ro',markersize=1.5, markeredgecolor='r',label='qualificado')
legend = plt.legend(loc='upper right',shadow=True, fontsize=11)
plt.grid(True)
plt.axis([datemin, datemax, 0, 60])
plt.ylabel('Temperatura (C)')
plt.title (f_in)

plt.subplot(412)
plt.plot(dateList,temp2, 'ro',markersize=1,markeredgecolor='r')
plt.grid(True)
plt.axis([datemin, datemax, 15, 32])
plt.ylabel('Temperatura (C)')

plt.subplot(413)
plt.plot(dateList,pres, 'b',markersize=1,markeredgecolor='b',label='original')
plt.plot(dateList, pres1,'ro',markersize=1.5, markeredgecolor='r',label='qualificado')
legend = plt.legend(loc='lower right',shadow=True, fontsize=11)
plt.grid(True)
plt.ylabel('Pressao (hPa)')

plt.subplot(414)
plt.plot(dateList, pres1,'ro',markersize=1.5, markeredgecolor='r')
plt.grid(True)
plt.ylabel('Pressao (hPa)')

plt.savefig(fname+".png",format='png', bbox_inches=0)
plt.show()
os.system("rm -f arq.txt")
