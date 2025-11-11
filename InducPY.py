import numpy as np

class part:
    def __init__(self,height,OD,ID,materiel):
        self.height = height
        self.OD = OD
        self.ID = ID
        self.materiel = materiel
        self.volume = 0.25*np.pi*((self.OD**2)-(self.ID**2))
        self.mass = self.volume*self.materiel.density


class materiel:
    def __init__(self, relative_mag_permability,resistance,specific_heat,density):
        self.mag_permability = relative_mag_permability*1.2566e-6
        self.resistance = resistance
        self.specific_heat = specific_heat
        self.density =  density


class coil:
    def __init__(self,ID,materiel,frequency):
        self.ID = ID
        self.materiel = materiel
        self.frequency= frequency



class heating_process:
    def __init__(self,part,coil,start_temp,target_temp):
        self.part = part
        self.coil= coil
        self.delta_T = target_temp-start_temp

    def required_power(self):
        self.delta_part = 1 / np.sqrt((np.pi * self.coil.frequency * self.part.materiel.mag_permability ) / self.part.materiel.resistance)
        self.delta_coil = 1 / np.sqrt((np.pi * self.coil.frequency * self.coil.materiel.mag_permability ) / self.coil.materiel.resistance)
        self.elec_effecincy = 1 / (1 + ((self.coil.ID + self.delta_coil) * self.coil.materiel.resistance * self.delta_coil) / ((self.part.OD - self.delta_part) * self.part.materiel.resistance * self.delta_part))
        return  self.part.mass*self.part.materiel.specific_heat*self.delta_T*self.elec_effecincy


