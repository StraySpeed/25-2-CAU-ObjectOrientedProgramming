#include "inf_int.h"
using namespace std;

// inf_int�� sqrt() �߰���
// =, ==, <, <=, +, -, *, / �� �����Ǿ��ٰ� ����
inf_int sqrt(const inf_int& value) {
	// ������ ������
	if (value < inf_int(0)) {
		// ���Ҽ��� �Ϸ��� �ߴµ�, �����غ��� inf_int�� �������̾ ���ص� �� �� ����
		// value.imaginary = true;
		// ���� ó��, ������ ������ ���� �� �Ұ���
		throw invalid_argument("Sqrt of negative number is not allowed");
	}
	// 0�� 1�� �������� �ڱ� �ڽ�
	if (value == inf_int(0) || value == inf_int(1)) {
		return value;
	}
	// Binary Search
	// 1���� value������ �������� value�� ������ ã�� (� ���� �������� �� value�� �Ǵ� �� ã��)
	// return mid: mid*mid == value (��Ȯ�� ���� ã���� ��)
	// return result: mid*mid < value�� ���� ū mid (��Ȯ�� ���� �ƴϰ�, �Ҽ��� ����)
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