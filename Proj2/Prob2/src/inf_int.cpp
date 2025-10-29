#include "inf_int.h"
#include <string>
#include <iostream>
#include <cstring>
#include <algorithm>

inf_int::inf_int() {
    inf_int::digits = new char[2];
    inf_int::digits[0] = '0';
    inf_int::digits[1] = '\0';    
    inf_int::length = strlen(inf_int::digits);
    inf_int::thesign = true;
}

inf_int::inf_int(int value) {
    std::string t = std::to_string(value);
    // 부호 음수면 부호 제거하고 sign을 false로
    if (t.substr(0, 1) == "-") {
        inf_int::thesign = false;
        t = t.substr(1);
    }
    else {
        inf_int::thesign = true;
    }
    std::reverse(t.begin(), t.end());
    inf_int::digits = new char[t.length() + 1];
    strcpy(inf_int::digits, t.c_str());
    inf_int::digits[t.length()] = '\0';
    inf_int::length = strlen(inf_int::digits);
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
void inf_int::Add(const char num, const unsigned int index) {
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


inf_int& inf_int::operator=(const inf_int& a)
{
    if (this->digits) {
        delete this->digits;		// 이미 문자열이 있을 경우 제거.
    }
    this->digits = new char[a.length + 1];

    for (unsigned int i = 0; i < a.length; i++)
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
	for (unsigned int i = 0; i < a.length; i++)
	{
		if (a.digits[i] > b.digits[i]) res = 1;
		else if (a.digits[i] == b.digits[i]) res = 0;
		else res = -1;
	}
	return res;
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
			for (i = 0; i < b.length; i++)
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

void inf_int::SUB(const char num, const unsigned int index)
{
	if (this->digits[index] >= num)
		this->digits[index] = this->digits[index] - num + '0';
	else
	{
		this->digits[index] = this->digits[index] - num + 10 + '0';
		// 빼지는 수가 더 큰 상황에서 내림
		int i = 1;
		for (unsigned i = 1; i < this->length; i++)
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