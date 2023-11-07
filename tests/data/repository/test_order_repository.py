import unittest
from pathlib import Path

from domain.repository import OrderRepository
from domain.models import Order
from data.factory_repository.factory_order_repository import FactoryFtpOrderRepository


class GettingOrdersTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cfg_file = Path('./configurations.yaml')

        cls.__order_rep: OrderRepository = FactoryFtpOrderRepository(
            param_cfg_file_path=cfg_file).provide_order_repository()

    def test_receiving_multiple_orders(self):
        actual_orders: list[Order] = self.__order_rep.get_orders()

        exp_orders: list[Order] = [
            Order(
                counterparty="ДЗЕРЖИНСКОЕ ТУ ДОАВ",
                car_plate="2824LS Е 876 УХ 134"
            ),
            Order(
                counterparty="Банк ДОМ.РФ",
                car_plate="Мерседес Е 366 УА 716"
            ),
            Order(
                counterparty="ГКУ ЦЗН БЫКОВСКОГО РАЙОНА",
                car_plate="Мерседес А001АА 134"
            )
        ]

        self.assertTrue(actual_orders == exp_orders)  # add assertion here


if __name__ == '__main__':
    unittest.main()
