#include <pybind11/pybind11.h>
#include <pybind11/stl.h> // std::string을 자동으로 변환하기 위해 필요
#include "precedence.h"   // 래핑할 C++ 클래스의 헤더

namespace py = pybind11;

// PYBIND11_MODULE 매크로를 사용하여 'precedence_wrapper'라는 이름의 파이썬 모듈을 정의합니다.
PYBIND11_MODULE(precedence_wrapper, m) {
    // 모듈에 대한 설명 (Python에서 help() 함수로 볼 수 있음)
    m.doc() = "A Python wrapper for the C++ Precedence utility class";

    // Precedence 클래스를 파이썬에 'Precedence'라는 이름으로 바인딩합니다.
    // py::class_의 반환값을 변수로 받아두면 중첩된 enum 등을 바인딩하기 편리합니다.
    py::class_<Precedence> precedence_class(m, "Precedence");

    // 1. 중첩된 enum 'precedence'를 바인딩합니다.
    // 파이썬에서는 'Precedence.Token'과 같은 형태로 접근할 수 있습니다.
    py::enum_<Precedence::precedence>(precedence_class, "Token")
        .value("LPAREN", Precedence::precedence::LPAREN)
        .value("RPAREN", Precedence::precedence::RPAREN)
        .value("PLUS", Precedence::precedence::PLUS)
        .value("MINUS", Precedence::precedence::MINUS)
        .value("TIMES", Precedence::precedence::TIMES)
        .value("DIVIDE", Precedence::precedence::DIVIDE)
        .value("MOD", Precedence::precedence::MOD)
        .value("EOS", Precedence::precedence::EOS)
        .value("OPERAND", Precedence::precedence::OPERAND)
        .export_values(); // 이 옵션은 Precedence.LPAREN처럼 enum 멤버에 바로 접근하게 해줍니다.

    // 2. static 데이터 멤버(상수 배열)를 바인딩합니다.
    // 'constexpr'이므로 수정할 수 없도록 .def_readonly_static을 사용합니다.
    // C-스타일 배열은 자동으로 파이썬 튜플로 변환됩니다.
    precedence_class.def_readonly_static("ISP", &Precedence::isp, "In-stack precedence values");
    precedence_class.def_readonly_static("ICP", &Precedence::icp, "In-coming precedence values");

    // 3. static 멤버 함수를 바인딩합니다.
    // .def_static을 사용합니다.
    // 파이썬의 작명 관례(snake_case)에 따라 getToken -> get_token 으로 이름을 변경해줍니다.
    precedence_class.def_static("get_token", &Precedence::getToken, 
                                "Get the token enum for a given symbol string.",
                                py::arg("symbol"));

    // postfix 함수도 바인딩합니다. to_postfix로 이름을 변경하여 의미를 더 명확하게 합니다.
    precedence_class.def_static("to_postfix", &Precedence::postfix,
                                "Convert an infix expression string to postfix notation.",
                                py::arg("str"));
}