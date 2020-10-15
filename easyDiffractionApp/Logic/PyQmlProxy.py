import sys
import json
import numpy as np
from dicttoxml import dicttoxml
from distutils.util import strtobool
from urllib.parse import urlparse

from PySide2.QtCore import QObject, Slot, Signal, Property
from PySide2.QtCharts import QtCharts

from easyCore import borg
from easyCore.Fitting.Fitting import Fitter
from easyCore.Fitting.Constraints import ObjConstraint, NumericConstraint
from easyCore.Utils.classTools import generatePath

from easyExampleLib.interface import InterfaceFactory
from easyExampleLib.model import Sin, DummySin

from easyDiffractionLib.sample import Sample as Sample2
from easyDiffractionLib import Crystal as Crystal2
from easyDiffractionLib.interface import InterfaceFactory as InterfaceFactory2
from easyDiffractionLib.Elements.Instruments.Instrument import Pattern as Pattern2

from easyDiffractionApp.Logic.QtDataStore import QtDataStore
from easyDiffractionApp.Logic.DisplayModels.DataModels import MeasuredDataModel, CalculatedDataModel


class PyQmlProxy(QObject):
    _borg = borg
    projectInfoChanged = Signal()
    modelChanged = Signal()
    constraintsChanged = Signal()
    calculatorChanged = Signal()
    minimizerChanged = Signal()
    statusChanged = Signal()
    phasesChanged = Signal()

    phases2Changed = Signal()
    model2Changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.interface2 = InterfaceFactory2()
        self.sample2 = Sample2(parameters=Pattern2(), interface=self.interface2)
        self.crystal2 = None
        x_data2 = np.linspace(5, 150, 400)
        self.data2 = QtDataStore(x_data2, np.zeros_like(x_data2), np.zeros_like(x_data2), None)
        self.phases2 = []
        self._calculated_data_model2 = CalculatedDataModel(self.data2)

        self.phases = self.initPhases()
        self.project_info = self.initProjectInfo()
        self.interface = InterfaceFactory()
        self.model = Sin(self.interface)
        self.fitter = Fitter(self.model, self.interface.fit_func)
        self.dummy_source = DummySin()
        self.data = QtDataStore(self.dummy_source.x_data, self.dummy_source.y_data, self.dummy_source.sy_data, None)
        self._measured_data_model = MeasuredDataModel(self.data)
        self._calculated_data_model = CalculatedDataModel(self.data)
        self.updateCalculatedData2()
        # when to emit status bar items cnahged
        self.calculatorChanged.connect(self.statusChanged)
        self.minimizerChanged.connect(self.statusChanged)

    # Data

    @Slot()
    def generateMeasuredData(self):
        self.dummy_source = DummySin()
        self.data = QtDataStore(self.dummy_source.x_data, self.dummy_source.y_data, self.dummy_source.sy_data, None)
        self._measured_data_model.updateData(self.data)

    @Slot()
    def updateCalculatedData(self):
        self.data.y_opt = self.interface.fit_func(self.data.x)
        self._calculated_data_model.updateData(self.data)
        self.modelChanged.emit()

    @Slot()
    def updateCalculatedData2(self):
        if self.crystal2 is None:
            return
        self.data2.y_opt = self.interface2.fit_func(self.data2.x)
        self._calculated_data_model2.updateData(self.data2)
        self.model2Changed.emit()

    # Calculator

    @Property('QVariant', notify=calculatorChanged)
    def calculatorList(self):
        return self.interface.available_interfaces

    @Property(int, notify=calculatorChanged)
    def calculatorIndex(self):
        return self.calculatorList.index(self.interface.current_interface_name)

    @calculatorIndex.setter
    def setCalculator(self, index: int):
        self.model.switch_interface(self.calculatorList[index])
        self.updateCalculatedData2()
        self.calculatorChanged.emit()

    # Minimizer

    @Property('QVariant', notify=minimizerChanged)
    def minimizerList(self):
        return self.fitter.available_engines

    @Property(int, notify=minimizerChanged)
    def minimizerIndex(self):
        return self.minimizerList.index(self.fitter.current_engine.name)

    @minimizerIndex.setter
    def setMinimizer(self, index: int):
        self.fitter.switch_engine(self.minimizerList[index])
        self.minimizerChanged.emit()

    @Slot()
    def startFitting(self):
        result = self.fitter.fit(self.data.x, self.data.y, weights=self.data.sy)
        self.data.y_opt = result.y_calc
        self._calculated_data_model.updateData(self.data)
        self.modelChanged.emit()

    @Slot()
    def startFitting2(self):
        result = self.fitter.fit(self.data2.x, self.data2.y, weights=self.data.sy)
        self.data2.y_opt = result.y_calc
        self._calculated_data_model2.updateData(self.data2)
        self.model2Changed.emit()

    # Charts

    @Slot(QtCharts.QXYSeries)
    def addMeasuredSeriesRef(self, series):
        self._measured_data_model.addSeriesRef(series)

    @Slot(QtCharts.QXYSeries)
    def addLowerMeasuredSeriesRef(self, series):
        self._measured_data_model.addLowerSeriesRef(series)

    @Slot(QtCharts.QXYSeries)
    def addUpperMeasuredSeriesRef(self, series):
        self._measured_data_model.addUpperSeriesRef(series)

    @Slot(QtCharts.QXYSeries)
    def setCalculatedSeriesRef(self, series):
        self._calculated_data_model2.setSeriesRef(series)

    # Undo/redo

    @Slot()
    def undo(self):
        self._borg.stack.undo()
        self.modelChanged.emit()

    @Slot(result=bool)
    def canUndo(self):
        return self._borg.stack.canUndo()

    @Slot()
    def redo(self):
        self._borg.stack.redo()
        self.modelChanged.emit()

    @Slot(result=bool)
    def canRedo(self):
        return self._borg.stack.canRedo()

    # Status

    @Property(str, notify=statusChanged)
    def statusModelAsXml(self):
        items = [ { "label": "Calculator", "value": self.interface.current_interface_name },
                  { "label": "Minimizer", "value": self.fitter.current_engine.name } ]
        xml = dicttoxml(items, attr_type=False)
        xml = xml.decode()
        return xml

    # Models

    def fitablesList(self):
        fitables_list = []
        pars_id, pars_path = generatePath(self.model)
        for index, par_path in enumerate(pars_path):
            par = borg.map.get_item_by_key(pars_id[index])
            fitables_list.append(
                { "number": index + 1,
                  "label": par_path,
                  "value": par.raw_value,
                  "unit": str(par.unit).replace("dimensionless", ""),
                  "error": par.error,
                  "fit": int(not par.fixed) }
            )
        return fitables_list

    @Property(str, notify=modelChanged)
    def fitablesListAsXml(self):
        xml = dicttoxml(self.fitablesList(), attr_type=False)
        xml = xml.decode()
        return xml

    @Property('QVariant', notify=modelChanged)
    def fitablesDict(self):
        fitables_dict = {}
        for par in self.model.get_parameters():
            fitables_dict[par.name] = par.raw_value
        return fitables_dict

    @Slot(str, str)
    def editFitableValueByName(self, name, value):
        for par in self.model.get_parameters():
            if par.name == name:
                par.value = float(value)
                self.updateCalculatedData2()

    @Slot(int, str, str)
    def editFitableByIndexAndName(self, index, name, value):
        #print("----", index, name, value)
        if index == -1: # TODO: Check why index is changed twice when name == "value"
            return
        par = self.model.get_parameters()[index]
        if name == "fit":
            par.fixed = not bool(strtobool(value))
        elif name == "value":
            par.value = float(value)
            self.updateCalculatedData2()
        else:
            print(f"Unsupported name '{name}'")

    # Constraints

    @Slot(int, str, str, str, int)
    def addConstraint(self, dependent_par_idx, relational_operator,
                      value, arithmetic_operator, independent_par_idx):
        if dependent_par_idx == -1 or value == "":
            print("Failed to add constraint: Unsupported type")
            return
        #if independent_par_idx == -1:
        #    print(f"Add constraint: {self.fitablesList()[dependent_par_idx]['label']}{relational_operator}{value}")
        #else:
        #    print(f"Add constraint: {self.fitablesList()[dependent_par_idx]['label']}{relational_operator}{value}{arithmetic_operator}{self.fitablesList()[independent_par_idx]['label']}")
        pars = self.model.get_parameters()
        if arithmetic_operator != "" and independent_par_idx > -1:
            c = ObjConstraint(pars[dependent_par_idx],
                              str(float(value)) + arithmetic_operator,
                              pars[independent_par_idx])
        elif arithmetic_operator == "" and independent_par_idx == -1:
            c = NumericConstraint(pars[dependent_par_idx],
                                  relational_operator.replace("=", "=="),
                                  float(value))
        else:
            print("Failed to add constraint: Unsupported type")
            return
        #print(c)
        c()
        self.fitter.add_fit_constraint(c)
        self.constraintsChanged.emit()
        self.updateCalculatedData2()

    def constraintsList(self):
        constraint_list = []
        for index, constraint in enumerate(self.fitter.fit_constraints()):
            if type(constraint) is ObjConstraint:
                independent_name = constraint.get_obj(constraint.independent_obj_ids).name
                relational_operator = "="
                value = float(constraint.operator[:-1])
                arithmetic_operator = constraint.operator[-1]
            elif type(constraint) is NumericConstraint:
                independent_name = ""
                relational_operator = constraint.operator.replace("==", "=")
                value = constraint.value
                arithmetic_operator = ""
            else:
                print(f"Failed to get constraint: Unsupported type {type(constraint)}")
                return
            number = index + 1
            dependent_name = constraint.get_obj(constraint.dependent_obj_ids).name
            enabled = int(constraint.enabled)
            constraint_list.append(
                { "number": number,
                  "dependentName": dependent_name,
                  "relationalOperator": relational_operator,
                  "value": value,
                  "arithmeticOperator": arithmetic_operator,
                  "independentName": independent_name,
                  "enabled": enabled }
            )
        return constraint_list

    @Property(str, notify=constraintsChanged)
    def constraintsListAsXml(self):
        xml = dicttoxml(self.constraintsList(), attr_type=False)
        xml = xml.decode()
        return xml

    @Slot(int)
    def removeConstraintByIndex(self, index: int):
        self.fitter.remove_fit_constraint(index)
        self.constraintsChanged.emit()

    @Slot(int, str)
    def toggleConstraintByIndex(self, index, enabled):
        constraint = self.fitter.fit_constraints()[index]
        constraint.enabled = bool(strtobool(enabled))
        self.constraintsChanged.emit()
        self.updateCalculatedData2()

    # App project info

    def initProjectInfo(self):
        return dict(name = "Example Project",
                    keywords = "diffraction, cfml, cryspy",
                    samples = "samples.cif",
                    experiments = "experiments.cif",
                    calculations = "calculation.cif",
                    modified = "18.09.2020, 09:24")

    @Property('QVariant', notify=projectInfoChanged)
    def projectInfoAsJson(self):
        return self.project_info

    @projectInfoAsJson.setter
    def setProjectInfoAsJson(self, json_str):
        self.project_info = json.loads(json_str)
        self.projectInfoChanged.emit()

    @Slot(str, str)
    def editProjectInfoByKey(self, key, value):
        self.project_info[key] = value
        self.projectInfoChanged.emit()

    # Test phases dict

    def initPhases(self):
        phases = [dict(
                    label = "Co2SiO4",
                    color = "darkolivegreen",
                    crystal_system = "orthorhombic",
                    space_group_name = "P n m a",
                    space_group_setting = "abc",
                    cell_length_a = 10.28,
                    cell_length_b = 10.28,
                    cell_length_c = 10.28,
                    cell_angle_alpha = 90.0,
                    cell_angle_beta = 90.0,
                    cell_angle_gamma = 90.0,
                    atoms = [
                        dict(label="Co1", type="Co", color="coral", x=0.0, y=0.0, z=0.0, occupancy=1.0, adp_type="Uiso", adp_iso=0.004),
                        dict(label="Co2", type="Co", color="coral", x=0.279, y=0.279, z=0.279, occupancy=1.0, adp_type="Uiso", adp_iso=0.007),
                        dict(label="Si", type="Si", color="steelblue", x=0.094, y=0.094, z=0.094, occupancy=1.0, adp_type="Uiso", adp_iso=0.005),
                        dict(label="O1", type="O", color="darkolivegreen", x=0.091, y=0.091, z=0.091, occupancy=1.0, adp_type="Uiso", adp_iso=0.008),
                        dict(label="O2", type="O", color="darkolivegreen", x=0.448, y=0.448, z=0.448, occupancy=1.0, adp_type="Uiso", adp_iso=0.008),
                        dict(label="O3", type="O", color="darkolivegreen", x=0.164, y=0.164, z=0.164, occupancy=1.0, adp_type="Uiso", adp_iso=0.011),
                    ]
                ),
                dict(
                    label = "CoO",
                    color = "steelblue",
                    crystal_system = "cubic",
                    space_group_name = "F m -3 m",
                    space_group_setting = "1",
                    cell_length_a = 3.02,
                    cell_length_b = 3.02,
                    cell_length_c = 3.02,
                    cell_angle_alpha = 90.0,
                    cell_angle_beta = 90.0,
                    cell_angle_gamma = 90.0,
                    atoms = [
                        dict(label="Co", type="Co", color="coral", x=0.0, y=0.0, z=0.0, occupancy=1.0, adp_type="Uiso", adp_iso=0.000),
                        dict(label="O", type="O", color="darkolivegreen", x=0.2471, y=0.4986, z=0.7497, occupancy=1.0, adp_type="Uiso", adp_iso=0.000),
                    ]
                )
               ]
        return phases

    @Property('QVariant', notify=phasesChanged)
    def phasesDict(self):
        return self.phases

    @phasesDict.setter
    def setPhasesDict(self, json_str):
        self.phases = json.loads(json_str)
        self.phasesChanged.emit()

    @Property(str, notify=phasesChanged)
    def phasesXml(self):
        xml = dicttoxml(self.phases, attr_type=False)
        xml = xml.decode()
        return xml

    @Slot(int, str, str)
    def editPhase(self, phase_index, parameter_name, new_value):
        #print("----", phase_index, parameter_name, new_value)
        self.phases[phase_index][parameter_name] = new_value
        self.phasesChanged.emit()

    @Slot(int, int, str, str)
    def editPhaseParameter(self, phase_index, parameter_index, parameter_name, new_value):
        #print("----", phase_index, parameter_index, parameter_name, new_value)
        self.phases[phase_index]['parameters'][parameter_index][parameter_name] = new_value
        self.phasesChanged.emit()



    ####



    def generalizePath(self, rcif_path: str) -> str:
        """
        Generalize the filepath to be platform-specific, so all file operations
        can be performed.
        :param URI rcfPath: URI to the file
        :return URI filename: platform specific URI
        """
        filename = urlparse(rcif_path).path
        if not sys.platform.startswith("win"):
            return filename
        if filename[0] == '/':
            filename = filename[1:].replace('/', os.path.sep)
        return filename

    @Slot(str)
    def addSampleFromCif(self, cif_path):
        #print("cif_path", cif_path)
        cif_path = self.generalizePath(cif_path)
        self.crystal2 = Crystal2.from_cif_file(cif_path)
        #print(self.crystal2)
        #print(self.crystal2.atoms)
        self.sample2.phase = self.crystal2
        self.updateCalculatedData2()
        self.phases2Changed.emit()
        self.crystal2.extent = np.array([2, 2, 2])
        print(self.crystal2.all_sites())
        print(self.crystal2.extent)


    @Property(str, notify=phases2Changed)
    def phasesCif(self):
        #print("str(self.crystal2.cif)", str(self.crystal2.cif))
        if self.crystal2 is None:
            return ""
        return str(self.crystal2.cif)

    @Property('QVariant', notify=phases2Changed)
    def phases2Dict(self):
        phases = [self.sample2.phase.as_dict()]
        return phases

    @Property(str, notify=phases2Changed)
    def phases2Xml(self):
        phases = [self.sample2.phase.as_dict()]
        xml = dicttoxml(phases, attr_type=False)
        xml = xml.decode()
        return xml
