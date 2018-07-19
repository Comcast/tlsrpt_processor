#!/usr/bin/env python
#
# Author: Alex Brotman (alex_brotman@comcast.com)
#
# Purpose: Parse a TLSRPT report, and output as specified
#
# Notes: RFC-TBD
#
# URL: https://github.com/Comcast/tlsrpt_processor/
#

import json,sys,getopt,time

def show_help():
	print("")
	print("This script should process a TLSRPT JSON file pass as an argument")
	print("Options are as follows:")
	print("-h				Show this help message")
	print("-i/-input 			Input file")
	print("-o/-output-style		Output Style (values: kv,csv)")
	print("")

try:
	opts, args = getopt.getopt(sys.argv[1:],"i:o:h",["input=","output-style=","help"])
except getopt.GetoptError as err:
	print str(err)
	print show_help()
	sys.exit(2)
input_file = None
output_style = None
for o,a in opts:
	if o in ("-h","-help"):
		show_help()
		sys.exit()
	elif o in ("-i","-input"):
		input_file = a
	elif o in ("-o","-output-style"):
		output_style = a
		if a not in ("kv","csv"):
			show_help()
			sys.exit(1)
	else:
		assert False, "Unrecognized option"

if input_file is None:
	print("\nERROR: Input file is required")
	show_help()
	sys.exit(1)


try:
	open(input_file,"r")
except IOError:
	print("Input File does not exist or does not have the proper permissions")
	sys.exit(1)

process_time = "%15.0f" % time.time()
process_time = process_time.strip()
csv_separator = "|"

with open(input_file) as json_file:
	try:
		data = json.load(json_file)
	except ValueError:
		print("Invalid JSON file")
		sys.exit(1)


	try:
		organization_name = data["organization-name"]
	except KeyError:
		organization_name = ""
		pass
	try: 
		start_date_time = data["date-range"]["start-datetime"] 
	except KeyError: 
		start_date_time="" 
		pass
	try:
		end_date_time = data["date-range"]["end-datetime"]
	except KeyError:
		end_date_time = ""
		pass
	try:
		contact_info = data["contact-info"]
	except KeyError:
		contact_info = ""
		pass
	try:
		email_address = data["email-address"]
	except KeyError:
		email_address = ""
		pass
	try:
		report_id = data["report-id"]
	except KeyError:
		report_id = ""
		pass


	for policy_set in data["policies"]:
		try:
			policy_type = policy_set["policy"]["policy-type"]
		except KeyError:
			policy_type = ""
			pass
		try:
			policy_string = policy_set["policy"]["policy-string"]
		except KeyError:
			policy_string = ""
			pass
		try:
			policy_domain = policy_set["policy"]["policy-domain"]
		except KeyError:
			policy_domain = ""
			pass
		try:
			policy_mx_host = policy_set["policy"]["mx-host"]
		except KeyError:
			policy_mx_host = ""
			pass
		try: 
			policy_success_count = policy_set["summary"]["total-successful-session-count"]
		except KeyError:
			policy_success_count = 0
			pass
		try:
			policy_failure_count = policy_set["summary"]["total-failure-session-count"]
		except KeyError:
			policy_failure_count = 0
			pass


		for failure_details_set in policy_set["failure-details"]:
			try:
				result_type = failure_details_set["result-type"]
			except KeyError:
				result_type = ""
				pass
			try:
				sending_ip = failure_details_set["sending-mta-ip"]
			except KeyError:
				sending_ip = ""
				pass
			try:
				receiving_mx_hostname = failure_details_set["receiving-mx-hostname"]
			except KeyError:
				receiving_mx_hostname = ""
				pass
			try:
				receiving_mx_helo = failure_details_set["receiving-mx-helo"]
			except KeyError:
				receiving_mx_helo = ""
				pass
			try:
				receiving_ip = failure_details_set["receiving-ip"]
			except KeyError:
				receiving_ip = ""
				pass
			try:
				failed_session_count = failure_details_set["failed-session-count"]
			except KeyError:
				failed_session_count = 0
				pass
			try:
				additional_info = failure_details_set["additional-information"]
			except KeyError:
				additional_info = ""
				pass
			try:
				failure_error_code = failure_details_set["failure-error-code"]
			except KeyError:
				failure_error_code = ""
				pass

			if output_style in ('kv'):

				sys.stdout.write('process-time="' + process_time + '"')
				sys.stdout.write(' report-id="' + report_id + '"')
				sys.stdout.write(' organization-name="' + organization_name + '"')
				sys.stdout.write(' start-date-time="' + start_date_time + '"')
				sys.stdout.write(' end-date-time="' + end_date_time + '"')
				sys.stdout.write(' contact-info="' + contact_info + '"')
				sys.stdout.write(' email-address="' + email_address + '"')
				sys.stdout.write(' policy-type="' + policy_type + '"')
				sys.stdout.write(' policy-string="' + ",".join(policy_string) + '"')
				sys.stdout.write(' policy-domain="' + policy_domain + '"')
				sys.stdout.write(' policy-mx-host="' + policy_mx_host + '"')
				sys.stdout.write(' policy-success-count="' + str(policy_success_count) + '"')
				sys.stdout.write(' policy-failure-count="' + str(policy_failure_count) + '"')
				sys.stdout.write(' result-type="' + result_type + '"')
				sys.stdout.write(' sending-ip="' + sending_ip + '"')
				sys.stdout.write(' receiving-mx-hostname="' + receiving_mx_hostname + '"')
				sys.stdout.write(' receiving-mx-helo="' + receiving_mx_helo + '"')
				sys.stdout.write(' receiving-ip="' + receiving_ip + '"')
				sys.stdout.write(' failed-count="' + str(failed_session_count) + '"')
				sys.stdout.write(' additional-info="' + additional_info + '"')
				sys.stdout.write(' failure-error-code="' + failure_error_code + '"')

			elif output_style in ('csv'):

				sys.stdout.write(process_time + csv_separator)
				sys.stdout.write(report_id + csv_separator)
				sys.stdout.write('"' + organization_name + '"' + csv_separator)
				sys.stdout.write(start_date_time + csv_separator)
				sys.stdout.write(end_date_time + csv_separator)
				sys.stdout.write(contact_info + csv_separator)
				sys.stdout.write(email_address + csv_separator)
				sys.stdout.write(policy_type + csv_separator)
				sys.stdout.write('"' + csv_separator.join(policy_string) + '"' + csv_separator)
				sys.stdout.write(policy_domain + csv_separator)
				sys.stdout.write(policy_mx_host + csv_separator)
				sys.stdout.write(str(policy_success_count) + csv_separator)
				sys.stdout.write(str(policy_failure_count) + csv_separator)
				sys.stdout.write(result_type + csv_separator)
				sys.stdout.write(sending_ip + csv_separator)
				sys.stdout.write(receiving_mx_hostname + csv_separator)
				sys.stdout.write(receiving_mx_helo + csv_separator)
				sys.stdout.write(receiving_ip + csv_separator)
				sys.stdout.write(str(failed_session_count) + csv_separator)
				sys.stdout.write('"' + additional_info + '"' + csv_separator)
				sys.stdout.write(failure_error_code)

			else:
				print "Unrecognized output style"
			sys.stdout.write('\n')
