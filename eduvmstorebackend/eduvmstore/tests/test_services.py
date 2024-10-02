import unittest
from unittest.mock import patch, Mock
from eduvmstorebackend.eduvmstore.services.nova_service import list_instances

@patch('app.services.nova_service.get_openstack_connection')
def test_list_instances(mock_conn):
    """Test list_instances function."""
    mock_conn.return_value.compute.servers.return_value = [
        Mock(name='instance1'), Mock(name='instance2')
    ]
    instances = list_instances()
    assert instances == ['instance1', 'instance2']


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
