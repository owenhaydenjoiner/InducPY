# Induction Heating Calculator

A Python module for modelling induction heating processes, calculating required power based on part geometry, material properties, and coil parameters.

## Dependencies

- `numpy`

---

## Classes

### `Material`

Represents a material with physical properties relevant to induction heating.

**Constructor:** `Material(relative_mag_permability, resistance, specific_heat, density)`

| Parameter | Type | Description |
|---|---|---|
| `relative_mag_permability` | `float` | Relative magnetic permeability (dimensionless). Internally converted to absolute permeability (H/m) |
| `resistance` | `float` | Electrical resistivity (Ω·m) |
| `specific_heat` | `float` | Specific heat capacity (J/kg·K) |
| `density` | `float` | Material density (kg/m³) |

**Attributes:**

| Attribute | Description |
|---|---|
| `mag_permability` | Absolute magnetic permeability in H/m (`relative × 1.2566e-6`) |
| `resistance` | Electrical resistivity (Ω·m) |
| `specific_heat` | Specific heat capacity (J/kg·K) |
| `density` | Density (kg/m³) |

---

### `Part`

Represents a hollow cylindrical part to be heated.

**Constructor:** `Part(height, OD, ID, material)`

| Parameter | Type | Description |
|---|---|---|
| `height` | `float` | Height of the part (m) |
| `OD` | `float` | Outer diameter (m) |
| `ID` | `float` | Inner diameter (m) |
| `material` | `Material` | Material of the part |

**Attributes:**

| Attribute | Description |
|---|---|
| `volume` | Cross-sectional volume calculated as `0.25 × π × (OD² - ID²)` (m³) |
| `mass` | Mass calculated as `volume × density` (kg) |

---

### `Coil`

Represents the induction coil used to heat the part.

**Constructor:** `Coil(ID, material, frequency)`

| Parameter | Type | Description |
|---|---|---|
| `ID` | `float` | Inner diameter of the coil (m) |
| `material` | `Material` | Material the coil is made from |
| `frequency` | `float` | Operating frequency of the coil (Hz) |

---

### `Heating_process`

Models the induction heating process and calculates the required power.

**Constructor:** `Heating_process(part, coil, start_temp, target_temp)`

| Parameter | Type | Description |
|---|---|---|
| `part` | `Part` | The part being heated |
| `coil` | `Coil` | The induction coil |
| `start_temp` | `float` | Initial temperature (°C or K) |
| `target_temp` | `float` | Target temperature (°C or K) |

#### Method: `required_power()`

Calculates the power (W) required to heat the part to the target temperature.

**Returns:** `float` — Required power in Watts.

Internally computes:

- **`delta_part`** — Skin depth of the part (m):
$$\delta_{part} = \frac{1}{\sqrt{\pi \cdot f \cdot \mu_{part} / \rho_{part}}}$$

  | Symbol | Description | Unit |
  |---|---|---|
  | $\delta_{part}$ | Electromagnetic skin depth of the part — the depth at which induced current density falls to ~37% of its surface value | m |
  | $f$ | Coil operating frequency (`Coil.frequency`) | Hz |
  | $\mu_{part}$ | Absolute magnetic permeability of the part (`Part.material.mag_permability`) | H/m |
  | $\rho_{part}$ | Electrical resistivity of the part (`Part.material.resistance`) | Ω·m |

- **`delta_coil`** — Skin depth of the coil (m):
$$\delta_{coil} = \frac{1}{\sqrt{\pi \cdot f \cdot \mu_{coil} / \rho_{coil}}}$$

  | Symbol | Description | Unit |
  |---|---|---|
  | $\delta_{coil}$ | Electromagnetic skin depth of the coil | m |
  | $f$ | Coil operating frequency (`Coil.frequency`) | Hz |
  | $\mu_{coil}$ | Absolute magnetic permeability of the coil (`Coil.material.mag_permability`) | H/m |
  | $\rho_{coil}$ | Electrical resistivity of the coil (`Coil.material.resistance`) | Ω·m |

- **`elec_efficiency`** — Electrical coupling efficiency (dimensionless):
$$\eta = \frac{1}{1 + \frac{(ID_{coil} + \delta_{coil}) \cdot \rho_{coil} \cdot \delta_{coil}}{(OD_{part} - \delta_{part}) \cdot \rho_{part} \cdot \delta_{part}}}$$

  | Symbol | Description | Unit |
  |---|---|---|
  | $\eta$ | Electrical coupling efficiency — fraction of coil power transferred to the part | dimensionless |
  | $ID_{coil}$ | Inner diameter of the coil (`Coil.ID`) | m |
  | $\delta_{coil}$ | Skin depth of the coil (from above) | m |
  | $\rho_{coil}$ | Electrical resistivity of the coil (`Coil.material.resistance`) | Ω·m |
  | $OD_{part}$ | Outer diameter of the part (`Part.OD`) | m |
  | $\delta_{part}$ | Skin depth of the part (from above) | m |
  | $\rho_{part}$ | Electrical resistivity of the part (`Part.material.resistance`) | Ω·m |

- **Required power:**
$$P = m \cdot c_p \cdot \Delta T \cdot \eta$$

  | Symbol | Description | Unit |
  |---|---|---|
  | $P$ | Required power to heat the part | W |
  | $m$ | Mass of the part (`Part.mass`) | kg |
  | $c_p$ | Specific heat capacity of the part (`Part.material.specific_heat`) | J/kg·K |
  | $\Delta T$ | Temperature rise required (`target_temp − start_temp`) | K or °C |
  | $\eta$ | Electrical coupling efficiency (from above) | dimensionless |

---

## Example Usage

```python
import numpy as np
from heating import Material, Part, Coil, Heating_process

# Define materials
steel = Material(
    relative_mag_permability=100,
    resistance=1.6e-7,
    specific_heat=490,
    density=7850
)

copper = Material(
    relative_mag_permability=1,
    resistance=1.68e-8,
    specific_heat=385,
    density=8960
)

# Create part (hollow steel cylinder)
part = Part(height=0.05, OD=0.06, ID=0.04, material=steel)

# Create coil (copper coil at 10 kHz)
coil = Coil(ID=0.07, material=copper, frequency=10000)

# Define heating process (room temp to 800°C)
process = Heating_process(part=part, coil=coil, start_temp=25, target_temp=800)

# Calculate required power
power = process.required_power()
print(f"Required Power: {power:.2f} W")
```

---

## Notes

- All dimensions should be in **SI units** (metres, kg, etc.).
- The volume calculation uses only the cross-sectional annular area — ensure `height` is accounted for if a full volumetric calculation is needed.