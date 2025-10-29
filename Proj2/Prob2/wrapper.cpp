#include <pybind11/pybind11.h>
#include <pybind11/stl.h>       // std::string, std::vector 등 자동 변환
#include <pybind11/operators.h> // 연산자 오버로딩 바인딩
#include <sstream>              // C++ 객체를 문자열로 변환하기 위해 사용

// 래핑할 모든 C++ 클래스의 헤더 파일
#include "inf_int.h"
#include "precedence.h"
#include "calculator.h"
#include "application.h"

namespace py = pybind11;

PYBIND11_MODULE(calculator, m) {
    m.doc() = "BongBong OOP Project2 ";

    //=========================================================================
    // 1. inf_int 클래스 래핑 (가장 기본이 되는 데이터 타입)
    //=========================================================================
    py::class_<inf_int>(m, "InfInt")
        // 생성자 바인딩 (기본, 정수, 문자열)
        .def(py::init<>(), "Default constructor, initializes to 0.")
        .def(py::init<int>(), "Constructor from an integer.", py::arg("value"))
        .def(py::init<const char*>(), "Constructor from a C-style string.", py::arg("value"))

        // Python의 print()와 str()을 위한 __str__ 메소드 바인딩
        .def("__str__", [](const inf_int& i) {
            std::stringstream ss;
            ss << i;
            return ss.str();
        })
        // 개발자용 표현을 위한 __repr__ 메소드 바인딩
        .def("__repr__", [](const inf_int& i) {
            std::stringstream ss;
            ss << i;
            return "<InfInt: '" + ss.str() + "'>";
        })

        // 산술 연산자 바인딩
        .def(py::self + py::self)
        .def(py::self - py::self)
        .def(py::self * py::self)
        .def(py::self / py::self)
        .def(py::self % py::self)

        // 비교 연산자 바인딩
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def(py::self > py::self)
        .def(py::self < py::self);
        //.def(py::self >= py::self, "Greater than or equal to comparison.")
        //.def(py::self <= py::self, "Less than or equal to comparison.");

    // inf_int를 사용하는 전역(friend) 함수들을 모듈 수준에서 바인딩
    m.def("pow", &pow, "Computes base raised to the power of exp.", py::arg("base"), py::arg("exp"));
    m.def("sqrt", &sqrt, "Computes the integer square root of a number.", py::arg("n"));

    //=========================================================================
    // 2. Precedence 클래스 래핑 (정적 유틸리티 클래스)
    //=========================================================================
    py::class_<Precedence> precedence_class(m, "Precedence");

    // 중첩된 enum 'precedence'를 'Token'이라는 이름의 파이썬 Enum으로 바인딩
    py::enum_<Precedence::precedence>(precedence_class, "Token")
        .value("LPAREN", Precedence::precedence::LPAREN)
        .value("RPAREN", Precedence::precedence::RPAREN)
        .value("PLUS", Precedence::precedence::PLUS)
        .value("MINUS", Precedence::precedence::MINUS)
        .value("TIMES", Precedence::precedence::TIMES)
        .value("DIVIDE", Precedence::precedence::DIVIDE)
        .value("MOD", Precedence::precedence::MOD)
        .value("POW", Precedence::precedence::POW)
        .value("SQRT", Precedence::precedence::SQRT)
        .value("EOS", Precedence::precedence::EOS)
        .value("OPERAND", Precedence::precedence::OPERAND)
        .export_values(); // Precedence.LPAREN 처럼 직접 접근 허용

    // 정적 상수 배열을 읽기 전용 속성으로 바인딩
    precedence_class.def_readonly_static("ISP", &Precedence::isp, "In-stack precedence values");
    precedence_class.def_readonly_static("ICP", &Precedence::icp, "In-coming precedence values");

    // 정적 멤버 함수를 바인딩 (Python 스타일 이름으로 변경)
    precedence_class.def_static("get_token", &Precedence::getToken,
                                "Get the token enum for a given symbol string.", py::arg("symbol"));
    precedence_class.def_static("to_postfix", &Precedence::postfix,
                                "Convert an infix expression string to postfix notation.", py::arg("str"));

    //=========================================================================
    // 3. Calculator 클래스 래핑
    //=========================================================================
    py::class_<Calculator>(m, "Calculator")
        // 생성자 바인딩
        .def(py::init<>(), "Initializes a Calculator instance.")

        // 멤버 함수 바인딩
        .def("calculate", &Calculator::calculate,
             "Calculates the result of an infix expression string.", py::arg("expr"))

        // getPrev() 함수를 'prev'라는 읽기 전용 속성으로 바인딩
        .def_property_readonly("prev", &Calculator::getPrev,
                               "The result of the previous calculation.");
}