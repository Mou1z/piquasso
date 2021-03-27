#
# Copyright (C) 2020 by TODO - All rights reserved.
#

from piquasso.api.circuit import Circuit
from piquasso.api.result import Result


class GaussianCircuit(Circuit):

    def get_instruction_map(self):
        return {
            "Interferometer": self._passive_linear,
            "Beamsplitter": self._passive_linear,
            "Phaseshifter": self._passive_linear,
            "MachZehnder": self._passive_linear,
            "Fourier": self._passive_linear,
            "GaussianTransform": self._linear,
            "Squeezing": self._linear,
            "QuadraticPhase": self._linear,
            "Squeezing2": self._linear,
            "ControlledX": self._linear,
            "ControlledZ": self._linear,
            "Displacement": self._displacement,
            "PositionDisplacement": self._displacement,
            "MomentumDisplacement": self._displacement,
            "MeasureHomodyne": self._measure_dyne,
            "MeasureHeterodyne": self._measure_dyne,
            "MeasureDyne": self._measure_dyne,
            "Vacuum": self._vacuum,
            "Mean": self._mean,
            "Covariance": self._covariance,
            "MeasureParticleNumber": self._measure_particle_number,
            "MeasureThreshold": self._measure_threshold,
        }

    def _passive_linear(self, instruction):
        self.state._apply_passive_linear(
            instruction._passive_representation,
            instruction.modes
        )

    def _linear(self, instruction):
        self.state._apply_linear(
            P=instruction._passive_representation,
            A=instruction._active_representation,
            modes=instruction.modes
        )

    def _displacement(self, instruction):
        self.state._apply_displacement(
            **instruction.params,
            modes=instruction.modes,
        )

    def _measure_dyne(self, instruction):
        outcomes = self.state._apply_generaldyne_measurement(
            **instruction.params,
            modes=instruction.modes,
        )

        self._add_result(
            [
                Result(instruction=instruction, outcome=outcome)
                for outcome in outcomes
            ]
        )

    def _vacuum(self, instruction):
        self.state.reset()

    def _mean(self, instruction):
        self.state.mean = instruction.params["mean"]

    def _covariance(self, instruction):
        self.state.cov = instruction.params["cov"]

    def _measure_particle_number(self, instruction):
        outcome = self.state._apply_particle_number_measurement(
            cutoff=instruction.params["cutoff"],
            shots=instruction.params["shots"],
            modes=instruction.modes,
        )

        self._add_result(
            Result(instruction=instruction, outcome=outcome)
        )

    def _measure_threshold(self, instruction):
        outcome = self.state._apply_threshold_measurement(
            shots=instruction.params["shots"],
            modes=instruction.modes,
        )

        self._add_result(
            Result(instruction=instruction, outcome=outcome)
        )
