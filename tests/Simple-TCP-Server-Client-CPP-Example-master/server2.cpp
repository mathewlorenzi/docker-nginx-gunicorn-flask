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

#define QUEUE_LENGTH 10
#define RECV_BUFFER_SIZE 2048

char msg[1500];

int server(char *server_port) {
    // create socket file descriptor
    int server_fd;
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0)
    {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    // create socket address
    // forcefully attach socket to the port
    struct sockaddr_in address;
    int opt = 1;
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt)))
    {
        perror("setsockopt failed");
        exit(EXIT_FAILURE);
    }
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(atoi(server_port));

    // bind socket to address
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0)
    {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    // listen to incoming connections
    if (listen(server_fd, QUEUE_LENGTH) < 0)
    {
        perror("listen failed");
        exit(EXIT_FAILURE);
    }

    while (1) {
        // accept a connection
        int sock;
        int addrlen = sizeof(address);
        if ((sock = accept(server_fd, (struct sockaddr *)&address, (socklen_t *)&addrlen)) < 0)
        {
            perror("accept failed");
            exit(EXIT_FAILURE);
        }

        while (1) {
            // receive message
            char buffer[RECV_BUFFER_SIZE];
            int recv_bytes = recv(sock, buffer, RECV_BUFFER_SIZE, 0);
            if (recv_bytes == 0)
            {
                fflush(stdout);
                break;
            }
            fwrite(buffer, recv_bytes, 1, stdout);

            // ECO: respond
            memset(&msg, 0, sizeof(msg));//clear the buffer
            strcpy(msg, "image content");
            send(sock, (char*)&msg, strlen(msg), 0);
        }
    }

    return 0;
}


int main(int argc, char **argv) {
    char *server_port;

    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./server-c [server port]\n");
        exit(EXIT_FAILURE);
    }

    server_port = argv[1];
    return server(server_port);
}
*/

// this works above


#include "create_tcp_server.h"

int main()
{
    bool debug = true;
    int queueLength = 10;
    int recvBufferSize = 2048;
    char *server_port = (char*)("5453");
    TcpServer tcpServer;

    //tcpServer.create(server_port);
    //tcpServer.server();

    bool succ = tcpServer.create(queueLength, recvBufferSize, server_port, debug);
    if(succ==false)
    {
        return 1;
    }

    while(1) // keep the server alive for further client reauest
    {
        succ = tcpServer.wait_to_receive();
        if(succ==false)
        {
            return 1;
        }
    }
    return 0;
}