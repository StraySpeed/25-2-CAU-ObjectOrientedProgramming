#include <application.h>
#include <iostream>
#include <string>


Application::Application() {
    isExit = false;
}

void Application::mainloop() {
    print_title();
    string input = "";
    int selectValue = -1;
    while (!isExit) {
        print_main_menu();
        while (true) {
            try {
                getline(cin, input);
                selectValue = stoi(input);
                break;
            }
            catch (const invalid_argument &e) {
                cout << endl << "Invalid selection." << endl;
            }
        }

        switch (selectValue) {
            case 1:
                print_calculate_menu();
                break;
            case 2:
                print_prev_value();
                break;
            case 0:
                cout << "Exit program." << endl;
                isExit = true;
                break;
            default:
                cout << endl << "Invalid selection." << endl;
                break;
        }
    }
}

/*
Print title(ASCII art)
*/
void Application::print_title() {
    string title[8];
    title[0] = "  _____        __ _____       _      _____      _            _       _             ";
    title[1] = " |_   _|      / _|_   _|     | |    / ____|    | |          | |     | |            ";
    title[2] = "   | |  _ __ | |_  | |  _ __ | |_  | |     __ _| | ___ _   _| | __ _| |_ ___  _ __ ";
    title[3] = "   | | | '_ \\|  _| | | | '_ \\| __| | |    / _` | |/ __| | | | |/ _` | __/ _ \\| '__|";
    title[4] = "  _| |_| | | | |  _| |_| | | | |_  | |___| (_| | | (__| |_| | | (_| | || (_) | |   ";
    title[5] = " |_____|_| |_|_| |_____|_| |_|\\__|  \\_____\\__,_|_|\\___|\\__,_|_|\\__,_|\\__\\___/|_|   ";
    title[6] = "             ______                                                                ";
    title[7] = "            |______|                                                               ";                                                                                   
    for (int i = 0; i < 8; i++) {
        cout << title[i] << endl;
    }
    cout << endl;
}

void Application::print_main_menu() {
    cout << "inf_int Calculator. Select Options." << endl;
    cout << "0. Exit" << endl;
    cout << "1. Calculate" << endl;
    cout << "2. See Previous Value" << endl;
}

void Application::print_calculate_menu() {
    string input;
    cout << "Enter expressions. : ";
    getline(cin, input);
    // calculate
}

void Application::print_prev_value() {
    // getPrev();
    cout << "Previous Value is " << endl;
}