#pragma once
#include <iostream>

using namespace std;

class Application {
    private:
        bool isExit;
        void print_title();
        void print_main_menu();
        void print_calculate_menu();
        void print_prev_value();

    public:
        void mainloop();
        Application();
};