#include <cstdlib>
#include <cstdio>
#include <cstdint>
#include <cinttypes>

#include <string>
#include <fstream>
#include <sstream>
#include <vector>
#include <list>
#include <tuple>
#include <utility>

const char *test_input = R"DELIM(2333133121414131402)DELIM";

static uint64_t work_p1(std::istream &in) {
    std::string line;
    std::getline(in, line);

    size_t tlen = 0;
    for (char c : line) {
        tlen += (c - '0');
    }

    std::vector<int32_t> data;
    data.resize(tlen, -1);

    {
        int32_t id = 0;
        size_t pos = 0;
        bool is_data = true;
        for (auto c : line) {
            int32_t v = c - '0';
            if (is_data) {
                for (int32_t i = 0; i < v; ++i) {
                    data[pos] = id;
                    pos += 1;
                }
                id += 1;
            }
            else {
                pos += v;
            }
            is_data = !is_data;
        }
    }

    size_t ins_pos = 0;
    size_t read_pos = data.size() - 1;
    while (read_pos > ins_pos) {
        if (data[ins_pos] != -1) {
            ins_pos += 1;
            continue;
        }
        if (data[read_pos] == -1) {
            read_pos -= 1;
            continue;
        }

        uint32_t tmp = data[ins_pos];
        data[ins_pos] = data[read_pos];
        data[read_pos] = tmp;
        ins_pos += 1;
        read_pos -= 1;
    }

    uint64_t ret = 0;
    for (size_t pos = 0; pos < data.size(); ++pos) {
        if (data[pos] == -1) {
            break;
        }
        ret += data[pos] * pos;
    }

    return ret;
}

static uint64_t work_p2(std::istream &in) {
    std::string line;
    std::getline(in, line);

    size_t tlen = 0;
    for (char c : line) {
        tlen += (c - '0');
    }

    typedef std::tuple<size_t, size_t, int32_t> DataBlock; // pos, len, id
    typedef std::pair<size_t, size_t> FreeBlock; // pos, len

    std::list<DataBlock> data_blocks;
    std::list<FreeBlock> free_blocks;

    {
        int32_t id = 0;
        size_t pos = 0;
        bool is_data = true;
        for (auto c : line) {
            int32_t v = c - '0';
            if (is_data) {
                data_blocks.emplace_back(pos, size_t(v), id);
                pos += v;
                id += 1;
            }
            else {
                free_blocks.emplace_back(pos, size_t(v));
                pos += v;
            }
            is_data = !is_data;
        }
    }

    for (auto data_it = data_blocks.rbegin(); data_it != data_blocks.rend(); ++data_it) {
        size_t data_pos = std::get<0>(*data_it);
        size_t data_len = std::get<1>(*data_it);
        int32_t id = std::get<2>(*data_it);

        for (auto free_it = free_blocks.begin(); free_it != free_blocks.end(); ++free_it) {
            size_t free_pos = free_it->first;
            size_t free_len = free_it->second;

            if (free_len >= data_len && free_pos < data_pos) {
                size_t free_rem = free_len - data_len;
                *data_it = DataBlock(free_pos, data_len, id);
                if (free_rem == 0) {
                    free_blocks.erase(free_it);
                }
                else {
                    *free_it = std::make_pair(size_t(free_pos + data_len), size_t(free_rem));
                }

                break;
            }
            else if (free_pos > data_pos) {
                break;
            }
        }
    }

    uint64_t ret = 0;
    for (const auto &d : data_blocks) {
        for (size_t i = 0; i < std::get<1>(d); ++i) {
            ret += (std::get<0>(d)+i) * std::get<2>(d);
        }
    }

    return ret;
}

int main() {
    std::string test_input_s = test_input;
    std::istringstream iss(test_input_s);
    std::ifstream in("input_09");

    if (work_p1(iss) != uint64_t(1928)) {
        fprintf(stderr, "Erreur test p1\n");
        return 1;
    }
    printf("%" PRIu64 "\n", work_p1(in));



    iss.clear();
    iss.seekg(0);
    in.clear();
    in.seekg(0);

    if (work_p2(iss) != uint64_t(2858)) {
        fprintf(stderr, "Erreur test p2\n");
        return 1;
    }
    printf("%" PRIu64 "\n", work_p2(in));
}