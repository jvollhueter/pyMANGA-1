import numpy as np
from ProjectLib import helpers as helpers


class Distance2Parent:
    """
    Distance2Parent dispersal module
    """
    def __init__(self, xml_args):
        """
        Args:
            xml_args (lxml.etree._Element): dispersal module specifications from project file tags
        """
        self.xml_args = xml_args
        self.getInputParameters(args=xml_args)

    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "required": ["type", "distribution"],
            "optional": ["scale", "loc", "high"]
        }
        myself = super(Distance2Parent, self)
        helpers.getInputParameters(myself, **tags)

        self.type = self.type.lower()
        if not hasattr(self, "loc"):
            self.loc = 0

    def getPositions(self, number_of_plants, plants):
        """
        Return positions of new plants, which are drawn from a user-defined distribution.
        Args:
            number_of_plants (int or list of int): number of plants that will be added to the model
            plants (dict): plant object, see ``pyMANGA.PopulationLib.PopManager.Plant``
        Returns:
            dict
        """
        if np.isscalar(number_of_plants):
            print("ERROR: it seems <production><per_individual> is False but needs to be True.")
            exit()

        self.xi, self.yi = [], []
        for i in range(len(plants)):
            plant = plants[i]
            xp, yp = plant.getPosition()
            n = int(number_of_plants[i])
            dist2parent = self.getDistances(number_of_plants=n)
            angle = np.random.uniform(low=0, high=2 * np.pi, size=n)
            self.xi.append(xp + dist2parent * np.sin(angle))
            self.yi.append(yp + dist2parent * np.cos(angle))

        # Flatten lists
        x = np.array(self.xi).flat
        y = np.array(self.yi).flat

        # Drop seeds that are outside the model domain
        idx = np.where((x < self.x_1) | (x > self.x_2) | (y < self.y_1) | (y > self.y_2))
        x = np.delete(x, idx)
        y = np.delete(y, idx)

        plant_positions = {"x": x, "y": y}
        return plant_positions

    def getDistances(self, number_of_plants):
        """
        Return distances between seedlings and parent plant.
        Args:
            number_of_plants (int): number of plants that will be added to the model
        Returns:
            list
        """
        try:
            if self.distribution in "normal":
                return np.random.normal(loc=self.loc, scale=self.scale, size=number_of_plants)

            if self.distribution in "uniform":
                return np.random.uniform(size=number_of_plants, high=self.high)

            if self.distribution in "exponential":
                return np.random.exponential(scale=self.scale, size=number_of_plants)
        except AttributeError:
            print("ERROR: A parameter defining the probability density function is missing. "
                  "Check the documentation of <dispersal>.")
            exit()

    def setModelDomain(self, x1, x2, y1, y2):
        """
        Adds model domain boundaries to the object.
        Args:
            x1 (float): x-coordinate of left bottom border of grid
            x2 (float): x-coordinate of right bottom border of grid
            y1 (float): y-coordinate of left top border of grid
            y2 (float): y-coordinate of right top border of grid
        """
        helpers.setModelDomain(self, x1, x2, y1, y2)
