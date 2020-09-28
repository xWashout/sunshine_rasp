add_executable(app
	       src/main.cpp
	       )
target_link_libraries(app PRIVATE mqtt paho-mqttpp3)
target_include_directories(app PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/inc")
