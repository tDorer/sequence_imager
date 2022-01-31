import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np 
from numpy import asarray, savetxt, loadtxt
#from argparse import ArgumentParser
import sys
from PIL import Image



def trans(hexa):
    hexdec = {'0' : 0,
          '1' : 1,
          '2' : 2,
          '3' : 3,
          '4' : 4,
          '5' : 5,
          '6' : 6,
          '7' : 7,
          '8' : 8,
          '9' : 9,
          'a' : 10,
          'b' : 11,
          'c' : 12,
          'd' : 13,
          'e' : 14,
          'f' : 15}
    dec = []
    for character in hexa:
        dec += [hexdec[character]]
    return dec
def evaluate(dec):
    switch = [(dec[0]*16+dec[1]),(dec[2]*16+dec[3]),(dec[4]*16+dec[5])]
    return max(switch)

def findloc(c, matrix):
    a = [0,0]
    for i in matrix:
        if i[0]==c:
            a = i
    if a[0] == 0:
        sys.exit(f'letter {c} found in sequence but is not defined in paramter file.')
    return a
    
basename = input("Please enter the name of your sequence file.\nDo not enter the .seq ending.\n> ")



#opens the sequence file as one letter code
with open (basename+'.seq', "r") as myfile:
    data = myfile.readlines()
sequence = []
for i in data:
    sequence.append(list((i.replace(' ','')).replace('\n', '')))
    
    
    
#opens the parameters .csv sheat
try:
    with open ('parameter.csv', "r") as myfile:
        data = myfile.readlines()
except:
    with open (input("Please enter the name of your paramter file.\nIncluding the ending.\n> ")) as myfile:
        data = myfile.readlines()
matrix = []
#create an 2D array 
for line in data:
    line = line.replace('\n','').split(',')
    if evaluate(trans(line[2][1:7])) < 144:  #the 144 is the set border to decide whether the letter should be white or black, putting a higher number makes more letters black.
        matrix.append([line[0],float(line[1])*30,str(line[2]),'white', float(line[3])])
    else:
        matrix.append([line[0],float(line[1])*30,str(line[2]),'black', float(line[3])])
matrix = np.array(matrix)


#expands the sequence array in a dimension with every data element from the parameters
data = []
for j in sequence[0]:
    data.append(findloc(j,matrix))
        

step = input("Please enter here a number to decide the distance between the amino acids in the plot. The Default use is 0.06.\nJust press Enter to use the default.\n> ")
if step:
    step = float(step)
else:
    step = 0.06

#creates coordinates in y-direction with periodic density
#first creates a sinus function shifted in y-direction by one
begin,start,y, fac = -np.pi*0.95, -np.pi, [],0.0001
a = 1+np.sin(np.arange(-0.5*np.pi,13000*len(sequence[0])*step*fac*np.pi,2*fac))
#then adding the numbers of the sinus array stepwise to a starting point
i=0
end = start - np.pi*(int(0.5*len(sequence[0])*step+1)+0.05)
while start>end:
    y.append(start)
    start-=a[i]*fac
    i+=1
#and also walk a little bit backwards, the following 5 lines could be commented out if the plot should start in the middle.
if not input("Do you want to start your plot in the left corner? Please press Enter for that case, please type 'MIDDLE' if you want to start in the center.> \n").upper() == 'MIDDLE':
    i,start=0,-np.pi
    while begin>start:
        start+=a[i]*fac
        y.insert(0,start)
        i+=1
y=np.array(y)




# !!! This step needs some time !!!
#use a fourier row to create a rectangular periodic signal, and set an exponent slightly higher than 1 to get rounded edges (the higher the exponent, the more the signal turns into a sinus)
x = np.zeros(len(y))
count=0
print('Creating a Fourier row. This step will take some time.')
for i in range(5000):
    x += 4/(2*i+1)**1.03/np.pi*np.sin((2*i+1)*y)
    print(f'{count/50}%', end='\r')
    count+=1
print('100.00%')
y/=30

    #filter data in regular distances, use 'step' to define the distance between the beads.

xs,ys, d, i = [x[0]], [y[0]], 1, 0
while len(xs) <len(data):
    d=((x[i]-xs[len(xs)-1])**2+(y[i]-ys[len(ys)-1])**2)**0.5
    if d<step: 
        i+=1
    else:
        a='free'
        for j in range(len(xs)):
            b = ((x[i]-xs[j])**2+(y[i]-ys[j])**2)**0.5
            if b<step:
                a='occupied'
                break
        if a == 'free':
            xs.append(x[i]),ys.append(y[i])
        i+=1

#creates the actual plot
fig, ax = plt.subplots(ncols=1,num=None, figsize=(16, (max(ys)-min(ys)+0.2)*16/2.2), dpi=320, facecolor='w', edgecolor='w')
ax.set(ylim=(max(ys)+min(ys),0), xlim=(-1.1,1.1))
ax.set_xticks([])
ax.set_yticks([])
n = 0

ax.plot(xs,ys, color = 'black', linewidth=3)

while n<len(data):
    ax.plot(xs[n],ys[n],linewidth=0,marker='o',markersize=float(data[n][1])*1.08,color='black')
    ax.plot(xs[n],ys[n],linewidth=0,marker='o',markersize=data[n][1],color=data[n][2])
    ax.annotate(data[n][0],(xs[n]-float(data[n][4]),ys[n]-0.0095),fontsize=13,color=data[n][3])
    n+=1
plt.savefig(basename+'.png', bbox_inches = 'tight',
    pad_inches = 0)
if input("Plot is finished, if you want to see it right now please type 'YES'.\n> ").upper() =='YES':
    plot = Image.open(basename+'.png')
    plot.show()



