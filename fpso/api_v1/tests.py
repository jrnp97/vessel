from django.test import TestCase

from rest_framework import status


# Create your tests here.


class TestVesselApi(TestCase):
    """ Class to define tests to proof VesselApi """
    API_PREFIX = '/fpso/api/v1'
    VESSEL_URI = '{prefix}/vessels/'
    VESSEL_DETAIL_URI = '{prefix}/vessels/{code}/'
    EQUIPMENT_URI = '{prefix}/vessels/{code}/equipment/'

    def setUp(self) -> None:
        self.vessel_code = 'MV102'

    def create_vessel(self, vessel_code):
        response = self.client.post(
            path=self.VESSEL_URI.format(prefix=self.API_PREFIX),
            data={
                'code': vessel_code,
            },
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg='Vessel Creation Failed.',
        )

    def test_vessel_creation_with_unique_code(self):
        payload = {
            'code': self.vessel_code,
        }
        self.create_vessel(self.vessel_code)

        response = self.client.post(
            path=self.VESSEL_URI.format(prefix=self.API_PREFIX),
            data=payload,
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg='Error Validating Vessel Unique Code On Creation',
        )

    def test_register_unique_and_new_equipment_for_one_vessel(self):
        self.create_vessel(self.vessel_code)
        payload = {
            'name': 'compressor',
            'code': '5310B9D7',
            'location': 'Brazil',
        }
        response = self.client.post(
            path=self.EQUIPMENT_URI.format(
                prefix=self.API_PREFIX,
                code=self.vessel_code,
            ),
            data=payload,
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg=f'Equipment creation for Vessel {self.vessel_code} Failed.',
        )

        response = self.client.post(
            path=self.EQUIPMENT_URI.format(
                prefix=self.API_PREFIX,
                code=self.vessel_code,
            ),
            data=payload,
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg=f'Unique Equipment code validation on create Failed.',
        )

    def test_disable_massive_equipment_for_vessel_payload_validation(self):
        self.create_vessel(self.vessel_code)
        # Testing Bad
        bad_payloads = [
            {},
            {
                'codes': [],
            },
            {
                'codes': 'Mimosa',
            }
        ]
        for payload in bad_payloads:
            response = self.client.delete(
                path=self.EQUIPMENT_URI.format(
                    prefix=self.API_PREFIX,
                    code=self.vessel_code,
                ),
                data=payload,
                content_type='application/json',
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_disable_massive_equipment_and_only_return_active_equipment_for_vessel(self):
        self.create_vessel(self.vessel_code)
        equipment_codes = ['5310B9D7', '5310B9D8', '5310B9D9']
        for code in equipment_codes:
            payload = {
                'name': 'compressor',
                'code': code,
                'location': 'Brazil',
            }
            response = self.client.post(
                path=self.EQUIPMENT_URI.format(
                    prefix=self.API_PREFIX,
                    code=self.vessel_code,
                ),
                data=payload,
            )
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                msg=f'Equipment creation for Vessel {self.vessel_code} Failed.',
            )

        payload = {
            'codes': equipment_codes,
        }
        response = self.client.delete(
            path=self.EQUIPMENT_URI.format(
                prefix=self.API_PREFIX,
                code=self.vessel_code,
            ),
            data=payload,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(
            path=self.EQUIPMENT_URI.format(
                prefix=self.API_PREFIX,
                code=self.vessel_code,
            ),
        )
        self.assertJSONEqual(
            response.content,
            [],
            msg='Bad Response structure from server.',
        )

    def test_only_show_active_equipment_for_vessel(self):
        self.create_vessel(self.vessel_code)
        payloads = [
            {
                'name': 'compressor',
                'code': '5310B9D7',
                'location': 'Brazil',
            },
            {
                'name': 'compressor',
                'code': '5310B9D8',
                'location': 'Brazil',
            },
            {
                'name': 'compressor',
                'code': '5310B9D9',
                'location': 'Brazil',
            }
        ]
        for payload in payloads:
            response = self.client.post(
                path=self.EQUIPMENT_URI.format(
                    prefix=self.API_PREFIX,
                    code=self.vessel_code,
                ),
                data=payload,
            )
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                msg=f'Equipment creation for Vessel {self.vessel_code} Failed.',
            )

        payload = {
            'codes': [payload['code'] for idx, payload in enumerate(payloads) if idx <= 1],
        }
        response = self.client.delete(
            path=self.EQUIPMENT_URI.format(
                prefix=self.API_PREFIX,
                code=self.vessel_code,
            ),
            data=payload,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(
            path=self.EQUIPMENT_URI.format(
                prefix=self.API_PREFIX,
                code=self.vessel_code,
            ),
        )
        equipments = response.json()
        self.assertEqual(len(equipments), 1)
        self.assertContains(
            response,
            text=payloads[2]['code'],
            status_code=status.HTTP_200_OK,
        )

    def test_disable_equipment_and_active_after_create_a_new_with_same_code_on_vessel(self):
        self.create_vessel(self.vessel_code)
        payload = {
            'name': 'compressor',
            'code': '5310B9D7',
            'location': 'Brazil'
        }
        response = self.client.post(
            path=self.EQUIPMENT_URI.format(
                prefix=self.API_PREFIX,
                code=self.vessel_code,
            ),
            data=payload,
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg=f'Equipment creation for Vessel {self.vessel_code} Failed.',
        )
        response = self.client.delete(
            path=self.EQUIPMENT_URI.format(
                prefix=self.API_PREFIX,
                code=self.vessel_code,
            ),
            data={
                'codes': ['5310B9D7']
            },
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.post(
            path=self.EQUIPMENT_URI.format(
                prefix=self.API_PREFIX,
                code=self.vessel_code,
            ),
            data=payload,
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f'Equipment creation for Vessel {self.vessel_code} Failed, {response.json()}.',
        )

    def test_update_equipment_data_when_reactivate(self):
        self.create_vessel(self.vessel_code)
        payload = {
            'name': 'compressor',
            'code': '5310B9D7',
            'location': 'Brazil',
        }
        response = self.client.post(
            path=self.EQUIPMENT_URI.format(
                prefix=self.API_PREFIX,
                code=self.vessel_code,
            ),
            data=payload,
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg=f'Equipment creation for Vessel {self.vessel_code} Failed.',
        )
        response = self.client.delete(
            path=self.EQUIPMENT_URI.format(
                prefix=self.API_PREFIX,
                code=self.vessel_code,
            ),
            data={
                'codes': ['5310B9D7']
            },
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        payload = {
            'name': 'compressor',
            'code': '5310B9D7',
            'location': 'Colombia',
        }
        response = self.client.post(
            path=self.EQUIPMENT_URI.format(
                prefix=self.API_PREFIX,
                code=self.vessel_code,
            ),
            data=payload,
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,

        )
        self.assertContains(
            response,
            status_code=status.HTTP_200_OK,
            text='Colombia',
        )
