#include "inf_int.h"
#include <string>
#include <iostream>
#include <cstring>


inf_int::inf_int() {
    inf_int::digits = new char[2];
    inf_int::digits[0] = '0';
    inf_int::digits[1] = '\0';    
    inf_int::length = strlen(inf_int::digits) - 1;
    inf_int::thesign = true;
}

inf_int::inf_int(int value) {
    std::string t = std::to_string(value);
    inf_int::digits = new char[t.length() + 1];
    strcpy(inf_int::digits, t.c_str());
    inf_int::digits[t.length()] = '\0';
    inf_int::length = strlen(inf_int::digits) - 1;
    inf_int::thesign = true;
}

inf_int::inf_int(const char* value) {
    // 부호가 음수일 때
    if (value[0] == '-') {
        inf_int::length = strlen(value) - 1;
        inf_int::thesign = false;
        inf_int::digits = new char[inf_int::length];
        strcpy(inf_int::digits, value+1);
    }
    // 부호가 양수일 때
    else {
        inf_int::length = strlen(value);
        inf_int::thesign = true;
        inf_int::digits = new char[inf_int::length];
        strcpy(inf_int::digits, value);
    }
}

inf_int::inf_int(const inf_int& value) {
    inf_int::length = value.length;
    inf_int::thesign = value.thesign;
    inf_int::digits = new char[inf_int::length + 1];
    strcpy(inf_int::digits, value.digits);
}

inf_int::~inf_int() {
    delete[] inf_int::digits;
}


// 
// to be filled by students
//
// example :
//
// bool operator==(const inf_int& a , const inf_int& b)
// {
//     // we assume 0 is always positive.
//     if ( (strcmp(a.digits , b.digits)==0) && a.thesign==b.thesign )
//         return true;
//     return false;
// }
//
