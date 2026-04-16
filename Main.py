from fontTools.ttx import process

import InducPY,InducPY_materials


Test_part = InducPY.Part(0.155, 0.05757, 0, InducPY_materiels.Inconel_718)
Coil = InducPY.Coil(120, InducPY_materiels.Copper_C1000, 120)
Process = InducPY.Heating_process(Test_part,Coil,20,1200)
print(Process.required_power())