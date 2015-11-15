/*************************************************************************
	> File Name: encryption.h
	> Author: charliezhao
	> Mail: 
	> Created Time: Fri 13 Nov 2015 11:48:35 PM PST
 ************************************************************************/

#ifndef _ENCRYPTION_H
#define _ENCRYPTION_H
#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#include <iostream>

class EncryptionCls {
public:
    EncryptionCls(const char *filename):filename(filename) {}
    
    ~EncryptionCls() {
        if(unlink(filename) == -1) {
            perror("unlink fail");
        }
    }
    
    int encry(void);
    int decipher(void);
    uint8_t encry_algorithm(uint8_t val);
    uint8_t decipher_algorithm(uint8_t val);
    
    void test(void);
private:
    const char *filename = NULL;
    const int32_t magicbegin = 0x20151112;
    const int32_t magicend = 0x11122015;
};

void usage(const char *name);


#endif
