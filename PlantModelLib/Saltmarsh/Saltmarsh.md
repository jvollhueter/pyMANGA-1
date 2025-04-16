# Description

This module calculates the growth (production of biovolume) of saltmarsh plants.
The growth is calculated using a simple model based on resource limitation and competition.
Resource limitation is modelled with submodels (e.g. FixedSalinity or SolarRadiation).
The same applies to the competition: Here the Zone of Influence (ZOI) models can be used.

This module can be used in simulations where you want to include the growth of saltmarsh plants.

# Usage

```xml
<population>
    <group>
        <vegetation_model_type> Saltmarsh </vegetation_model_type>
        <species> Saltmarsh </species>
    </group>
</population>
```

Go to [Examples](#examples) for more information

# Attributes

- ``vegetation_model_type`` (string): "Saltmarsh" (no other values accepted)
- ``species`` (string): Saltmarsh species oder PFT. Possible Inputs: "Saltmarsh" or path to individual species file.

# Value

Three dictionaries each with length = 1 (i.e., for each individual plant).

The dictionary ``geometry`` contains information about the plant geometry.
The dictionary ``growth_concept_information`` contains information plant growth.
The dictionary ``parameter`` contains the relevant parameters.


# Details
## Purpose

The purpose of this module is to describe the growth of saltmarsh plants based on resource limitation and competition.

## Plant geometry

In this module, a plant is described by two cylinders, one above ground and one blowground.
These two cylinders have two parameters, the height and the radius.
With this four parameters (h_ag, r_ag, h_bg, r_bg) the volume of the plant can be calculated.

## Process overview

- For the calculation of the below and above ground resources you have to use one ore more of the resource submodels (e.g. FixedSalinity or SolarRadiation).
the resources available to the plant are calculated from the minimum of the two resources (res_bg and res_ag).
````
res_tot = min(res_bg, res_ag)
````
- The plant can use only a part of this resources for growth.
First they have to use a part of the resources for maintenance:
````
maint = \left( V_{bio} \cdot f_{maint} \right) \cdot \Delta t
````
- variables starting with ``p_`` are species-specific parameters (see `pyMANGA.PopulationLib.Species`)
- Calculate new dbh (considering pyMANGAs time step length)
```
dbh = dbh + grow * time / (3600 * 24 * 365.25)
```
- Calculate root and crown radius
```
r_root = r_crown = p_zoi_scaling * dbh**0.5
``` 
- The JABOWA growth function calculates dbh and height in centimeters. For alignment with pyMANGA all variables are transformed to meters.

- Parameters ``p_b2`` and `p_b3` can be estimated using
```
b2 = 2 * (max_height - 137) / max_dbh
b3 = (max_height - 137) / max_dbh**2
```

## Application & Restrictions

**Application**

This module can be used to build the Kiwi model (<a href="https://doi.org/https://doi.org/10.1016/S0304-3800(00)00298-2" target="_blank">Berger & Hildenbrandt (2000)</a>).
To do so, combine it with the below-ground modules ``ResourceLib.Belowground.Individual.FON`` and ``ResourceLib.Belowground.Individual.FixedSalinity``.


# References

See <a href="https://doi.org/10.2307/2258570" target="_blank">Botkin et al. 1972</a> for the growth equations and parameterizations for some temperate species.
The growth function has been applied to mangroves, e.g., in <a href="https://doi.org/https://doi.org/10.1016/S0304-3800(00)00298-2" target="_blank">Berger & Hildenbrandt (2000)</a>.



*Note*: all values are given in SI units, but can be provided using equations (see examples).
For salinity, this means typical seawater salinity of 35 ppt is given as 0.035 kg/kg or 35\*10\**-3 kg/kg.
