# https://gist.github.com/pklaus/a635d4cfc305ba0e4cb6
# @pklaus 

import pickle
import os
import argparse
import sys


def main(argv):
    parser = argparse.ArgumentParser(description='Convert between pickle protocol versions.')
    parser.add_argument("input_file")
    parser.add_argument('-p','--protocol', default=pickle.HIGHEST_PROTOCOL, type=int, help='The pickle protocol version to write the OUTPUT_FILE.')
    args = parser.parse_args()

    print("Writing with protocol version",args.protocol)
    print("Highest supported protocol is",pickle.HIGHEST_PROTOCOL)

    # Unpickle the input_file
    # Fallback to latin1 encoding on UnicodeDecodeError
    f_in = open(args.input_file, 'rb')   
    try:
        data = pickle.load(f_in)
        print("Unpickling 1 OK")
        #data = pickle.load(f,encoding='latin1')
    except UnicodeDecodeError:
        print("UnicodeDecodeError, trying with latin1 encoding")
        error = True

        # Need to open an already opened file ?!
        # without it : Exception : could not find MARK
        f_in = open(args.input_file, 'rb')

        # UnicodeDecodeError so we try with latin1 encoding
        try:
            data = pickle.load(f_in,encoding='latin1')
            print("Unpickling 2 OK")
        except Exception as e:
            print("Oh oh...",e)    
        
    # Create output directory if necessary    
    if not os.path.exists("output"):
        print("Creating output directory")
        os.makedirs("output")
    
    # Dump to output\
    output_file = os.path.join(os.path.curdir+os.sep+"output", args.input_file)
    print("Writing to",output_file)
    f_out = open(output_file, 'wb')
    pickle.dump(data, f_out, args.protocol)

    # close the files
    f_in.close()
    f_out.close()

    return 0


if __name__ == "__main__":
    import sys
    main(sys.argv)