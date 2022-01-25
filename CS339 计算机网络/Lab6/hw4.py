from operator import attrgetter

from ryu.base import app_manager
from ryu.ofproto import ofproto_v1_3
from ryu.ofproto.ofproto_v1_3 import OFPPS_LIVE
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER, CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub
from ryu.lib.packet import ether_types
from ryu.lib.packet import  in_proto as inet
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib import stplib

class SimpleSwitch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    def __init__(self, *args, **kwargs):
        super(SimpleSwitch, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.failover = False

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

    def del_flow(self, datapath, match, out_port):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        mod = parser.OFPFlowMod(datapath=datapath,match=match,
                                command=ofproto.OFPFC_DELETE,out_port=out_port,
                                out_group=ofproto.OFPG_ANY,flags=ofproto.OFPFF_SEND_FLOW_REM)
        datapath.send_msg(mod)

    def add_group(self,datapath,type,group_id,buckets):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        req = parser.OFPGroupMod(datapath, ofproto.OFPGC_ADD,
                            type , group_id, buckets)
        datapath.send_msg(req)

    #监听交换机连接
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch()

        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)
        if datapath.id == 3 or datapath.id == 4:
            group_id = 1
            actions1 = [parser.OFPActionOutput(2)]
            actions2 = [parser.OFPActionOutput(ofproto.OFPP_IN_PORT)]
            buckets = [parser.OFPBucket(watch_port=2,actions=actions1),
                    parser.OFPBucket(watch_port=1,actions=actions2)]
            self.add_group(datapath,ofproto.OFPGT_FF,group_id,buckets)
            match = parser.OFPMatch(in_port=1)
            actions = [parser.OFPActionGroup(group_id=group_id)]
            self.add_flow(datapath,3,match,actions)

            group_id = 2
            actions1 = [parser.OFPActionOutput(1)]
            actions2 = [parser.OFPActionOutput(ofproto.OFPP_IN_PORT)]
            buckets = [parser.OFPBucket(watch_port=1,actions=actions1),
                    parser.OFPBucket(watch_port=2,actions=actions2)]
            self.add_group(datapath,ofproto.OFPGT_FF,group_id,buckets)
            match = parser.OFPMatch(in_port=2)
            actions = [parser.OFPActionGroup(group_id=group_id)]
            self.add_flow(datapath,3,match,actions)

        else: 
            match = parser.OFPMatch(in_port=2)
            actions = [parser.OFPActionOutput(1)]
            self.add_flow(datapath,1,match,actions)

            match = parser.OFPMatch(in_port=3)
            actions = [parser.OFPActionOutput(1)]
            self.add_flow(datapath,1,match,actions)

            if datapath.id == 1:
                match = parser.OFPMatch(in_port=2,eth_src='00:00:00:00:00:01')
                actions = [parser.OFPActionOutput(3)]
                self.add_flow(datapath,2,match,actions)
                match = parser.OFPMatch(in_port=3,eth_src='00:00:00:00:00:01')
                actions = [parser.OFPActionOutput(2)]
                self.add_flow(datapath,2,match,actions)
            elif datapath.id == 2:
                match = parser.OFPMatch(in_port=2,eth_src='00:00:00:00:00:02')
                actions = [parser.OFPActionOutput(3)]
                self.add_flow(datapath,2,match,actions)
                match = parser.OFPMatch(in_port=3,eth_src='00:00:00:00:00:02')
                actions = [parser.OFPActionOutput(2)]
                self.add_flow(datapath,2,match,actions)

            actions1 = [parser.OFPActionOutput(2)]
            actions2 = [parser.OFPActionOutput(3)]
            
            group_id = 1

            buckets = [parser.OFPBucket(watch_port=2,actions=actions1),
                    parser.OFPBucket(watch_port=3,actions=actions2)]
            self.add_group(datapath,ofproto.OFPGT_FF,group_id,buckets)

            match = parser.OFPMatch(in_port=1)
            actions = [parser.OFPActionGroup(group_id=group_id)]
            self.add_flow(datapath,3,match,actions)

    #管理在线的交换机列表
    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.debug('register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

    #监听未被流表匹配的分组，用于调试
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        self.logger.debug(f"datapath={datapath.id},{eth}")

    #监听端口状态变化
    @set_ev_cls(ofp_event.EventOFPPortStatus,MAIN_DISPATCHER)
    def _port_state_change_handler(self, ev):
        datapath = ev.msg.datapath
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto
        desc = ev.msg.desc
        if desc.state & ofproto.OFPPS_LIVE:
            if datapath.id in (1,2) and desc.port_no in (2,3) and self.failover:
                self.logger.warning(f"datapath {datapath.id} port {desc.port_no} UP!")
                if datapath.id == 1:
                    datapath_ = self.datapaths[2]
                else:
                    datapath_ = self.datapaths[1]
                out_port = 3 if desc.port_no == 2 else 2
                match = parser.OFPMatch(in_port=1)
                self.del_flow(datapath_,match,out_port)
                self.logger.info(f"del flow: datapath {datapath.id} in_port:1,out_port:{out_port}")
                self.failover = False
        else:
            if datapath.id in (1,2) and desc.port_no in (2,3) and not self.failover:
                self.logger.warning(f"datapath {datapath.id} port {desc.port_no} DOWN!")
                if datapath.id == 1:
                    datapath_ = self.datapaths[2]
                else:
                    datapath_ = self.datapaths[1]
                out_port = 3 if desc.port_no == 2 else 2
                match = parser.OFPMatch(in_port=1)
                actions = [parser.OFPActionOutput(out_port)]
                self.add_flow(datapath_,10,match,actions)
                self.logger.info(f"add flow: datapath {datapath.id} in_port:1,out_port:{out_port}")
                self.failover = True

