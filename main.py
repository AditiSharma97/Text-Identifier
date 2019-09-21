import argparse
import pandas as pd
import pickle

from preparedata import prepare_data
from identifylanguage import identify

def arg_parser():
	help_string = "Welcome to language identifier!"
	parser = argparse.ArgumentParser(description=help_string, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("mode", nargs='+', choices=['prepare_data', 'identify_language'])
	args = parser.parse_args()
	return args

def main():
	#run main.py with input prepare_data for the first time, then run with input identify_language
	args = arg_parser()
	
	if 'prepare_data' in args.mode:		
		prepare_data()
	elif 'identify_language' in args.mode:
		identify()	
	
if __name__=='__main__':
	main()
