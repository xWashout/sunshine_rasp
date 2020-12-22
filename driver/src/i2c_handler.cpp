#include <inc/i2c_handler.h>
#include <cstdint>
#include <linux/i2c-dev.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>

I2CHandler::I2CHandler() {
    if ((i2c_fd = open(i2c_fname, O_RDWR)) < 0) {
        char err[200];
        sprintf(err, "open('%s') in i2c_init\n", i2c_fname);
        perror(err);
    }
    printf("I2C init complete\n");
}

I2CHandler::~I2CHandler() {
    close(i2c_fd);
}

int I2CHandler::writeData(uint8_t slave_addr, uint8_t* ptr_data, uint8_t len) {
    int retVal = write(i2c_fd, ptr_data, len);
    printf("I2C write() return value =%d \n", retVal);
    return retVal;
}

int I2CHandler::readData(uint8_t slave_addr, uint8_t* ptr_data, uint8_t len) {
    int retVal = read(i2c_fd, ptr_data, len);
    printf("I2C read() return value =%d \n", retVal);
    return retVal;
}
