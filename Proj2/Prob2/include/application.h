#pragma once
#include <iostream>
#include "calculator.h"

using namespace std;

class Application {
    private:
        bool isExit;
        Calculator calculator;
        void print_title();
        void print_main_menu();
        void print_calculate_menu();
        void print_prev_value();

    public:
        void mainloop();
        Application();
};