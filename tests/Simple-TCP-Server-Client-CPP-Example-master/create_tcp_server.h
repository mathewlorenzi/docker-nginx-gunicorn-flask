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

int split_images(std::string &input, int inputSize, int chunkSize, std::string *output)
{
    nbChunks = (inputSize/chunkSize)+1;

    verify nb chunks

    output = new std::string[nbChunks];

    int start = 0;
    int end = inputSize;
    int step = chunkSize;// 2048;
    int index = 0;
    for(int i=start; i<end; i+=step)
    {
        int x1 = i;
        int x2 = i+step;
        if(x2>end) { x2=end; }
        if(index>=nbChunks){
            printf("[ERROR]split_images: error in size estimation\n");
            return -1;
        }
        chunkedSizes[index] = x2-x1+1;
        output[index] = input[x1:x2] ??
        index++;
    }
    return nbChunks

class TcpServer
{
public:
	TcpServer()
    {
        m_buffer = NULL;
        QUEUE_LENGTH = 0;
        RECV_BUFFER_SIZE = 0;
        m_debug = false;
    };
	~TcpServer()
    {
        if(RECV_BUFFER_SIZE>0){
            delete [] m_buffer; m_buffer=NULL;
        }
    };
    bool create(int queueLength, int recvBufferSize, char *server_port, bool debug) // 10, 2048, anyport
    {
        printf("[INFO]TcpServer::create with port %s\n", server_port);
        QUEUE_LENGTH = queueLength;
        RECV_BUFFER_SIZE = recvBufferSize;
        m_debug = debug;
        if(RECV_BUFFER_SIZE>0){
            m_buffer = new char[RECV_BUFFER_SIZE];
        }
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
    bool wait_to_receive(std::string outputPathJpgRecvImg, std::string pathImageJpegToReplyTo_resultEcoVision)
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
                //printf("RECV_BUFFER_SIZE %d sizebuffer %d\n", RECV_BUFFER_SIZE, sizeof(m_buffer));
                //printf("sizebuffer %d\n", sizeof(buffer));
                //while ((nDataLength = recv(sock, m_buffer, sizeof(m_buffer), 0)) > 0) {
                while ((nDataLength = recv(sock, buffer, RECV_BUFFER_SIZE, 0)) > 0) {
                    if(m_debug==true) { printf("received chunk %d size %d sizebuffer %d\n", index, nDataLength, sizeof(buffer)); }
                    myString.append(m_buffer, nDataLength);
                    //myString.append(buffer, nDataLength);
                    if(nDataLength<sizeof(m_buffer)){
                    //if(nDataLength<sizeof(buffer)){
                        break;
                    }
                    index++;
                }
                //std::string outputSavedImageStem = "temp";
                //std::string ext="jpeg";
                //std::ofstream outfile{outputSavedImageStem+"."+ext, std::ofstream::binary};
                std::ofstream outfile{outputPathJpgRecvImg, std::ofstream::binary};
                outfile.write(myString.c_str(), static_cast<std::streamsize>(myString.length()));
                

                // REF: old1

                // ECO: OK: respond text message
                /*char msg[2048];
                memset(&msg, 0, sizeof(msg));//clear the buffer
                strcpy(msg, "image content");
                send(sock, (char*)&msg, strlen(msg), 0);*/

                // ECO: respond a jpeg image
                std::ifstream inputFile{pathImageJpegToReplyTo_resultEcoVision, std::ifstream::binary};
                std::string inputFileBuffer;
                int inputSize = inputFile.read(inputFileBuffer);
                int chunkSize = RECV_BUFFER_SIZE;
                std::string *chunkedBuffer;
                int *chunkedSizes;
                int nbChunks = split_images(std::string &input, inputSize, chunkSize, chunkedBuffer, chunkedSizes);
                if(nbChunks<0){ printf("[ERROR]create_tcp_server.h: wait_to_receive: splitimages failed\n"); return false; }
                for(int ii=0; ii<nbChunks; ii++)
                {
                    send(sock, (char*)chunkedBuffer[ii].c_str(), chunkedSizes[ii], 0);
                }
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
    char *m_buffer;
    bool m_debug;
};


                // old1
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