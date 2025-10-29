#include <iostream>
#include <string>
#include <sstream>
#include <stack>
#include "calculator.h"
#include "inf_int.h"

Calculator::Calculator() {
    prev = inf_int(0);
}

inf_int Calculator::calculate(std::string expr) {
    stack<inf_int> s;
    std::istringstream iss(expr);
    std::string symbol;
    inf_int a, b;
    while (iss >> symbol) {
        if (symbol == "+") {
            a = inf_int(s.top());
            s.pop();
            b = inf_int(s.top());
            s.pop();
            s.push(a + b);
        }
        else if (symbol == "-") {
            a = inf_int(s.top());
            s.pop();
            b = inf_int(s.top());
            s.pop();
            s.push(b - a);
        }
        else if (symbol == "/") {
            a = inf_int(s.top());
            s.pop();
            b = inf_int(s.top());
            s.pop();
            //s.push(a / b);            
        }
        else if (symbol == "*") {
            a = inf_int(s.top());
            s.pop();
            b = inf_int(s.top());
            s.pop();
            s.push(a * b);            
        }
        else if (symbol == "%") {
            a = inf_int(s.top());
            s.pop();
            b = inf_int(s.top());
            s.pop();
            //s.push(a % b);            
        }
        else if (symbol == "PREV") {
            s.push(prev);
        }
        else {
            s.push(inf_int(symbol.c_str()));
        }
    }
    // 이전 계산값을 수정
    prev = s.top();
    return s.top();
}

inf_int Calculator::getPrev() const{
    return prev;
}