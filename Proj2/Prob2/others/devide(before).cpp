#include <iostream>
#include <cstring>
#include "inf_int.h"

using namespace std;

inf_int operator/(const inf_int& a, const inf_int& b) {

    // 몫, 절댓값 계산을 위한 inf_int
    inf_int quotient;   
    inf_int compare1;
    inf_int compare2;

    // 나누어지는 수와 나누는 수 대입 연산 후 절댓값 처리
    compare1.operator=(a);   
    compare1.thesign = true;
    compare2.operator=(b);
    compare2.thesign = true;

    // 나누는 수가 크거나 같다면 특이 케이스 처리
    if (strcmp(compare1.digits, compare2.digits) < 0) { 
        strcpy(quotient.digits,"0");
        quotient.length = 1;
    }
    else if (strcmp(compare1.digits, compare2.digits) == 0) {
        strcpy(quotient.digits, "1");
        quotient.length = 1;
    }
    // 나누어지는 수가 더 큰 경우
    else {    

        // 나누는 수로 계속 빼면서 몫에 1을 더할 inf_int
        inf_int one;
        strcpy(one.digits, "1");
        one.length = 1;
        one.thesign = true;

        // quotient 초기값 설정
        strcpy(quotient.digits, "0");
        quotient.length = 1;

        // 계속 빼가며 언젠가는 나누는 수보다 작아질 때까지 몫 +1 / 그떄 생긴 작아진 수는 나머지
        while (strcmp(compare1.digits, compare2.digits) >= 0) {
            compare1.operator=(operator-(compare1,compare2));
            quotient.operator=(operator+(quotient, one));
        }

    }

    // 위 연산으로 계산된 몫 길이
    // 나누는 수와 나누어지는 수 부호에 따라 몫 부호 결정
    quotient.length = strlen(quotient.digits);
    quotient.thesign = (a.thesign == b.thesign) ? true : false;

    return quotient;
}

inf_int operator%(const inf_int& a, const inf_int& b) {

    // 나머지, 절댓값 계산을 위한 inf_int
    inf_int remainder;
    inf_int compare1;
    inf_int compare2;

    // 나누어지는 수와 나누는 수 대입 연산 후 절댓값 처리
    compare1.operator=(a);
    compare1.thesign = true;
    compare2.operator=(b);
    compare2.thesign = true;

    // 나누는 수가 크거나 같다면 특이 케이스 처리
    if (strcmp(compare1.digits, compare2.digits) < 0) {
        remainder.operator=(compare1);
    }
    else if (strcmp(compare1.digits, compare2.digits) == 0) {
        strcpy(remainder.digits, "0");
        remainder.length = 1;
    }
    // 나누어지는 수가 더 큰 경우
    else {

        // 나누는 수보다 작아질 때까지 계속 빼가며 나머지 구하기
        while (strcmp(compare1.digits, compare2.digits) >= 0) {
            compare1.operator=(operator-(compare1, compare2));
        }
        remainder.operator=(compare1);

    }

    // 나머지 부호는 나누어지는 수 부호를 따라간다
    remainder.thesign = a.thesign;

    return remainder;
}



inf_int operator-(const inf_int&, const inf_int&) {
    // 구현된 내용 필요
}

inf_int operator+(const inf_int&, const inf_int&) {
    // 구현된 내용 필요
}

inf_int& inf_int::operator=(const inf_int&) {
    // 구현된 내용 필요
}

