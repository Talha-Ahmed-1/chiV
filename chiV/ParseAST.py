class ParseAST:
    def __init__(self):
        self.module_name = ""
        self.portlist = {}
        self.paramlist = {}
        self.instances = set()
        self.modules = set()

    def parser(self, filename):
        file = open(filename, "r")
        data = file.readlines()
        file.close()

        for i in data:
            if "InstanceList" in i:
                self.instances.add(i.split(" ")[7])
            elif "ModuleDef" in i:
                self.module_name = i.split(" ")[5]
                self.modules.add(self.module_name)
                self.portlist[self.module_name] = {}
                self.paramlist[self.module_name] = {}
            elif "Parameter" in i:
                param_name = i.split(" ")[11][:-1]
                param_type = data[data.index(i)+2].split(" ")[14][:-1]
                param_type = "String" if param_type == "StringConst" else "Int" if param_type == "IntConst" else "Float" if param_type == "FloatConst" else "Bool"
                param_value = data[data.index(i)+2].split(" ")[15]
                self.paramlist[self.module_name][param_name] = [param_type, int(param_value) if param_type == "IntConst" else float(param_value) if param_type == "FloatConst" else param_value]
            elif "Input" in i or "Output" in i or "Inout" in i:
                port_name = i.split(" ")[11][:-1]
                port_type = i.split(" ")[10][:-1]
                if  "Width" in data[data.index(i)+1]:
                    # port_name = i.split(" ")[11][:-1]
                    # port_type = i.split(" ")[10][:-1]
                    val1 = data[data.index(i)+2].split(" ")[15]
                    MSB = int(val1) if "IntConst" in data[data.index(i)+2] else val1
                    val2 = data[data.index(i)+3].split(" ")[15]
                    LSB = int(val2) if "IntConst" in data[data.index(i)+3] else val2
                    width = [MSB, LSB]
                    self.portlist[self.module_name][port_name] = [port_type, width]
                else:
                    # port_name = i.split(" ")[11][:-1]
                    # port_type = i.split(" ")[10][:-1]
                    width = [0, 0]
                    self.portlist[self.module_name][port_name] = [port_type, width]

    def get_top_module(self):
        return list(self.modules - self.instances)
    
    def get_portlist(self):
        return self.portlist
    
    def get_instances(self):
        return self.instances
    
    def get_modules(self):
        return list(self.modules)
    
    def get_paramlist(self):
        return self.paramlist
    
parser = ParseAST()
parser.parser("test.ast")
print(parser.get_paramlist())
print(parser.get_top_module())
print(parser.get_portlist())
print(parser.get_instances())
print(parser.get_modules())