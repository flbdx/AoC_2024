#include <cstdlib>
#include <cstdio>
#include <cstdint>
#include <cinttypes>
#include <cmath>

#include <string>
#include <fstream>
#include <sstream>
#include <vector>

const char *test_input = R"DELIM(190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
)DELIM";

static inline bool test(std::vector<uint32_t> &operands, std::vector<uint8_t> &operators, uint64_t target) {
    uint64_t r = operands[0];
    uint64_t b;
    for (size_t i = 0; i < operators.size(); ++i) {
        const auto &ope = operators[i];
        b = operands[i+1];
        if (ope == 0) {
            r = r + b;
        }
        else if (ope == 1) {
            r = r * b;
        }
        else {
            int e = int(::floor(log10(b)) + 1);
            while (e--) {
                r *= 10;
            }
            r += b;
        }
        if (r > target) {
            return false;
        }
    }
    return r == target;
}

static uint64_t work(std::istream &in, bool part2=false) {
    const unsigned int max_operator = part2 ? 3 : 2;
    uint64_t result = 0;

    for (std::string line; std::getline(in, line);) {
        if (line.size() == 0) {
            break;
        }
        std::istringstream iss(line);
        uint64_t target;
        std::vector<uint32_t> operands;
        iss >> target;
        {
            char sep;
            iss >> sep;
        }
        while (iss.good()) {
            uint32_t d;
            iss >> d;
            operands.push_back(d);
        }

        size_t n_operators = operands.size() - 1;
        uint64_t n_tests = 1;
        for (size_t i = 0; i < n_operators; ++i) {
            n_tests *= max_operator;
        }

        std::vector<uint8_t> operators(n_operators, 0);
        for (uint64_t i = 0; i < n_tests; ++i) {
            if (test(operands, operators, target)) {
                result += target;
                break;
            }

            for (size_t j = 0; j < n_operators; ++j) {
                operators[j] += 1;
                if (operators[j] == max_operator) {
                    operators[j] = 0;
                }
                else {
                    break;
                }
            }
        }
    }

    return result;
}

int main() {
    std::string test_input_s = test_input;
    std::istringstream iss(test_input_s);
    std::ifstream in("input_07");

    if (work(iss) != uint64_t(3749)) {
        fprintf(stderr, "Erreur test p1\n");
        return 1;
    }
    printf("%" PRIu64 "\n", work(in));



    iss.clear();
    iss.seekg(0);
    in.clear();
    in.seekg(0);

    if (work(iss, true) != uint64_t(11387)) {
        fprintf(stderr, "Erreur test p2\n");
        return 1;
    }
    printf("%" PRIu64 "\n", work(in, true));
}