import os

from parmed.amber import AmberParm

from lib import config, arg_parser


def update_radii(topology_file: str, radiis: dict):
    '''
        This function is used to update atom radius based on opt standard
        :param topology_file: path to the topology file
        :radiis: list of atom radiis
        :return: replace the topology file with the new one
        '''
    parm = AmberParm(topology_file)
    for i, atom in enumerate(parm.atoms):
        if atom.atomic_number in radiis.keys(): parm.atoms[i].solvent_radius = radiis[atom.atomic_number]

    os.remove(topology_file)
    parm.write_parm(topology_file)

if __name__ == '__main__':
    args = arg_parser.parse_tleap_arguments()
    config_params = config.parse_config_yml(args.config_file)

    os.chdir(args.working_directory)


    # origin_dir = os.getcwd()
    # err, num_errs = run_tleap_cli("tleap.in")
    #
    # # topology files to update radii in them
    # topologies_list = ['mutation_complex.prmtop', 'mutation_ligand.prmtop', 'wildtype_receptor.prmtop',
    #                    'wildtype_ligand.prmtop', 'wildtype_complex.prmtop', 'wildtype_complex_solvated.prmtop']
    #
    # if num_errs > 0:
    #     logging.error(f"tLEAP failed on parameterizing files with log {err}")
    #     exit(-1)
    # if config_params['scan']['update_atom_radii']:
    #     for topology_file in topologies_list:
    #         update_radii(topology_file, config_params['scan']['atom_radii'])
    # os.chdir(origin_dir)