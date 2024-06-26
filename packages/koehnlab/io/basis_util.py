import numpy as np
import math as m
from koehnlab.spin_hamiltonians import spin_utils

def get_propmat_prod(lMat,multiplicity:int,spat_num:int):
        """
        Returns the given l matrix in productbasis (spin-spatial basis).
        Args:
        ---------------------
        lMat -- matrix of angular momentum
        multiplicity -- multiplicity of the system
        spat_num - number of spatial states
        Returns:
        ---------------------
        Lmat -- Matrix of angular momentum in productbasis 
        """
        dim = int(multiplicity*spat_num)
        Lmat = np.zeros((dim,dim),dtype = complex)
        for x in range(dim):
                for y in range(dim):
                        ms = m.floor(x/spat_num)
                        ms_strich = m.floor(y/spat_num)
                        i = int(x%spat_num)
                        j = int(y%spat_num)
                        if ms == ms_strich:
                            Lmat[x,y] = lMat[i,j]
        return Lmat

def get_spinmat_prod(sMat,multiplicity:int,spat_num:int):
        """
        Computes the spin matrix elements of the given spin matrix in the productbasis (spin-spatial basis).
        Blocked over ms number.
        Args:
        ------------------------
        sMat -- spin matrix in spin basis
        multiplicity -- Multiplicity of the system
        spat_num -- number of spatial states

        Returns:
        ------------------------
        SmatX,SmatY,SmatZ -- spin matrix in the productbasis 
        """
        dim = int(multiplicity*spat_num)
        spin = 0.5*(multiplicity-1)
        Smat = np.zeros((dim,dim),dtype = complex)
        if spin == 0:
                return Smat
        else:
                for x in range(dim):
                    for y in range(dim):
                        ms = m.floor(x/spat_num)
                        ms_strich = m.floor(y/spat_num)
                        i = x%spat_num
                        j = y%spat_num
                        if i==j:
                                Smat[x,y] = sMat[ms,ms_strich]
        return Smat

def get_multispinmat_wf0(spins,coord:str):
     """
     Returns the spin matrix of all given Spins in the WF0-basis, the basis of zeroth order wavefunctions
     for all spins.
     
     Args:
     -----------------------------
     spins -- array of multiple spin states, sorted in descending order
     coord -- string with possible values: 'x','y','z'
     
     Returns:
     -----------------------------
     SMat -- Spin Matrix for multiple spins

     """
     multiplicities = [2*S+1 for S in spins]
     dim = int(np.sum(multiplicities))
     SMat = np.zeros((dim,dim),dtype = complex)
     lower_bound = 0
     upper_bound = 0
     for i,mult in enumerate(multiplicities):
          spin_mat_coord = spin_utils.spinMat(spins[i],coord)
          upper_bound += int(mult)
          assert upper_bound - lower_bound == np.shape(spin_mat_coord)[0]
          assert upper_bound - lower_bound == np.shape(spin_mat_coord)[1]
          SMat[lower_bound:upper_bound,lower_bound:upper_bound] = spin_mat_coord
          lower_bound = upper_bound
     return SMat


def get_multispinmat_prod(spins,spat_nums,coord:str):
        """
        Returns the spin matrix of all given Spins S in the productbasis of spin and spatial basis, 
        of all spins and all spatial coordinates

        Args:
        --------------------------
        spins -- array of multiple spin states, sorted in descending order
        spat_nums -- array of numbers of spatial states corresponding to the spin states
        coord -- x,y,z

        Returns:
        --------------------------
        Smat -- spin matrix in Productbasis of given spin and spatial states in Js
        """
        assert len(spins) == len(spat_nums)
        multiplicities = [2*S+1 for S in spins]
        dim = int(np.sum(multiplicities*spat_nums))
        Smat = np.zeros((dim,dim),dtype = complex)
        lower_bound = 0
        upper_bound = 0
        for i,mult in enumerate(multiplicities):
            Spin = (mult-1)/2
            spinmat_coord = spin_utils.spinMat(Spin,coord)
            spinmat_prod = get_spinmat_prod(spinmat_coord,mult,spat_nums[i])
            upper_bound += int(mult*spat_nums[i])
            shape = np.shape(spinmat_prod)
            diff = upper_bound - lower_bound
            assert diff == shape[0]
            assert diff == shape[1]
            Smat[lower_bound:upper_bound,lower_bound:upper_bound] = spinmat_prod
            lower_bound = upper_bound
        return Smat

def get_multipropmat_prod(lMat,spins,spat_nums):
        """
        Calculates the l matrix in the productbasis for multiple spins

        Args:
        --------------------------
        lMat -- matrix of angular momentum that needs to be transformed in the basis for multiple spins in (kg*m^2)/s
        spins -- array of multiple spin states, sorted in ascending order 
        spat_nums -- array of numbers of spatial states corresponding to the spin states

        Returns:
        --------------------------
        Lmat -- matrix of angular momentum in Productbasis of given spin and spatial states in (kg*m^2)/s
        """
        assert len(spins) == len(spat_nums)
        multiplicities = [2*S+1 for S in spins]
        dim = int(np.sum(multiplicities*spat_nums))
        Lmat = np.zeros((dim,dim),dtype = complex)
        lower_bound = 0
        upper_bound = 0
        for mult in multiplicities:
            i = multiplicities.index(mult)
            if (i == 0):
                spat_num = int(spat_nums[i])
                #print(spat_nums[i])
                lmat = lMat[:spat_num,:spat_num]
                propmat_prod = get_propmat_prod(lmat,mult,spat_nums[i])
            else:
                propmat_prod = get_propmat_prod(lMat[int(spat_nums[i-1]):int(sum(spat_nums[:i+1])),int(spat_nums[i-1]):int(sum(spat_nums[:i+1]))],mult,spat_nums[i])
            upper_bound += int(mult*spat_nums[i])
            shape = np.shape(propmat_prod)
            diff = upper_bound-lower_bound
            assert diff == shape[0]
            assert diff == shape[1]
            Lmat[lower_bound:upper_bound,lower_bound:upper_bound] = propmat_prod
            lower_bound = upper_bound
        return Lmat

def transform_so(Mat,eigvecs):
        """
        Transforms a given matrix m into the SO basis

        Args:
        ---------------------
        Mat -- matrix which is transformed to SO basis
        eigvecsh -- eigenvectors of the SO matrix to perform the transformation

        Returns:
        --------------------
        Mmat -- matrix m transformed into SO basis
        """
        Mmat = np.matmul(np.conj(eigvecs.T),np.matmul(Mat,eigvecs))
        return Mmat




