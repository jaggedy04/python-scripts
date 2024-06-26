import numpy as np
import h5py
from enum import Enum
from koehnlab import print_utilities
from koehnlab.io import basis_util
from koehnlab.spin_hamiltonians import spin_utils

#class Basis(Enum):
#    WF0 = "WF0"
#    PROD = "PROD"
#    SO = "SO"

def get_2dmat(matrix_3d):
        '''
        reshape
        Transforming a three dimensional matrix containing complex values in the third dimension (first index) into two dimensional complex matrix

        Args:
        ------------------------
        matrix_3d -- 3 dimensional matrix containing the complex values as third dimension

        Returns:
        ------------------------
        2d_matrix -- two dimensional complex matrix
        '''
        matrix = np.zeros((np.shape(matrix_3d)[1],np.shape(matrix_3d)[2]),dtype = complex)
        for i in range(np.shape(matrix_3d)[1]):
                for j in range(np.shape(matrix_3d)[2]):
                        matrix[i,j] = complex(matrix_3d[0,i,j] , matrix_3d[1,i,j])
        return matrix


def get_property_matrix(path:str,prop:str,basis:str):
    '''
    Returns the matrix of a given operator in a given basis which is stored
    in a HDF5 File in the given path.

    Args:
    ----------------------
    path -- The path the HDF5 file is stored
    prop -- the operator of which the matrix is extracted from Molpro. 
            (DMX,DMY,DMZ,LX(),LY(),LZ(),SOC matrix)
    basis -- the basis in which the property matrix should be returned. 
  	     Choose one of the three options of Basis Enum
    Returns:
    ---------------------
    PropMat -- The property matrix of given operator in the given basis

    '''
    with h5py.File(path,'r') as h5file:
        SpinStates = h5file['Spin QNs'][:] # type: ignore
        SpatStates = h5file['Spatial states'][:] # type: ignore
        SpinStates = np.array(SpinStates)
        SpatStates = np.array(SpatStates)
        SO = h5file['SOC matrix'][:] # type: ignore
        SO_2dmat = get_2dmat(SO)
        if prop == 'SO':
             return SO_2dmat
        elif(prop[0] == 'D'):
            PropMat = h5file[prop][:] # type: ignore
        elif(prop[0] == 'L'):
            PropMat = -1j*h5file[prop][:] # type: ignore
        else:
            raise Exception("an error occurred","unexpected value for matrix")
    if basis == 'WF0':
        return PropMat
    elif basis == 'PROD':
            PropMat = basis_util.get_multipropmat_prod(PropMat,SpinStates,SpatStates)
            return PropMat
    elif basis == 'SO':
        PropMat = basis_util.get_multipropmat_prod(PropMat,SpinStates,SpatStates)
        #print(np.shape(PropMat))
        eigvalsh,eigvecsh = np.linalg.eigh(SO_2dmat)
        PropMat = basis_util.transform_so(PropMat,eigvecsh)
        return PropMat
    else:
        raise Exception("an error occurred","unexpected value for basis")



def get_spin_spat_states(path:str):
    """
    Returns the spin states of the system and the associated number of spatial states in an 1d array
    
    Args:
    -----------------------
    path -- the path to the HDF5 File where the arrays from Molpro are stored

    Returns:
    -----------------------
    SpinStates -- the Spin states of the system in descending order
    SpatStates -- the number of spatial states associated to the spin states
    """
    with h5py.File(path,'r') as h5file:
        SpinStates = h5file['Spin QNs'][:] # type: ignore
        SpatStates = h5file['Spatial states'][:] # type: ignore
        SpinStates = np.array(SpinStates)
        SpatStates = np.array(SpatStates)
    return SpinStates, SpatStates

