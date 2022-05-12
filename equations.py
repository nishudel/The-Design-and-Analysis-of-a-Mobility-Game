import numpy as np
import random
######################## Typical Gekko Stuff ########################
from gekko import GEKKO
m = GEKKO() # Initialize gekko

### variable array for all the actions
# a=(a_1,a_2,...,a_n)
# a_i=(p_i,h_i,origin_i,destination_i,theta_i)

travellers = 10  # Total number of travellers |I|
c = 4   # Number of individual decisions of each traveller |a_i|

# The optimization variable
a = m.Array(m.Var,(travellers,c))


####################### Constraints for decision variables- Pre define #######################
# Pre-define variables to determine the bounds of sets that implement
# constraints in the optimisation problem for each component of a_i

## set of paths connecting the origin and destination ##
# Each number p_i is mapped to a path 
p_l=1   # Lower bound of the number 
p_u=3   # Upper bound
# Define the map - [i,j] implies ei-ej from source to destination
path_map={'1':[1,4],'2':[2,5],'3':[2,3,4] }  

## Set of mobility services
h_l=1
h_u=4
service_map={'1':'car','2':'tram','3':'bus','4':'bike'}

## Set of (o_i,d_i) pairs
# Here the map: if pair=i then (o_i,d_i) is connected by e_i
pair_l=1
pair_u=5
pair_map={'1':['S','A'],'2':['S','B'],'3':['B','A'],'4':['A','T'],'5':['B','T']} 

## mobility payement
# Since all theta_i are the same
theta_l=0
theta_u=2
# Need a map only if the theta_i's are different

##############################################
####################### Apply constraints to  decision variable #######################

## path constraints
a[:,0].value=1
a[:,0].lower=p_l
a[:,0].upper=p_u
a[:,0].integer=True
## mobility service constraints
a[:,1].value=1
a[:,1].lower=h_l
a[:,1].upper=h_u
a[:,1].integer=True
## (o_i,d_i) constraints
a[:,2].value=1
a[:,2].lower=pair_l
a[:,2].upper=pair_u
a[:,2].integer=True
## Theta_i constraints
a[:,3].value=1
a[:,3].lower=theta_l
a[:,3].upper=theta_u
##############################################
####################### Constraints needed to calculate objective function  #######################

## Capacity of each service of a given type- service_map={'1':'car','2':'tram','3':'bus','4':'bike'}
epsilon=[4,100,50,1]
## Range of theta
bar_theta_i=10 # bar superscript theta
theta_i_bar=1  # bar subscript theta
## socio-economic characteristic
alpha_vector=0.5*np.ones(travellers) 
## mean and variance for b() function for each o_i
b_vars={'S':[1,2],'A':[2,3],'B':[1,3]}

####################### Objective function #######################
def pi_i(traveller):
    theta_range=range(1,11)
    pi_i=random.choice(theta_range)
    return pi_i

def b(pair_i):
    o_i=pair_map[pair_i][0]
    myu=b_vars[o_i][0]
    sigma=b_vars[o_i][1]
    b_val=np.random.normal(myu,sigma)
    return b_val

def u_i(a,traveller):
    ### Tau: T(x_i,y_i)
    # Co-traveller set - needs to be defined
    S_o_i=set()
    x_i,y_i=0
    pair_i=a[traveller,2]
    for i in list(S_o_i):
        x_i+=pi_i(traveller)+b(pair_i)

        if (i!=traveller):
            y_i+=pi_i(traveller)+b(pair_i)

    ## Custom Tau function T(x_i,y_i)=(x_i)^2+(y_i)^2

    Tau=(x_i)^2+(y_i)^2

    ### g(theta_i)
    # traveller-1 used for array index beginning with 0 instead of 1
    theta_i=a[traveller-1,3]
    g= bar_theta_i/(theta_i+alpha_vector[traveller-1]*pi_i(traveller))


    u_i=Tau+g


    return u_i
























