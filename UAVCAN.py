
def b2i(b): return int(b, 2)

class UAVCANv0:
    def __init__(self):
        self.IDs                = set()
        self.Message_type_IDs   = set()
        self.Service_type_IDs   = set()
        self.Node_IDs           = set()

    def parseID(self, id):
        self.id = id
        id = format(int(id, 16), '029b')

        Priority        = b2i(id[:5])
        Service         = True if id[21] == "1" else False
        Source_node_ID  = b2i(id[22:])

        if Source_node_ID not in self.Node_IDs:
            self.Node_IDs.add(Source_node_ID)

        # service transfer
        if (Service):
            Service_type_ID     = b2i(id[5:13])
            if Service_type_ID not in self.Service_type_IDs:
                self.Service_type_IDs.add(Service_type_ID)

            Request             = True if id[13] == "1" else False

            Destination_node_ID = b2i(id[14:21])
            if Destination_node_ID not in self.Node_IDs:
                self.Node_IDs.add(Destination_node_ID)
        # message transfer
        else:
            if Source_node_ID == 0:
                Discriminator                   = b2i(id[5:19])
                Lower_bits_of_message_type_ID   = b2i(id[19:21])
                if Lower_bits_of_message_type_ID not in self.Message_type_IDs:
                    self.Message_type_IDs.add(Lower_bits_of_message_type_ID)
            else:
                Message_type_ID                 = b2i(id[5:21])
                if Message_type_ID not in self.Message_type_IDs:
                    self.Message_type_IDs.add(Message_type_ID)

        if self.id not in self.IDs:
            # print(self.Discriminator, end=", ")
            self.IDs.add(self.id)

    def generateID(self, dump = True):
        IDs = {
        }
        for Priority in range(1, 32):
            for Source_node_ID in self.Node_IDs:
                # Message frame
                for Message_type_ID in self.Message_type_IDs:
                    ID  = int(Priority << 24) + int(Message_type_ID << 8) + Source_node_ID
                    IDs[f'{ID:08X}'] = {
                        "Priority": Priority,
                        "Message_type_ID": Message_type_ID,
                        "Service": 0,
                        "Source_node_ID": Source_node_ID
                    }
                    # print("M", f'{ID:X}', Priority, Message_type_ID, 0, Source_node_ID)
                # Service frame
                for Service_type_ID in self.Service_type_IDs:
                    for Destination_node_ID in self.Node_IDs:
                        for Request in [0, 1]:
                            ID = int(Priority << 24) + int(Service_type_ID << 16) + int(Request << 15) + int(Destination_node_ID << 8) + int(1 << 16) + Source_node_ID
                            IDs[f'{ID:08X}'] = {
                                "Priority": Priority,
                                "Service_type_ID": Service_type_ID,
                                "Request": Request,
                                "Destination_node_ID": Destination_node_ID,
                                "Service": 1,
                                "Source_node_ID": Source_node_ID
                            }
                            # print("S", f'{ID:X}', Priority, Service_type_ID, Request, Destination_node_ID, 1, Source_node_ID)
        import json
        print(json.dumps(sorted(IDs.items(), key = lambda key: key[0]), indent=4))


class _UAVCANv0:
    global ids
    def __init__(self, raw):
        # print(raw)
        t, i, self.id, dlc, data = list(map(str.strip, raw.strip().split("  ")))[:5]

        self.parseID()
        # print(self.__dict__)

    def parseID(self):
        id = format(int(self.id, 16), '029b')

        self.Priority       = b2i(id[:5])
        self.Service        = True if id[21] == "1" else False
        self.Source_node_ID = b2i(id[22:])

        # service transfer
        if (self.Service):
            self.Service_type_ID    = b2i(id[5:13])
            self.Request            = True if id[13] == "1" else False
            self.Destination_node_ID= b2i(id[14:21])
            # print(self.Request, self.Service_ID, self.Destination_node_ID, self.Source_node_ID)
        # message transfer
        else:
            if self.Source_node_ID == 0:
                self.Discriminator                  = b2i(id[5:19])
                self.Lower_bits_of_message_type_ID  = b2i(id[19:21])
            else: self.Message_type_ID              = b2i(id[5:21])

        if self.id not in ids and self.Source_node_ID == 0:
            # print(self.__dict__)
            print(self.Discriminator, end=", ")
            ids.append(self.id)


class UAVCANv1:
    global ids
    def __init__(self, raw):
        # print(raw)
        t, i, self.id, dlc, data = list(map(str.strip, raw.strip().split("  ")))[:5]

        self.parseID()
        # print(self.__dict__)

    def parseID(self):
        id = format(int(self.id, 16), '029b')

        Priority       = b2i(id[:3])
        Service        = True if id[3] == "1" else False
        Source_node_ID = b2i(id[22:])

        # service transfer
        if (self.Service):
            self.Request                = True if id[4] == "1" else False
            self.Service_ID             = b2i(id[6:15])
            self.Destination_node_ID    = b2i(id[15:22])
            # print(self.Request, self.Service_ID, self.Destination_node_ID, self.Source_node_ID)
        # message transfer
        else:
            self.Anonymous      = b2i(id[4])
            self.Subject_ID     = b2i(id[8:21])

        if self.id not in ids:
            print(self.__dict__)
            ids.append(self.id)


if __name__ == "__main__":
    uavcan = UAVCANv0()
    
    with open("uavcan_with_control.txt", "r") as r:
        for l in r.readlines():
            t, i, id, dlc, data = list(map(str.strip, l.strip().split("  ")))[:5]
            uavcan.parseID(id)

    uavcan.generateID()
