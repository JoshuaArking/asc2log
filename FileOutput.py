

class FileOutput:  # this class has one instance per input filename
    def __init__(self, filename):
        self.source = filename
        self.networkList: dict = {}

    def new(self, network):  # add a new network to the file
        if network in list(self.networkList.keys()):
            print("This network already exists!")
        else:
            new_filename = self.source.replace(self.source[-4:], "_" + str(network) + ".log").replace("samples/", "output/")  # general file type handling
            new_network = open(new_filename, 'w')
            self.networkList[network] = new_network

    def write(self, network, data):
        if network in list(self.networkList.keys()):
            self.networkList[network].write(data)
        else:
            self.new(network)
            self.write(network, data)

    def close(self, network):
        self.networkList[network].close()

    def __del__(self):
        for network in list(self.networkList.keys()):
            if not self.networkList[network].closed:
                self.networkList[network].close()