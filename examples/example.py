import sys, os

ROOT = os.path.join(os.getcwd(),     "chiV")
sys.path.insert(0, ROOT)

from ParseAST import ParseAST
from BlackBoxGen import BlackBoxGen

parser = ParseAST()
parser.parser("/home/talha/chiV/examples/test.ast")
module = parser.get_top_module()
portlist = parser.get_portlist()
# print(parser.get_instances())
# print(parser.get_modules())
# print(module)
# print(portlist)

bb_gen = BlackBoxGen()
bb = bb_gen.gen_bb(module[0], portlist)
for i in bb:
    print(i)