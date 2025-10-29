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



inf_int& inf_int::operator=(const inf_int& a)
{
    if (this->digits) {
        delete this->digits;		// 이미 문자열이 있을 경우 제거.
    }
    this->digits = new char[a.length + 1];

    for (int i = 0; i < a.length; i++)
        this->digits[i] = a.digits[i];
    this->length = a.length;
    this->thesign = a.thesign;
    this->digits[this->length] = '\0';

    return *this;
}

bool operator==(const inf_int& a, const inf_int& b)
{
    // we assume 0 is always positive.
    if ((strcmp(a.digits, b.digits) == 0) && a.thesign == b.thesign)	// 부호가 같고, 절댓값이 일치해야함.
        return true;
    return false;
}

bool operator!=(const inf_int& a, const inf_int& b)
{
	return !operator==(a, b);
}

bool operator>(const inf_int& a, const inf_int& b)
{
	if (a.thesign != b.thesign) return a.thesign;
	else
	{
		bool res = true;
		if (a.length > b.length) res = true;
		else if (a.length < b.length) res = false;
		else if (absCompare(a, b) > 0) res = true;
		else res = false;

		if (a.thesign) return res;// a의 부호가 양수 == 둘 다 양수
		else return !res;
	}
}

bool operator<(const inf_int& a, const inf_int& b)
{
	if (operator>(a, b) || operator==(a, b)) {
		return false;
	}
	else {
		return true;
	}
}

int absCompare(const inf_int& a, const inf_int& b) // a가 크면 true 아니면 false
{
	int res = 0;
	if (a.length > b.length) res = 1; 
	else if (a.length < b.length) res = -1;
	else
	{
		for (int i = 0; i < a.length; i++)
		{
			if (a.digits[i] > b.digits[i]) res = 1;
			else if (a.digits[i] == b.digits[i]) res = 0;
			else res = -1;
		}
	}
	return res;
}

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

inf_int operator-(const inf_int& a, const inf_int& b)
{
	inf_int c;
	unsigned int i;

	if (a.thesign == b.thesign) {	// 이항의 부호가 같을 경우 + 연산자로 연산
		if (absCompare(a, b) == 0) c = 0;
		else if (absCompare(a, b) == 1)
		{
			c = a;
			for (i = 0; i < b.length; i++)
			{
				c.SUB(b.digits[i], i);
			}
			c.thesign = a.thesign;
		}
		else
		{
			c = b;
			for (i = 0; i < a.length; i++) // b.length로 되어 있어서 오류
			{
				c.SUB(a.digits[i], i);
			}
			c.thesign = !(a.thesign);
		}
		return c;
	}
	else {	// 이항의 부호가 다를 경우  연산자로 연산
		c = b;
		c.thesign = a.thesign;

		return a + c;
	}
}

//inf_int operator*(const inf_int& a, const inf_int& b)
//{
	// to be filled
//}


ostream& operator<<(ostream& out, const inf_int& a)
{
	int i;

	if (a.thesign == false) {
		out << '-';
	}
	for (i = a.length - 1; i >= 0; i--) {
		out << a.digits[i];
	}
	return out;
}

void inf_int::Add(const char num, const unsigned int index)	// a의 index 자리수에 n을 더한다. 0<=n<=9, ex) a가 391일때, Add(a, 2, 2)의 결과는 411
{
	if (this->length < index) {
		this->digits = (char*)realloc(this->digits, index + 1);

		if (this->digits == NULL) {		// 할당 실패 예외처리
			cout << "Memory reallocation failed, the program will terminate." << endl;

			exit(0);
		}

		this->length = index;					// 길이 지정
		this->digits[this->length] = '\0';	// 널문자 삽입
	}

	if (this->digits[index - 1] < '0') {	// 연산 전에 '0'보다 작은 아스키값인 경우 0으로 채움. 쓰여지지 않았던 새로운 자리수일 경우 발생
		this->digits[index - 1] = '0';
	}

	this->digits[index - 1] += num - '0';	// 값 연산


	if (this->digits[index - 1] > '9') {	// 자리올림이 발생할 경우
		this->digits[index - 1] -= 10;	// 현재 자릿수에서 (아스키값) 10을 빼고
		Add('1', index + 1);			// 윗자리에 1을 더한다
	}
}

void inf_int::SUB(const char num, const unsigned int index)
{
	if (this->digits[index] >= num)
		this->digits[index] = this->digits[index] - num + '0';
	else
	{
		this->digits[index] = this->digits[index] - num + 10 + '0';
		// 빼지는 수가 더 큰 상황에서 내림
		int i = 1;
		for (i = 1; i < this->length; i++)
		{
			if (this->digits[index + i] != '0') break;
			this->digits[index + i] = '9';
		}
		this->digits[index + i] = this->digits[index + i] - 1;

		// 자릿수가 줄어드는 상황
		if (this->digits[index + i] == '0')
		{
			this->length = this->length - 1;
			inf_int temp = *this;
			*this = temp;
		}
	}
}