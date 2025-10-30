#include "inf_int.h"
using namespace std;

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