module_name = "JustRead"
key_class = """case object {module_name}Key extends Field[Option[{module_name}Params]](None)"""

top_IO_class = """trait {module_name}TopIO extends Bundle {
	val isReady = Output(Bool())
}"""

bb_IO_class = """class {module_name}IO extends Bundle {
	val clock = Input(Clock())
	val reset = Input(UInt(1.W))
	val reg_out = Output(UInt(32.W))
}"""

has_IO_class = """trait Has{module_name}BlackboxIO extends BaseModule {
	val io = IO(new {module_name}BlackboxIO())
}"""

bb_impl = """class {module_name}BB() extends BlackBox() with HasBlackBoxResource with Has{module_name}BlackboxIO
{
	addResource("/chipshop/{file_name}.v")
}"""

bus_TL_class = """class {module_name}TL(params: {module_name}Params, beatBytes: Int)(implicit p: Parameters)
	extends TLRegisterRouter(
		params.address, "{module_name}", Seq("talha,{module_name}"),
		beatBytes = beatBytes)(
			new TLRegBundle(params, _) with {module_name}TopIO)(
				new TLRegModule(params, _, _) with {module_name}TopModule)"""

periphery_impl_class = """trait CanHavePeriphery{module_name}ModuleImp extends LazyModuleImp {
	val outer: CanHavePeriphery{module_name}
}"""

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
}"""

with_class = """class With{module_name}(address: BigInt, width: Int) extends Config((site, here, up) => {
  case {module_name}Key => Some({module_name}Params())
})"""

# print(bb_impl.replace("{module_name}", module_name))