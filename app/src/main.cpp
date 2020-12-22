
#include <thread>
#include <mqtt_wrapper.h>
// #include <wiringPiI2C.h>
// #include <wiringPi.h>
// #include <iostream> // for debugging
// extern "C" {
//     #include <linux/i2c-dev.h>
//     #include <i2c/smbus.h>
// }
// #include <stdio.h>
// #include <string.h>
// #include <fcntl.h>
// #include <unistd.h>
// #include <linux/i2c-dev.h>
// #include <sys/ioctl.h>

// typedef unsigned char   u8;

// int i2c_fd = -1; 
// const char *i2c_fname = "/dev/i2c-1";


// int i2c_init(void) {
//     if ((i2c_fd = open(i2c_fname, O_RDWR)) < 0) {
//         char err[200];
//         sprintf(err, "open('%s') in i2c_init", i2c_fname);
//         perror(err);
//         return -1;
//     }
//     return i2c_fd;
// }

// void i2c_close(void) {
//     close(i2c_fd);
// }

// int i2c_write(uint8_t slave_addr, uint8_t* ptr_data, uint8_t len) {

//     int error = write(i2c_fd, ptr_data, len);
//     printf("error code =%d \n", error);

//     return 0;
// }

// // Read the given I2C slave device's register and return the read value in `*result`:
// int i2c_read(u8 slave_addr, u8 reg, u8 *result) {
//     int retval;
//     u8 outbuf[1], inbuf[1];
//     struct i2c_msg msgs[2];
//     struct i2c_rdwr_ioctl_data msgset[1];

//     msgs[0].addr = slave_addr;
//     msgs[0].flags = 0;
//     msgs[0].len = 1;
//     msgs[0].buf = outbuf;

//     msgs[1].addr = slave_addr;
//     msgs[1].flags = I2C_M_RD | I2C_M_NOSTART;
//     msgs[1].len = 1;
//     msgs[1].buf = inbuf;

//     msgset[0].msgs = msgs;
//     msgset[0].nmsgs = 2;

//     outbuf[0] = reg;

//     inbuf[0] = 0;

//     *result = 0;
//     if (ioctl(i2c_fd, I2C_RDWR, &msgset) < 0) {
//         perror("ioctl(I2C_RDWR) in i2c_read");
//         return -1;
//     }

//     *result = inbuf[0];
    
//     return 0;
// }

#include <i2c_handler.h>
#include <BME280.h>
#include <INA219.h>
#include <CCS811.h>
#include <HDC2010.h>

int main(int argc, char *argv[])
{    
    // MqttWrapper mqttWrapper;
    // const char* message1 = "hello1";
    // const char* message2 = "hello2";
    // const std::string message3 = "hello1";
    // const std::string message4 = "hello2";
    // mqttWrapper.Publisher(message1, message3);
    // mqttWrapper.Publisher(message2, message4);

    I2CHandler i2CHandler;


    return 0;
}

