import numpy as np

class Part:
    def __init__(self,height,OD,ID,materiel):
        self.height = height
        self.OD = OD
        self.ID = ID
        self.materiel = materiel
        self.volume = 0.25*np.pi*((self.OD**2)-(self.ID**2))
        self.mass = self.volume*self.materiel.density


class Materiel:
    def __init__(self, relative_mag_permability,resistance,specific_heat,density):
        self.mag_permability = relative_mag_permability*1.2566e-6
        self.resistance = resistance
        self.specific_heat = specific_heat
        self.density =  density


class Coil:
    def __init__(self,ID,materiel,frequency):
        self.ID = ID
        self.materiel = materiel
        self.frequency= frequency



class Heating_process:
    def __init__(self,part,coil,start_temp,target_temp):
        self.Part = part
        self.Coil = coil
        self.delta_T = target_temp-start_temp

    def required_power(self):
        self.delta_part = 1 / np.sqrt((np.pi * self.Coil.frequency * self.Part.Materiel.mag_permability) / self.Part.Materiel.resistance)
        self.delta_coil = 1 / np.sqrt((np.pi * self.Coil.frequency * self.Coil.Materiel.mag_permability) / self.Coil.Materiel.resistance)
        self.elec_effecincy = 1 / (1 + ((self.Coil.ID + self.delta_coil) * self.Coil.Materiel.resistance * self.delta_coil) / ((self.Part.OD - self.delta_part) * self.Part.Materiel.resistance * self.delta_part))
        return  self.Part.mass*self.Part.Materiel.specific_heat*self.delta_T*self.elec_effecincy


