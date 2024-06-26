import numpy as np
from .phys_const import muBcm,ge
from koehnlab import print_utilities

def get_magnetic_moment_matrix(sMat,lMat,unit: bool):
        """
        Computes the magnetic moment of the system in the basis of given spin and angular momentum matrix
        Procedure taken from: L. F. Chibotaru, L. Ungur; Ab initio calculation of anisotropic magnetic properties of complexes. I. Unique definition of
        pseudospin Hamiltonians and their derivation. J. Chem. Phys. 14 August 2012; 137 (6): 064112. https://doi.org/10.1063/1.4739763
        Args:
        ---------------------
        sMat -- spin matrix 
        lmat -- angular momentum matrix
        unit -- Boolean if in multiples of bohr magneton

        Returns:
        ---------------------
        muMat -- matrix of magnetic moment 
        """
        if unit:
            muMat = -muBcm*(ge*sMat+lMat)
        else: 
            muMat = -1*(ge*sMat+lMat)
        return muMat

def get_A_matrix(mu_x,mu_y,mu_z,n):
        """
        Computes the A matrix to calculate g-Tensor afterwards
        Procedure taken from: L. F. Chibotaru, L. Ungur; Ab initio calculation of anisotropic magnetic properties of complexes. I. Unique definition of
        pseudospin Hamiltonians and their derivation. J. Chem. Phys. 14 August 2012; 137 (6): 064112. https://doi.org/10.1063/1.4739763
        Args:
        ---------------------
        mu_x,y,z -- matrices of magnetic moment in SO basis in every dimension in J/T
        n -- number of states that are crucial, only needed if pseudospin is used so not all states are included in calculation

        Returns:
        ---------------------
        Amat -- helper matrix for g-Tensor
        """
        mu_x_n = mu_x[:n,:n]
        mu_y_n = mu_y[:n,:n]
        mu_z_n = mu_z[:n,:n]
        mu = [mu_x_n,mu_y_n,mu_z_n]
        print_utilities.printMatF(mu_x_n)
        Amat = np.zeros((3,3))
        for alpha in range(3):
                for beta in range(3):
                        prod = np.matmul(mu[alpha],mu[beta])
                        trace = np.matrix.trace(prod)
                        assert np.abs(trace.imag) < 1E-6
                        Amat[alpha,beta] = 0.5*trace.real
        return Amat

def get_g_tensor(Amat,multiplicity:int):
        """
        returns the g-Tensorin cartesian coordinates and his main values with given multiplicity of the system,
        also returns the rotation matrix between main axes and main magnetic axes. 
        Procedure taken from: L. F. Chibotaru, L. Ungur; Ab initio calculation of anisotropic magnetic properties of complexes. I. Unique definition of
        pseudospin Hamiltonians and their derivation. J. Chem. Phys. 14 August 2012; 137 (6): 064112. https://doi.org/10.1063/1.4739763
        Args:
        ----------------------
	Amat -- helpermatrix from from above
        multiplicity -- multiplicity of the system

        Returns:
        ----------------------
        g_diag -- eigenvalues of g-Tensor on diagonal
        Rmat -- rotation matrix
        """
        S = 0.5*(multiplicity-1)
        g_diag = np.zeros(np.shape(Amat))
        eigvalA,Rmat = np.linalg.eigh(Amat)
        print(eigvalA)
        for i in range(len(eigvalA)):
                g_diag[i,i] = np.sqrt((6*eigvalA[i])/(S*(S+1)*(2*S+1)))
        return g_diag,Rmat
