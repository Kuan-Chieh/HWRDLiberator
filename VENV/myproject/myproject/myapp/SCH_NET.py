class SCH_NET:
    #def _init_(self):
    #    filename = "";

    def open_net_file(self, fn):
        self.Netfile = open(fn, 'r');

    def parse(self):
        print("parsing SCH netlist....")
        self.wNets = [];
        tmpNet = [];

        self.Netfile.readline(); #header
        self.Netfile.readline(); #header
        self.Netfile.readline(); #first NET

        tmpNet.append(self.Netfile.readline()[1:-2]);
        for line in self.Netfile:
            if line == "NET_NAME\n":
                self.wNets.append(tmpNet.copy());
                tmpNet.clear();
                tmpNet.append(self.Netfile.readline()[1:-2]);
                continue;
            
            if line.find("NODE_NAME") != -1:
                tNode = line.replace("\n", '').split('\t')
                tNode = tNode[1].split(' ')
                tmpNet.append(tNode[0]);
                continue;

            if line.find('END.') != -1:
                tmp = tmpNet;
                self.wNets.append(tmp.copy());
                break;
        print("parsing SCH netlist OK.")

    def find_part(self, part):
        tnet = [];
        for net in self.wNets:
            for pp in net:
                if pp == part:
                    tnet.append(net[0]);
        return tnet;

    def print_wNet(self):
        for net in self.wNets:
            print(net);


if __name__ == '__main__':

    tn = SCH_NET()
    tn.open_net_file('wnet.dat');
    tn.parse();
    tn.print_wNet();
