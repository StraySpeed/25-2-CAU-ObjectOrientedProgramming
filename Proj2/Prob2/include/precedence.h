#pragma once
#include <iostream>
#include <string>

class Precedence {
    public:
        enum precedence {
            LPAREN, RPAREN, PLUS, MINUS, TIMES, DIVIDE, MOD, POW, SQRT, EOS, OPERAND
        };
        // in-stack precedence
        static constexpr int isp[11] = { 0, 19, 12, 12, 13, 13, 13, 14, 16, 0, 0};
        // in-coming precedence
        static constexpr int icp[11] = { 20, 19, 12, 12, 13, 13, 13, 14, 17, 0, 0 };

        static precedence getToken(std::string symbol);

        static std::string postfix(std::string str);
};