# SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

from PySide2.QtCore import Signal, QObject

from easyDiffractionLib.sample import Sample
from easyDiffractionLib.Profiles.P1D import Instrument1DCWParameters
from easyDiffractionLib.Profiles.P1D import Instrument1DTOFParameters
from easyDiffractionLib.Profiles.P1D import Powder1DParameters


class SampleLogic(QObject):
    """
    """
    SampleChanged = Signal()

    def __init__(self, parent=None, interface=None):
        super().__init__(parent)
        self.parent = parent
        self._interface = interface
        self._phases = parent.l_phase
        self._sample = self._defaultCWSample()

    ####################################################################################################################
    ####################################################################################################################
    # SAMPLE
    ####################################################################################################################
    ####################################################################################################################

    def _defaultCWSample(self):
        sample = Sample(
            phases=self._phases.phases,
            parameters=Instrument1DCWParameters.default(),
            pattern=Powder1DParameters.default(),
            interface=self._interface)
        sample.pattern.zero_shift = 0.0
        sample.pattern.scale = 100.0
        sample.parameters.wavelength = 1.912
        sample.parameters.resolution_u = 0.1447
        sample.parameters.resolution_v = -0.4252
        sample.parameters.resolution_w = 0.3864
        sample.parameters.resolution_x = 0.0
        sample.parameters.resolution_y = 0.0  # 0.0961
        return sample

    def _defaultTOFSample(self):
        sample = Sample(
            phases=self._phases.phases,
            parameters=Instrument1DTOFParameters.default(),
            pattern=Powder1DParameters.default(),
            interface=self._interface)
        sample.pattern.zero_shift = 0.0
        sample.pattern.scale = 100.0
        sample.parameters.dtt1 = 6167.24700
        sample.parameters.dtt2 = -2.28000
        sample.parameters.ttheta_bank = 145.00
        sample.parameters.resolution_sigma0 = 0
        sample.parameters.resolution_sigma1 = 0
        sample.parameters.resolution_sigma2 = 0
        sample.parameters.resolution_gamma0 = 0
        sample.parameters.resolution_gamma1 = 0
        sample.parameters.resolution_gamma2 = 0
        sample.parameters.resolution_alpha0 = 0
        sample.parameters.resolution_alpha1 = 0
        sample.parameters.resolution_beta0 = 0
        sample.parameters.resolution_beta1 = 0
        return sample

    @property
    def experimentType(self):
        exp_type = None
        if issubclass(type(self._sample.parameters), Instrument1DCWParameters):
            exp_type = 'powder1DCW'
        elif issubclass(type(self._sample.parameters), Instrument1DTOFParameters):
            exp_type = 'powder1DTOF'
        else:
            raise AttributeError('Unknown EXP type')
        return exp_type

    @experimentType.setter
    def experimentType(self, new_exp_type: str):
        phases = self._phases.phases
        pattern = self._sample.pattern

        if new_exp_type == 'powder1DCW':
            params = Instrument1DCWParameters.default()
            self._sample = self._defaultCWSample()
        elif new_exp_type == 'powder1DTOF':
            params = Instrument1DTOFParameters.default()
            self._sample = self._defaultTOFSample()
        else:
            raise AttributeError('Unknown Experiment type')

        interface = self._interface
        test_str = 'N' + new_exp_type
        if not self._interface.current_interface.feature_checker(test_str=test_str):
            interfaces = self._interface.interface_compatability(test_str)
            interface.switch(interfaces[0])

        self._sample = Sample(
            phases=phases,
            parameters=params,
            pattern=pattern,
            interface=self._interface)
        self.parent.l_phase.phasesAsObjChanged.emit()
        self.parent.proxy.fitting.calculatorListChanged.emit()
        #self.parent.parametersChanged.emit()

