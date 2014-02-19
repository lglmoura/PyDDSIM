"""
Defines the module with the specification of ISimulation interface.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@vocs.ufrj.br 
@since: 15/07/2009
"""



from pydssim.network.abstract_network import AbstractNetwork

class P2PNetwork(AbstractNetwork):
    """
    classdocs
    """

    def __init__(self, simulation,peers ,newPeerTime,neighbors):
       
        AbstractNetwork.initialize(self, simulation, peers ,newPeerTime,neighbors)
        