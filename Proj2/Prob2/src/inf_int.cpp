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

// 기존 코드 : 1234 입력시 1234로 저장
// 수정 코드 : 1234 입력시 4321로 저장
inf_int::inf_int(const char* s) {
    thesign = true;
    if (*s == '-') {
        thesign = false;
        ++s;
    }
    // 선행0 제거    ex) 0000123 -> 123
    while (*s == '0' && *(s + 1) != '\0') {
        ++s;
    }
    length = (unsigned)std::strlen(s);
    digits = new char[length + 1];
    for (unsigned i = 0; i < length; ++i) {   // 역순복사
        digits[i] = s[length - 1 - i];
    }
    digits[length] = '\0';
    if (length == 1 && digits[0] == '0') {
        thesign = true; // 0은양수
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

// 교수님 Add 함수
inf_int::Add(const char num, const unsigned int index) {
    if (length < index) {
        unsigned newLen = index;
        char* nd = new char[newLen + 1];
        for (unsigned i = 0; i < length; ++i) {
            nd[i] = digits[i];
        }
        for (unsigned i = length; i < newLen; ++i) {
            nd[i] = '0';
        }
        nd[newLen] = '\0';
        delete[] digits; digits = nd; length = newLen;
    }
    if (digits[index - 1] < '0') {
        digits[index - 1] = '0';
    }
    digits[index - 1] += (num - '0');
    if (digits[index - 1] > '9') {
        digits[index - 1] -= 10;
        Add('1', index + 1);
    }
}

// 교수님 operator+ 함수
inf_int operator+(const inf_int& a, const inf_int& b)
{
    inf_int c;
    unsigned int i;

    if (a.thesign == b.thesign) {	// 이항의 부호가 같을 경우 + 연산자로 연산
        for (i = 0; i < a.length; i++) {
            c.Add(a.digits[i], i + 1);
        }
        for (i = 0; i < b.length; i++) {
            c.Add(b.digits[i], i + 1);
        }

        c.thesign = a.thesign;

        return c;
    }
    else {	// 이항의 부호가 다를 경우 - 연산자로 연산
        c = b;
        c.thesign = a.thesign;

        return a - c;
    }
}

// operator*
inf_int operator*(const inf_int& a, const inf_int& b)
{
    
    // 0입력시 결과가 0으로 return값 : 0
    if ((a.length == 1 && a.digits[0] == '0') ||
        (b.length == 1 && b.digits[0] == '0')) {
        return inf_int(0);
    }

    inf_int c;          // 0으로시작
    c.thesign = (a.thesign == b.thesign); // 부호 체크 (a,b 부호 같을시 true / 다를 시 false)

    for (unsigned int i = 0; i < a.length; ++i) {
        int ai = a.digits[i] - '0';
        for (unsigned int j = 0; j < b.length; ++j) {
            int bj = b.digits[j] - '0';
            int prod = ai * bj; // 0..81
            // a = 4321, b = 12345 저장되어 있을시
            // a[0] * b[0]
            // a[0] * b[1]
            // ... 이런식으로 작동
            // 우리가 평소 54321 * 1234할 때
            // 54321 * 4 
            // 54321 * 3
            // 54321 * 2
            // 54321 * 1 하는 형태의 곱셈

            // 일의자리
            c.Add(char('0' + (prod % 10)), i + j + 1);
            // 십의자리(캐리)
            if (prod >= 10) c.Add(char('0' + (prod / 10)), i + j + 2);
        }
    }

    // 상위0 제거 ex) 000013131 입력 받아졌을 경우
    while (c.length > 1 && c.digits[c.length - 1] == '0') {
        c.length--;
        c.digits[c.length] = '\0';
    }
    if (c.length == 1 && c.digits[0] == '0') {
        c.thesign = true;
    }

    return c;
}

// e가0인지
bool is_zero(const inf_int& e) {
    return (e.length == 1 && e.digits[0] == '0');
}

// e가짝수인지(역순저장: digits[0]이1의자리)
bool is_even(const inf_int& e) {
    int u = e.digits[0] - '0';
    return (u % 2) == 0;
}

// e = e / 2 (제자리나눗셈), 역순저장기준구현
void div2(inf_int& e) {
    int carry = 0;
    for (int i = (int)e.length - 1; i >= 0; --i) {
        int cur = (e.digits[i] - '0') + carry * 10; // 상위자리부터내려옴(역순의반대방향)
        int q = cur / 2;
        int r = cur % 2;
        e.digits[i] = char('0' + q);
        carry = r;
    }
    // 상위0 정리  ex) 000013131 입력 받아졌을 경우
    while (e.length > 1 && e.digits[e.length - 1] == '0') {
        e.length--;
        e.digits[e.length] = '\0';
    }
}

inf_int pow(inf_int base, inf_int exp) {
    // 0^0 = 1로정의
    if (is_zero(base) && is_zero(exp)) {
        return inf_int(1);
    }

    inf_int result(1);

    // 음수지수는지원하지않음
    if (exp.thesign == false) {
        return inf_int(0);
    }

    while (is_zero(exp) == false) { // 지수가 0이 아닐 경우에만 작동
        if (!is_even(exp)) {          // exp의최하위비트가1이면
            result = result * base;   // 곱하기
        }
        div2(exp);            // exp(지수)를 2로 나눔
        if (!is_zero(exp)) {
            base = base * base;       // base = base^2
        }
    }
    return result;
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
