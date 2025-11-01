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
    if (a == inf_int(0) || b == inf_int(0)) {
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

inf_int pow(const inf_int& base, const inf_int& exp) {
    // 0^0 = 1로정의
    if (is_zero(base) && is_zero(exp)) {
        return inf_int(1);
    }

    inf_int result(1);
    inf_int b = base;
    inf_int e = exp;

    // 음수지수는지원하지않음
    if (e < inf_int(0)) {
        return inf_int(0);
    }

    while (!is_zero(e)) { // 지수가 0이 아닐 경우에만 작동
        if (!is_even(e)) {          // exp의최하위비트가1이면
            result = result * b;   // 곱하기
        }
        div2(e);            // exp(지수)를 2로 나눔
        if (!is_zero(e)) {
            b = b * b;       // base = base^2
        }
    }
    return result;
}


inf_int& inf_int::operator=(const inf_int& a)
{
    // 자기 자신을 대입하는 경우 고려
    if (*this == a) return *this;
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

bool operator>=(const inf_int& a, const inf_int& b) {
    return !(a < b);
}

bool operator<=(const inf_int& a, const inf_int& b) {
    return !(a > b);
}

int absCompare(const inf_int& a, const inf_int& b) // a가 크면 true 아니면 false
{
	if (a.length > b.length) return 1; 
	else if (a.length < b.length) return -1;
	else {
        for (int i = a.length - 1; i >= 0; --i) {
            if (a.digits[i] > b.digits[i]) return 1; // 다른 지점을 찾으면 즉시 반환
            if (a.digits[i] < b.digits[i]) return -1; // 다른 지점을 찾으면 즉시 반환
       }
    }

    return 0; // 모든 자릿수가 같음
}

inf_int operator-(const inf_int& a, const inf_int& b)
{
    inf_int c;

    // 1. 두 피연산자의 부호가 다른 경우
    if (a.thesign != b.thesign) {
        c = b;
        c.thesign = a.thesign; // 부호를 같게 만들어준 뒤
        return a + c;          // 덧셈 연산으로 전환
    }

    // 2. 두 피연산자의 부호가 같은 경우
    int cmp = absCompare(a, b); // 절댓값 비교

    // 2-1. 두 수의 절댓값이 같은 경우 (예: 8 - 8)
    if (cmp == 0) {
        return inf_int(0); // 결과는 0
    }
    // 2-2. a의 절댓값이 b보다 큰 경우
    else if (cmp > 0) {
        c = a; // 큰 수에서
        for (unsigned int i = 0; i < b.length; i++) {
            c.SUB(b.digits[i], i); // 작은 수를 뺌
        }
        c.thesign = a.thesign; // 부호는 원래 부호를 따름
    }
    // 2-3. b의 절댓값이 a보다 큰 경우
    else { // cmp < 0
        c = b; // 큰 수에서
        for (unsigned int i = 0; i < a.length; i++) {
            c.SUB(a.digits[i], i); // 작은 수를 뺌
        }
        c.thesign = !a.thesign; // 부호는 원래 부호의 반대가 됨
    }

    // 3. 결과값의 불필요한 앞자리 0 제거
    while (c.length > 1 && c.digits[c.length - 1] == '0') {
        c.length--;
    }
    
    // 버퍼 오버플로우 방지를 위해 문자열의 끝을 명시
    c.digits[c.length] = '\0'; 

    // 최종 결과가 0인 경우 부호를 항상 양수로 통일
    if (c.length == 1 && c.digits[0] == '0') {
        c.thesign = true;
    }

    return c;
}

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
    // 현재 자릿수에서 뺄셈이 가능한 경우 (내림 불필요)
    if (this->digits[index] >= num) {
        this->digits[index] = this->digits[index] - num + '0';
    }
    // 내림이 필요한 경우
    else {
        // 10을 빌려와서 뺄셈 수행
        this->digits[index] = this->digits[index] + 10 - num + '0';

        // 0이 아닌 상위 자릿수를 찾을 때까지 1씩 빌려오는 과정
        unsigned int i = index + 1; // 바로 위 자릿수부터 시작
        while (this->digits[i] == '0') {
            this->digits[i] = '9'; // 0이었던 자리는 9가 됨
            i++;
        }
        this->digits[i]--; // 0이 아니었던 첫 상위 자릿수에서 1을 뺌
    }
}

// 새롭게 구현한 몫과 나눗셈
inf_int operator/(const inf_int& a, const inf_int& b) {

    // b가 0이면 오류 출력? 어떻게 해야할까?

    // 몫, 절댓값 계산을 위한 inf_int
    inf_int quotient;
    inf_int compare1(a);
    inf_int compare2(b);
    compare1.thesign = true;
    compare2.thesign = true;
    if (b == inf_int(0)) throw std::invalid_argument("Division by zero is not allowed.");

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

// inf_int에 sqrt() 추가함
// =, ==, <, <=, +, -, *, / 가 구현되었다고 가정
inf_int sqrt(const inf_int& value) {
	// 음수의 제곱근
	if (value < inf_int(0)) {
		// 복소수도 하려고 했는데, 생각해보니 inf_int가 정수형이어서 안해도 될 거 같음
		// value.imaginary = true;
		// 예외 처리, 음수의 제곱근 정의 안 할거임
		throw invalid_argument("Sqrt of negative number is not allowed");
	}
	// 0과 1의 제곱근은 자기 자신
	if (value == inf_int(0) || value == inf_int(1)) {
		return value;
	}
	// Binary Search
	// 1부터 value까지의 범위에서 value의 제곱근 찾기 (어떤 수를 제곱했을 때 value가 되는 수 찾기)
	// return mid: mid*mid == value (정확한 값을 찾았을 때)
	// return result: mid*mid < value인 가장 큰 mid (정확한 값은 아니고, 소수점 버림)
	inf_int left(1), right = value, mid, result;

	while (!(left > right)) {
		mid = (left + right) / inf_int(2);
		inf_int midSquare = mid * mid;
		if (midSquare == value) {
			return mid;
		} else if (midSquare < value) {
			left = mid + inf_int(1);
			result = mid; // Update answer
		} else {
			right = mid - inf_int(1);
		}
	}
	return result;
}
    
inf_int abs(const inf_int& value) {
    inf_int temp(value);
    // thesign을 무조건 양수로
    temp.thesign = true;
    return temp;
}

inf_int operator-(const inf_int& value) {
    inf_int temp(value);
    // 0은 부호 안 바꿈
    if (temp == inf_int(0)) return temp;
    // thesign을 반대로
    temp.thesign = !temp.thesign;
    return temp;
}

inf_int nthroot(const inf_int& base, inf_int exponent) {
	// exponent가 1보다 작은 경우
	if (exponent < inf_int(1)) {
		throw invalid_argument("exponent must be bigger than 0");
	} 

	// 음수도 조건적으로 가능함(음수 base에 홀수 exponent면 base의 부호를 그대로 따라감)
	// imaginary가 나오는 경우 예외 처리 하기 (음수 base에 짝수 exponent인 경우 제외하기)
	if (base < inf_int(0) && (exponent % inf_int(2)) == inf_int(0)) {
		throw invalid_argument("nth root of negative number is allowed only if odd exponent");
	}

	// 0, 1, -1(위에서 걸러진 후)의 n제곱근은 자기 자신
	if (base == inf_int(0) || base == inf_int(1) || base == inf_int(-1)) {
		return base;
	}

	// Binary Search
	// mid*mid 대신 pow(mid, n)으로
	bool positive = true;
	if ((base < 0)) positive = false;
	inf_int left(1), right = abs(base), mid, result;

	while (!(left > right)) {
		mid = (left + right) / inf_int(2);
		inf_int midpow = pow(mid, exponent);
		if (midpow == abs(base)) {
			// return 시에 원래 부호 붙이기
			if (positive) {
				return mid;
			}
			return -mid;
		} else if (midpow < abs(base)) {
			left = mid + inf_int(1);
			result = mid;
		} else {
			right = mid - inf_int(1);
		}
	}
	// return 시에 원래 부호 붙이기
	if (positive) {
		return result;	
	}
	return -result;
}