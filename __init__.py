from opsdroid.skill import Skill
from opsdroid.matchers import match_regex
from netapp_ontap import config
from netapp_ontap import HostConnection
from netapp_ontap.resources import Cluster, Aggregate, Port, Volume, Autosupport, IpInterface, Disk, Chassis, Account, Svm
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
    async def get_cluster_version(self, message):
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
        A skills function to get ontap cluster name. The parser looks for the message argument.

        Arguments:
            message {str} -- create a {size} MB volume called {name} on svm {svm} and aggregate {aggr}
        """
        name = message.regex.group('name')
        size = message.regex.group('size')
        size = int(size) * 1024 * 1024
        aggr = message.regex.group('aggr')
        svm = message.regex.group('svm')

        volume = Volume.from_dict({'name': name, 'svm': {'name': svm}, 'size': size, 'aggregates': [{'name': aggr}]})
        volume.post()
        await message.respond('All done! Response: {}'.format(volume))