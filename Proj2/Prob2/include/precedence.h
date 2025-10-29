#pragma once
#include <iostream>
#include <string>

class Precedence {
    public:
        enum precedence {
            LPAREN, RPAREN, PLUS, MINUS, TIMES, DIVIDE, MOD, EOS, OPERAND
        };
        // in-stack precedence
        static constexpr int isp[9] = { 0, 19, 12, 12, 13, 13, 13, 0, 0};
        // in-coming precedence
        static constexpr int icp[9] = { 20, 19, 12, 12, 13, 13, 13, 0, 0 };

        static precedence getToken(std::string symbol);

        static std::string postfix(std::string str);
};