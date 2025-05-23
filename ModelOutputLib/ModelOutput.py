#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os


class ModelOutput:
    """
    Parent class for all model output modules.
    """

    def __init__(self, args):
        """
        Get relevant tags from project file and create output directory and/or file.
        Check if output file exists and can be overwritten.
        Args:
            args (lxml.etree._Element): module specifications from project file tags
        """
        self.prj_args = args
        # Set initial parameters
        self._output_counter = 0
        self.inside_range = False
        self.output_each_timestep = False

        self.createOutputDir()
        self.setOutputTime()
        self.setOutputVariables()

        try:
            self.delimiter = self.prj_args.find("delimiter").text
        except AttributeError:
            self.delimiter = "\t"

    def createOutputDir(self):
        """
        Create a directory where the output will be saved.
        If not specified in the project file, it must be empty.
        """
        self.output_dir = self.checkRequiredKey("output_dir")

        # Check if overwriting previous output is allowed
        allow_previous_output = self.prj_args.find("allow_previous_output")
        if allow_previous_output is not None:
            allow_previous_output = eval(allow_previous_output.text)
        else:
            allow_previous_output = False

        # If overwriting is not allowed, check if the directory is empty
        if not allow_previous_output:
            dir_files = 0
            try:
                dir_files = len(os.listdir(self.output_dir))
            except FileNotFoundError:
                pass

            if dir_files > 0:
                print("ERROR: Output directory '" + self.output_dir + "' is not empty.")
                exit()

        # Create directory, if it does not already exist
        try:
            os.mkdir(self.output_dir)
        except FileExistsError:
            pass
        print("Output file path: " + os.path.join(os.getcwd(), self.output_dir))

    def all_none(self, l):
        """
        Check if all items of a list are None
        Credits: @Dog eat cat world https://stackoverflow.com/a/62816203
        Args:
            l (list): list of items
        Returns:
            bool
        """
        return not any(map(None.__ne__, l))

    def setOutputTime(self):
        """
        Set variables defining when output is written.
        If nothing is defined in the project file, write output at every time step.
        """
        self.output_each_nth_timestep = self.prj_args.find("output_each_nth_timestep")
        self.output_times = self.prj_args.find("output_times")
        self.output_time_range = self.prj_args.find("output_time_range")

        # If nothing is defined, write output every timestep
        if self.all_none([self.output_each_nth_timestep, self.output_times, self.output_time_range]):
            self.output_each_timestep = True
            print("WARNING: No output frequency has been defined. Output is written at each time step.")
        else:
            # Get output time steps for two periods (shape: [i, j])
            if self.output_each_nth_timestep is not None:
                self.output_each_nth_timestep = eval(self.output_each_nth_timestep.text)
                # If only one value is provided, output is written in every timestep during the second period
                if len(self.output_each_nth_timestep) == 1:
                    self.output_each_nth_timestep.append(1)
                elif len(self.output_each_nth_timestep) > 2:
                    raise ValueError("The tag \'<output_each_nth_timestep>\' in the xml file"
                                     " caused an error. Please check your input!")

            # Check if specific time steps to write output are defined
            if self.output_times is not None:
                self.output_times = eval(self.output_times.text)

            # Check if period to write output with different frequencies are defined
            if self.output_time_range is not None:
                self.output_time_range = eval(self.output_time_range.text)
                if len(self.output_time_range) != 2:
                    raise ValueError("The tag \'<output_time_range>\' in the xml file"
                                     " caused an error. Please check your input!")
                if self.all_none([self.output_each_nth_timestep, self.output_times]):
                    self.output_each_nth_timestep = [0, 1]
                    print(
                        "WARNING: No output frequency has been defined. Output is written at each time step within the "
                        "defined period.")

    def setOutputVariables(self):
        """
        Set variables that are written to the output file
        """
        ## Geometric measures included in output
        self.geometry_outputs = []
        ## Parameters included in output
        self.parameter_outputs = []
        ## Parameters included in output
        self.growth_outputs = []
        ## Network information included in output
        self.network_outputs = []
        for key in self.prj_args.iterchildren("geometry_output"):
            self.geometry_outputs.append(key.text.strip())
        for key in self.prj_args.iterchildren("parameter_output"):
            self.parameter_outputs.append(key.text.strip())
        for key in self.prj_args.iterchildren("growth_output"):
            self.growth_outputs.append(key.text.strip())
        for key in self.prj_args.iterchildren("network_output"):
            self.network_outputs.append(key.text.strip())

    def getOutputType(self):
        """
        Get selected output type.
        Returns:
            string
        """
        return self.case

    def getOutputDir(self):
        """
        Get output directory.
        Returns:
            string
        """
        return self.output_dir

    def addSelectedHeadings(self, string):
        """
        Collect selected output parameters to create a file header.
        Args:
            string (string): beginning of header, e.g. plant ID
        Returns:
            string
        """
        for geometry_output in self.geometry_outputs:
            string += self.delimiter + geometry_output
        for parameter_output in self.parameter_outputs:
            string += self.delimiter + parameter_output
        for growth_output in self.growth_outputs:
            string += self.delimiter + growth_output
        for network_output in self.network_outputs:
            string += self.delimiter + network_output
        return string

    def addSelectedOutputs(self, plant, string, growth_information):
        """
        Collect values of selected output parameters to fill output file.
        Args:
            plant (dict): plant object
            string (string): beginning of line, e.g. plant ID
            growth_information (dict): dictionary containing growth information of the respective plant
        Returns:
            string
        """
        if len(self.geometry_outputs) > 0:
            geometry = plant.getGeometry()
            for geometry_output in self.geometry_outputs:
                string += self.delimiter + self.getNewValue(geometry, geometry_output)
        if len(self.parameter_outputs) > 0:
            parameter = plant.getParameter()
            for parameter_output in self.parameter_outputs:
                string += self.delimiter + self.getNewValue(parameter, parameter_output)
        if len(self.growth_outputs) > 0:
            for growth_output_key in self.growth_outputs:
                string += self.delimiter + self.getNewValue(growth_information, growth_output_key)
        if len(self.network_outputs) > 0:
            network = plant.getNetwork()
            for network_output in self.network_outputs:
                string += self.delimiter + self.getNewValue(network, network_output)
        return string

    def getNewValue(self, key, value):
        """
        Extract variable value from dictionary
        Args:
            key (dict): dictionary of plant variables
            value (string): name of output variable
        Returns:
            numeric or string
        """
        try:
            string = str(key[value])
        except KeyError:
            string = "NaN"
        return string

    def checkRequiredKey(self, key):
        """
        Check whether a key (i.e., required element) is specified in project file.
        Args:
            key (string): name of key to be checked
        Returns:
            string or raise KeyError
        """
        tmp = self.prj_args.find(key)
        if tmp is None:
            raise KeyError("Required key '" + key + "' in project file at " +
                           "position MangaProject_model_output is missing.")
        elif tmp.text.strip() == "":
            raise KeyError("Key '" + key + "' in project file at position " +
                           "MangaProject_model_output needs to be specified.")
        return tmp.text

    def writeOutput(self, plant_groups, time, force_output=False, group_died=False):
        """
        Check whether it is output time and call the output method of the selected module.
        Args:
            plant_groups (dict): plant groups object
            time (float): current time step
            force_output (bool): indicate whether writing output is forced
            group_died (bool): indicate whether a whole plant group died
        """
        if not any([force_output, group_died]):
            self.cond, self.inside_range = False, False

            # Condition 1: Are we in a certain output time?
            if self.output_times is not None:
                self.cond = time in self.output_times

            if not self.cond:
                # Condition 2: Are we in the n-th timestep?
                if self.output_each_nth_timestep is not None:
                    # Check whether time range is defined
                    if self.output_time_range is not None:
                        self.inside_range = self.output_time_range[0] <= time <= self.output_time_range[1]

                    if self.inside_range:
                        # Condition inside time range
                        if self.output_each_nth_timestep[1] != 0:
                            self.cond = self._output_counter % int(self.output_each_nth_timestep[1]) == 0
                    else:
                        # Condition outside of range
                        if self.output_each_nth_timestep[0] != 0:
                            self.cond = self._output_counter % int(self.output_each_nth_timestep[0]) == 0

        # Check whether one of the above conditions is fulfilled
        if any([self.cond, force_output, group_died, self.output_each_timestep]):
            self.outputContent(plant_groups=plant_groups,
                               time=time,
                               group_died=group_died)

        # Only increase counter during regular method calls
        # Reason: if one or multiple groups die during a time step, an output is forced
        if not group_died:
            self._output_counter += 1

    def outputContent(self, plant_groups, time, **kwargs):
        """
        Write output content to file, i.e., values of selected parameters.
        Args:
            plant_groups (dict): plant groups object
            time (float): current time step
            **kwargs (dict): named arguments
        """
        pass
