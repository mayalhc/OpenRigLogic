#-*- coding: utf-8 -*-
import inspect
import os
import unittest

if hasattr(os, 'add_dll_directory') and 'LD_LIBRARY_PATH' in os.environ:
    for ld_lib_path in os.environ['LD_LIBRARY_PATH'].split(';'):
        os.add_dll_directory(ld_lib_path)

import riglogic


ANY_MISSING = "{} missing from wrapper"

METHODS_MISSING = """
methods missing in tests, but found in {className}:
{missing}
methods missing in {className}, but found in tests:
{extraneous}
"""

PARAMS_MISSING = """
{methodName}'s parameter list:
{parameters}
params missing in tests, but found in {methodName}'s params:
{missing}
params missing in {methodName}, but found in tests:
{extraneous}
"""


def merged(source, *args):
    """Return a copy of the `source` dict with all `args` merged into it"""
    result = source.copy()
    for ext in args:
        result.update(ext)
    return result


class TestClass(unittest.TestCase):

    def setUp(self):
        self.allSymbols = inspect.getmembers(riglogic)

    def findObject(self, source, objectName, **kwargs):
        objects = [item for item in source if item[0] == objectName]
        self.assertTrue(len(objects) != 0,
                        kwargs.get('error', ANY_MISSING.format(objectName)))
        return (objects[0][0], objects[0][1])

    def findClass(self, className):
        return self.findObject(self.allSymbols, className)

    def findMethod(self, obj, methodName, **kwargs):
        return self.findObject(inspect.getmembers(obj), methodName, **kwargs)

    def findAllMethods(self, obj):
        members = inspect.getmembers(obj, predicate=lambda m: inspect.ismethod(m) or inspect.isbuiltin(m) or inspect.isfunction(m))
        return [k for (k, v) in members if "__" not in k and
                k != "_s" and k != "thisown"]

    def findAllParameters(self, obj):
        if inspect.isbuiltin(obj):
            return []

        spec = inspect.getfullargspec(obj)
        return [arg for arg in spec.args if "self" not in arg]

    def formatErrorMessage(self, template, result, expected, **kwargs):
        missing = sorted(set(result).difference(expected))
        extraneous = sorted(set(expected).difference(result))
        return template.format(missing=missing,
                               extraneous=extraneous,
                               **kwargs)

    def assertClassExists(self, className):
        (foundClassName, foundClassObject) = self.findClass(className)
        with self.subTest(className):
            self.assertTrue(inspect.isclass(foundClassObject))
            self.assertTrue(className == foundClassName)

    def assertMethodParametersExist(self, methodName, methodObject, parameters):
        foundParameters = self.findAllParameters(methodObject)
        errorMessage = self.formatErrorMessage(PARAMS_MISSING,
                                               result=foundParameters,
                                               expected=parameters,
                                               parameters=foundParameters,
                                               methodName=methodName)
        self.assertEqual(len(foundParameters), len(parameters), errorMessage)
        for param in parameters:
            self.assertTrue(param in foundParameters, errorMessage)

    def assertClassMethodsExist(self, className, methods):
        (className, classObject) = self.findClass(className)
        foundMethods = self.findAllMethods(classObject)
        errorMessage = self.formatErrorMessage(METHODS_MISSING,
                                               foundMethods,
                                               methods,
                                               className=className)
        self.assertEqual(len(foundMethods), len(methods), errorMessage)
        for (methodName, parameters) in methods.items():
            (methodName, methodObject) = self.findMethod(classObject,
                                                         methodName,
                                                         error=errorMessage)
            with self.subTest(className + "_" + methodName):
                compoundMethodName = '.'.join((className, methodName))
                self.assertMethodParametersExist(compoundMethodName,
                                                 methodObject,
                                                 parameters)


class TestLibrary(TestClass):
    tests = {}

    def testExistence(self):
        for (className, methods) in self.tests.items():
            self.assertClassExists(className)
            self.assertClassMethodsExist(className, methods)


class TestVersionInfo(TestLibrary):
    tests = {
        "VersionInfo": {
            "getMajorVersion": [],
            "getMinorVersion": [],
            "getPatchVersion": [],
            "getVersionString": []
        }
    }


class TestRigLogic(TestLibrary):
    tests = {
        "RigLogic": {
            "getConfiguration": [],
            "getLODCount": [],
            "getRBFSolverIndicesForLOD": ["lod"],
            "getMLOperationIndicesForLOD": ["lod", "mlTypeIndex", "mlOperationSetIndex"],
            "getBlendShapeChannelIndicesForLOD": ["lod"],
            "getAnimatedMapIndicesForLOD": ["lod"],
            "getJointIndicesForLOD": ["lod"],
            "getNeutralJointValues": [],
            "getJointVariableAttributeIndices": ["lod"],
            "getJointGroupCount": [],
            "getRBFSolverCount": [],
            "getMeshCount": [],
            "getSwingCount": [],
            "getTwistCount": [],
            "getMeshRegionCount": ["meshIndex"],
            "getMLTypeCount": [],
            "getMLOperationSetCount": ["mlTypeIndex"],
            "getMLOperationCount": ["mlTypeIndex", "mlOperationSetIndex"],
            "mapGUIToRawControls": ["instance"],
            "mapRawToGUIControls": ["instance"],
            "calculate": ["instance"],
            "calculateMLControls": ["instance"],
            "calculateMLOperation": ["instance", "mlTypeIndex", "mlOperationSetIndex", "mlOperationIndex"],
            "calculateRBFControls": ["instance"],
            "calculateRBFSolver": ["instance", "solverIndex"],
            "calculatePSDControls": ["instance"],
            "calculateJoints": ["instance"],
            "calculateJointGroup": ["instance", "jointGroupIndex"],
            "calculateBlendShapes": ["instance"],
            "calculateAnimatedMaps": ["instance"],
            "collectCalculationStats": ["instance", "stats"]
        }
    }


class TestRigInstance(TestLibrary):
    tests = {
        "RigInstance": {
            "getGUIControlCount": [],
            "getGUIControl": ["index"],
            "getGUIControlValues": [],
            "setGUIControl": ["index", "value"],
            "getRawControlCount": [],
            "getRawControl": ["index"],
            "getRawControlValues": [],
            "setRawControl": ["index", "value"],
            "getPSDControlCount": [],
            "getPSDControl": ["index"],
            "getPSDControlValues": [],
            "getMLControlCount": [],
            "getMLControl": ["index"],
            "getMLControlValues": [],
            "getMLMaskValues": [],
            "getMLTypeCount": [],
            "getMLOperationSetCount": ["mlTypeIndex"],
            "getMLOperationCount": ["mlTypeIndex", "mlOperationSetIndex"],
            "getRBFControlCount": [],
            "getRBFControl": ["index"],
            "getRBFControlValues": [],
            "getLOD": [],
            "setLOD": ["level"],
            "getAnimatedMapOutputs": [],
            "getBlendShapeOutputs": [],
            "getJointOutputs": []
        }
    }


if __name__ == '__main__':
    unittest.main()
