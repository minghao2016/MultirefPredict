#######################################################################
#  This script reads in the json file generated by MultirefPredict 
#  add generate the Gaussian Cube format output containing the 
#  I_ND and I_D density for visualizing the electron density related
#  static and dynamic correlation
####################################################################
import sys
import subprocess
import math
import json

def help_msg():
    print("Usage: python generate_IND_density.py [multirefPredi_generated_json_file]")

def sanity_check():
    if len(sys.argv) < 2:
        help_msg()
        exit()

    try:
        fin=open(sys.argv[1])
    except OSError:
        print("Cannot open file ",sys.argv[1])
        help_msg()
        exit()
    return fin
    

def parse_json_input():

    fin = sanity_check()

    try:
        multiref_dict = json.load(fin)
    except json.JSONDecodeError:
        print("The provided file object cannot be deserialized with json")
        help_msg()
    
        exit()
    
    FON_stdout = multiref_dict['stdout'].splitlines()

    #write the molden file
    molden_str =  multiref_dict['extras']['scr/geometry.molden']
    #molden_name = sys.argv[1].replace(".json",".molden")
    molden_name = "geometry.molden"
    with open(molden_name,"w") as f:
        f.write(molden_str)

    return FON_stdout,molden_name

def parse_tc_stdout(FON_stdout):
    norb = 0
    fons ={}
    restricted = False
    
    # Parse output file and extract FON
    for i in range(0,len(FON_stdout)):
        if "Wavefunction: RESTRICTED" in FON_stdout[i]:
            restricted = True
        if "Total orbitals" in FON_stdout[i]:
            norb = int(FON_stdout[i].strip('\n').split()[-1])
        if "SCF Fractional Occupations" in FON_stdout[i]:
            nlines = int(math.ceil(float(norb)/4))
            for j in range(i+3, i+3+nlines):
                line = FON_stdout[j].strip('\n').split()
                for k in range(0,len(line)):
                    if k%2 == 0:
                        idx = int(line[k])
                        fon = float(line[k+1])
                        if fon > 1e-6 and fon < 1.0:
                            fons[idx] = fon
    return fons,restricted

# Calculate the related multiwfn input files
def gen_multiwfn_input(fons, restricted):
    I_ND_wfn_name = "I_ND.multiwfn"
    I_ND_wfn_input = open(I_ND_wfn_name, "w")
    
    I_D_wfn_name = "I_D.multiwfn"
    I_D_wfn_input = open(I_D_wfn_name, "w")
    
    I_ND_cub_name = "I_ND.cub"
    I_D_cub_name = "I_D.cub"
    
    keycount = 0
    factor = 2.0 if restricted else 1.0
    for key,value in fons.items():
        my_I_T = 0.25 * math.sqrt(value * (1-value)) * factor
    
        my_I_ND = 0.5* value * (1-value) * factor
    
        my_I_D = my_I_T - my_I_ND
    
        # Generate Multiwfn input files used for generating real space I_ND function
        if keycount == 0:
            I_ND_wfn_input.write("5\n4\n{0:d}\n1\n0\n13\n11\n9\n2.0".format(key)+\
                    "\n11\n5\n{0:f}\n0\n{1:s}\n-1\n".format(my_I_ND, I_ND_cub_name))
            I_D_wfn_input.write("5\n4\n{0:d}\n1\n0\n13\n11\n9\n2.0".format(key)+\
                    "\n11\n5\n{0:f}\n0\n{1:s}\n-1\n".format(my_I_D, I_D_cub_name))
        else:
            I_ND_wfn_input.write("5\n4\n{0:d}\n1\n0\n13\n11\n9\n2.0".format(key)+\
                    "\n11\n5\n{0:f}\n11\n2\n{1:s}\n0\n{1:s}\n-1\n".format(my_I_ND, I_ND_cub_name))
            I_D_wfn_input.write("5\n4\n{0:d}\n1\n0\n13\n11\n9\n2.0".format(key)+\
                    "\n11\n5\n{0:f}\n11\n2\n{1:s}\n0\n{1:s}\n-1\n".format(my_I_D, I_D_cub_name))
        keycount += 1
    
    I_ND_wfn_input.close()
    I_D_wfn_input.close()
    
    return I_ND_wfn_name,I_D_wfn_name


def generate_IND_cubes():
    FON_stdout,molden_name = parse_json_input()
    fons,restricted = parse_tc_stdout(FON_stdout)
    I_ND_wfn_name,I_D_wfn_name = gen_multiwfn_input(fons, restricted)
   #Execute Multiwfn to generate the cube files
    cmd = "Multiwfn "+molden_name + " <" +I_ND_wfn_name
    print(cmd)
    subprocess.run(cmd,shell=True)
    
    cmd = "Multiwfn "+molden_name + " <" + I_D_wfn_name 
    print(cmd)
    subprocess.run(cmd,shell=True)

if __name__ == "__main__":
    generate_IND_cubes()