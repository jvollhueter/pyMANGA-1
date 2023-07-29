# first approach saltmarsh model

from PlantModelLib import PlantModel
import numpy as np

class Saltmarsh(PlantModel):
    def __init__(self, args):
        """
        Plant model concept.
        Args:
            args: Bettina module specifications from project file tags
        """
        print("Growth and death dynamics of type Saltmarsh Model")
        super().iniMortalityConcept(args)

    def prepareNextTimeStep(self, t_ini, t_end):
        """
        Prepare next time step by initializing relevant variables.
        Args:
            t_ini (int): start of current time step in seconds
            t_end (int): end of current time step in seconds
        """
        self.time = t_end - t_ini

    def progressPlant(self, tree, aboveground_resources, belowground_resources):
        """
        Manage growth procedures for a timestep --- read tree geometry and parameters,
        schedule computations, and update tree geometry and survival.
        Args:
            tree (dict): tree object
            aboveground_resources (float): aboveground resource growth reduction factor
            belowground_resources (float): belowground resource growth reduction factor
        """
        # print(tree.getGrowthConceptInformation()['salinity'])
        geometry = tree.getGeometry()
        growth_concept_information = tree.getGrowthConceptInformation()
        self.parameter = tree.getParameter()
        self.r_ag = geometry["r_ag"]
        self.h_ag = geometry["h_ag"]
        self.r_bg = geometry["r_bg"]
        self.h_bg = geometry["h_bg"]
        self.max_h = self.parameter["max_h"]
        self.survive = 1

        self.treeVolume()

        # Define variables that are only required for specific Mortality
        # concepts
        super().setMortalityVariables(growth_concept_information)

        self.treeMaintenance()
        self.bgResources(belowground_resources)
        self.agResources(aboveground_resources)
        self.growthResources()
        self.treeGrowthWeights()
        self.treeGrowth()

        geometry["r_ag"] = self.r_ag
        geometry["h_ag"] = self.h_ag
        geometry["r_bg"] = self.r_bg
        geometry["h_bg"] = self.h_bg
        growth_concept_information["ag_resources"] = self.ag_resources
        growth_concept_information["bg_resources"] = self.bg_resources
        growth_concept_information["growth"] = self.grow
        growth_concept_information["available_resources"] = (
            self.available_resources)
        growth_concept_information["inc_r_ag"] = \
            self.inc_r_ag
        growth_concept_information["inc_h_ag"] = \
            self.inc_h_ag
        growth_concept_information["inc_r_bg"] = \
            self.inc_r_bg
        growth_concept_information["inc_h_bg"] = \
            self.inc_h_bg
        # growth_concept_information["salinity"] = tree.salinity

        # Get Mortality-related variables
        super().getMortalityVariables(growth_concept_information)

        tree.setGeometry(geometry)
        tree.setGrowthConceptInformation(growth_concept_information)
        if self.survive == 1:
            tree.setSurvival(1)
        else:
            tree.setSurvival(0)

    def treeGrowth(self):
        """
        Update tree geometry.

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'increase of allometric measures'.
        Sets:
            multiple float
        """
        self.inc_h_ag = self.w_h_ag * self.grow

        if self.h_ag + self.inc_h_ag < self.max_h:
            self.h_ag += self.inc_h_ag

            self.inc_r_ag = self.w_r_ag * self.grow
            self.r_ag += self.inc_r_ag

            self.inc_r_bg = self.w_r_bg * self.grow
            self.r_bg += self.inc_r_bg

            self.inc_h_bg = self.w_h_bg * self.grow
            self.h_bg += self.inc_h_bg

        else:

            print('nein   , max_h', self.max_h, '    h_ag: ', self.h_ag)
            self.inc_r_ag = 0

            self.inc_h_ag = 0

            self.inc_r_bg = 0

            self.inc_h_bg = 0

    def treeGrowthWeights(self):
        """
        Calculate the growth weights for distributing biomass increment to the tree geometries.

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'weights'.
        Sets:
            multiple float
        """
        self.w_r_ag = self.parameter['w_r_ag']

        self.w_h_ag = self.parameter['w_h_ag']

        self.w_r_bg = self.parameter['w_r_bg']

        self.w_h_bg = self.parameter['w_h_bg']

    def treeMaintenance(self):
        """
        Calculate the resource demand for biomass maintenance.

        For parameter reference, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 2.5.
        Sets:
            float
        """
        self.maint = self.volume * self.parameter["maint_factor"] * self.time

    def flowLength(self):
        """
        Calculate the flow length from fine roots to leaves.
        Sets:
            float
        """
        self.flow_length = (2 * self.r_crown + self.h_stem +
                            0.5**0.5 * self.r_root)

    ## This function calculates the total tree volume.
    def treeVolume(self):
        """
        Calculate the total tree volume.

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'volume of plant components'.
        Sets:
            float
        """
        self.volume = np.pi * self.r_ag**2 * self.h_ag + \
                      np.pi * self.r_bg**2 * self.h_bg

    def agResources(self, aboveground_resources):
        """
        Calculate the available aboveground resources (intercepted light measured equivalent to respective water uptake).

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'resistances'.
        Args:
            aboveground_resources (float): aboveground resource growth reduction factor
        Sets:
            float
        """
        self.ag_resources = aboveground_resources

    def bgResources(self, belowground_resources):
        """
        Calculate the available belowground resources (m³ water per time step).

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'resistances'.
        Args:
            belowground_resources (float): belowground resource growth reduction factor
        Sets:
            float
        """
        self.bg_resources = belowground_resources
        print('belowground resources:___________', belowground_resources)

    def growthResources(self):
        """
        Calculate the available resources and the biomass increment.

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'resources'.
        Sets:
            multiple float
        """
        self.available_resources = min(self.ag_resources, self.bg_resources)
        print('______', self.available_resources)
        self.grow = (self.parameter["growth_factor"] *
                     (self.available_resources)) # - self.maint))
        # Check if trees survive based on selected mortality concepts
        super().setTreeKiller()
