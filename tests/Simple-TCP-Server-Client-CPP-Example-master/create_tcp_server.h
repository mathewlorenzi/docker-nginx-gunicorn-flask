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
            delete [] replyImageBuffer; replyImageBuffer=NULL;
        }
        delete [] replyChunkedBuffer; replyChunkedBuffer = NULL;
        delete [] replyChunkedSizes; replyChunkedSizes = NULL;
        delete [] dumbArrayChar; dumbArrayChar = NULL;
    };
    bool create(int queueLength, int recvBufferSize, char *server_port, bool debug) // 10, 2048, anyport
    {
        printf("[INFO]TcpServer::create with port %s\n", server_port);
        QUEUE_LENGTH = queueLength;
        RECV_BUFFER_SIZE = recvBufferSize;
        m_debug = debug;

        maxNbChunks = 100; // 100x2048 = 204 800 kb for the ecovision size: should be enough
        replyChunkedBuffer = new std::string[maxNbChunks];
        replyChunkedSizes = new int[maxNbChunks];
        replyImageBufferSize = maxNbChunks*RECV_BUFFER_SIZE;
        replyImageBuffer = new char[replyImageBufferSize];
        dumbArrayChar = new char[RECV_BUFFER_SIZE];

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
                //char buffer[2048];
                std::string myString;
                int nDataLength;
                int index=0;
                //printf("RECV_BUFFER_SIZE %d sizebuffer %d\n", RECV_BUFFER_SIZE, sizeof(m_buffer));
                //printf("sizebuffer %d\n", sizeof(buffer));
                while ((nDataLength = recv(sock, m_buffer, RECV_BUFFER_SIZE, 0)) > 0) {
                //while ((nDataLength = recv(sock, buffer, RECV_BUFFER_SIZE, 0)) > 0) {
                    if(m_debug==true) { printf(" ... received chunk %d size %d sizebuffer %d\n", index, nDataLength, RECV_BUFFER_SIZE); }
                    myString.append(m_buffer, nDataLength);
                    //myString.append(buffer, nDataLength);
                    // if(nDataLength<sizeof(m_buffer)){
                    if(nDataLength<RECV_BUFFER_SIZE){
                    //if(nDataLength<sizeof(buffer)){
                        if(m_debug==true) { printf(" ... break\n"); }        
                        break;
                    }
                    index++;
                }
                if(m_debug==true) { printf(" ... finished loop\n"); }
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
                
                
                inputFile.seekg (0, inputFile.end);
                int inputSize = inputFile.tellg();
                inputFile.seekg (0, inputFile.beg);

                if(inputSize>replyImageBufferSize)
                {
                    printf("[ERROR]wait_to_receive: error in size estimation %d vs %d\n", inputSize, replyImageBufferSize);
                    return false;
                } 
                inputFile.read(replyImageBuffer, inputSize);





//std::ofstream outfile2{"debug_img_to_send-as-a-areply.jpg", std::ofstream::binary};
// outfile2.write(replyImageBuffer, static_cast<std::streamsize>(inputSize));
//std::string debugOut;



                int nbChunks = get_nb_chunks(inputSize);
                if(nbChunks<0){ printf("[ERROR]create_tcp_server.h: wait_to_receive: splitimages failed\n"); return false; }
                if(m_debug==true) { printf(" ... sending as a reply %d nbChunks\n", nbChunks); }
                int start = 0;
                for(int ii=0; ii<nbChunks; ii++)
                {
                    int stop = start + RECV_BUFFER_SIZE;
                    if(stop > inputSize){
                        stop = inputSize;
                    }
                    // printf(" ... %d -> %d-1\n", start, stop);
                    int j=0;
                    for(int dumi=start; dumi<stop; dumi++)
                    {
                        dumbArrayChar[j] = replyImageBuffer[dumi];
                        j++;
                    }
                    //printf(" ... %d vs %d\n", j, stop-start);
                    send(sock, (char *)dumbArrayChar, stop-start, 0);
                    start = stop;
                }




                /*int nbChunks = split_image(inputSize);
                if(nbChunks<0){ printf("[ERROR]create_tcp_server.h: wait_to_receive: splitimages failed\n"); return false; }
                if(m_debug==true) { printf(" ... sending as a reply %d nbChunks\n", nbChunks); }
                for(int ii=0; ii<nbChunks; ii++)
                {
                    if(m_debug==true) { printf(" ... sending chunk %d size %d\n", ii, replyChunkedSizes[ii]); }
                    send(sock, (char *)replyChunkedBuffer[ii].c_str(), replyChunkedSizes[ii], 0);
//debugOut += replyChunkedBuffer[ii].c_str();
                }*/
                printf("[INFO]TcpServer::wait_to_receive client: msg received and replied\n");
//outfile2.write(debugOut.c_str(), static_cast<std::streamsize>(inputSize));
//printf("%d vs %d\n", sizeof(debugOut), inputSize);
                return true;
            }
        }
        return false;
    }
    int get_nb_chunks(int inputSize)
    {
        int nbChunks = inputSize/RECV_BUFFER_SIZE;

        float ratio1 = float(inputSize) / float(RECV_BUFFER_SIZE); // 403/23=17.52
        int ratio2 = inputSize/RECV_BUFFER_SIZE;                   // 403/23=17        
        int est2 = ratio2*RECV_BUFFER_SIZE;                        // 17*23=391
        if(inputSize>est2){                                  // 403-391
            nbChunks += 1;
        }

        if(nbChunks>maxNbChunks){
            printf("[ERROR]split_image: error1 in size estimation\n");
            return -1;
        }
        return nbChunks;
    }
    int split_image(int inputSize) // input is replyImageBuffer
    {
        int nbChunks = inputSize/RECV_BUFFER_SIZE;

        float ratio1 = float(inputSize) / float(RECV_BUFFER_SIZE); // 403/23=17.52
        int ratio2 = inputSize/RECV_BUFFER_SIZE;                   // 403/23=17        
        int est2 = ratio2*RECV_BUFFER_SIZE;                        // 17*23=391
        if(inputSize>est2){                                  // 403-391
            nbChunks += 1;
        }

        if(nbChunks>maxNbChunks){
            printf("[ERROR]split_image: error1 in size estimation\n");
            return -1;
        }

        int start = 0;
        int end = inputSize;
        int step = RECV_BUFFER_SIZE;// 2048;
        int index = 0;
        for(int i=start; i<end; i+=step)
        {
            int x1 = i;
            int x2 = i+step-1;
            if(x2>=end) { x2=end-1; }
            if(index>=nbChunks){
                printf("[ERROR]split_image: error2 in size estimation\n");
                return -1;
            }
            replyChunkedSizes[index] = x2-x1+1;
            //auto size = std::distance(itStart, itEnd);
            //std::string newStr = myStr.subStr(itStart, size);

            // TODO fast way to do this or at least with pointers
            int dumbi=0;
            for(int ai=x1; ai<=x2; ai++){
                dumbArrayChar[dumbi] = replyImageBuffer[ai];
                dumbi++;
            }
            replyChunkedBuffer[index] = std::string(dumbArrayChar); // is size respected ?????????

            index++;
        }
        return nbChunks;
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

    int maxNbChunks;
    std::string *replyChunkedBuffer;
    char *replyImageBuffer; int replyImageBufferSize;
    int *replyChunkedSizes;
    char *dumbArrayChar;
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