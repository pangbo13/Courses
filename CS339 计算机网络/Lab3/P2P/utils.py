from hashlib import md5
import json

def MD5_checksum(f):
    pre_pos = f.tell()
    alg = md5()
    buffer = f.read(1024*1024)
    while buffer:
        alg.update(buffer)
        buffer = f.read(1024*1024)
    f.seek(pre_pos)
    return alg.hexdigest()


class ChunkStatus(object):
    UNDOWNLOAD = 0x0
    DOWNLOADING = 0x1
    DOWNLOADED = 0x2

class OPType(object):
    CHEL = 0x1
    SHEL = 0x2
    PHEL = 0x3
    CLREQ = 0x4
    CLRES = 0x5
    DREQ = 0x6
    DATA = 0x7
    CHECK = 0x8
    ERROR = 0x9

class P2PParser(object):
    class ParsedMsg(object):
        def __init__(self):
            super().__init__()
            self.op = None
            self.args = None
            self.content = None
            self.json = None
            self.error = None
    @staticmethod
    def parse(buffer: bytes) -> ParsedMsg:
        try:
            head, content = buffer.split(b'\r\n',1)
            head_split = head.split(b' ')
        except ValueError:
            if buffer:
                raise P2PException.ProtocolNotCompatible(buffer[:100])
            else:
                raise P2PException.RecvEmptyExcption()
        if len(head_split) > 1:
            op = head_split[0]
            args = head_split[1:]
        else:
            op = head_split[0]
            args = []
        res = P2PParser.ParsedMsg()
        if op == b'CHEL':
            #CHEL port
            res.op = OPType.CHEL
            if len(args) != 1:
                raise P2PException.HeadArgsError(head)
            else:
                res.args = int(args[0])
                res.content = content
        elif op == b'SHEL':
            #SHEL filesize chuncksize
            res.op = OPType.SHEL
            if len(args) != 2:
                raise P2PException.HeadArgsError(head)
            else:
                res.args = (int(args[0]),int(args[1]))
                res.content = content
                res.json = json.loads(content)
        elif op == b'PHEL':
            res.op = OPType.PHEL
            if len(args) != 0:
                raise P2PException.HeadArgsError(head)
            else:
                res.content = content
        elif op == b'CLREQ':
            res.op = OPType.CLREQ
            if len(args) != 0:
                raise P2PException.HeadArgsError(head)
            else:
                res.content = content
        elif op == b'CLRES':
            res.op = OPType.CLRES
            if len(args) != 1:
                raise P2PException.HeadArgsError(head)
            else:
                res.args = int(args[0])
                res.content = content
                res.json = json.loads(content)
        elif op == b'DREQ':
            #DREQ chunkid
            res.op = OPType.DREQ
            if len(args) != 1:
                raise P2PException.HeadArgsError(head)
            else:
                res.args = int(args[0])
                res.content = content
        elif op == b'DATA':
            #DATA offset size
            res.op = OPType.DATA
            if len(args) != 2:
                raise P2PException.HeadArgsError(head)
            else:
                res.args = (int(args[0]),int(args[1]))
                res.content = content
        elif op == b'CHECK':
            #CHECK checksum
            res.op = OPType.CHECK
            if len(args) != 1:
                raise P2PException.HeadArgsError(head)
            else:
                res.args = args[0].decode()
                res.content = content
        elif op == b'ERROR':
            #ERROR errorid
            if len(args) != 1:
                raise P2PException.HeadArgsError(head)
            else:
                res.args = args[0].decode()
                res.content = content
        else:
            raise P2PException.UnkonwnOPException(op)
        return res
            
class P2PException(object):
    class UnkonwnOPException(Exception):
        def __init__(self, *args: object) -> None:
            super().__init__(*args)
    class HeadArgsError(Exception):
        def __init__(self, *args: object) -> None:
            super().__init__(*args)
    class ProtocolNotCompatible(Exception):
        def __init__(self, *args: object) -> None:
            super().__init__(*args)
    class RecvEmptyExcption(Exception):
        def __init__(self, *args: object) -> None:
            super().__init__(*args)