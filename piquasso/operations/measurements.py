#
# Copyright (C) 2020 by TODO - All rights reserved.
#

import numpy as np

from piquasso.core.registry import _register
from piquasso.api.operation import Operation


@_register
class MeasureParticleNumber(Operation):
    """Particle number measurement.

    # TODO: Measure only certain modes!
    """

    def __init__(self):
        pass


@_register
class MeasureDyne(Operation):
    """General-dyne measurement."""

    def __init__(self, detection_covariance):
        super().__init__(detection_covariance)


@_register
class MeasureHomodyne(MeasureDyne):
    """Homodyne measurement."""

    def __init__(self, *, z=1e-4):
        super().__init__(
            detection_covariance=np.array(
                [
                    [z ** 2, 0],
                    [0, (1 / z) ** 2],
                ]
            )
        )


@_register
class MeasureHeterodyne(MeasureDyne):
    """Heterodyne measurement."""

    def __init__(self):
        super().__init__(
            detection_covariance=np.identity(2)
        )
