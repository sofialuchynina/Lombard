#pragma once

#ifdef _WIN32
#define API __declspec(dllexport)
#else
#define API
#endif

extern "C" {
    API int boss_items_statistics(const char* items_path, const char* out_path);

    API int boss_detect_anomalies(
        const char* items_path,
        const char* out_path,
        double factor
    );

    API int boss_sort_items(
        const char* items_path,
        const char* out_path,
        int ascending
    );
}
