import unittest
from pathlib import Path
from pprint import pprint

from domain.repository import EquipmentsRepository
from domain.models import Equipment
from data.factory_repository.factory_equipment_repository import (
    FactoryEquipmentsRepository,
    FactoryFtpEquipmentsRepository
)


class GettingEquipmentsListTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cfg_file = Path('./configurations.yaml')

        cls.__equipments_rep: EquipmentsRepository \
            = FactoryFtpEquipmentsRepository(cfg_file).provide_equipments_repository()

    def test_receiving_multiple_position_of_equipment(self):
        actual_equipments: list[Equipment] = self.__equipments_rep.get_equipments()

        exp_equipments: list[Equipment] = [
            Equipment(
                name="*1,1 Платы материнские старые до поколения Pentium 4,ноутбуков,серверов (Очищенные),,,"),
            Equipment(
                name="*1,1,1 Платы ноутбуков(Очищенные),,,,"),
            Equipment(
                name="Костюм СЕВЕР МТ-2,зимний,к+бр.,тк.смес,утеп Термоф илл,т. син  с СОП,р.. 44-46/170-176")
        ]

        self.assertTrue(actual_equipments == exp_equipments)


if __name__ == '__main__':
    unittest.main()
