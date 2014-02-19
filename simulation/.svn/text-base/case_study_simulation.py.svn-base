'''
Created on 27/10/2009

@author: LGustavo
'''
from pydssim.simulation.reciprocal_trade_simulation_p2p import ReciprocalTradeSimulationP2P
from pydssim.simulation.process.factory.new_portalpeers_simulation_process_factory import NewPortalPeersSimulationProcessFactory
from pydssim.simulation.process.factory.new_superpeers_simulation_process_factory import NewSuperPeersSimulationProcessFactory
from pydssim.simulation.process.factory.begin_simulation_process_factory import BeginSimulationProcessFactory
from pydssim.simulation.process.factory.new_peers_simulation_process_factory import NewPeersSimulationProcessFactory
from pydssim.simulation.process.factory.new_trading_simulation_process_factory import NewTradingSimulationProcessFactory
from pydssim.simulation.process.factory.out_peers_simulation_process_factory import OutPeersSimulationProcessFactory
from pydssim.simulation.process.factory.out_superpeers_simulation_process_factory import OutSuperPeersSimulationProcessFactory

simulation = ReciprocalTradeSimulationP2P()
simulation.setSimulationTime(3850)
simulation.setResourcePeer(7)
simulation.initializeTrust(20, "1/1/2009 1:30", "1/1/2009 1:32")
simulation.initializeNetwork(640, 3000, 10)

simulation.addSimulationProcessFactory(NewPortalPeersSimulationProcessFactory())
simulation.addSimulationProcessFactory(NewSuperPeersSimulationProcessFactory())
simulation.addSimulationProcessFactory(NewPeersSimulationProcessFactory())
simulation.addSimulationProcessFactory(OutPeersSimulationProcessFactory())
#simulation.addSimulationProcessFactory(OutSuperPeersSimulationProcessFactory())
simulation.addSimulationProcessFactory(BeginSimulationProcessFactory())
#simulation.addSimulationProcessFactory(NewTradingSimulationProcessFactory())


print simulation.start()
