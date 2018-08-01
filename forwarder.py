import time
import datetime
import socket


def parse_log_line(line):
    strptime = datetime.datetime.strptime
    hostname = socket.gethostname()
    time = line.split(' ')[3][1::]
    entry = {}
    entry['datetime'] = strptime(
        time, "%d/%b/%Y:%H:%M:%S").strftime("%Y-%m-%d %H:%M")
    entry['source'] = "'{}'".format(hostname)
    entry['type'] = "'www_access'"
    entry['log'] = "'{}'".format(line.rstrip())
    return entry


def show_entry(entry):
    temp = ",".join([
        entry['datetime'],
        entry['source'],
        entry['type'],
        entry['log']
    ])
    print("{}".format(temp))
    return temp


def follow(syslog_file):
    fout = open("access_logs.csv", "at")
    syslog_file.seek(0, 2)
    while True:
        line = syslog_file.readline()
        if not line:
            time.sleep(0.1)
            continue
        else:
            entry = parse_log_line(line)
            if not entry:
                continue
            csv_line = show_entry(entry)
            fout.write("{}\n".format(csv_line))


f = open("/var/log/apache2/access.log", "rt")
follow(f)
