from pathlib import Path

import unittest

from data.source.local.storage_applications_impl.SQLite.SQLite_storage_application import SQLiteStorageApplications
from data.source.local.model import ApplicationStorageDto, PreservationApplicationDto


class GettingAllApplicationsTestCase(unittest.TestCase):
    path_to_tes_db = Path(
        'D:\\programms\Python\\RecyclingCenterServer\\tests\\data\\source\\local\\storage_applications_impl\\SQLite\\test_db\\test_db.db'
    )

    def setUp(self):
        self.stor_applications = SQLiteStorageApplications('test_get_all_db', self.path_to_tes_db)

    def test_get_all(self):
        actual_applications: list[ApplicationStorageDto] = self.stor_applications.get_all()

        exp_data = [
            (1, "2824LS Е 876 УХ 134", "ДЗЕРЖИНСКОЕ ТУ ДОАВ", "inbound", "phones", "camera 1", "scales 1", 23.0, 3.0,
             1.0, 2.0, "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "2023-11-03", 0),
            (2, "ABC123", "Company X", "inbound", "Truck", "camera 1", "scales 2", 5000.0, 200.0, 50.0, 4950.0,
             "https://example.com/photo1.jpg", "2023-11-02", 0),
            (3, "JKL456", "Company TT", "outbound", "Truck", "camera 2", "scales 2", 6000.0, 250.0, 0.1, 5675.0,
             "https://example.com/photo3.jpg", "2023-11-04", 0),
            (4, "Mercedes J4Y 3443", "Company TYT", "outbound", "washing machines", "camera 1", "scales 2", 650.0, 40,
             0.3, 530.0, "https://example.com/photo3.jpg", "2023-11-04", 0),
            (
                5, "Мерседес А001АА 134", "ГКУ ЦЗН БЫКОВСКОГО РАЙОНА", "inbound", "monitors", "camera 1", "scales 2",
                650.0,
                0.0, 0.2, 600.0, "ftp://example.com/photo9.jpg", "2023-11-04", 0)

        ]
        exp_applications: list[ApplicationStorageDto] = [
            ApplicationStorageDto(*record) for record in exp_data
        ]

        self.assertTrue(exp_applications == actual_applications)  # add assertion here


class SaveApplicationTestCases(unittest.TestCase):
    path_to_tes_db = Path(
        'D:\\programms\Python\\RecyclingCenterServer\\tests\\data\\source\\local\\storage_applications_impl\\SQLite\\test_db\\test_db.db'
    )

    test_record_1 = PreservationApplicationDto(
        car_plate="JKL456",
        counterparty="ДЗЕРЖИНСКОЕ ТУ ДОАВ",
        operation_type='inbound',
        equipment_type='notebooks',
        camera_type='camera 2',
        scales_type='scales 2',
        weight_gross=3.5,
        weight_extra=0.2,
        weight_container=2,
        weight_net=1.5,
        url_photo='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        date='03.11.2023',
        end_weighing=False
    )

    test_record_2 = PreservationApplicationDto(
        car_plate="GPT323",
        counterparty="ДЗЕРЖИНСКОЕ ТУ ДОАВ",
        operation_type='inbound',
        equipment_type='printers',
        camera_type='camera 1',
        scales_type='scales 2',
        weight_gross=300,
        weight_extra=0.2,
        weight_container=5,
        weight_net=280,
        url_photo='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        date='04.11.2023',
        end_weighing=False
    )

    test_record_3 = PreservationApplicationDto(
        car_plate="HDS323",
        counterparty="Банк ДОМ.РФ",
        operation_type='outbound',
        equipment_type='monitors',
        camera_type='camera 1',
        scales_type='scales 1',
        weight_gross=81,
        weight_extra=0.1,
        weight_container=1,
        weight_net=78,
        url_photo='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        date='12.11.2023',
        end_weighing=False
    )

    stor_applications = None

    def setUp(self):
        self.stor_applications = SQLiteStorageApplications("test_save_db", self.path_to_tes_db)

    def test_save_one_application(self):
        self.stor_applications.save(self.test_record_1)
        actual_applications = self.stor_applications.get_all()

        exp_applications: list[ApplicationStorageDto] = [
            ApplicationStorageDto(
                id=1,
                car_plate="JKL456",
                counterparty="ДЗЕРЖИНСКОЕ ТУ ДОАВ",
                operation_type='inbound',
                equipment_type='notebooks',
                camera_type='camera 2',
                scales_type='scales 2',
                weight_gross=3.5,
                weight_extra=0.2,
                weight_container=2,
                weight_net=1.5,
                url_photo='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                date='03.11.2023',
                end_weighing=False
            )
        ]

        self.assertTrue(exp_applications == actual_applications)

    def test_save_any_applications(self):
        self.stor_applications.save(self.test_record_1)
        self.stor_applications.save(self.test_record_2)
        self.stor_applications.save(self.test_record_3)

        actual_applications = self.stor_applications.get_all()

        exp_applications: list[ApplicationStorageDto] = [
            ApplicationStorageDto(
                id=1,
                car_plate="JKL456",
                counterparty="ДЗЕРЖИНСКОЕ ТУ ДОАВ",
                operation_type='inbound',
                equipment_type='notebooks',
                camera_type='camera 2',
                scales_type='scales 2',
                weight_gross=3.5,
                weight_extra=0.2,
                weight_container=2,
                weight_net=1.5,
                url_photo='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                date='03.11.2023',
                end_weighing=False
            ),
            ApplicationStorageDto(
                id=2,
                car_plate="GPT323",
                counterparty="ДЗЕРЖИНСКОЕ ТУ ДОАВ",
                operation_type='inbound',
                equipment_type='printers',
                camera_type='camera 1',
                scales_type='scales 2',
                weight_gross=300,
                weight_extra=0.2,
                weight_container=5,
                weight_net=280,
                url_photo='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                date='04.11.2023',
                end_weighing=False
            ),
            ApplicationStorageDto(
                id=3,
                car_plate="HDS323",
                counterparty="Банк ДОМ.РФ",
                operation_type='outbound',
                equipment_type='monitors',
                camera_type='camera 1',
                scales_type='scales 1',
                weight_gross=81,
                weight_extra=0.1,
                weight_container=1,
                weight_net=78,
                url_photo='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                date='12.11.2023',
                end_weighing=False
            )
        ]

        self.assertTrue(exp_applications == actual_applications)

    def tearDown(self):
        self.stor_applications.remove_storage()


if __name__ == '__main__':
    unittest.main()
