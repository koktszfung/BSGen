import pymatgen
from pymatgen.ext.matproj import MPRester
from pymatgen.electronic_structure.core import Spin
import numpy
from multiprocessing import Pool
import json


def download(mp_num):
    mat_id = "mp-" + str(mp_num)
    try:
        bandstructure = m.get_bandstructure_by_material_id(material_id=mat_id, line_mode=True)
        if bandstructure is None:
            return
        bands = bandstructure.bands[Spin.up].T  # (kpoints, bands)
        spacegroup = m.get_doc(mat_id)["spacegroup"]
        sgnum = spacegroup["number"]
    except IndexError:
        return
    except pymatgen.ext.matproj.MPRestError:
        return
    except Exception as e:
        print(e)
        return
    else:

        # all possible high symmetry labels
        all_hslabels = numpy.loadtxt(all_hs_path, str)

        # filter out bands of intermediate kpoints (cur_hslabels, bands)
        cur_hslabels_to_bands = {}
        for kpath in bandstructure.branches:
            cur_hslabels_to_bands[kpath["name"].split("-")[0]] = bands[kpath["start_index"]]
            cur_hslabels_to_bands[kpath["name"].split("-")[1]] = bands[kpath["end_index"]]

        # pad zeros to missing high symmetry labels (all_hspoints, bands)
        all_hslabels_to_bands = {
            hslabels:
                cur_hslabels_to_bands[hslabels].tolist()
                if (hslabels in cur_hslabels_to_bands) else
                [0] * bands.shape[1]
            for hslabels in all_hslabels
        }

        all_bands = numpy.array(list(all_hslabels_to_bands.values())).T.tolist()  # (bands, all_hslabels)

        input_dict = {"number": sgnum, "bands": all_bands}
        file_path = write_dir + "input_data_{}.json".format(mp_num)
        with open(file_path, "w") as file:
            json.dump(input_dict, file, indent=4)


m = MPRester("vI8phwVV3Ie6s4ke")
all_hs_path = "../all_hs_files/all_hslabels.txt"
write_dir = "data/input_data_all/"
n_thread = 180

# downloaded data
# 1 - 500000 (15924)
# 1 - 540000 (17285)


def errorfunc(e):
    raise e


def main(start, end):
    pool = Pool(n_thread)

    for mp_id in range(start, end):
        pool.apply_async(download,
                         args=(mp_id,),
                         error_callback=errorfunc)
    pool.close()
    pool.join()
    print('All subprocesses done.')


if __name__ == "__main__":
    total_start = 500000
    interval = 10000
    for i in range(10):
        main(total_start, total_start+interval * i)
