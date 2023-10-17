from ctypes import cdll, byref
import ctypes as ct
import pandas as pd
import datetime

#---------------------------------------------------------------------------


path_lib="/home/mt_licit/anaconda3/envs/symupy/lib/libSymuFlow.so"
# Parameters
symuvia_input="/home/mt_licit/project/symupy_run/resources/l63v-multiscale/l63v-multiscale.xml"
demand_input="/home/mt_licit/project/symupy_run/resources/l63v-multiscale/l63v-copert_od_matrix_sym.csv"

#---------------------------------------------------------------------------

# Load symuflow libray into memory.
symuflow_lib = cdll.LoadLibrary(path_lib)

if symuflow_lib is None:
    print('error: Symuvia not loaded !')

# SymuVia input loading
m = symuflow_lib.SymLoadNetworkEx(symuvia_input.encode('UTF8'))
if(m!=1):
    print('error: SymuVia input file not loaded !')
else:
    print('SymuVia input data are loaded')

# demand loading
demand = pd.read_csv(demand_input,sep=";")   #columns: origin;typeofvehicle;creation;path;destination

# Init
time=0
bEnd = ct.c_int(0)
period=0
VNC=0
VC=0

#------------------------
# Time step flow calculation
#------------------------
while(bEnd.value==0):

    # Vehicles creation (warning: vehicules with time creation between 0 and 1 are not generated)
    if(time>0):
        squery = str(time) + ' < creation <= ' + str(time+1)
        dts = demand.query(squery)

        for index, row in dts.iterrows():
            tc = ct.c_double(row.creation-time)
            print(row)
            if(row.origin!=row.destination):

                ok = symuflow_lib.SymCreateVehicleEx(row.origin.encode('UTF8'), row.destination.encode('UTF8'), row.typeofvehicle.encode('UTF8'), 1, tc)
                if(ok<0):
                    print('Vehicle not created: ', ok, ' ', row)
                    VNC=VNC+1
                else:
                    VC=VC+1
                    print ("not ok")
                # input('Press Enter')
            else:
                print('Vehicle not created: ', row)
                VNC=VNC+1

    # Time step calculation
    ok = symuflow_lib.SymRunNextStepLiteEx(1, byref(bEnd))
    time=time+1
    # print (time)
    # if time%60==0: print("min  "+str(int(time/60)))
    if time%900==0:  print("ts   "+str(datetime.timedelta(seconds=time)))
    if time%3600==0: print("time "+str(datetime.timedelta(seconds=time)))

if(bEnd.value!=0):
        symuflow_lib.SymUnloadCurrentNetworkEx()
        print(f'Microscopic simulation completed')
        print(VC, ' ', VNC)

del symuflow_lib
