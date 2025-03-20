
class InitialPop:
    """
    Constructor to initialize initial population modules, by calling respective initialization methods.
    """
    def __init__(self, xml_args):
        """
        Args:
            xml_args (lxml.etree._Element): initial population module specifications from project file tags
        """
        self.iniInitialPopulation(xml_args=xml_args)

    def iniInitialPopulation(self, xml_args):
        """
        Initialize selected initial population module.
        Args:
            xml_args (lxml.etree._Element): dispersal module specifications from project file tags
        """
        case = xml_args.find("type").text
        module_dir = 'PopulationLib.InitialPop.'
        # Class needs to be imported on demand to avoid circular import
        from ProjectLib.Project import MangaProject
        self.initial_population = MangaProject.importModule(self=self,
                                                            module_name=case,
                                                            modul_dir=module_dir,
                                                            prj_args=xml_args)

    def setModelDomain(self, x1, x2, y1, y2):
        """
        Adds model domain boundaries to the object.
        Args:
            x1 (float): x-coordinate of left bottom border of grid
            x2 (float): x-coordinate of right bottom border of grid
            y1 (float): y-coordinate of left top border of grid
            y2 (float): y-coordinate of right top border of grid
        """
        self.initial_population.setModelDomain(x1, x2, y1, y2)

    def getPlantAttributes(self):
        """
        Handler to get group dictionaries (i.e., plant positions, geometries and network parameters).
        Returns:
            three dicts
        """
        positions, geometry, network = self.initial_population.getPlantAttributes()
        return positions, geometry, network

