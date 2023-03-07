class BlackBoxGen:
    def gen_ports(self, portlist):
        bundles = []
        for i in portlist:
            for j in portlist[i]:
                port_type = "Analog" if portlist[i][j][0] == "Inout" else portlist[i][j][0]
                port_name = j
                port_width = portlist[i][j][1]
                port = " "*8 + f"val {port_name} = {port_type}(UInt({port_width}.W))\n"
                bundles.append(port)

        return bundles
    
    def gen_class(self, module):
        class_name = module
        class_def = f"class {class_name} extends BlackBox{{"
        return [class_def]
    
    def gen_bundles(self, portlist):
        ports = "".join(map(str, self.gen_ports(portlist)))
        structure = " "*4 + f"val io = IO(new Bundle{{\n" + ports + " "*4 + "})\n"
        return [structure]
    
    def gen_bb(self, module, portlist):
        bb = self.gen_class(module) + self.gen_bundles(portlist) + list("}")
        return bb
        

# portlist = {'top': {'rd': ['Inout', 1], 'rs1': ['Input', 1], 'rs2': ['Input', 1], 'write_enable': ['Input', 32], 'ready': ['Output', 8]}}

# gen = BlackBoxGen()
# a = gen.gen_bb("top", portlist)
# a = gen.gen_ports(portlist)
# a = gen.gen_bundles(portlist)
# for i in a:
#     print(i)