import argparse
import math
import json
from collections import Counter
from datetime import datetime

ip_dictionary = Counter()
bytes_exchanged = 0
events_counter = 0
max_date = datetime.min
min_date = datetime.max
logs = []


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1000, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def ip_frequency(ip):
    global ip_dictionary
    if ip != '-':
        ip_dictionary[ip] += 1


def events_per_second():
    global max_date
    global min_date
    dif = max_date - min_date
    return events_counter / dif.total_seconds()


def processing_file(args):
    log_file = open(args.path, 'r')

    while True:
        log_line = log_file.readline()
        if not log_line:
            log_file.close()
            break
        else:
            clean_log = log_line.split()

            if args.most or args.least:
                client_ip = clean_log[2]
                des_ip = clean_log[8].split("/")[1]
                ip_frequency(client_ip)
                ip_frequency(des_ip)

            if args.bytes:
                header = clean_log[1]
                response = clean_log[4]
                global bytes_exchanged
                bytes_exchanged += int(header) + int(response)

            if args.event:
                global events_counter
                global max_date
                global min_date

                events_counter += 1
                time_stamp = datetime.fromtimestamp(float(clean_log[0]))

                if time_stamp > max_date:
                    max_date = time_stamp
                if time_stamp < min_date:
                    min_date = time_stamp

            if args.output:

                global logs
                element = {'timestamp': clean_log[0], 'header_in_bytes': clean_log[1], 'client_ip': clean_log[2],
                           'response_code': clean_log[3], 'response_in_bytes': clean_log[4],
                           'http_request_method': clean_log[5], 'url': clean_log[6], 'username': clean_log[7],
                           'access_and_destination': clean_log[8], 'response_type': clean_log[9]}
                logs.append(element)


def main():


    parser = argparse.ArgumentParser(description='Analyzes log files')
    parser.add_argument('-p', '--path', metavar='PATH_FOLDER', required=True,help='Path to folder containing access logs files')
    parser.add_argument('-m', '--most', required=False, help='Most frequent IP', action='store_true')
    parser.add_argument('-l', '--least', required=False, help='Least frequent IP', action='store_true')
    parser.add_argument('-e', '--event', required=False, help='Events per second', action='store_true')
    parser.add_argument('-b', '--bytes', required=False, help='Total amount of bytes exchanged', action='store_true')
    parser.add_argument('-o', '--output', metavar='FILE_NAME', required=False, help='Write the name of the output file',type=str)
    args = parser.parse_args()

    if args.path and not (args.most or args.least or args.bytes or args.event or args.output):

        print("No option was provided, -h argument will display a list of options")

    else:

        processing_file(args)

        if args.most:
            print(
                f'The most frequent IP is: {ip_dictionary.most_common(1)[0][0]} with {ip_dictionary.most_common(1)[0][1]} ocurrences')
        if args.least:
            print(
                f'The least frequent IP is: {ip_dictionary.most_common()[:-1 - 1:-1][0][0]} with {ip_dictionary.most_common()[:-1 - 1:-1][0][1]} ocurrences')  # [:-n-1:-1]
        if args.bytes:
            print(f'The total amount of bytes exchanged is: {convert_size(bytes_exchanged)}')
        if args.event:
            print("On average the rate of events per second: {:.2f} events/s".format(events_per_second()))
        if args.output:
            file_name = str(args.output)
            global logs
            with open(file_name+".json", "w") as final:
                json.dump(logs, final, indent=2)
            final.close()
            print("A JSON files has been created")


if __name__ == '__main__':
    main()
