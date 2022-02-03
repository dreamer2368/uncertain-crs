import torch
import numpy as np
torch.set_default_dtype(torch.float64)

class ExpKernel(torch.nn.Module):
    def __init__(self):
        """
        In the constructor we instantiate four parameters and assign them as
        member parameters.
        """
        super().__init__()
        self.var = torch.nn.Parameter(1.0 + 0.1 * torch.randn(()))
        self.scale = torch.nn.Parameter(1.0 + 0.1 * torch.randn(()))
        self.var.clamp(min=0.0)
        self.scale.clamp(min=0.0)

    def forward(self, xd):
        """
        In the forward function we accept a Tensor of input data and we must return
        a Tensor of output data. We can use Modules defined in the constructor as
        well as arbitrary operators on Tensors.
        """
        return self.var * torch.exp( - xd ** 2 / self.scale )
    
    def covariance(self, x1, x2):
        assert((x1.dim()==1) and (x2.dim()==1))
        xd = x1.repeat(x2.size(0),1).t() - x2.repeat(x1.size(0),1)
        return self.var * torch.exp( - xd ** 2 / self.scale )
    
class ExpKernelPack(torch.nn.Module):
    def __init__(self,n=1,requires_grad=True):
        """
        In the constructor we instantiate four parameters and assign them as
        member parameters.
        """
        super().__init__()
        self.n = n
        self.var = torch.nn.Parameter(1.0 + 0.1 * torch.randn(n),requires_grad=requires_grad)
        self.scale = torch.nn.Parameter(1.0 + 0.1 * torch.randn(n),requires_grad=requires_grad)
        self.var.clamp(min=0.0)
        self.scale.clamp(min=0.0)

    def forward(self, n, xd):
        """
        In the forward function we accept a Tensor of input data and we must return
        a Tensor of output data. We can use Modules defined in the constructor as
        well as arbitrary operators on Tensors.
        """
        return self.var[n] * torch.exp( - xd ** 2 / self.scale[n] )
    
    def covariance(self, n, x1, x2):
        assert((x1.dim()==1) and (x2.dim()==1))
        xd = x1.repeat(x2.size(0),1).t() - x2.repeat(x1.size(0),1)
        return self.var[n] * torch.exp( - xd ** 2 / self.scale[n] )
    
class MaternPack(torch.nn.Module):
    def __init__(self,n,nu=1.5,requires_grad=True):
        """
        In the constructor we instantiate four parameters and assign them as
        member parameters.
        """
        if nu not in {0.5, 1.5, 2.5}:
            raise RuntimeError("nu expected to be 0.5, 1.5, or 2.5")
        super().__init__()
        self.nu = nu
        self.var = torch.nn.Parameter(2.0 + 0.1 * torch.randn(n),requires_grad=requires_grad)
        self.scale = torch.nn.Parameter(2.0 + 0.1 * torch.randn(n),requires_grad=requires_grad)
        self.var.clamp(min=0.0)
        self.scale.clamp(min=0.0)

    def forward(self, n, xd):
        import math
        """
        In the forward function we accept a Tensor of input data and we must return
        a Tensor of output data. We can use Modules defined in the constructor as
        well as arbitrary operators on Tensors.
        """
        expComponent = torch.exp( - math.sqrt(self.nu * 2) * torch.abs(xd) / self.scale[n] )
        
        if (self.nu == 0.5):
            constant_component = 1.0
        elif (self.nu == 1.5):
            constant_component = 1.0 + math.sqrt(3) * torch.abs(xd) / self.scale[n]
        elif (self.nu == 2.5):
            constant_component = 1.0 + math.sqrt(5) * torch.abs(xd) / self.scale[n] + 5.0 / 3.0 * torch.abs(xd) ** 2 / (self.scale[n]**2)
        return self.var[n] * constant_component * expComponent
    
    def covariance(self, n, x1, x2):
        import math
        assert((x1.dim()==1) and (x2.dim()==1))
        xd = x1.repeat(x2.size(0),1).t() - x2.repeat(x1.size(0),1)
        
        expComponent = torch.exp( - math.sqrt(self.nu * 2) * torch.abs(xd) / self.scale[n])
        
        if (self.nu == 0.5):
            constant_component = 1.0
        elif (self.nu == 1.5):
            constant_component = 1.0 + math.sqrt(3) * torch.abs(xd) / self.scale[n]
        elif (self.nu == 2.5):
            constant_component = 1.0 + math.sqrt(5) * torch.abs(xd) / self.scale[n] + 5.0 / 3.0 * torch.abs(xd) ** 2 / (self.scale[n]**2)
        return self.var[n] * constant_component * expComponent