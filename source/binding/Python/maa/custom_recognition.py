import ctypes
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Tuple

import numpy

from .buffer import ImageBuffer, RectBuffer, StringBuffer
from .context import Context
from .define import *


class CustomRecognition(ABC):
    _handle: MaaCustomRecognitionCallback

    def __init__(self):
        self._handle = self._c_analyze_agent

    @dataclass
    class AnalyzeArg:
        task_detail: TaskDetail
        current_task_name: str
        custom_recognition_name: str
        custom_recognition_param: str
        image: numpy.ndarray
        roi: Rect

    @dataclass
    class AnalyzeResult:
        box: Optional[RectType]
        detail: str

    @abstractmethod
    def analyze(
        self,
        context: Context,
        argv: AnalyzeArg,
    ) -> AnalyzeResult:
        raise NotImplementedError

    @property
    def c_handle(self) -> MaaCustomRecognitionCallback:
        return self._handle

    @property
    def c_arg(self) -> ctypes.c_void_p:
        return ctypes.c_void_p.from_buffer(ctypes.py_object(self))

    @staticmethod
    @MaaCustomRecognitionCallback
    def _c_analyze_agent(
        c_context: MaaContextHandle,
        c_task_id: MaaTaskId,
        c_current_task_name: ctypes.c_char_p,
        c_custom_reco_name: ctypes.c_char_p,
        c_custom_reco_param: ctypes.c_char_p,
        c_image: MaaImageBufferHandle,
        c_roi: MaaRectHandle,
        c_transparent_arg: ctypes.c_void_p,
        c_out_box: MaaRectHandle,
        c_out_detail: MaaStringBufferHandle,
    ) -> int:
        if not c_transparent_arg:
            return int(False)

        self: CustomRecognition = ctypes.cast(c_transparent_arg, ctypes.py_object).value

        context = Context(c_context)
        task_detail = context.tasker._get_task_detail(int(c_task_id))
        if not task_detail:
            return int(False)

        image = ImageBuffer(c_image).get()

        result: CustomRecognition.AnalyzeResult = self.analyze(
            context,
            CustomRecognition.AnalyzeArg(
                task_detail=task_detail,
                current_task_name=c_current_task_name.decode(),
                custom_recognition_name=c_custom_reco_name.decode(),
                custom_recognition_param=c_custom_reco_param.decode(),
                image=image,
                roi=RectBuffer(c_roi).get(),
            ),
        )

        if result.box:
            RectBuffer(c_out_box).set(result.box)

        StringBuffer(c_out_detail).set(result.detail)

        ret = result.box is not None
        return int(ret)