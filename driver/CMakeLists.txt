add_library(driver
            src/i2c_handler.cpp
            inc/i2c_handler.h
            inc/CCS811.h
            src/CCS811.cpp
            inc/HDC2010.h
            src/HDC2010.cpp
            inc/BME280.h
            inc/BME280_defs.h
            src/BME280.cpp
            inc/INA219.h
            src/INA219.cpp
           )

target_include_directories(driver PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/../driver/inc")