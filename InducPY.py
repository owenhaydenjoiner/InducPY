import numpy as np

class Part:
    def __init__(self, height, OD, ID, Material):
        self.height = height
        self.OD = Oa
        self.ID = ID
        self.Material = Material
        self.volume = 0.25*np.pi*((self.OD**2)-(self.ID**2))
        self.mass = self.volume*self.Material.density


class Material:
    def __init__(self, relative_mag_permability,resistance,specific_heat,density):
        self.mag_permability = relative_mag_permability*1.2566e-6
        self.resistance = resistance
        self.specific_heat = specific_heat
        self.density =  density


class Coil:
    def __init__(self,id,Material,frequency):
        self.ID = id
        self.Material = Material
        self.frequency= frequency



class Heating_process:
    def __init__(self,Part,Coil,start_temp,target_temp):
        self.Part = Part
        self.Coil = Coil
        self.delta_T = target_temp-start_temp

    def required_power(self):
        self.delta_part = 1 / np.sqrt((np.pi * self.Coil.frequency * self.Part.Material.mag_permability) / self.Part.Material.resistance)
        self.delta_coil = 1 / np.sqrt((np.pi * self.Coil.frequency * self.Coil.Material.mag_permability) / self.Coil.Material.resistance)
        self.elec_effecincy = 1 / (1 + ((self.Coil.ID + self.delta_coil) * self.Coil.Material.resistance * self.delta_coil) / ((self.Part.OD - self.delta_part) * self.Part.Material.resistance * self.delta_part))
        return  self.Part.mass*self.Part.Material.specific_heat*self.delta_T*self.elec_effecincy


