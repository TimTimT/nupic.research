# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2014, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

import abc
from prettytable import PrettyTable



class AbstractAgent(object):
  __metaclass__ = abc.ABCMeta


  def __init__(self, world):
    """
    @param world (AbstractWorld) The world this agent belongs in.
    """
    self._world = world


  @abc.abstractmethod
  def chooseMotorValue(self):
    """
    Return a plausible next motor value.

    @return (object) motor value (type depends on world)
    """
    return

  def generateSensorimotorSequence(self, length, verbosity=0):
    """
    Generate a sensorimotor sequence of the given length through this agent's
    world.

    @param length (int)           Length of sequence to generate

    @param verbosity (int)        If > 0 print the sequence details

    @return (tuple) (sensor sequence, motor sequence, sensorimotor sequence)
    """
    sensorSequence = []
    motorSequence = []
    sensorimotorSequence = []

    for _ in xrange(length):
      sensorPattern = self._world.sense()
      motorValue = self.chooseMotorValue()
      motorPattern = self._world.move(motorValue)
      sensorSequence.append(sensorPattern)
      motorSequence.append(motorPattern)

      sensorimotorPattern = (sensorPattern |
        set([x + self._world.universe.nSensor for x in motorPattern]))
      sensorimotorSequence.append(sensorimotorPattern)

    if verbosity > 0:
      table = PrettyTable(["Iteration", "Sensor", "Motor"])
      for i in xrange(len(sensorSequence)):
        sensorPattern = sensorSequence[i]
        motorPattern = motorSequence[i]
        if sensorPattern is None:
          table.add_row([i, "<reset>", "<reset>"])
        else:
          table.add_row([i, list(sensorPattern), list(motorPattern)])
      print table

    return (sensorSequence, motorSequence, sensorimotorSequence)
