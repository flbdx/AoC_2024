#include <cstdlib>
#include <cstdio>
#include <cstdint>

#include <string>
#include <fstream>
#include <sstream>
#include <set>
#include <utility>
#include <vector>

const char *test_input = R"DELIM(....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
)DELIM";

typedef std::pair<short, short> Position;
typedef Position Direction;

static inline Direction turn_right(const Direction &d) {
    return {-d.second, d.first};
}
static inline Position move(const Position &p, const Direction &d) {
    return {p.first + d.first, p.second + d.second};
}

static void read_inputs(std::istream &in, std::set<Position> &grid, Position &guard_position, int &width, int &height) {
    int max_x = 0;
    int max_y = 0;
    int y = 0;
    int x = 0;
    grid.clear();

    for (std::string line; std::getline(in, line); ) {
        if (line.size() == 0) {
            break;
        }
        x = 0;
        for (char c : line) {
            if (c == '#') {
                grid.insert({x, y});
            }
            else if (c == '^') {
                guard_position = {x, y};
            }
            max_x = std::max(max_x, x);
            x += 1;
        }
        max_y = std::max(max_y, y);
        y += 1;
    }

    width = max_x + 1;
    height = max_y + 1;
}

static size_t work_p1(std::istream &in) {
    std::set<Position> grid;
    Position guard_position;
    int width;
    int height;
    read_inputs(in, grid, guard_position, width, height);

    Direction dir = {0, -1};
    Position pos = guard_position;
    std::set<Position> visited;
    visited.insert(pos);

    while (true) {
        Position next_p = move(pos, dir);
        if (grid.count(next_p)) {
            dir = turn_right(dir);
            continue;
        }
        else {
            if (next_p.first < 0 || next_p.first >= width) {
                break;
            }
            if (next_p.second < 0 || next_p.second >= height) {
                break;
            }
            pos = next_p;
            visited.insert(pos);
        }
    }

    return visited.size();
}

static size_t work_p2(std::istream &in) {
    std::set<Position> grid;
    Position guard_position;
    int width;
    int height;
    read_inputs(in, grid, guard_position, width, height);

    Direction dir = {0, -1};
    Position pos = guard_position;
    std::set<Position> obstacle_candidates;
    obstacle_candidates.insert(pos);

    while (true) {
        Position next_p = move(pos, dir);
        if (grid.count(next_p)) {
            dir = turn_right(dir);
            continue;
        }
        else {
            if (next_p.first < 0 || next_p.first >= width) {
                break;
            }
            if (next_p.second < 0 || next_p.second >= height) {
                break;
            }
            pos = next_p;
            obstacle_candidates.insert(pos);
        }
    }

    obstacle_candidates.erase(guard_position);
    size_t res = 0;

    std::vector<uint64_t> visited;
    visited.resize(width * height);
    auto mark = [&visited, &width](const Position &pos, const Direction &dir) {
        size_t idx = pos.second * width + pos.first;
        uint64_t v = dir.first + 1 + (dir.second + 1) * 4;
        v = (uint64_t)(1) << v;
        visited[idx] |= v;
    };
    auto is_marked = [&visited, &width](const Position &pos, const Direction &dir) {
        size_t idx = pos.second * width + pos.first;
        uint64_t v = dir.first + 1 + (dir.second + 1) * 4;
        v = (uint64_t)(1) << v;
        return (visited[idx] & v) != 0;
    };

    for (const Position &obstacle : obstacle_candidates) {
        visited = {};
        visited.resize(width * height, 0);
        pos = guard_position;
        dir = {0, -1};

        while (true) {
            Position next_p = move(pos, dir);
            if (next_p.first < 0 || next_p.first >= width || next_p.second < 0 || next_p.second >= height) {
                break;
            }
            else if (grid.count(next_p) || next_p == obstacle) {
                dir = turn_right(dir);
                continue;
            }
            else if (is_marked(next_p, dir)) {
                res += 1;
                break;
            }
            else {
                pos = next_p;
                mark(pos, dir);
            }
        }
    }

    return res;
}

int main() {
    std::string test_input_s = test_input;
    std::istringstream iss(test_input_s);
    std::ifstream in("input_06");

    if (work_p1(iss) != size_t(41)) {
        fprintf(stderr, "Erreur test p1\n");
        return 1;
    }
    printf("%zu\n", work_p1(in));



    iss.clear();
    iss.seekg(0);
    in.clear();
    in.seekg(0);

    if (work_p2(iss) != size_t(6)) {
        fprintf(stderr, "Erreur test p2\n");
        return 1;
    }
    printf("%zu\n", work_p2(in));
}