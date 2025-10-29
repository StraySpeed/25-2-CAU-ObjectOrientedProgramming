#pragma once
#include <string>
#include "inf_int.h"

class Calculator {
    private:
        inf_int prev = 0;
  
    public:
        inf_int calculate(std::string expr);
        inf_int getPrev() const;
};