#pragma once
#ifndef _INF_INT_H_
#define _INF_INT_H_
#include <iostream>

using namespace std;

class inf_int
{
private:
    char* digits;  
    unsigned int length;
    bool thesign;  
   
public:
    inf_int();               
    inf_int(int);
    inf_int(const char*);
    inf_int(const inf_int&); 
    ~inf_int();
    inf_int& operator=(const inf_int&); 

    friend bool operator==(const inf_int&, const inf_int&);
    friend bool operator!=(const inf_int&, const inf_int&);
    friend bool operator>(const inf_int&, const inf_int&);
    friend bool operator<(const inf_int&, const inf_int&);

    friend inf_int operator+(const inf_int&, const inf_int&);
    friend inf_int operator-(const inf_int&, const inf_int&);
    friend inf_int operator*(const inf_int&, const inf_int&);
    friend inf_int operator/(const inf_int&, const inf_int&);
    friend inf_int operator%(const inf_int&, const inf_int&);

    friend ostream& operator<<(ostream&, const inf_int&);
   
};

#endif