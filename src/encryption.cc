#include "encryption.h"

uint8_t EncryptionCls::encry_algorithm(uint8_t val) {
    uint8_t nval = 0;
    for(int8_t i = 0; i < 8; ++i) {
        if(val & 0x1<<i) {
            nval |= 0x1<<(7-i);
        } 
    }
    
    nval = ((nval&0x0f)<<4) + ((nval&0xf0)>>4);
    return nval;
}

uint8_t EncryptionCls::decipher_algorithm(uint8_t val) {
    uint8_t nval = 0;
    for(int8_t i = 0; i < 8; ++i) {
        if(val & 0x1<<i) {
            nval |= 0x1<<(7-i);
        }
    } 
    nval = ((nval&0x0f)<<4) + ((nval&0xf0)>>4);
    return nval;

}

void EncryptionCls::test(void) {

    uint8_t val = 10;
    uint8_t eval = encry_algorithm(val);
    uint8_t dval = decipher_algorithm(eval);
    std::cout<<"encry_algorithm("<<val<<")="<<int(eval);
    std::cout<<std::endl;

    std::cout<<"decipher_algorithm("<<eval<<")="<<int(dval);
    std::cout<<std::endl;
}


int EncryptionCls::encry(void) {
    if(access(filename, R_OK) == -1) {
        perror("access fail");
        return -1;
    }

    struct stat st;
    if(stat(filename, &st) == -1) {
        perror("stat fail");
        return -1;
    }

    int32_t len = st.st_size;
    // std::cout<<filename<<" size "<<len<<std::endl;

    int fd = open(filename, O_RDONLY);
    if(fd == -1) {
        perror("open fail");
        return -1;
    }
    
    char encry_filename[4096] = {"\0"}; 
    snprintf(encry_filename, 4096, "%s.enc", filename);
    
    int nfd = open(encry_filename, O_WRONLY|O_CREAT, S_IRUSR|S_IWUSR);
    if(nfd == -1) {
        perror("open fail");
        return -1;
    }
    
    uint8_t c = 0;
    while(read(fd, (void *)&c, 1) != 0) {
        uint8_t nval = encry_algorithm(c);
        if(write(nfd, (void *)&nval, 1) == -1) {
            perror("write fail");
            return -1;
        }
    }

    return 0;
}

int EncryptionCls::decipher(void) {
    if(strstr(filename, ".enc") == NULL) {
        perror("filename error");
        return -1;
    }
    
    int fd = open(filename, O_RDONLY);
    if(fd == -1) {
        perror("open fail");
        return -1;
    }
    
    char nfilename[1024] = {"\0"};
    strncpy(nfilename, filename, strlen(filename)-4);
    int nfd = open(nfilename, O_WRONLY|O_CREAT, S_IRUSR|S_IWUSR);
    if(nfd == -1) {
        perror("open fail");
        return -1;
    }
    
    uint8_t c = 0;
    while(read(fd, (void *)&c, 1) != 0) {
        uint8_t nval = decipher_algorithm(c);
        if(write(nfd, (void *)&nval, 1) == -1) {
            perror("write fail");
            return -1;
        } 
    }
    return 0;
}

void usage(const char *name) {
    std::cout<<name<<" [d|e] [filename [filename [filename [...]]]]"<<std::endl;        
    std::cout<<std::flush; 
    exit(-1);
}

int main(int argc, char **argv) {
    if(argc == 1) {
        usage(argv[0]);
    }   
    
    const char *op = argv[1];
    if(strcmp(op, "d") == 0) {
        for(int i = 2; i < argc; ++i) {
            EncryptionCls inst(argv[i]);
            inst.decipher();
        }
    } 
    else if(strcmp(op, "e") == 0) {
        for(int i = 2; i < argc; ++i) {
            EncryptionCls inst(argv[i]);
            inst.encry();
        }
    }
    else {
        usage(argv[0]);
    }
    // EncryptionCls inst("/home/charlie/encryption/src/encryption.cc");
    // inst.test();
    // inst.encry();
    
    // EncryptionCls inst2("/home/charlie/encryption/src/encryption.cc.enc");
    // inst2.decipher();
    return 0;
}
