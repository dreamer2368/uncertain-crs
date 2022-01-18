# Copyright (c) 2012, GPy authors (see AUTHORS.txt).
# Licensed under the BSD 3-clause license (see LICENSE.txt)

from GPy.kern import Kern
from GPy.core.parameterization import Param
from paramz.transformations import Logexp
# from paramz.caching import Cache_this
# from GPy.kern.src.psi_comp import PSICOMP_Linear
import numpy as np

class TanhVar(Kern):
    """
    Tanh variance of mean between x1 and x2 in 1D only.

    :param input_dim: the number of input dimensions
    :type input_dim: int
    :param variance:
    :type variance: float
    """
    def __init__(self, input_dim=1, var1=1., var2=1., slope=1., phase=0., active_dims=None, name='TanhVar'):
        assert input_dim==1, "TanhVar supports 1D only"
        super(TanhVar, self).__init__(input_dim, active_dims, name)

        self.var1 = Param('variance1', var1, Logexp())
        self.var2 = Param('variance2', var2, Logexp())
        # self.slope = slope
        # self.phase = phase
        self.slope = Param('slope', slope)
        self.phase = Param('phase', phase)
        self.link_parameters(self.var1)
        self.link_parameters(self.var2)
        self.link_parameters(self.slope)
        self.link_parameters(self.phase)

    def to_dict(self):
        """
        Convert the object into a json serializable dictionary.
        Note: It uses the private method _save_to_input_dict of the parent.
        :return dict: json serializable dictionary containing the needed information to instantiate the object
        """

        input_dict = super(TanhVar, self)._save_to_input_dict()
        input_dict["class"] = "Custom.kern.Tanh_Var"
        return input_dict

    def K(self,X,X2=None):
        if X2 is None:
            X2 = X
        Xm = 0.5 * ( X + X2.T )

        return 0.5 * (self.var1 + self.var2) + 0.5 * (self.var2 - self.var1) * np.tanh( self.slope * Xm + self.phase )

    def Kdiag(self,X):
        Xm = X.flatten()
        return 0.5 * (self.var1 + self.var2) + 0.5 * (self.var2 - self.var1) * np.tanh( self.slope * Xm + self.phase )

    def update_gradients_full(self, dL_dK, X, X2=None):
        if X2 is None:
            X2 = X
        Xm = 0.5 * ( X + X2.T )

        tanhTerm = np.tanh( self.slope * Xm + self.phase )
        self.var1.gradient = np.sum( dL_dK * (0.5 - 0.5 * tanhTerm) )
        self.var2.gradient = np.sum( dL_dK * (0.5 + 0.5 * tanhTerm) )
        self.slope.gradient = np.sum( dL_dK * ( (1.0 - tanhTerm**2) * Xm ) )
        self.phase.gradient = np.sum( dL_dK * (1.0 - tanhTerm**2) )

class TanhDiagVar(Kern):
    """
    Tanh variance of mean between x1 and x2 in 1D only.

    :param input_dim: the number of input dimensions
    :type input_dim: int
    :param variance:
    :type variance: float
    """
    def __init__(self, input_dim=1, var1=1., var2=1., slope=1., phase=0., active_dims=None, name='TanhDiagVar'):
        assert input_dim==1, "TanhVar supports 1D only"
        super(TanhDiagVar, self).__init__(input_dim, active_dims, name)

        self.var1 = Param('variance1', var1, Logexp())
        self.var2 = Param('variance2', var2, Logexp())
        # self.slope = slope
        # self.phase = phase
        self.slope = Param('slope', slope)
        self.phase = Param('phase', phase)
        self.link_parameters(self.var1)
        self.link_parameters(self.var2)
        self.link_parameters(self.slope)
        self.link_parameters(self.phase)

    def to_dict(self):
        """
        Convert the object into a json serializable dictionary.
        Note: It uses the private method _save_to_input_dict of the parent.
        :return dict: json serializable dictionary containing the needed information to instantiate the object
        """

        input_dict = super(TanhDiagVar, self)._save_to_input_dict()
        input_dict["class"] = "Custom.kern.Tanh_Diag_Var"
        return input_dict

    def K(self,X,X2=None):
        if X2 is None:
            X2 = X
        return np.where(X==X2.T, 0.5 * (self.var1 + self.var2) + 0.5 * (self.var2 - self.var1) * np.tanh( self.slope * X + self.phase ), 0.)

    def Kdiag(self,X):
        Xm = X.flatten()
        return 0.5 * (self.var1 + self.var2) + 0.5 * (self.var2 - self.var1) * np.tanh( self.slope * Xm + self.phase )

    def update_gradients_full(self, dL_dK, X, X2=None):
        if X2 is None:
            X2 = X

        tanhTerm = np.where(X==X2.T, np.tanh( self.slope * X + self.phase ), 0.)
        self.var1.gradient = np.sum( dL_dK * np.where(X==X2.T, 0.5 - 0.5 * tanhTerm, 0.) )
        self.var2.gradient = np.sum( dL_dK * np.where(X==X2.T, 0.5 + 0.5 * tanhTerm, 0.) )
        self.slope.gradient = np.sum( dL_dK * np.where(X==X2.T, (1.0 - tanhTerm**2) * X, 0.) )
        self.phase.gradient = np.sum( dL_dK * np.where(X==X2.T, 1.0 - tanhTerm**2, 0.) )

class SinDiagVar(Kern):
    """
    Sin variance of mean between x1 and x2 in 1D only.

    :param input_dim: the number of input dimensions
    :type input_dim: int
    :param variance:
    :type variance: float
    """
    def __init__(self, input_dim=1, var1=1., var2=1., slope=1., phase=0., active_dims=None, name='SinDiagVar'):
        assert input_dim==1, "SinVar supports 1D only"
        super(SinDiagVar, self).__init__(input_dim, active_dims, name)

        self.var1 = Param('variance1', var1, Logexp())
        self.var2 = Param('variance2', var2, Logexp())
        # self.slope = slope
        # self.phase = phase
        self.slope = Param('slope', slope)
        self.phase = Param('phase', phase)
        self.link_parameters(self.var1)
        self.link_parameters(self.var2)
        self.link_parameters(self.slope)
        self.link_parameters(self.phase)

    def to_dict(self):
        """
        Convert the object into a json serializable dictionary.
        Note: It uses the private method _save_to_input_dict of the parent.
        :return dict: json serializable dictionary containing the needed information to instantiate the object
        """

        input_dict = super(SinDiagVar, self)._save_to_input_dict()
        input_dict["class"] = "Custom.kern.Sin_Diag_Var"
        return input_dict

    def K(self,X,X2=None):
        if X2 is None:
            X2 = X
        return np.where(X==X2.T, 0.5 * (self.var1 + self.var2) + 0.5 * (self.var2 - self.var1) * np.sin( self.slope * X + self.phase ), 0.)

    def Kdiag(self,X):
        Xm = X.flatten()
        return 0.5 * (self.var1 + self.var2) + 0.5 * (self.var2 - self.var1) * np.sin( self.slope * Xm + self.phase )

    def update_gradients_full(self, dL_dK, X, X2=None):
        if X2 is None:
            X2 = X

        sinTerm = np.where(X==X2.T, np.sin( self.slope * X + self.phase ), 0.)
        self.var1.gradient = np.sum( dL_dK * np.where(X==X2.T, 0.5 - 0.5 * sinTerm, 0.) )
        self.var2.gradient = np.sum( dL_dK * np.where(X==X2.T, 0.5 + 0.5 * sinTerm, 0.) )
        self.slope.gradient = np.sum( dL_dK * np.where(X==X2.T, (1.0 - sinTerm**2) * X, 0.) )
        self.phase.gradient = np.sum( dL_dK * np.where(X==X2.T, 1.0 - sinTerm**2, 0.) )

class ExpDiagVar(Kern):
    """
    Sin variance of mean between x1 and x2 in 1D only.

    :param input_dim: the number of input dimensions
    :type input_dim: int
    :param variance:
    :type variance: float
    """
    def __init__(self, input_dim=1, variance=1., slope=1., phase=0., active_dims=None, name='ExpDiagVar'):
        assert input_dim==1, "ExpVar supports 1D only"
        super(ExpDiagVar, self).__init__(input_dim, active_dims, name)

        self.variance = Param('variance', variance, Logexp())
        # self.var2 = Param('variance2', var2, Logexp())
        self.slope = Param('slope', slope, Logexp())
        self.phase = Param('phase', phase)
        self.link_parameters(self.variance)
        self.link_parameters(self.slope)
        self.link_parameters(self.phase)

    def to_dict(self):
        """
        Convert the object into a json serializable dictionary.
        Note: It uses the private method _save_to_input_dict of the parent.
        :return dict: json serializable dictionary containing the needed information to instantiate the object
        """

        input_dict = super(ExpDiagVar, self)._save_to_input_dict()
        input_dict["class"] = "Custom.kern.Exp_Diag_Var"
        return input_dict

    def K(self,X,X2=None):
        if X2 is None:
            X2 = X
        return np.where(X==X2.T, self.variance * np.exp( - self.slope * (X - self.phase)**2 ), 0.)

    def Kdiag(self,X):
        Xm = X.flatten()
        return self.variance * np.exp( - self.slope * (Xm - self.phase)**2 )

    def update_gradients_full(self, dL_dK, X, X2=None):
        if X2 is None:
            X2 = X

        expTerm = np.where(X==X2.T, np.exp( - self.slope * (X - self.phase)**2 ), 0.)
        self.variance.gradient = np.sum( dL_dK * np.where(X==X2.T, expTerm, 0.) )
        self.slope.gradient = np.sum( dL_dK * np.where(X==X2.T, - self.variance * expTerm * (X - self.phase)**2, 0.) )
        self.phase.gradient = np.sum( dL_dK * np.where(X==X2.T, self.variance * expTerm * (-2.0 * self.slope) * (self.phase - X), 0.) )
