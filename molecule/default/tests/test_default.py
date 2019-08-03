import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'

# Check if MongoDB is enabled and running
def test_mongo_runnind_and_enabled(host):
    mongo = host.service("mongod")
    assert mongo.is_running
    assert mongo.is_enabled

def test_mongo_file(host):
    config_file = host.file('/etc/mongod.conf')
    assert config_file.is_file
    assert config_file.contains("bindIp: 0.0.0.0")
# Check mongod port availability
def test_mongo_port(host):
    host_addr = host.addr("localhost")
    assert host_addr.port('27017').is_reachable
    assert host.socket("tcp://0.0.0.0:27017").is_listening
