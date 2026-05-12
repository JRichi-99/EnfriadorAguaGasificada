from Elements.Coil import Coil
from Elements.Shell import Shell
from Elements.Singularities import SingularityLoss
from Elements.Tube import Tube

class FluxSystem():
    def __init__(self):
        self.n_elements = 0
        self.system = []
        self.tubes = []
        self.singularities = []
        self.volume = 0
    
    def add_element(self, element):
        self.system.append(element)
        if isinstance(element, Tube):
            self.tubes.append((element, self.n_elements))
        elif isinstance(element, SingularityLoss):
            self.singularities.append((element, self.n_elements))
        self.n_elements += 1

    def add_coil(self, element: Coil):
        self.add_element(element)
        
    def add_shell(self, element: Shell):
        self.add_element(element)
    
    def add_tube(self, element: Tube):
        self.add_element(element)
    
    def add_singularity_loss(self, element: SingularityLoss):
        self.add_element(element)

    def conect(self):
        for i, element in enumerate(self.system):
            if i == 0 or i == self.n_elements-1:
                continue
            if isinstance(element, SingularityLoss):
                element.set_in_out(self.system[i-1], self.system[i+1])
    
    def get_volume(self):
        self.volume = 0
        for element in self.system:
            if isinstance(element, Shell):
                self.volume += element.vol_in_free
            elif isinstance(element, Tube):
                self.volume += element.vol_in
        return self.volume
    




            
            
            
        
        
            


    

    

        