import sys
import socket
import csv
import ipaddress
from os import path

if __name__ == '__main__':
    chunk_encoding = False
    if (len(sys.argv) == 3):
        arg1_list = sys.argv[1].split("/")
        # check protocol
        if arg1_list[0] == "https:":
            print("ERROR: HTTPS not supported.")
            sys.exit()

        # check if a file is specified
        try:
            request_file = arg1_list[3]
        except:
            request_file = ""

        #check if dest_ip and dest_port are specified
        dest_ip_and_port = arg1_list[2].split(":")
        if len(dest_ip_and_port) == 2:
            dest_ip = dest_ip_and_port[0]
            dest_port = dest_ip_and_port[1]
        else:
            dest_ip = dest_ip_and_port[0]
            dest_port = 80

        # set host name
        host_name = sys.argv[2]
        # since we are give nthe ip address in this case we do not need
        # to perform the dns lookup
    elif (len(sys.argv) == 2):
        url = sys.argv[1]
        lst = url.split("/")
        host_name_and_port = lst[2].split(':')
        # check protocol
        if lst[0] == "https:":
            print("ERROR: HTTPS not supported.")
            sys.exit()
        if len(host_name_and_port) == 2:
            host_name=host_name_and_port[0]
            dest_port=host_name_and_port[1]
        else:
            host_name =host_name_and_port[0]
            dest_port = 80
        # since we do not have the ip address in this case
        # we must perform the DNS lookup
        try:
            dest_ip = socket.gethostbyname(host_name)
        except:
            print("ERROR: Website does not exist.")
            sys.exit()
        try:
            request_file = lst[3]
        except:
            request_file = ""
    else:
        print("ERROR: Unable to recognize command line arguments.")
        sys.exit()

    # validate ip_addresss
    try:
        ipaddress.ip_address(dest_ip)
        socket.inet_aton(dest_ip)
    except:
        print("ERROR: Invalid IP address.")
        sys.exit()
    

    # create TCP connection
    no_response = False
    try:
        socket.setdefaulttimeout(2)
        timeout = socket.getdefaulttimeout()
        s = socket.create_connection((dest_ip,dest_port))
        s.settimeout(2)
    except:
        print("ERROR: No response from server.")
        no_response = True
        # sys.exit()

    # construct GET string
    get_request = "GET /"+request_file+" HTTP/1.1\r\nHost: "+host_name+"\r\n\r\n"


    # write to socket
    try:
        s.send(get_request.encode())
    except:
        pass

    # read from socket
    buf = ""
    try:
        while True:
            data = s.recv(1024)
            if not data:
                break
            buf += data.decode()
    except:
        pass
    
    # find source ip and port
    source_ip = '-'
    source_port = '-'
    try:
        source_ip,source_port = s.getsockname()
    except:
        pass

    # tell the server the connection is over
    if dest_port == 80:
        s.shutdown(socket.SHUT_RDWR)
    
    # close the socket
    try:
        s.close()
    except:
        pass

    # separate the header from payload
    position = buf.find("\r\n\r\n")
    if (position == -1) and not no_response:
        print("ERROR: Empty reply from server.")
    header = buf[:position]
    lower_buf = buf.lower()
    obj_begin = buf.find("\r\n\r\n")
    header = buf[:obj_begin]
    payload = buf[obj_begin:]

    # find the server response line
    try:
        header_list = header.split("\n")
        status_code = header_list[0].split()[1]
        server_response_line = status_code + " "+ header_list[0].split()[2]
        server_response_line = header_list[0]
        server_response_line_list = header_list[0].split()
        server_response_line_list.pop(0)
        server_response_line =""
        for i in server_response_line_list:
            server_response_line+=i
            server_response_line+= " "
    except:
        status_code = "-"
        successful = False
        server_response_line = "Empty reply from server"

    # check if successful
    if (status_code == "200"):
        successful = True
    else:
        successful = False
    chunk_encoding = False
    if (buf[:obj_begin].find("Transfer-Encoding: chunked")!=-1):
        print("ERROR: Program does not support chunk encoding.")
        successful = False
        chunk_encoding = True


    ### CSV FILE

    requested_url = "http://"+host_name + "/" + request_file
    fields = ['Successful or Unsuccessful', 'Server Status Code', 'Requested URL','Host Name', 'Source IP', 'Destination IP', 'Source Port', 'Destination Port','Server Response Line' ]
    # make sure that errors are logged not just thrown
    if chunk_encoding:
       successful = False
       status_code = '-' 
       requested_url = requested_url 
       host_name = host_name
       source_ip = "-"
       dest_ip = "-"
       source_port = "-"
       dest_port = dest_port
       server_response_line = "-" 
    if no_response:
        successful = False
        status_code = '-'
        requested_url = requested_url
        host_name = host_name
        source_ip = '-'
        dest_ip = '-'
        dest_port = dest_port
        server_response_line = "No response from server"

    row = [successful,status_code,requested_url,host_name,source_ip,dest_ip,source_port,dest_port,server_response_line]
    # if log.csv does not exist, create one and add the fields
    if(not path.exists("Log.csv")):
        with open('Log.csv','w',newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(fields)
            csv_writer.writerow(row)    
            csvfile.close()
    # if log.csv exists, hen just append entries, do not create the file or enter the fields
    else:
        with open('Log.csv','a',newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(row)    
            csvfile.close()

    # write to HTTPoutput.html

    # write to terminal
    if (successful):
        file=open("HTTPoutput.html",'w')
        file.write(buf[obj_begin+4:])
        file.close
        print("Success ",requested_url," ",status_code) 
    else:
        if (not chunk_encoding):
            print("Unsuccessful ",requested_url," ",status_code)
    sys.exit()
