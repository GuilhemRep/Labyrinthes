import matplotlib.pyplot as plt
import random
import numpy as np

# ---------------------------------------Generate the lab---------------------------------------
def check(i,j):         # Checks if this box (i,j) is a path
    global M
    global lab_width
    global lab_height
    if i<0 or j<0 or j>=lab_height or i>=lab_width:
        return False
    elif M[i,j]==0:
        return True
    else:
        return False

def neighbour_generation(t):     # Returns the list of a box's neighbours
    i=t[0]
    j=t[1]
    l=[[i,j+2],[i+2,j],[i-2,j],[i,j-2]]
    neighbour=[]
    for x in l:
        if check(x[0],x[1]):
            neighbour.append(x)
    return neighbour

def reset():            # Finds a new strating point for the next path
    global M
    global case
    global lab_width
    global lab_height
    global last
    for i in range(last,lab_width//2+1):
        for j in range(lab_height//2+1):
            if M[2*i,2*j]==1:
                if len(neighbour_generation([2*i,2*j]))>=1:
                    case=[2*i,2*j]
                    last=case[0]//2
                    return True
    return False

def line(next):
    global case
    global M
    M[case[0],case[1]]=1
    x=int(0.5*(case[0]+next[0]))
    y=int(0.5*(case[1]+next[1]))
    M[x,y]=1
    M[next[0],next[1]]=1

# ---------------------------------------Drawing functions---------------------------------------
def border(M):
    p=np.size(M[:,0])           # Cols
    q=np.size(M[0,:])           # Lines
    N=np.zeros((p+2,q+2))       # Matrix of size (p+2)*(q+2) zeros
    c=0.1
    for i in range(p+2):        # Draws the border
        N[i,0]=c
        N[i,q+1]=c
    for j in range(q+2):
        N[0,j]=c
        N[p+1,j]=c
    for i in range(p):
        for j in range(q):
            N[i+1,j+1]=M[i,j]
    return N

def lab2plot(M):
    p=np.size(M[:,0])
    q=np.size(M[0,:])
    r=min(512//p,512//q)
    img=np.zeros((r*p,r*q))
    for i in range(p):
        for j in range(q):
            for o1 in range(r):
                for o2 in range(r):
                    img[i*r+o1,j*r+o2]=int(M[i,j]*255)
    return img

# ---------------------------------------Conversion functions---------------------------------------
def matrix2lab(M):
    p=np.size(M[:,0])
    q=np.size(M[0,:])
    a,b=p//3,q//3
    M1=np.zeros((a,b))
    for i in range(a):
        for j in range(b):
            M1[i,j]=M[i,j][0]
    return M1

def lab2matrix(M):
    p=np.size(M[:,0])
    q=np.size(M[0,:])
    M1=np.array([[[0.,0.,0.] for j in range(q)] for i in range(p)])
    for i in range(p):
        for j in range(q):
            M1[i,j]=[M[i,j],-1,-1]
    return M1

# ---------------------------------------Solve it---------------------------------------
def neighbour_solve(i,j):
    def check(a,b):             # Already visited?
        if a<0 or b<0 or a>=lab_width or b>=lab_height:
            return False
        if M[a,b,0]==1:
            if M[a,b,1]!=-1:
                return False
            return True         # Path to tag!
        return False            # Else : a wall

    global M
    global topology
    global lab_width
    global lab_height
    test=[[i+1,j],[i,j+1],[i-1,j],[i,j-1]]
    if topology==1:        #Torus
        for x in test:
            if x[0]<0:
                x[0]=lab_width-1
            if x[0]>=lab_width:
                x[0]=0
            if x[1]<0:
                x[1]=lab_height-1
            if x[1]>=lab_height:
                x[1]=0
    elif topology==2:        #Klein
        for x in test:
            if x[0]<0:
                x[0]=lab_width-1
                x[1]=lab_height-x[1]
            if x[0]>=lab_width:
                x[0]=0
                x[1]=lab_height-x[1]
            if x[1]<0:
                x[1]=lab_height-1
                x[0]=lab_width-x[0]
            if x[1]>=lab_height:
                x[1]=0
                x[0]=lab_width-x[0]
    elif topology==3:        #Möbius
        for x in test:
            if x[1]<0:
                x[1]=lab_height-1
                x[0]=lab_width-1-x[0]
            if x[1]>=lab_height:
                x[1]=0
                x[0]=lab_width-1-x[0]
    elif topology==4:         #Cylinder
        for x in test:
            if x[1]<0:
                x[1]=lab_height-1
            if x[1]>=lab_height:
                x[1]=1
    l=[]
    for x in test:
        if check(x[0],x[1]):
            M[x[0],x[1]]=[1,i,j]
            l.append((x[0],x[1]))
    return(l)

def next(l):
    global M
    liste=[]
    for x in l:
        liste+=neighbour_solve(x[0],x[1])
    return liste

def research(i,j,l):
    return((i,j) in l)

def explore(a,b,y,z):
    global M
    global cote
    global number_paths
    l=[(a,b)]
    M[a,b]=[1,-2,-2]          # Considered as a visited path
    security=0
    while not(research(y,z,l)) and security<number_paths:
        security+=1
        l1=next(l)
        if len(l1)>0:
            l+=l1
        else:
            return False
    if security>=number_paths:
        return False
    else:
                # Let's draw
        M[y,z,0]=0.5
        t1,t2=int(M[y,z,1]),int(M[y,z,2])
        pencil=0.5
        while(t1!=a or t2!=b):
            M[t1,t2,0]=pencil
            t1,t2=int(M[t1,t2,1]),int(M[t1,t2,2])
            pencil+=0.0        # Change to a decimal number to get a coloured path
        M[a,b,0]=pencil
    return True


# -----------------------------------USER FUNCTIONS!--------------------------------------
lab_height=90
lab_width=90


# Solving method : choose your topology :
# 0=Euclidian plane, 1=Torus, 2=Klein bottle, 3=Möbius loop, 4=Cylinder

topology=0



# ---------------------------------------Solving programm---------------------------------------
if lab_width%2==0:
    lab_width+=1
if lab_height%2==0:
    lab_height+=1
number_paths=lab_height*lab_width

M=np.array([[0]*lab_height]*lab_width)
M[0,0]=1
last=0      # Last drawn box
case=[0,0]
for _ in range(number_paths):
    l=neighbour_generation(case)
    if len(l)!=0:
        direction=random.randint(0,len(l)-1)
        line(l[direction])
        case=l[direction]
    else:
        if not(reset()):
            break
M=lab2matrix(M)
if topology==0:
    explore(0,0,lab_width-1,lab_height-1)
elif topology==3:
    explore(lab_width//2+1,0,lab_width//2+1,lab_height//2+1)
elif topology==4:
    explore(lab_width//2+1,0,lab_width//2+1,lab_height//2+1)
else:
    explore(0,0,lab_width//2+1,lab_height//2+1)
M=matrix2lab(M)
img=lab2plot(M)

plt.imshow(img,cmap=plt.cm.CMRmap)
plt.show()