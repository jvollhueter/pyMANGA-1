import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from ProjectLib import XMLtoProject
from TimeLoopLib import TreeDynamicTimeStepping
import unittest
import glob
import os

filepathExampleSetups = path.join(path.dirname(path.abspath(__file__)),"Test_Setups_small/*.xml")
xml = glob.glob(filepathExampleSetups)
errors = []
if xml:
    for xmlfile in xml:
        resultsFilepath = path.join(path.dirname(path.abspath(__file__)),"Test_Setups_small/testoutputs/*.*")
        results = glob.glob(resultsFilepath)
        for result in results:
            os.remove(result)
        print("________________________________________________")
        print("In the following the setup", xmlfile, "is tested.")
    
        class MyTest(unittest.TestCase):
    
            def test(self):
                try:
                    prj = XMLtoProject(xml_project_file=xmlfile)
                    time_stepper = TreeDynamicTimeStepping(prj)
                    prj.runProject(time_stepper)
                except:
                    self.fail(errors.append(xmlfile))
    
        if __name__ == "__main__":
            unittest.main(exit=False)
        print("The setup", xmlfile, "was tested.")
        print("________________________________________________")
    print("The testing of all example setups is finished")
    print("")
    if errors:
        if len(errors) == 1:
            print("An error occured while testing the following example setup:")
        else:
            print("Errors occured while testing the following example setups:")
        n = range(len(errors))
        for x in n:
            print("")
            print(errors[x])
        print("")
    else:
        print("The tests of all example setups were successful")
        print("")
else: print("unfortunately no project-file could be found.")