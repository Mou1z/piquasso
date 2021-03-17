#
# Copyright (C) 2020 by TODO - All rights reserved.
#

import numpy as np
from BoSS.BosonSamplingSimulator import BosonSamplingSimulator
from BoSS.simulation_strategies.GeneralizedCliffordsSimulationStrategy \
    import GeneralizedCliffordsSimulationStrategy

from piquasso.api.circuit import Circuit


class SamplingCircuit(Circuit):
    r"""A circuit for fast boson sampling."""

    def get_operation_map(self):
        return {
            "B": self._multiply_interferometer,
            "R": self._multiply_interferometer,
            "MZ": self._multiply_interferometer,
            "F": self._multiply_interferometer,
            "Sampling": self.sampling,
            "Interferometer": self.interferometer,
        }

    def _multiply_interferometer(self, operation):
        r"""Adds additional phase shifter to the effective interferometer.

        This can be interpreted as placing additional phase shifter (in the network)
        just before performing the sampling. This is realized by multiplying
        interferometer matrix with a matrix representing the phase shifter.

        The annihilation and creation operators on given mode are evolved in the
        following way:

        .. math::
            P(\phi) \hat{a}_k P(\phi)^\dagger = e^{i \phi} \hat{a}_k \\
            P(\phi) \hat{a}_k^\dagger P(\phi)^\dagger
                = e^{- i \phi} \hat{a}_k^\dagger

        Do note, that multiplication occurs only on one specified (as the argument)
        mode and the phase shifter acts as an identity on every other mode.

        Adds additional beam splitter to the effective interferometer.


        This can be interpreted as placing additional beam splitter (in the network)
        just before performing the sampling. This is realized by multiplying
        interferometer matrix with a matrix representing the phase shifter.

        The matrix representation of the beam splitters' operation on two modes is:

        .. math::
            B = \begin{bmatrix}
                t  & r^* \\
                -r & t
            \end{bmatrix},

        where
            :math:`t = \cos(\theta)` and
            :math:`r = e^{- i \phi} \sin(\theta)`.

        Do note, that multiplication occurs only on two specified (as the arguments)
        modes and the beam splitter acts as an identity on every other mode.
        """

        self.state.multiply_interferometer_on_modes(
            operation._passive_representation,
            operation.modes,
        )

    def interferometer(self, operation):
        """Interferometer.

        Adds additional interferometer to the effective interferometer.

        This can be interpreted as placing another interferometer in the network, just
        before performing the sampling. This operation is realized by multiplying
        current effective interferometer matrix with new interferometer matrix.

        Do note, that new interferometer matrix works as interferometer matrix on
        qumodes (provided as the arguments) and as an identity on every other mode.
        """

        J = operation.params[0]
        modes = operation.modes

        assert \
            J.shape == (len(modes), len(modes)), \
            "The number of qumodes should be equal to " \
            "the size of the interferometer matrix."

        self.state.multiply_interferometer_on_modes(J, modes)

    def sampling(self, operation):
        params = operation.params

        simulation_strategy = \
            GeneralizedCliffordsSimulationStrategy(self.state.interferometer)
        sampling_simulator = BosonSamplingSimulator(simulation_strategy)

        initial_state = np.array(self.state.initial_state)
        shots = params[0]
        self.state.results = \
            sampling_simulator.get_classical_simulation_results(initial_state,
                                                                samples_number=shots)
