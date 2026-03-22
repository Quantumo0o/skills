#!/usr/bin/env python3
# 饮食行为健康分析工具配置文件
import os
import sys

from enum import Enum

from skills.smyx_common.scripts.config import ConstantEnum as ConstantEnumBase

from skills.face_analysis.scripts.config import ApiEnum as ApiEnumParent, ConstantEnum as ConstantEnumParent, \
    SceneCodeEnum


class ApiEnum(ApiEnumParent):
    # ANALYSIS_URL = "/web/ai-analysis/v2/start-common-ai-analysis"

    # ANALYSIS_RESULT_URL = "/web/ai-analysis/get-common-ai-analysis-result"

    # PAGE_URL = "/web/ai-analysis/page-common-ai-analysis-result"

    # DETAIL_EXPORT_URL = ApiEnumParent.BASE_URL_HEALTH + "/health/order/api/getReportDetailExport?id="

    @classmethod
    def init(cls, config=None):
        clsName = cls.__name__
        print("aazzzz ^^^^^^ 饮食常量j*******+======>>>> get cls and new ==.et fullname  AAAA BSSE:", cls, config,
              "__clsName",
              clsName,
              "os.environ", os.environ, "deaul", cls.ANALYSIS_RESULT_URL)
        ApiEnumParent.ANALYSIS_URL = "/web/ai-analysis/v2/start-common-ai-analysis"
        ApiEnumParent.ANALYSIS_RESULT_URL = "/web/ai-analysis/get-common-ai-analysis-result"
        ApiEnumParent.PAGE_URL = "/web/ai-analysis/page-common-ai-analysis-result"
        print("gggg^^^^^^ 饮食常量 faeterj*******+======>>>> get cls and new ==.et fullname  AAAA BSSE:", cls, config,
              "__clsName",
              clsName,
              "os.environ", os.environ, "deaul", cls.ANALYSIS_RESULT_URL)


class ConstantEnum(ConstantEnumParent):
    DEFAULT__ANALYSIS_TYPE = "comprehensive"

    @classmethod
    def init(cls, config=None):
        clsName = cls.__name__
        print("饮食常量j*******+======>>>> get cls and new ==.et fullname  AAAA BSSE:", cls, config, "__clsName",
              clsName,
              "os.environ", os.environ, "deaul", cls.DEFAULT__SCENE_CODE)
        ConstantEnumParent.DEFAULT__SCENE_CODE = SceneCodeEnum.DIET_ANALYSIS.value
        print("饮食常量 faeterj*******+======>>>> get cls and new ==.et fullname  AAAA BSSE:", cls, config, "__clsName",
              clsName,
              "os.environ", os.environ, "deaul", cls.DEFAULT__SCENE_CODE)
