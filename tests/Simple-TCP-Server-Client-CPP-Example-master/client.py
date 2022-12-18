import socket
import base64

host_ip, server_port = "127.0.0.1", 5454
data = " Hello how are you?\n"

def client_sends_msg():

    # Initialize a TCP client socket using SOCK_STREAM
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Establish connection to TCP server and exchange data
        tcp_client.connect((host_ip, server_port))
        encoded = data.encode()
        print(type(encoded)) # bytes
        tcp_client.sendall(encoded)

        # Read data from the TCP server and close the connection
        received = tcp_client.recv(1024)

        # send an image now

        #with open("../../todel.png", mode='rb'):


    finally:
        tcp_client.close()

    print ("Bytes Sent:     {}".format(data))
    print ("Bytes Received: {}".format(received.decode()))

def split_images(input):
    '''new_ids = []
    function = lambda x, y: [x, y]
    for i in range(0, len(input), 1024):
        try:
            new_ids.append(function(input[i], input[i + 1023]))
        except IndexError:
            new_ids.append(input[i])
    return new_ids'''

    output = []
    start = 0
    end = len(input)
    step = 2048
    for i in range(start, end, step):
        x = i
        output.append(input[x:x+step])
    return output

def client_sends_img():

    # Initialize a TCP client socket using SOCK_STREAM
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Establish connection to TCP server and exchange data
        tcp_client.connect((host_ip, server_port))

        with open("../../todel.jpg", mode='rb') as f:
            data = f.read()

            dataSplit = split_images(data)
            index = 0
            for chunk in dataSplit:
                nb = tcp_client.send(chunk)
                print(index, "type", type(chunk), "len", len(chunk), "sent", nb)
                index+=1

            # print("type", type(data))
            # print("len", len(data))
            
            
            
            # tcp_client.sendall(data)





            #encodedData = base64.encodebytes(data)
            #encodedData = base64.encodebytes(data).decode('ascii')
            # encoded = encodedData.encode()
            # print(type(encoded))
            # tcp_client.sendall(encodedData)


            # ok for a message
            # received = tcp_client.recv(1024)

            # receive the image
            received = b""
            while True:
                curr = tcp_client.recv(2048)
                print(len(curr))
                received += curr
                if len(curr) < 2048:
                    break
            

        """with open("../../todel.png", mode='rb') as f:
            img_byte_arr = f.read()
            encoded = base64.encodebytes(img_byte_arr).decode('ascii')
            #encoded = data.encode()

            print(type(encoded))
            tcp_client.sendall(encoded)

            # Read data from the TCP server and close the connection
            received = tcp_client.recv(1024)
        """


    finally:
        tcp_client.close()

    # for a messqge
    # print ("Bytes Received: {}".format(received.decode()))

    # for an image
    with open("temp_received.jpg", "wb") as fout:
        fout.write(received)


#client_sends_msg()
client_sends_img()
