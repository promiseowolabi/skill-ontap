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
