#include "calculator.h"
#include "precedence.h"
#include "inf_int.h"
#include <iostream>
#include <string>
#include <fstream>

using namespace std;

int main() {
	fstream textfile;
    string line; string delimeter = ",";
	string file = "test.txt";
	string expression, answer;
	inf_int cal;
	Calculator c;
	int pos = 0;
    textfile.open(file, ios::in);
    if (textfile.is_open()) {
        while (getline(textfile, line)) {
            // parse line
			pos = line.find(delimeter, 0);
			expression = line.substr(0, pos);
			answer = line.substr(pos + 1);
			cal = c.calculate(Precedence::postfix(expression));
			if (cal == inf_int(answer.c_str())) {
				cout << "Correct!" << endl;
			}
			else {
				cout << "Wrong!" << endl;
				cout << "Expression = " << expression << endl;
				cout << "Postfix = " << Precedence::postfix(expression) << endl;
				cout << "Answer = " << answer << endl;
				cout << "Calculated Answer = " << cal << endl;
			}
        }
        textfile.close();
    }
    else {
        // Exception
        cout << "Cannot Open " + file << endl;
        throw new exception();
    }
	return 0;
}