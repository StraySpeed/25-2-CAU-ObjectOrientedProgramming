#ifndef _INF_INT_H_
#define _INF_INT_H_

#include <iostream>

using namespace std;

class inf_int
{
private :
    char* digits;  // You may modify this to "string digits;" if you want.
    unsigned int length;
    bool thesign;   // true if positive , false if negative.
    // ex) 15311111111111111 -> digits="11111111111111351", length=17, thesign=true;
    // ex) -12345555555555 -> digits="55555555554321", length=14, thesign=false
    // you may insert additional private members here.

public :
    inf_int();               // assign 0 as a default value
    inf_int(int);
    inf_int(const char* );
    inf_int(const inf_int&); // copy constructor
    ~inf_int(); // destructor

    inf_int& operator=(const inf_int&); // assignment operator

    friend bool operator==(const inf_int& , const inf_int&);
    friend bool operator!=(const inf_int& , const inf_int&);
    friend bool operator>(const inf_int& , const inf_int&);
    friend bool operator<(const inf_int& , const inf_int&);
    friend bool operator>=(const inf_int& , const inf_int&);
    friend bool operator<=(const inf_int& , const inf_int&);
    friend int absCompare(const inf_int& a, const inf_int& b); // 절댓값 비교

    // 더하기, 빼기 연산자
    friend inf_int operator+(const inf_int& , const inf_int&);
    friend inf_int operator-(const inf_int& , const inf_int&);
    void Add(const char num, const unsigned int index);
    void SUB(const char num, const unsigned int index);

    // 곱하기, pow 연산자
    friend inf_int operator*(const inf_int& , const inf_int&);

    // 나누기, 나머지 연산자
    friend inf_int operator/(const inf_int& , const inf_int&);
    friend inf_int operator%(const inf_int& , const inf_int&);

    // 출력
    friend ostream& operator<<(ostream& , const inf_int&);
    // friend istream& operator>>(istream& , inf_int&);    // not required

    // pow시 사용하는 함수
    friend bool is_zero(const inf_int& e); // 지수가 0인지 체크
    friend bool is_even(const inf_int& e); // 지수가 짝수인지 체크
    friend void div2(inf_int& e);          // 지수를 2로 나누는 함수
    friend inf_int pow(const inf_int& base, const inf_int& exp); // 거듭제곱 함수
};

// 제곱근
inf_int sqrt(const inf_int&);
#endif