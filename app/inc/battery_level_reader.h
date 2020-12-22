#pragma once

class BatteryLevelReader {
public:
    BatteryLevelReader() = default;
    ~BatteryLevelReader() = default;

    int readLevel();
};