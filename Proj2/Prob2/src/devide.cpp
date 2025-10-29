#include <iostream>
#include <cstring>
#include "inf_int.h"

using namespace std;

inf_int operator/(const inf_int& a, const inf_int& b) {

    // ��, ���� ����� ���� inf_int
    inf_int quotient;   
    inf_int compare1;
    inf_int compare2;

    // ���������� ���� ������ �� ���� ���� �� ���� ó��
    compare1.operator=(a);   
    compare1.thesign = true;
    compare2.operator=(b);
    compare2.thesign = true;

    // ������ ���� ũ�ų� ���ٸ� Ư�� ���̽� ó��
    if (operator<(compare1, compare2)) { 
        strcpy(quotient.digits,"0");
        quotient.length = 1;
    }
    else if (operator==(compare1, compare2)) {
        strcpy(quotient.digits, "1");
        quotient.length = 1;
    }
    // ���������� ���� �� ū ���
    else {    

        // ������ ���� ��� ���鼭 �� 1�� ���� inf_int
        inf_int one;
        strcpy(one.digits, "1");
        one.length = 1;
        one.thesign = true;

        // quotient �ʱⰪ ����
        strcpy(quotient.digits, "0");
        quotient.length = 1;

        // ��� ������ �������� ������ ������ �۾��� ������ �� +1 / �׋� ���� �۾��� ���� ������
        while (!operator<(compare1, compare2)) {
            compare1.operator=(operator-(compare1,compare2));
            quotient.operator=(operator+(quotient, one));
        }

    }

    // �� �������� ���� �� ����
    // ������ ���� ���������� �� ��ȣ�� ���� �� ��ȣ ����
    quotient.length = strlen(quotient.digits);
    quotient.thesign = (a.thesign == b.thesign) ? true : false;

    return quotient;
}

inf_int operator%(const inf_int& a, const inf_int& b) {

    // ������, ���� ����� ���� inf_int
    inf_int remainder;
    inf_int compare1;
    inf_int compare2;

    // ���������� ���� ������ �� ���� ���� �� ���� ó��
    compare1.operator=(a);
    compare1.thesign = true;
    compare2.operator=(b);
    compare2.thesign = true;

    // ������ ���� ũ�ų� ���ٸ� Ư�� ���̽� ó��
    if (operator<(compare1, compare2)) {
        remainder.operator=(compare1);
    }
    else if (operator==(compare1, compare2)) {
        strcpy(remainder.digits, "0");
        remainder.length = 1;
    }
    // ���������� ���� �� ū ���
    else {

        // ������ ������ �۾��� ������ ��� ������ ������ ���ϱ�
        while (!operator<(compare1, compare2)) {
            compare1.operator=(operator-(compare1, compare2));
        }
        remainder.operator=(compare1);

    }

    // ������ ��ȣ�� ���������� �� ��ȣ�� ���󰣴�
    remainder.thesign = a.thesign;

    return remainder;
}




