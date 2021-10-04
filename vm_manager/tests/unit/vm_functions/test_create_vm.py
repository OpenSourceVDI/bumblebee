import pdb

import uuid

from unittest.mock import Mock, patch

from django.conf import settings
from django.test import TestCase

from researcher_workspace.tests.factories import UserFactory
from researcher_desktop.utils.utils import get_desktop_type, desktops_feature

from vm_manager.tests.factories import InstanceFactory, VMStatusFactory, \
    VolumeFactory

from vm_manager.constants import VM_MISSING, NO_VM
from vm_manager.vm_functions.create_vm import _create_volume, _create_instance
from vm_manager.utils.utils import get_nectar


class Fake(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"{self.__class__} id={self.id}}}"

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.id == other.id


class FakeFlavor(Fake):
    pass


class FakeVolume(Fake):
    pass


class FakeServer(Fake):
    pass


FLAVORS = [
    FakeFlavor(id=uuid.uuid4(), name='m3.medium',
               ram='1', disk='1', vcpus='1'),
]

VOLUMES = [
    FakeVolume(id='1', name='m3.medium', ram='1', disk='1', vcpus='1'),
]


class FakeNectar(object):
    def __init__(self):
        self.nova = Mock()
        self.nova.flavors.list = Mock(return_value=FLAVORS)
        self.nova.servers.create = Mock(
            return_value=FakeServer(
                id=uuid.UUID(bytes=b'\x12\x34\x56\x78' * 4)))

        self.allocation = Mock()
        self.keystone = Mock()
        self.glance = Mock()

        self.cinder = Mock()
        self.cinder.volumes.list = Mock(return_value=VOLUMES)
        self.cinder.volumes.create = Mock(
            return_value=FakeVolume(
                id=uuid.UUID(bytes=b'\x12\x34\x56\x78' * 4)))

        net_id = uuid.UUID(bytes=b'\x11\x11\x11\x11' * 4)
        self.VM_PARAMS = {
            "size": 20,
            "metadata_volume": {'readonly': 'False'},
            "availability_zone_volume": settings.OS_AVAILABILITY_ZONE,
            "availability_zone_server": settings.OS_AVAILABILITY_ZONE,
            "block_device_mapping": [{
                'source_type': "volume",
                'destination_type': 'volume',
                'delete_on_termination': False,
                'uuid': None,
                'boot_index': '0',
                'volume_size': 20,
            }],
            "id_net": net_id,
            "list_net": [{'net-id': net_id}],
        }


class CreateVMTests(TestCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.FEATURE = desktops_feature()
        self.UBUNTU = get_desktop_type('ubuntu')
        self.CENTOS = get_desktop_type('centos')
        self.user = UserFactory.create()

    def test_launch_has_instance(self):
        volume = VolumeFactory.create(
            user=self.user,
            operating_system=self.UBUNTU.id,
            requesting_feature=self.UBUNTU.feature)
        instance = InstanceFactory.create(
            user=self.user,
            boot_volume=volume
        )

        self.assertIsNotNone(instance)

    @patch('vm_manager.utils.utils.Nectar', new=FakeNectar)
    @patch('vm_manager.vm_functions.create_vm.generate_server_name')
    def test_create_volume(self, mock_gen):
        mock_gen.return_value = "abcdef"
        result = _create_volume(self.user, self.UBUNTU)

        self.assertIsNotNone(result)
        self.assertEqual(uuid.UUID(bytes=b'\x12\x34\x56\x78' * 4), result.id)
        self.assertEqual(self.user, result.user)
        self.assertEqual(self.UBUNTU.source_volume_id, result.image)
        self.assertEqual(self.UBUNTU.id, result.operating_system)
        self.assertEqual(self.UBUNTU.feature, result.requesting_feature)
        self.assertEqual(self.UBUNTU.default_flavor.id, result.flavor)

        mock_gen.assert_called_once_with(self.user.username, self.UBUNTU.id)
        fake = get_nectar()
        fake.cinder.volumes.create.assert_called_once_with(
            name="abcdef",
            source_volid=self.UBUNTU.source_volume_id,
            size=fake.VM_PARAMS['size'],
            availability_zone=fake.VM_PARAMS['availability_zone_volume'],
            metadata=fake.VM_PARAMS['metadata_volume'])
        fake.cinder.volumes.set_bootable.assert_called_once_with(
            volume=FakeVolume(id=result.id), flag=True)

    @patch('vm_manager.vm_functions.create_vm.get_nectar')
    def test_create_volume_exists(self, mock_get):
        fake_volume = VolumeFactory.create(
            id=uuid.UUID(bytes=b'\x13\x24\x57\x68' * 4),
            user=self.user,
            image=self.UBUNTU.source_volume_id,
            operating_system=self.UBUNTU.id,
            requesting_feature=self.UBUNTU.feature,
            flavor=self.UBUNTU.default_flavor.id)
        fake_instance = InstanceFactory.create(
            boot_volume=fake_volume,
            user=self.user)
        fake_vmstatus = VMStatusFactory.create(
            user=self.user,
            instance=fake_instance,
            operating_system=self.UBUNTU.id,
            requesting_feature=self.UBUNTU.feature,
            status=VM_MISSING)

        result = _create_volume(self.user, self.UBUNTU)
        self.assertEqual(fake_volume, result)
        mock_get.assert_not_called()

    @patch('vm_manager.utils.utils.Nectar', new=FakeNectar)
    def test_create_volume_deleted(self):
        fake_volume = VolumeFactory.create(
            id=uuid.UUID(bytes=b'\x13\x24\x57\x68' * 4),
            user=self.user,
            image=self.UBUNTU.source_volume_id,
            operating_system=self.UBUNTU.id,
            requesting_feature=self.UBUNTU.feature,
            flavor=self.UBUNTU.default_flavor.id)
        fake_instance = InstanceFactory.create(
            id=uuid.UUID(bytes=b'\x87\x65\x43\x21' * 4),
            boot_volume=fake_volume,
            user=self.user)
        fake_vmstatus = VMStatusFactory.create(
            user=self.user,
            instance=fake_instance,
            operating_system=self.UBUNTU.id,
            requesting_feature=self.UBUNTU.feature,
            status=NO_VM)

        fake = get_nectar()
        fake.cinder.volumes.create.reset_mock()

        result = _create_volume(self.user, self.UBUNTU)
        self.assertNotEqual(fake_volume, result)
        self.assertEqual(uuid.UUID(bytes=b'\x12\x34\x56\x78' * 4), result.id)

        fake.cinder.volumes.create.assert_called_once()