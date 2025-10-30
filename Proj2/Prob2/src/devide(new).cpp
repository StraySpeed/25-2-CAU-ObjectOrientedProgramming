#include <iostream>
#include <cstring>
#include "inf_int.h"

using namespace std;


// ���Ӱ� ������ ��� ������

inf_int operator/(const inf_int& a, const inf_int& b) {

    // b�� 0�̸� ���� ���? ��� �ؾ��ұ�?

    // ��, ���� ����� ���� inf_int
    inf_int quotient;
    inf_int compare1(a);
    inf_int compare2(b);
    compare1.thesign = true;
    compare2.thesign = true;

    // ������ ���� ũ�ų� ���ٸ� Ư�� ���̽� ó��
    if (operator<(compare1, compare2)) {
        strcpy(quotient.digits, "0");
        quotient.length = 1;
    }
    else if (operator==(compare1, compare2)) {
        strcpy(quotient.digits, "1");
        quotient.length = 1;
    }
    // ���������� ���� �� ū ���
    else {

        // inf_int�� 10�� 1, �ڸ��� ���̿� ���� ��� ������
        inf_int ten(10);
        inf_int one(1);
        int exp = compare1.length - compare2.length;

        for (int i = exp; i >= 0; i--) {
            // inf_int�� ����, compare1���� num*sub ����
            inf_int exponent(i);
            inf_int num(0);
            inf_int sub = operator*(compare2, pow(ten, exponent));

            // ���� ���ڸ� �� ���ϱ�
            while (operator>(compare1, operator*(num, sub))) {
                num = operator+(num, one);
            }

            if (operator>(num, inf_int(0))) {
                num = operator-(num, one);
                if (operator>(num, inf_int(0))) {
                    compare1 = operator-(compare1, operator*(num, sub));
                    quotient = operator+(quotient, operator*(num, pow(ten, exponent)));
                }
            }
            else{
                continue; 
            }
            // ���� ���ٰ� compare1�� ������ ������ �۾����� �� ���� ������
            if (operator<(compare1, compare2)) {
                break;
            }
        }
    }
    // �� ��ȣ ���� �� ���� ����
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

    // ������, �� ���� inf_int
    inf_int store = operator/(a, b);
    inf_int remainder = operator-(a, operator*(b, store));

    // ������ ��ȣ�� ���������� �� ��ȣ�� ���󰣴�.
    remainder.length = strlen(remainder.digits);
    remainder.thesign = a.thesign;

    return remainder;
}
