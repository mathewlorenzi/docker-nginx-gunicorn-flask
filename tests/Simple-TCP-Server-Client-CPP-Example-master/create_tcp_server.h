/*#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netdb.h>
#include <netinet/in.h>
#include <errno.h>
*/
#include <stdio.h> //printf
#include <stdlib.h>  //atoi
#include <string.h> //memset
#include <netinet/in.h>

// eco
#include <string>
#include <iostream> // std::cout
#include <fstream> // to save image as binary

#include "base64.h"

class TcpServer
{
public:
	TcpServer() {};
	~TcpServer() {};
    bool create(int queueLength, int recvBufferSize, char *server_port)
    {
        printf("[INFO]TcpServer::create with port %s\n", server_port);
        QUEUE_LENGTH = queueLength;
        RECV_BUFFER_SIZE = recvBufferSize;
        // create socket file descriptor
        if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0)
        {
            printf("[ERROR]socket failed\n");
            return false;
        }
        // create socket address, forcefully attach socket to the port
        int opt = 1;
        if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt)))
        {
            printf("[ERROR]setsockopt failed\n");
            return false;
        }
        address.sin_family = AF_INET;
        address.sin_addr.s_addr = INADDR_ANY;
        address.sin_port = htons(atoi(server_port));
        // bind socket to address
        if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0)
        {
            printf("[ERROR]bind failed\n");
            return false;
        }
        // listen to incoming connections
        if (listen(server_fd, QUEUE_LENGTH) < 0)
        {
            printf("[ERROR]listen failed\n");
            return false;
        }
        printf("[INFO]TcpServer::create with port %s successful\n", server_port);
        return true;
    }
    bool wait_to_receive()
    {
        printf("[INFO]TcpServer::wait_connection of a client\n");
        while (1)
        {
            // accept a connection
            int addrlen = sizeof(address);
            if ((sock = accept(server_fd, (struct sockaddr *)&address, (socklen_t *)&addrlen)) < 0)
            {
                printf("[ERROR]accept failed\n");
                return false;
            }
            printf("[INFO]TcpServer::wait_to_receive client message\n");
            while (1) {
                // receive message
                char buffer[2048];
                std::string myString;
                int nDataLength;
                int index=0;
                while ((nDataLength = recv(sock, buffer, sizeof(buffer), 0)) > 0) {
                    printf("...%d here %d\n", index, nDataLength);
                    myString.append(buffer, nDataLength);
                    if(nDataLength<sizeof(buffer)){
                        break;
                    }
                    index++;
                }
                std::string outputSavedImageStem = "temp";
                std::string ext="jpeg";
                std::ofstream outfile{outputSavedImageStem+"."+ext, std::ofstream::binary};
                outfile.write(myString.c_str(), static_cast<std::streamsize>(myString.length()));
                

try change png t jpeg from camera.html,
in main server; web app, record, and see if it really is a jpeg by the size of it 
better spend time compressing than overloading the network

                /*printf("...here2 %d\n", myString.length());
                std::string outputSavedImageStem = "temp";
                std::string ext="png";
                std::ofstream outfile{outputSavedImageStem+"."+ext, std::ofstream::binary};
                outfile.write(myString.c_str(), static_cast<std::streamsize>(myString.length()));
                std::string outputSavedImage = outputSavedImageStem + ".jpg";
                std::string cmdConvert = "convert " + outputSavedImageStem+"."+ext + " " + outputSavedImageStem + ".jpg";
                bool printDetails = true;
                if(printDetails==true){
                    std::cout << cmdConvert << std::endl;
                }
                system(cmdConvert.c_str());
                */



                /*char buffer[RECV_BUFFER_SIZE];
                int recv_bytes = recv(sock, buffer, RECV_BUFFER_SIZE, 0);
                if (recv_bytes == 0)
                {
                    fflush(stdout);
                    break;
                }
                // dont print if image received : fwrite(buffer, recv_bytes, 1, stdout);

                printf("recv_bytes %d\n", recv_bytes);

                bool printDetails = true;
                
                //char *buffer2 = new char[recv_bytes];
                // std::string b = base64_decode(buffer, false);
                std::string outputSavedImageStem = "temp";
                std::string ext="png";
                std::ofstream outfile{outputSavedImageStem+"."+ext, std::ofstream::binary};
                //outfile.write(b.c_str(), static_cast<std::streamsize>(b.size()));
                //outfile.write(buffer2, static_cast<std::streamsize>(recv_bytes));
                outfile.write(buffer, static_cast<std::streamsize>(recv_bytes));
                std::string outputSavedImage = outputSavedImageStem + ".jpg";
                std::string cmdConvert = "convert " + outputSavedImageStem+"."+ext + " " + outputSavedImageStem + ".jpg";
                if(printDetails==true){
                    std::cout << cmdConvert << std::endl;
                }
                system(cmdConvert.c_str());
                // _msg = "[INFO]create_tcp_server: " + outputSavedImage + " <= " + filenameWithStamp;
                // std::cout << _msg << std::endl;
                */




                // ECO: respond
                char msg[2048];
                memset(&msg, 0, sizeof(msg));//clear the buffer
                strcpy(msg, "image content");
                send(sock, (char*)&msg, strlen(msg), 0);

                printf("[INFO]TcpServer::wait_to_receive client: msg received and replied\n");
                return true;
            }
        }
        return false;
    }
    //#define QUEUE_LENGTH 10
    //#define RECV_BUFFER_SIZE 2048    
    int QUEUE_LENGTH;
    int RECV_BUFFER_SIZE;
    struct sockaddr_in address;
    int server_fd;
    int sock;
};
