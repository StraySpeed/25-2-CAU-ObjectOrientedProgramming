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

	while (left <= right) {
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