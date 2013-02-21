import sys
import getopt
import re
from __init__ import generate_params, write_files, generation_modes, search_modes

_verbose = False

def error():
    print """Try `python gen_yaml.py --help` for more information"""
    sys.exit(2)

def show_help():
    print """
Usage: python gen_yaml.py [OPTIONS] TEMPLATE-FILE H-PARAMETER-FILE
Produce yaml files given a template and hyper-parameters ranges
    -o FILE, --out=FILE    file name on which it builds yaml files {{1,2,3,...}}
                           default = TEMPLATE-FILE{{1,2,3,...}}.yaml
    -f, --force            Force yaml files creation even if files with th 
                           same name already exist
    -s, --search=MODE	   Search mode. 
		           {search_modes}
                           default : fix-grid-search
    -g, --generate=MODE    Generation mode. Applied to every learning rate.
                           Locally defined generation mode has predominance
                           default, {generation_modes}
                           default : log-uniform
                            
    -v, --verbose          Verbose mode

File configurations:

    Yaml template
        Use %(save_path)s for the filename of the yaml template. 
        The file name to save .pkl models in the yaml file will be the same as the 
        yaml file name. For a file test1.yaml, save_path will be replaced by test1.
        Look at the template.yaml file for an example.

    Hyper parameters configuration file
        # Hyper-parameters  min     max     how much (optional generation mode)

Example:
    python gen_yaml.py --out=mlp template.yaml hparams.conf
""".format(generation_modes=", ".join(generation_modes.keys()),search_modes=", ".join(search_modes.keys()))

def main(argv):
    save = ""
    force = False
    generate = "log-uniform"
    search_mode = "fix-grid-search"

    try:
        opts, args = getopt.getopt(argv,"vhfo:s:g:",
                        ["verbose","help","force","out=","search=","generate="])
    except getopt.GetoptError as getopt_error:
        print getopt_error.msg, getopt_error.opt
        error()
    else:
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                show_help()
                sys.exit()
            elif opt in ("-v","--verbose"):
                global _verbose
                _verbose = True
            elif opt in ("-f","--force"):
                force = True
            elif opt in ("-o","--out"):
                save = re.sub('.yaml$','',arg)
            elif opt in ("-g","--generate"):
                if arg not in generation_modes.keys():
                    print "generate MODE is invalid: " +arg
                    error()
                generate = arg
            elif opt in ("-s","--search"):
                if arg not in search_modes.keys():
                    print "search MODE is invalid: " +arg
                    error()
                search_mode = arg

    template, hparams = read_args(args)

    if not save:
        save = re.sub('.yaml$','',args[0])

    hpnames, hpvalues = generate_params(hparams,generate,search_mode)

    # fill template
    template = ''.join(template)

    write_files(template,hpnames,hpvalues,save)

    if _verbose:
        print '\n'.join(files)+'\n'

def read_args(args):
    if len(args)>2:
        print "Too many arguments given: ",len(args)
        error()
    elif len(args)<2:
        print "Missing file arguments"
        error()
    else:
       return args[0], args[1]

if __name__ == "__main__":
    main(sys.argv[1:])
