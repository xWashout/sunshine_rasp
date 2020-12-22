#pragma once

#include <cstdint>

class I2CHandler {
  public:
    I2CHandler();
    ~I2CHandler();
    int writeData(uint8_t slave_addr, uint8_t* ptr_data, uint8_t len);
    int readData(uint8_t slave_addr, uint8_t* ptr_data, uint8_t len);

  private:
    int i2c_fd = -1;
    const char *i2c_fname = "/dev/i2c-1";
};