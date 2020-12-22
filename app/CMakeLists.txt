add_executable(app
	       src/main.cpp
		   )
		   
# add_library(batteryReader
# 		    src/battery_level_reader.cpp
# 			inc/battery_level_reader.h
# 		   )

target_link_libraries(app PRIVATE mqtt driver paho-mqttpp3 i2c wiringPi)
target_include_directories(app PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/inc")