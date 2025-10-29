#include <iostream>
#include <sstream>
#include <stack>
#include "precedence.h"

Precedence::precedence Precedence::getToken(std::string symbol) {
    if (symbol == "(") return LPAREN;
    else if (symbol == ")") return RPAREN;
    else if (symbol == "+") return PLUS;
    else if (symbol == "-") return MINUS;
    else if (symbol == "/") return DIVIDE;
    else if (symbol == "*") return TIMES;
    else if (symbol == "%") return MOD;
    else if (symbol == ";") return EOS;
    else if (symbol == "^") return POW;
    else if (symbol == "SQRT") return SQRT;
    else return OPERAND;
}

std::string Precedence::postfix(std::string str) {
    std::stack<std::string> stack;
    std::string symbol;
    Precedence::precedence token;
    std::string const DELIMETER = " ";
    std::string returnstr = "";

    // for safety:precedence 0
    stack.push(";");  

    // parse string with " "
    std::istringstream iss(str);
    while (iss >> symbol) {
        // check precedence
        token = Precedence::getToken(symbol);
        if (token == Precedence::EOS) break;

        if (token == Precedence::OPERAND) returnstr = returnstr + symbol + " ";
        
        else if (token == Precedence::RPAREN) {
            while (stack.top() != "(") {
                returnstr = returnstr + stack.top() + " ";
                stack.pop();
            } 
            stack.pop(); // discard "("
        }
        else {
            while (Precedence::isp[Precedence::getToken(stack.top())] >= Precedence::icp[token]) {
                returnstr = returnstr + stack.top() + " ";
                stack.pop();
            }
            stack.push(symbol);
        }
    }
    while ((symbol = stack.top()) != ";") {
        returnstr = returnstr + symbol + " ";
        stack.pop();
    }
    return returnstr;
}