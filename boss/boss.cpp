#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <cmath>

#ifdef _WIN32
#define API __declspec(dllexport)
#else
#define API
#endif

struct Item {
    int id;
    std::string name;
    double price;
    std::string status;
};

static bool load_items(const char* path, std::vector<Item>& items) {
    std::ifstream in(path);
    if (!in.is_open()) return false;

    items.clear();
    std::string line;

    std::getline(in, line);

    while (std::getline(in, line)) {
        if (line.empty()) continue;

        std::stringstream ss(line);
        std::string id, name, price, status;

        if (!std::getline(ss, id, '|')) continue;
        if (!std::getline(ss, name, '|')) continue;
        if (!std::getline(ss, price, '|')) continue;
        if (!std::getline(ss, status, '|')) continue;

        try {
            items.push_back({
                std::stoi(id),
                name,
                std::stod(price),
                status
                });
        }
        catch (...) {}
    }
    return true;
}

extern "C" API
int boss_items_statistics(const char* items_path, const char* out_path) {
    std::vector<Item> items;
    if (!load_items(items_path, items)) return 1;

    int total = items.size();
    int available = 0, sold = 0, pawn = 0, returned = 0;
    double total_value = 0.0;

    for (auto& i : items) {
        if (i.status == "в наявності") available++;
        else if (i.status == "продано") sold++;
        else if (i.status == "застава") pawn++;
        else if (i.status == "повернено клієнту") returned++;

        total_value += i.price;
    }

    std::ofstream out(out_path);
    if (!out.is_open()) return 2;

    out << "total=" << total << "\n";
    out << "available=" << available << "\n";
    out << "sold=" << sold << "\n";
    out << "pawn=" << pawn << "\n";
    out << "returned=" << returned << "\n";
    out << "total_value=" << total_value << "\n";

    return 0;
}

extern "C" API
int boss_detect_anomalies(const char* items_path,
    const char* out_path,
    double factor) {
    std::vector<Item> items;
    if (!load_items(items_path, items)) return 1;

    if (items.empty()) return 0;

    double sum = 0.0;
    for (auto& i : items) sum += i.price;
    double mean = sum / items.size();

    double sq = 0.0;
    for (auto& i : items)
        sq += (i.price - mean) * (i.price - mean);

    double stddev = std::sqrt(sq / items.size());
    double limit = mean + factor * stddev;

    std::ofstream out(out_path);
    if (!out.is_open()) return 2;

    out << "id|name|price|status\n";
    for (auto& i : items) {
        if (i.price > limit) {
            out << i.id << "|" << i.name << "|" << i.price << "|" << i.status << "\n";
        }
    }
    return 0;
}

extern "C" API
int boss_sort_items(const char* items_path,
    const char* out_path,
    int ascending) {
    std::vector<Item> items;
    if (!load_items(items_path, items)) return 1;

    std::sort(items.begin(), items.end(),
        [ascending](const Item& a, const Item& b) {
            return ascending ? a.price < b.price : a.price > b.price;
        });

    std::ofstream out(out_path);
    if (!out.is_open()) return 2;

    out << "id|name|price|status\n";
    for (auto& i : items) {
        out << i.id << "|" << i.name << "|" << i.price << "|" << i.status << "\n";
    }
    return 0;
}
