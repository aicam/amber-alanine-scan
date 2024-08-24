from lib import arg_parser, config

if __name__ == "__main__":

    args = arg_parser.parse_main_arguments()

    config_params = config.parse_config_yml(args.config_file)