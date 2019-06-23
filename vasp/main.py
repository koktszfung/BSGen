import os
import json
import numpy
from typing import Union, List
from gen_vasp_input import struct_from_sgnum, write_vasp_input
from gen_nn_input import write_nn_input_label_based, write_nn_input_coord_based
from plot_vasp_output import plot_bs


def vasp(sgnum: int, index: int,):
    try:
        print("\tvasp {} start".format(index))
        os.system("mpiexec -n 4 vasp-544-s > vasp.out")
    except Exception as e:
        print("\tskipped due to {}".format(e))
        return
    else:
        os.system("cp vasprun.xml vaspruns/vasprun_{}_{}".format(sgnum, index))
        print("\tvasp end")


def gen_bs_from_sgnum(sgnum: int,
                      scale: float,
                      division: int,
                      index: int,
                      init_coords: Union[List[List[float]], numpy.ndarray] = None,
                      plot: bool = False):
    struct = struct_from_sgnum(
        sgnum=sgnum,
        scale=scale,
        init_coords=numpy.random.rand(1, 3) if init_coords is None else init_coords,
        species=None,
    )

    write_vasp_input(
        structure=struct,
        kpath_division=division,
        write_dir=".",
    )

    # vasp(sgnum=sgnum, index=index)

    write_nn_input_label_based(
        sgnum=sgnum,
        index=index,
        all_hs_path="all_hs_files/all_hslabels.txt",
        vasprun_path="vasprun.xml",
        write_dir="input_data/label_based/"
    )

    write_nn_input_coord_based(
        structure=struct,
        sgnum=sgnum,
        index=index,
        all_hs_path="all_hs_files/all_hspoints.txt",
        vasprun_path="vasprun.xml",
        write_dir="input_data/coord_based/"
    )

    if plot:
        plot_bs("vasprun.xml")


def kwargs_from_file(file_path):
    with open(file_path) as file:
        return json.load(file)


def main(sgnum: int,
         scale: float,
         division: int,
         start: int = 0,
         total: int = 1,
         init_coords: Union[List[List[float]], numpy.ndarray] = None,
         plot: bool = False):
    print("main {} start".format(sgnum))
    for i in range(start, start + total):
        gen_bs_from_sgnum(
            sgnum=sgnum,
            scale=scale,
            division=division,
            index=i,
            init_coords=init_coords,
            plot=i == start + total - 1 and plot,
        )
    print("main end")


if __name__ == '__main__':
    main(**kwargs_from_file("config.json"))
