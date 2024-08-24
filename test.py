import logging
from lib import arg_parser, utils
from lib.MMPBSA_generator import generate_directories
from lib.dat_parser import extract_result
from lib.run import run_MMPBSA, run_tleap
from lib.utils import check_exist_data

if __name__ == "__main__":
    utils.setup_logging()
    utils.check_compatibility()

    args = arg_parser.parse_main_arguments()

    config_params = utils.parse_config_yml(args.config_file)

    if args.extract_result:
        extract_result(args, config_params)
        logging.info("Result has been extracted successfully")
        exit(0)

    working_directories = generate_directories(args, config_params)

    check_exist_data(args, config_params)

    if not config_params['scan']['skip_parameterization']:
        run_tleap(working_directories, args, config_params)
    else:
        logging.info('Skipping tLEAP parameterization')

    if config_params['scan']['only_parameterization']:
        logging.info("The parameter `only_parameterization` is set to true and folders are parameterized only and ready to run by MMPBSA.py")
        exit(0)

    run_MMPBSA(working_directories)

