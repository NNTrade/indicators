from __future__ import annotations
from typing import List, Tuple, Union
from numpy import NaN, number
import numpy as np
from ..misc.direction import direction
from ..rules import rules
from ..misc.wave import wave


class builder:
    def __init__(self, impulse_direction: direction, fluent_builder=False) -> None:
        self.__waves: List[wave] = []
        self.__direction = impulse_direction
        self.fluent_builder = fluent_builder
        pass

    def get_wave(self, wave_number: int) -> wave:
        return self.__waves[wave_number-1]

    def build(self) -> wave:
        if len(self.__waves) >= 2:
            return wave(self.__waves[0].start, self.__waves[-1].end, sub_waves=self.waves)
        if len(self.__waves) == 1:
            return wave(self.__waves[0].start, self.__waves[-1].end)
        return None

    @property
    def waves(self) -> List[wave]:
        return [wv for wv in self.__waves]

    @property
    def direction(self):
        return self.__direction

    @property
    def next_wave(self) -> int:
        _ret = len(self.__waves) + 1
        if _ret > 5:
            return -1
        return _ret

    @property
    def next_wave_direction(self) -> direction:
        next_wave = self.next_wave
        if next_wave <= 0:
            raise Exception("All waves is setted")

        if next_wave % 2 == 0:
            return self.direction.revers()
        else:
            return self.direction

    @property
    def isComplete(self) -> bool:
        return self.next_wave <= 0

    def clone(self) -> builder:
        _ret = builder(self.direction, self.fluent_builder)
        _ret.__waves = [wv for wv in self.__waves]
        return _ret

    def __add_wave(self, wave) -> builder:
        if self.fluent_builder:
            _ret = self.clone()
        else:
            _ret = self

        _ret.__waves.append(wave)
        return _ret

    def __check_waves_linking(self, wave: wave, wave_number: int):
        if len(self.__waves) >= wave_number:
            raise Exception(f"Wave {wave_number} is already setted")

        if len(self.__waves) < wave_number-1:
            raise Exception(
                f"Wave {wave_number-1} should be setted before wave {wave_number}")

        if not rules.EXx_eq_SWx1(self.__waves[wave_number-2],wave):
            raise Exception(
                f"Start of wave {wave_number} should be the same as end of wave {wave_number-1}")

    def __check_wave1(self, wave1: wave) -> Tuple[bool, List[str]]:
        error_list = []

        if len(self.__waves) >= 1:
            error_list.append("Wave 1 is already setted")

        if wave1.direction is None:
            error_list.append("Wave must have direction")

        return (len(error_list) == 0), error_list

    def add_wave1(self, wave1: wave) -> builder:
        return_status, error_list = self.__check_wave1(wave1)
        if return_status:
            return self.__add_wave(wave1)
        else:
            raise Exception("Wave adding check FAIL: \n" +
                            "\n".join([("- " + err) for err in error_list]))

    def try_add_wave1(self, wave1: wave) -> Tuple[bool, Union[List[str], builder]]:
        return_status, error_list = self.__check_wave1(wave1)
        if return_status:
            return True, self.__add_wave(wave1)
        return return_status, error_list

    def __check_wave2(self, wave2: wave) -> Tuple[bool, List[str]]:
        error_list = []
        self.__check_waves_linking(wave2, 2)

        if wave2.direction is None:
            error_list.append("Wave must have direction")
        else:
            if not rules.EW2_gt_SW1(self.get_wave(1), wave2, self.__direction):
                error_list.append("EW2 > SW1: FAIL")

        return (len(error_list) == 0), error_list

    def add_wave2(self, wave2: wave) -> builder:
        return_status, error_list = self.__check_wave2(wave2)
        if return_status:
            return self.__add_wave(wave2)
        else:
            raise Exception("Wave adding check FAIL: \n" +
                            "\n".join([("- " + err) for err in error_list]))

    def try_add_wave2(self, wave2: wave) -> Tuple[bool, Union[List[str], builder]]:
        return_status, error_list = self.__check_wave2(wave2)
        if return_status:
            return True, self.__add_wave(wave2)
        return return_status, error_list

    def __check_wave3(self, wave3: wave) -> Tuple[bool, List[str]]:
        error_list = []

        self.__check_waves_linking(wave3, 3)

        if wave3.direction is None:
            error_list.append("Wave must have direction")
        else:
            if not rules.EW3_gt_EW1(self.get_wave(1), wave3, self.__direction):
                error_list.append("EW3 > EW1: FAIL")

            if not rules.TWx_not_TWy_not_TWz([self.get_wave(1), self.get_wave(2), wave3]):
                error_list.append("TWx <> TWy <>TWz: FAIL")

        return (len(error_list) == 0), error_list

    def add_wave3(self, wave3: wave) -> builder:
        return_status, error_list = self.__check_wave3(wave3)
        if return_status:
            return self.__add_wave(wave3)
        else:
            raise Exception("Wave adding check FAIL: \n" +
                            "\n".join([("- " + err) for err in error_list]))

    def try_add_wave3(self, wave3: wave) -> Tuple[bool, Union[List[str], builder]]:
        return_status, error_list = self.__check_wave3(wave3)
        if return_status:
            return True, self.__add_wave(wave3)
        return return_status, error_list

    def __check_wave4(self, wave4: wave) -> Tuple[bool, List[str]]:
        error_list = []

        self.__check_waves_linking(wave4, 4)

        if wave4.direction is None:
            error_list.append("Wave must have direction")
        else:
            if not rules.EW4_gt_EW1(self.get_wave(1), wave4, self.__direction):
                error_list.append("EW4 > EW1: FAIL")

            if not rules.W2_dif_W4(self.get_wave(2), wave4):
                error_list.append("W2 different W4: FAIL")

            if not rules.TWx_not_TWy_not_TWz([self.get_wave(2), self.get_wave(3), wave4]):
                error_list.append("TWx <> TWy <>TWz: FAIL")

        return (len(error_list) == 0), error_list

    def add_wave4(self, wave4: wave) -> builder:
        return_status, error_list = self.__check_wave4(wave4)
        if return_status:
            return self.__add_wave(wave4)
        else:
            raise Exception("Wave adding check FAIL: \n" +
                            "\n".join([("- " + err) for err in error_list]))

    def try_add_wave4(self, wave4: wave) -> Tuple[bool, Union[List[str], builder]]:
        return_status, error_list = self.__check_wave4(wave4)
        if return_status:
            return True, self.__add_wave(wave4)
        return return_status, error_list

    def __check_wave5(self, wave5: wave) -> Tuple[bool, List[str]]:
        error_list = []

        self.__check_waves_linking(wave5, 5)

        if wave5.direction is None:
            error_list.append("Wave must have direction")
        else:
            if not rules.HW3_gt_HW1_or_HW3_gt_HW5(self.get_wave(1), self.get_wave(3), wave5):
                error_list.append("HW3 > HW1 || HW3 > HW5: FAIL")

            if not rules.EW5_gt_EW3(self.get_wave(3), wave5, self.__direction):
                error_list.append("EW5 > EW3: FAIL")

            if not rules.HWx_gt_HWy_and_HWx_gt_HWz(self.get_wave(1), self.get_wave(3), wave5):
                error_list.append("HWx >> HWy & HWx >> HWz: FAIL")

            if not rules.TWx_not_TWy_not_TWz([self.get_wave(3), self.get_wave(4), wave5]):
                error_list.append("TWx <> TWy <>TWz: FAIL")

        return (len(error_list) == 0), error_list

    def add_wave5(self, wave5: wave) -> builder:
        return_status, error_list = self.__check_wave5(wave5)
        if return_status:
            return self.__add_wave(wave5)
        else:
            raise Exception("Wave adding check FAIL: \n" +
                            "\n".join([("- " + err) for err in error_list]))

    def try_add_wave5(self, wave5: wave) -> Tuple[bool, Union[List[str], builder]]:
        return_status, error_list = self.__check_wave5(wave5)
        if return_status:
            return True, self.__add_wave(wave5)
        return return_status, error_list

    def add(self, wave: wave) -> builder:
        next = self.next_wave
        if next == 1:
            self.add_wave1(wave)
        elif next == 2:
            self.add_wave2(wave)
        elif next == 3:
            self.add_wave3(wave)
        elif next == 4:
            self.add_wave4(wave)
        elif next == 5:
            self.add_wave5(wave)
        else:
            raise Exception("All waves is setted")

    def try_add(self, wave: wave) -> Tuple[bool, Union[List[str], builder]]:
        next = self.next_wave
        if next == 1:
            return self.try_add_wave1(wave)
        elif next == 2:
            return self.try_add_wave2(wave)
        elif next == 3:
            return self.try_add_wave3(wave)
        elif next == 4:
            return self.try_add_wave4(wave)
        elif next == 5:
            return self.try_add_wave5(wave)
        else:
            return False, ["All waves is setted"]


class factory:
    def __init__(self, impulse_direction: direction) -> None:
        self.impulse_direction = impulse_direction
        pass

    def build(self, impulse_direction: direction = np.NaN, waves: List[wave] = [], fluent_builder=False) -> builder:
        if np.isnan(impulse_direction):
            impulse_direction = self.impulse_direction

        _ret = builder(impulse_direction, fluent_builder)
        for wave in waves:
            _ret.add(wave)
