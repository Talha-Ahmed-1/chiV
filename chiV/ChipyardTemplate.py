module_name = "JustRead"
from ParseAST import *

class ChipyardTemplate(ParseAST):
	def __init__(self):
		pass

	def key_class_gen(self, module_name):
		key_class = """case object {module_name}Key extends Field[Option[{module_name}Params]](None)""".format(module_name=module_name)
		return key_class

	def top_IO_class_gen(self, module_name):
		top_IO_class = """trait {module_name}TopIO extends Bundle {
			val isReady = Output(Bool())
		}""".format(module_name=module_name)

	def bb_IO_class_gen(self, module_name):
		bb_IO_class = """class {module_name}IO extends Bundle {
			val clock = Input(Clock())
			val reset = Input(UInt(1.W))
			val reg_out = Output(UInt(32.W))
		}""".format(module_name=module_name)

	def has_IO_class_gen(self, module_name):
		has_IO_class = """trait Has{module_name}BlackboxIO extends BaseModule {
			val io = IO(new {module_name}BlackboxIO())
		}""".format(module_name=module_name)

	def bb_impl_gen(self, module_name, file_name):
		bb_impl = """class {module_name}BB() extends BlackBox() with HasBlackBoxResource with Has{module_name}BlackboxIO
		{
			addResource("/chipshop/{file_name}.v")
		}""".format(module_name=module_name, file_name=file_name)

	def bus_TL_class_gen(self, module_name):
		bus_TL_class = """class {module_name}TL(params: {module_name}Params, beatBytes: Int)(implicit p: Parameters)
			extends TLRegisterRouter(
				params.address, "{module_name}", Seq("talha,{module_name}"),
				beatBytes = beatBytes)(
					new TLRegBundle(params, _) with {module_name}TopIO)(
						new TLRegModule(params, _, _) with {module_name}TopModule)""".format(module_name=module_name)

	def peripheral_impl_class_gen(self, module_name):
		periphery_impl_class = """trait CanHavePeriphery{module_name}ModuleImp extends LazyModuleImp {
			val outer: CanHavePeriphery{module_name}
		}""".format(module_name=module_name)

	def peripheral_class_gen(self, module_name):
		periphery_class = """trait CanHavePeriphery{module_name} { this: BaseSubsystem =>
			private val portName = "Port0"

			val module_obj = p({module_name}Key) match { 	
				case Some(params) => { 				
					val module_obj = LazyModule(new {module_name}TL(params, pbus.beatBytes)(p))
					pbus.toVariableWidthSlave(Some(portName)) { module_obj.node } 
					Some(module_obj)
				}
				case None => None
			}
		}""".format(module_name=module_name)

	def with_class_gen(self, module_name):
		with_class = """class With{module_name}(address: BigInt, width: Int) extends Config((site, here, up) => {
		case {module_name}Key => Some({module_name}Params())
		})""".format(module_name=module_name)

	def param_class_gen(self, module_name, address, paramlist, paraminfo):
		param_class = """case class {module_name}Params(\n\taddress: BigInt = {base_address}"""
		
		if len(paramlist) > 0:
			param_class += ",\n"
			for i in paramlist:
				param_value = f"\"{paraminfo[i][1]}\"" if paraminfo[i][1] != "" else "\"\""
				param_class += """\t{param_name}: {param_type} = {param_value}""".format(param_name=i, param_type=paraminfo[i][0], param_value=param_value)
				if i != paramlist[-1]:
					param_class += ",\n"
				else:
					param_class += "\n)"

		print(param_class.format(module_name=module_name, base_address=address))

	

# params = {'top': {'acha': ['IntConst', 1], 'theek': ['IntConst', 0], 'kya': ['StringConst', '']}}
paraminfo = {'DW': ['Int', '31'], 'theek': ['Float', '0.6'], 'kya': ['String', 'hello']}
paramlist = ['DW', 'theek', 'kya']

temp = ChipyardTemplate()
temp.param_class_gen("JustRead", "0x1000", paramlist, paraminfo)

# print(bb_impl.replace("{module_name}", module_name))