#pragma once
#include <string>
class MqttWrapper
{
public:
    MqttWrapper() = default;
    ~MqttWrapper() = default;

    int Publisher(const char* PAYLOAD4, const std::string TOPIC);
};
