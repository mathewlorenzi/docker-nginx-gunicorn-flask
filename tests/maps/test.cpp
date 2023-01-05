// https://stackoverflow.com/questions/49103709/how-to-use-shared-memory-in-python-and-c-c

#include <sys/mman.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

// 16h57mn03mn123ms
// 9 digits
// 9*10 = 90

int test_org()
{
    // assume file exists. the python script must be run first
    int fd = -1;
    if ((fd = open("pods.txt", O_RDWR, 0)) == -1)
    {
        printf("unable to open pods.txt\n");
        return 0;
    }
    // open the file in shared memory
    char* shared = (char*) mmap(NULL, 8, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);

    // periodically read the file contents
    while (true)
    {
        printf("0x%02X 0x%02X 0x%02X 0x%02X 0x%02X 0x%02X 0x%02X 0x%02X\n", shared[0], shared[1], shared[2], shared[3], shared[4], shared[5], shared[6], shared[7]);
        sleep(1);
    }

   return 0;
}

int test1()
{
    // assume file exists. the python script must be run first
    int fd = -1;
    if ((fd = open("pods.txt", O_RDWR, 0)) == -1)
    {
        printf("unable to open pods.txt\n");
        return 0;
    }
    // open the file in shared memory
    char* shared = (char*) mmap(NULL, 9, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);

    // periodically read the file contents
    while (true)
    {
        for(int i=0; i<9; i++){
            printf("0x%02X ", shared[i]);
        }
        printf("\n");
        for(int i=0; i<9; i++){
            printf("%d ", int(shared[i]));
        }
        printf("\n");        
        sleep(1);
    }

   return 0;
}

int main(void)
{
    // return test_org();
    return test1();
}

