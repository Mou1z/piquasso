#
# Copyright 2021-2024 Budapest Quantum Computing Group
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import piquasso as pq

import numpy as np

from jax import grad, jit


def test_mean_photon_number_gradient():
    def func(r):
        simulator = pq.GaussianSimulator(d=2, connector=pq.JaxConnector())

        with pq.Program() as program:
            pq.Q() | pq.Vacuum()

            pq.Q(0) | pq.Squeezing(r)

            pq.Q(0, 1) | pq.Beamsplitter()

        result = simulator.execute(program)

        mean_photon_number = result.state.mean_photon_number(modes=(0, 1))

        return mean_photon_number

    grad_func = jit(grad(func))

    r = 0.3

    assert np.allclose(func(r), np.sinh(r) ** 2)
    assert np.allclose(grad_func(r), 2 * np.sinh(r) * np.cosh(r))


def test_variance_photon_number_gradient():
    def func(r):
        simulator = pq.GaussianSimulator(d=2, connector=pq.JaxConnector())

        with pq.Program() as program:
            pq.Q() | pq.Vacuum()

            pq.Q(0) | pq.Displacement(r)

            pq.Q(0, 1) | pq.Beamsplitter()

        result = simulator.execute(program)

        variance_photon_number = result.state.variance_photon_number(modes=(0, 1))

        return variance_photon_number

    grad_func = jit(grad(func))

    r = 0.3
    assert np.allclose(func(r), r**2)
    assert np.allclose(grad_func(r), 2 * r)
