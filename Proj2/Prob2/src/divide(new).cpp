#include <iostream>
#include <cstring>
#include "inf_int.h"

using namespace std;


// 새롭게 구현한 몫과 나눗셈

inf_int operator/(const inf_int& a, const inf_int& b) {

    // b가 0이면 오류 출력? 어떻게 해야할까?

    // 몫, 절댓값 계산을 위한 inf_int
    inf_int quotient;
    inf_int compare1(a);
    inf_int compare2(b);
    compare1.thesign = true;
    compare2.thesign = true;

    // 나누는 수가 크거나 같다면 특이 케이스 처리
    if (operator<(compare1, compare2)) {
        strcpy(quotient.digits, "0");
        quotient.length = 1;
    }
    else if (operator==(compare1, compare2)) {
        strcpy(quotient.digits, "1");
        quotient.length = 1;
    }
    // 나누어지는 수가 더 큰 경우
    else {

        // inf_int형 10과 1, 자리수 차이에 의한 계산 시작점
        inf_int ten(10);
        inf_int one(1);

        int exp = compare1.length - compare2.length;

        for (int i = exp; i >= 0; i--) {
            // inf_int형 지수, compare1에서 num*sub 빼기
            inf_int exponent(i);
            inf_int num(0);
            inf_int sub = operator*(compare2, pow(ten, exponent));

            // 몫의 한자리 씩 구하기
            inf_int temp; 
            while (true) {
                temp = operator*(operator+(num, one), sub);
                if (operator>(temp, compare1)) {
                    break; // (num+1)*sub 가 compare1보다 커지면 멈춤
                }
                num = operator+(num, one);
            }

            if (operator>(num, inf_int(0))) {
                compare1 = operator-(compare1, operator*(num, sub));
                quotient = operator+(quotient, operator*(num, pow(ten, exponent)));
            }
            else{
                continue; 
            }
            // 점점 빼다가 compare1이 나누는 수보다 작아지면 그 수가 나머지
            if (operator<(compare1, compare2)) {
                break;
            }
        }
    }
    // 몫 부호 결정 및 길이 설정
    if (a.thesign == b.thesign) {
        quotient.thesign = true;
    }
    else {
        quotient.thesign = false;
    }
    
    quotient.length = strlen(quotient.digits);
    return quotient;
}



inf_int operator%(const inf_int& a, const inf_int& b) {

    // 나머지, 몫에 대한 inf_int
    inf_int store = operator/(a, b);
    inf_int remainder = operator-(a, operator*(b, store));

    // 나머지 부호는 나누어지는 수 부호를 따라간다.
    remainder.length = strlen(remainder.digits);
    remainder.thesign = a.thesign;

    return remainder;
}
