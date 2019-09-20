from opsdroid.skill import Skill
from opsdroid.matchers import match_regex
from datetime import datetime
from netapp_ontap import config
from netapp_ontap import HostConnection
from netapp_ontap.resources import Cluster, Aggregate, Port, Volume, Autosupport, IpInterface, Disk, Snapshot, Account, Svm
import urllib3

# To enable certificate warnings comment the line below:
# urllib3.disable_warnings()

conn = HostConnection('192.168.1.200', username='admin', password='N3tapp1!', verify=False)

config.CONNECTION = conn

def _hostname_to_text(hostname):
    if hostname[:4] == '&lt;': 
        hostname = hostname[4:-4]
        return hostname
    else:
        return hostname
        
class NetAppSkill(Skill):

    
    def __init__(self, opsdroid, config):
        super(NetAppSkill, self).__init__(opsdroid, config)

    @match_regex('get ontap cluster info')
    async def get_cluster_info(self, message):
        """
        A skills function to get ontap cluster information. The parser looks for the message argument.

        Arguments:
            message {str} -- get ontap cluster info
        """
        clus = Cluster()
        clus.get()
        await message.respond('All done! Response: {}'.format(clus))

    @match_regex('get ontap cluster version')
    async def get_cluster_version(self, message):
        """
        A skills function to get ontap cluster version. The parser looks for the message argument.

        Arguments:
            message {str} -- get ontap cluster version
        """
        clus = Cluster()
        clus.get()
        await message.respond('All done! Response: {}'.format(clus.version))

    @match_regex('get ontap cluster name')
    async def get_cluster_name(self, message):
        """
        A skills function to get ontap cluster name. The parser looks for the message argument.

        Arguments:
            message {str} -- get ontap cluster name
        """
        clus = Cluster()
        clus.get()
        await message.respond('All done! Response: {}'.format(clus.name))
    
    @match_regex('create a (?P<size>[0-9:]+) MB volume called (?P<name>[\w\'_]+) on svm (?P<svm>[\w\'_]+) and aggregate (?P<aggr>[\w\'_]+)')
    async def create_volume(self, message):
        """
        A skills function to create a volume. The parser looks for the message argument.

        Arguments:
            message {str} -- create a {size} MB volume called {name} on svm {svm} and aggregate {aggr}
        """
        name = message.regex.group('name')
        size = message.regex.group('size')
        aggr = message.regex.group('aggr')
        svm = message.regex.group('svm')
        volume = Volume.from_dict({'name': name, 'svm': {'name': svm}, 'size': int(size)*1024*1024, 'aggregates': [{'name': aggr}]})
        volume.post()
        await message.respond('All done! Response: {}'.format(volume))

    @match_regex('delete volume (?P<name>[\w\'_]+) on svm (?P<svm>[\w\'_]+)')
    async def delete_volume(self, message):
        """
        A skills function to delete a volume. The parser looks for the message argument.

        Arguments:
            message {str} -- delete volume {name} on svm {svm}
        """
        name = message.regex.group('name')
        svm = message.regex.group('svm')
        volume = Volume.find(name=name, svm=svm)
        volume.delete()
        await message.respond('All done! Response: {}'.format(volume))

    @match_regex('get volumes on svm (?P<svm>[\w\'_]+)')
    async def get_volumes(self, message):
        """
        A skills function to get volumes on an SVM. The parser looks for the message argument.

        Arguments:
            message {str} -- get volumes on svm {svm}
        """
        svm = message.regex.group('svm')
        volumes = []
        for vol in Volume.get_collection(svm=svm):
            vol.get(fields='name')
            volumes.append(vol.name)
        await message.respond('All done! Response: {}'.format(volumes))

    @match_regex('get all aggregates on cluster')
    @match_regex('get aggregates on cluster')
    async def get_aggregates(self, message):
        """
        A skills function to get all aggregates on the cluster. The parser looks for the message argument.

        Arguments:
            message {str} -- get aggregates on cluster
        """
        aggregates = []
        for aggr in Aggregate.get_collection():
            aggr.get(fields='name')
            aggregates.append(aggr.name)
        await message.respond('All done! Response: {}'.format(aggregates))

    @match_regex('get all ports on cluster')
    @match_regex('get ports on cluster')
    async def get_ports(self, message):
        """
        A skills function to get all ports state on the cluster. The parser looks for the message argument.

        Arguments:
            message {str} -- get ports state on cluster
        """
        ports = []
        for port in Port.get_collection():
            port.get()
            ports.append([port.name, port.state])
        await message.respond('All done! Response: {}'.format(ports))

    @match_regex('get all interfaces on cluster')
    @match_regex('get interfaces on cluster')
    async def get_interfaces(self, message):
        """
        A skills function to get all interfaces on the cluster. The parser looks for the message argument.

        Arguments:
            message {str} -- get interfaces state on cluster
        """
        interfaces = []
        for interface in IpInterface.get_collection():
            interface.get()
            interfaces.append([interface.name, interface.state])
        await message.respond('All done! Response: {}'.format(interfaces))

    @match_regex('create a snapshot of (?P<name>[\w\'_]+) on svm (?P<svm>[\w\'_]+)')
    @match_regex('take a snapshot of (?P<name>[\w\'_]+) on svm (?P<svm>[\w\'_]+)')
    async def create_snapshot(self, message):
        """
        A skills function to take a snapshot of a volume. The parser looks for the message argument.

        Arguments:
            message {str} -- create a snapshot of {volume} on svm {svm}
        """
        name = message.regex.group('name')
        svm = message.regex.group('svm')
        time = datetime.now()
        time = str(time)
        volume = Volume.find(name=name, svm={'name': svm})
        volume.get()
        snapshot = Snapshot.from_dict({
        'name': 'snapshot_%s' % time,
        'volume': volume.to_dict(),
        })
        snapshot.post()
        await message.respond('All done! Response: {}'.format(snapshot))

    @match_regex('create a clone of (?P<volume>[\w\'_]+) on svm (?P<svm>[\w\'_]+) called (?P<name>[\w\'_]+)')
    @match_regex('create a flexclone of (?P<volume>[\w\'_]+) on svm (?P<svm>[\w\'_]+) called (?P<name>[\w\'_]+)')
    async def create_flexclone(self, message):
        """
        A skills function to create a clone of a volume. The parser looks for the message argument.

        Arguments:
            message {str} -- create a clone of {volume} on svm {svm} called {name}
        """
        parent_volume = message.regex.group('volume')
        svm = message.regex.group('svm')
        name = message.regex.group('name')
        flexclone = Volume.from_dict({"name": name, "clone": {"parent_volume": {"name": parent_volume}, "is_flexclone": "true"}, "svm": {"name": svm}})
        flexclone.post()
        await message.respond('All done! Response: {}'.format(flexclone))

    @match_regex('create and mount a (?P<size>[0-9:]+) MB volume called (?P<name>[\w\'_]+) on svm (?P<svm>[\w\'_]+) and aggregate (?P<aggr>[\w\'_]+)')
    @match_regex('create and mount a (?P<size>[0-9:]+) MB volume (?P<name>[\w\'_]+) on svm (?P<svm>[\w\'_]+) (?P<aggr>[\w\'_]+)')
    async def create_volume(self, message):
        """
        A skills function to create a volume. The parser looks for the message argument.

        Arguments:
            message {str} -- create a {size} MB volume called {name} on svm {svm} and aggregate {aggr}
        """
        name = message.regex.group('name')
        size = message.regex.group('size')
        aggr = message.regex.group('aggr')
        svm = message.regex.group('svm')
        volume = Volume.from_dict({'name': name, 'svm': {'name': svm}, 'nas': {'path': '/'+name} , 'size': int(size)*1024*1024, 'aggregates': [{'name': aggr}]})
        volume.post()
        await message.respond('All done! Response: {}'.format(volume))
