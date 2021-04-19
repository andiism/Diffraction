# noqa: E501
import os
import datetime
from typing import Union

from dicttoxml import dicttoxml
# import xmltodict
# from xml.dom.minidom import parseString
import json

from easyCore import np, borg
from easyCore.Symmetry.tools import SpacegroupInfo
from easyCore.Utils.UndoRedo import FunctionStack
from easyCore.Utils.classTools import generatePath

from easyDiffractionLib.sample import Sample
from easyAppLogic.Utils.Utils import generalizePath
from easyDiffractionApp.Logic.DataStore import DataSet1D, DataStore
from easyDiffractionLib import Phases, Phase, Lattice, Site, SpaceGroup
from easyDiffractionLib.Elements.Experiments.Experiment import Pars1D
from easyDiffractionLib.Elements.Experiments.Pattern import Pattern1D


class State(object):
    """
    """
    def __init__(self, parent=None, interface=None):
        self.parent = parent
        self._interface = interface
        self._interface_name = interface.current_interface_name
        self.project_save_filepath = ""
        self.project_load_filepath = ""
        self._project_info = self._defaultProjectInfo()

        self._experiment_parameters = None
        self._experiment_data_as_xml = ""
        self.experiment_data = None
        self._experiment_data = None
        self._experiment_loaded = False
        self._experiment_skipped = False
        self.experiments = self._defaultExperiments()

        self._parameters = None
        self._instrument_parameters = None
        self._status_model = None
        self._state_changed = False

        self.phases = None
        self._phases_as_obj = []
        self._phases_as_xml = ""
        self._phases_as_cif = ""
        self._sample = self._defaultSample()
        self._current_phase_index = 0
        # Experiment
        self._pattern_parameters_as_obj = self._defaultPatternParameters()
        self._instrument_parameters_as_obj = self._defaultInstrumentParameters()  # noqa: E501
        self._instrument_parameters_as_xml = ""
        # Parameters
        self._parameters_as_obj = []
        self._parameters_as_xml = []
        self._parameters_filter_criteria = ""

        self._data = self._defaultData()
        self._simulation_parameters_as_obj = self._defaultSimulationParameters()

    ####################################################################################################################
    ####################################################################################################################
    # data
    ####################################################################################################################
    ####################################################################################################################

    def _defaultData(self):
        x_min = self._defaultSimulationParameters()['x_min']
        x_max = self._defaultSimulationParameters()['x_max']
        x_step = self._defaultSimulationParameters()['x_step']
        num_points = int((x_max - x_min) / x_step + 1)
        x_data = np.linspace(x_min, x_max, num_points)

        data = DataStore()

        data.append(
            DataSet1D(
                name='D1A@ILL data',
                x=x_data, y=np.zeros_like(x_data),
                x_label='2theta (deg)', y_label='Intensity',
                data_type='experiment'
            )
        )
        data.append(
            DataSet1D(
                name='{:s} engine'.format(self._interface_name),
                x=x_data, y=np.zeros_like(x_data),
                x_label='2theta (deg)', y_label='Intensity',
                data_type='simulation'
            )
        )
        data.append(
            DataSet1D(
                name='Difference',
                x=x_data, y=np.zeros_like(x_data),
                x_label='2theta (deg)', y_label='Difference',
                data_type='simulation'
            )
        )
        return data

    def _defaultSimulationParameters(self):
        return {
            "x_min": 10.0,
            "x_max": 120.0,
            "x_step": 0.1
        }

    ####################################################################################################################
    ####################################################################################################################
    # experiment
    ####################################################################################################################
    ####################################################################################################################

    def _defaultExperiment(self):
        return {
            "label": "D1A@ILL",
            "color": "#00a3e3"
        }

    def _loadExperimentData(self, file_url):
        print("+ _loadExperimentData")
        file_path = generalizePath(file_url)
        data = self._data.experiments[0]
        data.x, data.y, data.e = np.loadtxt(file_path, unpack=True)
        return data

    def _experimentDataParameters(self, data):
        x_min = data.x[0]
        x_max = data.x[-1]
        x_step = (x_max - x_min) / (len(data.x) - 1)
        parameters = {
            "x_min":  x_min,
            "x_max":  x_max,
            "x_step": x_step
        }
        return parameters

    def _onExperimentDataAdded(self):
        self._experiment_parameters = self._experimentDataParameters(self._experiment_data)  # noqa: E501
        self.simulationParametersAsObj = json.dumps(self._experiment_parameters)  # noqa: E501
        self.experiments = [self._defaultExperiment()]

    def experimentDataXYZ(self):
        return (self._experiment_data.x, self._experiment_data.y, self._experiment_data.e)  # noqa: E501

    def _defaultExperiments(self):
        return []

    def experimentLoaded(self, loaded: bool):
        print(">>> EXPERIMENT LOADED: {}".format(str(loaded)))
        if self._experiment_loaded == loaded:
            return
        self._experiment_loaded = loaded

    def experimentSkipped(self, skipped: bool):
        if self._experiment_skipped == skipped:
            return
        self._experiment_skipped = skipped

    def _setExperimentDataAsXml(self):
        self._experiment_data_as_xml = dicttoxml(self.experiments, attr_type=True).decode()  # noqa: E501

    def addExperimentDataFromXye(self, file_url):
        def outer1(obj):
            def inner():
                obj._experiment_data = self._loadExperimentData(file_url)
                obj.experimentLoaded(True)
                obj.experimentSkipped(False)
                obj.parent.undoRedoChanged.emit()
                obj.parent.experimentDataAdded.emit()
            return inner

        def outer2(obj):
            def inner():
                obj.experiments.clear()
                obj.experimentLoaded(False)
                obj.experimentSkipped(True)
                obj.parent.undoRedoChanged.emit()
                obj.experimentDataRemoved.emit()
            return inner

        borg.stack.push(FunctionStack(self, outer1(self), outer2(self)))
        self.parent.experimentLoadedChanged.emit()

    def removeExperiment(self):
        def outer1(obj):
            def inner():
                obj.experiments.clear()
                obj.experimentDataRemoved.emit()
                obj.experimentLoaded = False
                obj.experimentSkipped = False
                obj.parent.undoRedoChanged.emit()
            return inner

        def outer2(obj):
            data = self._experiment_data

            def inner():
                obj._experiment_data = data
                obj.parent.experimentDataAdded.emit()
                obj.experimentLoaded = True
                obj.experimentSkipped = False
                obj.parent.undoRedoChanged.emit()
            return inner

        borg.stack.push(FunctionStack(self, outer1(self), outer2(self)))
        self.parent.experimentLoadedChanged.emit()

    ####################################################################################################################
    ####################################################################################################################
    # project
    ####################################################################################################################
    ####################################################################################################################

    def _defaultProjectInfo(self):
        return dict(
            name="Example Project",
            location=os.path.join(os.path.expanduser("~"), "Example Project"),
            short_description="diffraction, powder, 1D",
            samples="Not loaded",
            experiments="Not loaded",
            calculations="Not created",
            modified=datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
        )

    def projectInfoAsJson(self, json_str):
        self._project_info = json.loads(json_str)

    def projectInfoAsCif(self):
        cif_list = []
        for key, value in self._project_info.items():
            if ' ' in value:
                value = f"'{value}'"
            cif_list.append(f'_{key} {value}')
        cif_str = '\n'.join(cif_list)
        return cif_str

    def editProjectInfo(self, key, value):
        if self._project_info[key] == value:
            return
        self._project_info[key] = value

    def createProject(self):
        projectPath = self._project_info['location']
        mainCif = os.path.join(projectPath, 'project.cif')
        samplesPath = os.path.join(projectPath, 'samples')
        experimentsPath = os.path.join(projectPath, 'experiments')
        calculationsPath = os.path.join(projectPath, 'calculations')
        if not os.path.exists(projectPath):
            os.makedirs(projectPath)
            os.makedirs(samplesPath)
            os.makedirs(experimentsPath)
            os.makedirs(calculationsPath)
            with open(mainCif, 'w') as file:
                file.write(self.projectInfoAsCif)
        else:
            print(f"ERROR: Directory {projectPath} already exists")

    def stateHasChanged(self, changed: bool):
        if self._state_changed == changed:
            return
        self._state_changed = changed

    def _loadProjectAs(self, filepath):
        """
        """
        self.project_load_filepath = filepath
        print("LoadProjectAs " + filepath)
        self._loadProject()

    def _loadProject(self):
        """
        """
        path = generalizePath(self.project_load_filepath)
        if not os.path.isfile(path):
            print("Failed to find project: '{0}'".format(path))
            return
        with open(path, 'r') as xml_file:
            descr = json.load(xml_file)

        self._phases_as_cif = descr['phases']
        self._sample.phases = Phases.from_cif_str(self._phases_as_cif)

        # send signal to tell the proxy we changed phases
        self.parent.phaseAdded.emit()
        self.parent.phasesAsObjChanged.emit()

        # experiment
        if 'experiments' in descr:
            self.experimentLoaded = True
            self._data.experiments[0].x = np.array(descr['experiments'][0])
            self._data.experiments[0].y = np.array(descr['experiments'][1])
            self._data.experiments[0].e = np.array(descr['experiments'][2])
            self._experiment_data = self._data.experiments[0]
            self.parent.experimentDataAdded.emit()
            self.parent._onParametersChanged()

            # background
            if 'background' in descr:
                self.parent._background_proxy.removeAllPoints()
                bg_x = descr['background'][0]
                bg_y = descr['background'][1]
                for i, point in enumerate(bg_x):
                    bg_point = (point, bg_y[i])
                    self.parent._background_proxy.addPoint(bg_point)
        else:
            # delete existing experiment
            self.removeExperiment()
            self.experimentLoaded = False
            if descr['experiment_skipped']:
                self.experimentSkipped = True
                self.parent.experimentSkippedChanged.emit()

        # project info
        self.projectInfoAsJson = json.dumps(descr['project_info'])

    def _saveProject(self):
        """
        """
        projectPath = self.projectInfoAsJson['location']
        project_save_filepath = os.path.join(projectPath, 'project.json')
        descr = {}
        descr['phases'] = self._phases_as_cif

        if self.experiments:
            experiments_x = self._data.experiments[0].x
            experiments_y = self._data.experiments[0].y
            experiments_e = self._data.experiments[0].e
            descr['experiments'] = [experiments_x, experiments_y, experiments_e]  # noqa: E501

            bg_x = self._background_proxy.asObj.x_sorted_points
            bg_y = self._background_proxy.asObj.y_sorted_points
            descr['background'] = [bg_x, bg_y]

        descr['project_info'] = self._project_info
        # Reading those is not yet implemented
        descr['parameters'] = self._parameters_as_obj
        descr['instrument_parameters'] = self._instrument_parameters_as_obj
        descr['experiment_skipped'] = self._experiment_skipped

        content_json = json.dumps(descr, indent=4, default=self.default)
        path = generalizePath(project_save_filepath)
        createFile(path, content_json)

    def default(self, obj):
        if type(obj).__module__ == np.__name__:
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            else:
                return obj.item()
        raise TypeError('Unknown type:', type(obj))

    ####################################################################################################################
    ####################################################################################################################
    # SAMPLE
    ####################################################################################################################
    ####################################################################################################################

    def _defaultSample(self):
        sample = Sample(parameters=Pars1D.default(), pattern=Pattern1D.default(), interface=self._interface)  # noqa: E501
        sample.pattern.zero_shift = 0.0
        sample.pattern.scale = 1.0
        sample.parameters.wavelength = 1.912
        sample.parameters.resolution_u = 0.1447
        sample.parameters.resolution_v = -0.4252
        sample.parameters.resolution_w = 0.3864
        sample.parameters.resolution_x = 0.0
        sample.parameters.resolution_y = 0.0961
        return sample

    def addSampleFromCif(self, cif_url):
        cif_path = generalizePath(cif_url)
        if borg.stack.enabled:
            borg.stack.beginMacro(f'Loaded cif: {cif_path}')
        self._sample.phases = Phases.from_cif_file(cif_path)
        if borg.stack.enabled:
            borg.stack.endMacro()

    ####################################################################################################################
    ####################################################################################################################
    # phases
    ####################################################################################################################
    ####################################################################################################################

    def currentPhaseIndex(self, new_index: int):
        if self._current_phase_index == new_index or new_index == -1:
            return
        self._current_phase_index = new_index

    def removePhase(self, phase_name: str):
        if phase_name in self._sample.phases.phase_names:
            del self._sample.phases[phase_name]
            return True
        return False

    def addDefaultPhase(self):
        if borg.stack.enabled:
            borg.stack.beginMacro('Loaded default phase')
        self._sample.phases = self._defaultPhase()
        if borg.stack.enabled:
            borg.stack.endMacro()

    def _defaultPhase(self):
        space_group = SpaceGroup.from_pars('P 42/n c m')
        cell = Lattice.from_pars(8.56, 8.56, 6.12, 90, 90, 90)
        atom = Site.from_pars(label='Cl1', specie='Cl', fract_x=0.125, fract_y=0.167, fract_z=0.107)  # noqa: E501
        atom.add_adp('Uiso', Uiso=0.0)
        phase = Phase('Dichlorine', spacegroup=space_group, cell=cell)
        phase.add_atom(atom)
        return phase

    def _onPhaseAdded(self, background_obj):
        if self._interface.current_interface_name != 'CrysPy':
            self._interface.generate_sample_binding("filename", self._sample)
        self._sample.phases.name = 'Phases'
        self._sample.set_background(background_obj)

    def currentCrystalSystem(self):
        phases = self._sample.phases
        if not phases:
            return ''

        current_system = phases[self._current_phase_index].spacegroup.crystal_system  # noqa: E501
        current_system = current_system.capitalize()
        return current_system

    def setCurrentCrystalSystem(self, new_system: str):
        new_system = new_system.lower()
        space_group_numbers = SpacegroupInfo.get_ints_from_system(new_system)
        top_space_group_number = space_group_numbers[0]
        top_space_group_name = SpacegroupInfo.get_symbol_from_int_number(top_space_group_number)  # noqa: E501
        self._setCurrentSpaceGroup(top_space_group_name)

    def phasesAsExtendedCif(self):
        if len(self._sample.phases) == 0:
            return

        symm_ops = self._sample.phases[0].spacegroup.symmetry_opts
        symm_ops_cif_loop = "loop_\n _symmetry_equiv_pos_as_xyz\n"
        for symm_op in symm_ops:
            symm_ops_cif_loop += f' {symm_op.as_xyz_string()}\n'
        return self._phases_as_cif + symm_ops_cif_loop

    def phasesAsCif(self, phases_as_cif):
        if self._phases_as_cif == phases_as_cif:
            return
        self._sample.phases = Phases.from_cif_str(phases_as_cif)

    def _setPhasesAsObj(self):
        self._phases_as_obj = self._sample.phases.as_dict()['data']

    def _setPhasesAsXml(self):
        self._phases_as_xml = dicttoxml(self._phases_as_obj, attr_type=True).decode()  # noqa: E501

    def _setPhasesAsCif(self):
        self._phases_as_cif = str(self._sample.phases.cif)

    def _setCurrentSpaceGroup(self, new_name: str):
        phases = self._sample.phases
        if phases[self._current_phase_index].spacegroup.space_group_HM_name == new_name:  # noqa: E501
            return
        phases[self._current_phase_index].spacegroup.space_group_HM_name = new_name  # noqa: E501

    def _spaceGroupSettingList(self):
        phases = self._sample.phases
        if not phases:
            return []

        current_number = self._currentSpaceGroupNumber()
        settings = SpacegroupInfo.get_compatible_HM_from_int(current_number)
        return settings

    def _spaceGroupNumbers(self):
        current_system = self.currentCrystalSystem().lower()
        numbers = SpacegroupInfo.get_ints_from_system(current_system)
        return numbers

    def _currentSpaceGroupNumber(self):
        phases = self._sample.phases
        current_number = phases[self._current_phase_index].spacegroup.int_number  # noqa: E501
        return current_number

    def getCurrentSpaceGroup(self):
        def space_group_index(number, numbers):
            if number in numbers:
                return numbers.index(number)
            return 0

        phases = self._sample.phases
        if not phases:
            return -1

        space_group_numbers = self._spaceGroupNumbers()
        current_number = self._currentSpaceGroupNumber()
        current_idx = space_group_index(current_number, space_group_numbers)
        return current_idx

    def currentSpaceGroup(self, new_idx: int):
        space_group_numbers = self._spaceGroupNumbers()
        space_group_number = space_group_numbers[new_idx]
        space_group_name = SpacegroupInfo.get_symbol_from_int_number(space_group_number)  # noqa: E501
        self._setCurrentSpaceGroup(space_group_name)

    def formattedSpaceGroupList(self):
        def format_display(num):
            name = SpacegroupInfo.get_symbol_from_int_number(num)
            return f"<font color='#999'>{num}</font> {name}"

        space_group_numbers = self._spaceGroupNumbers()
        display_list = [format_display(num) for num in space_group_numbers]
        return display_list

    def crystalSystemList(self):
        systems = [system.capitalize() for system in SpacegroupInfo.get_all_systems()]  # noqa: E501
        return systems

    def formattedSpaceGroupSettingList(self):
        def format_display(num, name):
            return f"<font color='#999'>{num}</font> {name}"

        raw_list = self._spaceGroupSettingList()
        formatted_list = [format_display(i + 1, name) for i, name in enumerate(raw_list)]  # noqa: E501
        return formatted_list

    def currentSpaceGroupSetting(self):
        phases = self._sample.phases
        if not phases:
            return 0

        settings = self._spaceGroupSettingList()
        current_setting = phases[self._current_phase_index].spacegroup.space_group_HM_name.raw_value  # noqa: E501
        current_number = settings.index(current_setting)
        return current_number

    def setCurrentSpaceGroupSetting(self, new_number: int):
        settings = self._spaceGroupSettingList()
        name = settings[new_number]
        self._setCurrentSpaceGroup(name)

    ####################################################################################################################
    # Phase: Atoms
    ####################################################################################################################
    def addDefaultAtom(self):
        atom = Site.from_pars(label='Label2',
                              specie='O',
                              fract_x=0.05,
                              fract_y=0.05,
                              fract_z=0.05)
        atom.add_adp('Uiso', Uiso=0.0)
        self._sample.phases[self._current_phase_index].add_atom(atom)

    def removeAtom(self, atom_label: str):
        del self._sample.phases[self._current_phase_index].atoms[atom_label]

    ####################################################################################################################
    # Simulation parameters
    ####################################################################################################################

    def simulationParametersAsObj(self, json_str):
        if self._simulation_parameters_as_obj == json.loads(json_str):
            return

        self._simulation_parameters_as_obj = json.loads(json_str)

    def _defaultPatternParameters(self):
        return {
            "scale":      1.0,
            "zero_shift": 0.0
        }

    def _setPatternParametersAsObj(self):
        parameters = self._sample.pattern.as_dict()
        self._pattern_parameters_as_obj = parameters
 
    ####################################################################################################################
    # Instrument parameters (wavelength, resolution_u, ..., resolution_y)
    ####################################################################################################################

    def _defaultInstrumentParameters(self):
        return {
            "wavelength":   1.0,
            "resolution_u": 0.01,
            "resolution_v": -0.01,
            "resolution_w": 0.01,
            "resolution_x": 0.0,
            "resolution_y": 0.0
        }

    def _setInstrumentParametersAsObj(self):
        parameters = self._sample.parameters.as_dict()
        self._instrument_parameters_as_obj = parameters

    def _setInstrumentParametersAsXml(self):
        parameters = [self._instrument_parameters_as_obj]
        self._instrument_parameters_as_xml = dicttoxml(parameters, attr_type=True).decode()  # noqa: E501
 
    ####################################################################################################################
    # Calculated data
    ####################################################################################################################

    def _updateCalculatedData(self):
        if not self.experimentLoaded and not self.experimentSkipped:
            return

        self._sample.output_index = self._current_phase_index

        #  THIS IS WHERE WE WOULD LOOK UP CURRENT EXP INDEX
        sim = self._data.simulations[0]

        if self.experimentLoaded:
            exp = self._data.experiments[0]
            sim.x = exp.x

        elif self.experimentSkipped:
            x_min = float(self._simulation_parameters_as_obj['x_min'])
            x_max = float(self._simulation_parameters_as_obj['x_max'])
            x_step = float(self._simulation_parameters_as_obj['x_step'])
            num_points = int((x_max - x_min) / x_step + 1)
            sim.x = np.linspace(x_min, x_max, num_points)

        sim.y = self._interface.fit_func(sim.x)    # noqa: E501
        hkl = self._interface.get_hkl()

        self.parent._plotting_1d_proxy.setCalculatedData(sim.x, sim.y)
        self.parent._plotting_1d_proxy.setBraggData(hkl['ttheta'], hkl['h'], hkl['k'], hkl['l'])  # noqa: E501

    ####################################################################################################################
    # Fitables (parameters table from analysis tab & ...)
    ####################################################################################################################

    def _setParametersAsObj(self):
        self._parameters_as_obj.clear()

        par_ids, par_paths = generatePath(self._sample, True)
        for par_index, par_path in enumerate(par_paths):
            par_id = par_ids[par_index]
            par = borg.map.get_item_by_key(par_id)

            if not par.enabled:
                continue

            if self._parameters_filter_criteria.lower() not in par_path.lower():  # noqa: E501
                continue

            self._parameters_as_obj.append({
                "id":     str(par_id),
                "number": par_index + 1,
                "label":  par_path,
                "value":  par.raw_value,
                "unit":   '{:~P}'.format(par.unit),
                "error":  float(par.error),
                "fit":    int(not par.fixed)
            })

    def _setParametersAsXml(self):
        self._parameters_as_xml = dicttoxml(self._parameters_as_obj, attr_type=False).decode()  # noqa: E501

    def setParametersFilterCriteria(self, new_criteria):
        if self._parameters_filter_criteria == new_criteria:
            return
        self._parameters_filter_criteria = new_criteria

    ####################################################################################################################
    # Any parameter
    ####################################################################################################################
    def editParameter(self, obj_id: str, new_value: Union[bool, float, str]):  # noqa: E501
        if not obj_id:
            return

        obj = self._parameterObj(obj_id)
        if obj is None:
            return

        if isinstance(new_value, bool):
            if obj.fixed == (not new_value):
                return

            obj.fixed = not new_value
            self.parent._onParametersChanged()
            self.parent.undoRedoChanged.emit()

        else:
            if obj.raw_value == new_value:
                return

            obj.value = new_value
            self.parent.parametersChanged.emit()

    def _parameterObj(self, obj_id: str):
        if not obj_id:
            return
        obj_id = int(obj_id)
        obj = borg.map.get_item_by_key(obj_id)
        return obj

    ####################################################################################################################
    ####################################################################################################################
    # STATUS
    ####################################################################################################################
    ####################################################################################################################

    def statusModelAsObj(self):
        obj = {
            "calculation":  self._interface.current_interface_name,
            "minimization": f'{self.parent.fitter.current_engine.name} ({self.parent._current_minimizer_method_name})'  # noqa: E501
        }
        self._status_model = obj
        return obj

    def statusModelAsXml(self):
        model = [
            {"label": "Calculation", "value": self._interface.current_interface_name},  # noqa: E501
            {"label": "Minimization",
             "value": f'{self.parent.fitter.current_engine.name} ({self.parent._current_minimizer_method_name})'}  # noqa: E501
        ]
        xml = dicttoxml(model, attr_type=False)
        xml = xml.decode()
        return xml


# utilities. Should probably be moved away from here
def createFile(path, content):
    if os.path.exists(path):
        print(f'File already exists {path}. Overwriting...')
        os.unlink(path)
    try:
        message = f'create file {path}'
        with open(path, "w") as file:
            file.write(content)
    except Exception as exception:
        print(message, exception)