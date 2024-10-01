#pragma once

#include <filesystem>
#include <memory>
#include <optional>

#include <onnxruntime/onnxruntime_cxx_api.h>

#include "Conf/Conf.h"
#include "Utils/NonCopyable.hpp"

MAA_RES_NS_BEGIN

class ONNXResMgr : public NonCopyable
{
public:
    // TODO: 拆一下放两个 ResMgr 里？
    inline static const std::filesystem::path kClassifierDir = "classify";
    inline static const std::filesystem::path kDetectorDir = "detect";

    //~ONNXResMgr();

public:
    bool use_cpu();
    bool use_gpu(int device_id);

    bool lazy_load(const std::filesystem::path& path, bool is_base);
    void clear();

public:
    std::shared_ptr<Ort::Session> classifier(const std::string& name) const;
    std::shared_ptr<Ort::Session> detector(const std::string& name) const;

private:
    std::shared_ptr<Ort::Session> load(const std::string& name, const std::vector<std::filesystem::path>& roots) const;

    std::vector<std::filesystem::path> classifier_roots_;
    std::vector<std::filesystem::path> detector_roots_;

    Ort::Env env_;
    Ort::SessionOptions options_;
    std::optional<int> gpu_device_id_;

    mutable std::unordered_map<std::string, std::shared_ptr<Ort::Session>> classifiers_;
    mutable std::unordered_map<std::string, std::shared_ptr<Ort::Session>> detectors_;
};

MAA_RES_NS_END
