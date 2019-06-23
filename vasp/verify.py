from pymatgen.core.lattice import Lattice
from pymatgen.core.structure import IStructure
from gen_vasp_input import struct_from_sgnum, write_vasp_input


struct = struct_from_sgnum(227, 3.867)
print("\n", struct.lattice.angles)
write_vasp_input(struct, 20)
