from __future__ import annotations
from typing import List, Tuple, Union
from numpy import NaN
import numpy as np

from ...misc.direction import direction
from ...rules import rules
from ...misc.wave import wave


class builder_impulse_five:
    def __init__(self, impulse_direction: direction, fluent_builder=False) -> None:
        self.__wave1: wave = None
        self.__wave2: wave = None
        self.__wave3: wave = None
        self.__wave4: wave = None
        self.__wave5: wave = None
        self.__direction = impulse_direction
        self.fluent_builder = True
        pass

    @property
    def direction(self):
        return self.__direction
    
    def clone(self) -> builder_impulse_five:
        _ret = builder_impulse_five(self.direction, self.fluent_builder)
        _ret.__wave1 = self.__wave1
        _ret.__wave2 = self.__wave2
        _ret.__wave3 = self.__wave3
        _ret.__wave4 = self.__wave4
        _ret.__wave5 = self.__wave5
        return _ret

    def __add_wave(self, wave, number) -> builder_impulse_five:
        if self.fluent_builder:
            _ret = self.clone()
        else:
            _ret = self
            
        if number == 1:
            _ret.__wave1 = wave
        elif number == 2:
            _ret.__wave2 = wave
        elif number == 3:
            _ret.__wave3 = wave
        elif number == 4:
            _ret.__wave4 = wave
        elif number == 5:
            _ret.__wave5 = wave
        return _ret
    
    def __check_wave1(self, wave1: wave) -> Tuple[bool, List[str]]:
        error_list = []

        if self.__wave1 is not None:
            error_list.append("Wave 1 is already setted")

        if wave1.direction is None:
            error_list.append("Wave must have direction")
            
        return (len(error_list) == 0), error_list

    def add_wave1(self, wave1: wave) -> builder_impulse_five:
        return_status, error_list = self.__check_wave1(wave1)
        if return_status:
            return self.__add_wave(wave1,1)
        else:
            raise Exception("Wave adding check FAIL: \n" +
                            "\n".join([("- " + err) for err in error_list]))

    def try_add_wave1(self, wave1: wave) -> Tuple[bool, Union[List[str],builder_impulse_five]]:
        return_status, error_list = self.__check_wave1(wave1)
        if return_status:
            return True, self.__add_wave(wave1,1)
        return return_status, error_list

    def __check_wave2(self, wave2: wave) -> Tuple[bool, List[str]]:
        error_list = []

        if self.__wave2 is not None:
            raise Exception("Wave 2 is already setted")

        if self.__wave1 is None:
            raise Exception("Wave 1 should be setted before wave 2")
        
        if not self.__wave1.end.isEqual(wave2.start):
            raise Exception(
                "Start of wave 2 should be the same as end of wave 1")

        if wave2.direction is None:
            error_list.append("Wave must have direction")
        else:
            if not rules.EW2_gt_SW1(self.__wave1, wave2, self.__direction):
                error_list.append("EW2 > SW1: FAIL")

        return (len(error_list) == 0), error_list

    def add_wave2(self, wave2: wave)->builder_impulse_five:
        return_status, error_list = self.__check_wave2(wave2)
        if return_status:
            return self.__add_wave(wave2,2)
        else:
            raise Exception("Wave adding check FAIL: \n" +
                            "\n".join([("- " + err) for err in error_list]))

    def try_add_wave2(self, wave2: wave) -> Tuple[bool, Union[List[str],builder_impulse_five]]:
        return_status, error_list = self.__check_wave2(wave2)
        if return_status:
            return True, self.__add_wave(wave2,2)
        return return_status, error_list

    def __check_wave3(self, wave3: wave) -> Tuple[bool, List[str]]:
        error_list = []

        if self.__wave3 is not None:
            raise Exception("Wave 3 is already setted")

        if self.__wave2 is None:
            raise Exception("Wave 2 should be setted before wave 3")

        if not self.__wave2.end.isEqual(wave3.start):
            raise Exception(
                "Start of wave 3 should be the same as end of wave 2")
            
        if wave3.direction is None:
            error_list.append("Wave must have direction")
        else:
            if not rules.EW3_gt_EW1(self.__wave1, wave3, self.__direction):
                error_list.append("EW3 > EW1: FAIL")

            if not rules.TWx_not_TWy_not_TWz([self.__wave1, self.__wave2, wave3]):
                error_list.append("TWx <> TWy <>TWz: FAIL")

        return (len(error_list) == 0), error_list

    def add_wave3(self, wave3: wave)->builder_impulse_five:
        return_status, error_list = self.__check_wave3(wave3)
        if return_status:
            return self.__add_wave(wave3,3)
        else:
            raise Exception("Wave adding check FAIL: \n" +
                            "\n".join([("- " + err) for err in error_list]))

    def try_add_wave3(self, wave3: wave) -> Tuple[bool, Union[List[str],builder_impulse_five]]:
        return_status, error_list = self.__check_wave3(wave3)
        if return_status:
            return True, self.__add_wave(wave3,3)
        return return_status, error_list

    def __check_wave4(self, wave4: wave) -> Tuple[bool, List[str]]:
        error_list = []

        if self.__wave4 is not None:
            raise Exception("Wave 4 is already setted")

        if self.__wave3 is None:
            raise Exception("Wave 3 should be setted before wave 4")

        if not self.__wave3.end.isEqual(wave4.start):
            raise Exception(
                "Start of wave 4 should be the same as end of wave 3")
            
        if wave4.direction is None:
            error_list.append("Wave must have direction")
        else:
            if not rules.EW4_gt_EW1(self.__wave1, wave4, self.__direction):
                error_list.append("EW4 > EW1: FAIL")

            if not rules.W2_dif_W4(self.__wave2, wave4):
                error_list.append("W2 different W4: FAIL")

            if not rules.TWx_not_TWy_not_TWz([self.__wave2, self.__wave3, wave4]):
                error_list.append("TWx <> TWy <>TWz: FAIL")

        return (len(error_list) == 0), error_list

    def add_wave4(self, wave4: wave)->builder_impulse_five:
        return_status, error_list = self.__check_wave4(wave4)
        if return_status:
            return self.__add_wave(wave4,4)
        else:
            raise Exception("Wave adding check FAIL: \n" +
                            "\n".join([("- " + err) for err in error_list]))

    def try_add_wave4(self, wave4: wave) -> Tuple[bool, Union[List[str],builder_impulse_five]]:
        return_status, error_list = self.__check_wave4(wave4)
        if return_status:
            return True, self.__add_wave(wave4,4)
        return return_status, error_list

    def __check_wave5(self, wave5: wave) -> Tuple[bool, List[str]]:
        error_list = []

        if self.__wave5 is not None:
            raise Exception("Wave 5 is already setted")

        if self.__wave4 is None:
            raise Exception("Wave 4 should be setted before wave 5")

        if not self.__wave4.end.isEqual(wave5.start):
            raise Exception(
                "Start of wave 5 should be the same as end of wave 4")

        if wave5.direction is None:
            error_list.append("Wave must have direction")
        else:
            if not rules.HW3_gt_HW1_or_HW3_gt_HW5(self.__wave1, self.__wave3, wave5):
                error_list.append("HW3 > HW1 || HW3 > HW5: FAIL")

            if not rules.EW5_gt_EW3(self.__wave3, wave5, self.__direction):
                error_list.append("EW5 > EW3: FAIL")

            if not rules.HWx_gt_HWy_and_HWx_gt_HWz(self.__wave1, self.__wave3, wave5):
                error_list.append("HWx >> HWy & HWx >> HWz: FAIL")

            if not rules.TWx_not_TWy_not_TWz([self.__wave3, self.__wave4, wave5]):
                error_list.append("TWx <> TWy <>TWz: FAIL")

        return (len(error_list) == 0), error_list

    def add_wave5(self, wave5: wave)->builder_impulse_five:
        return_status, error_list = self.__check_wave5(wave5)
        if return_status:
            return self.__add_wave(wave5,5)
        else:
            raise Exception("Wave adding check FAIL: \n" +
                            "\n".join([("- " + err) for err in error_list]))

    def try_add_wave5(self, wave5: wave) -> Tuple[bool, Union[List[str],builder_impulse_five]]:
        return_status, error_list = self.__check_wave5(wave5)
        if return_status:
            return True, self.__add_wave(wave5,5)
        return return_status, error_list

    def get_wave(self,wave_number:int)->wave:
        if wave_number == 1: return self.__wave1
        elif wave_number == 2: return self.__wave2
        elif wave_number == 3: return self.__wave3
        elif wave_number == 4: return self.__wave4
        elif wave_number == 5: return self.__wave5
    
        raise Exception("Wrong wave number")
    
    @property
    def next_wave(self) -> int:
        if self.__wave1 is None:
            return 1
        elif self.__wave2 is None:
            return 2
        elif self.__wave3 is None:
            return 3
        elif self.__wave4 is None:
            return 4
        elif self.__wave5 is None:
            return 5
        else:
            return -1

    def add(self, wave: wave)->builder_impulse_five:
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

    def try_add(self, wave: wave) -> Tuple[bool, Union[List[str],builder_impulse_five]]:
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

    def next_wave_direction(self) -> direction:
        next_wave = self.next_wave
        if next_wave <= 0:
            raise Exception("All waves is setted")

        if next_wave % 2 == 0:
            return self.direction.revers()
        else:
            return self.direction
    
    @property
    def isComplete(self)->bool:
        return self.next_wave <= 0


class factory_impulse_five:
    def __init__(self, impulse_direction: direction) -> None:
        self.impulse_direction = impulse_direction
        pass

    def build(self, impulse_direction: direction = np.NaN, waves: List[wave] = [], fluent_builder = False) -> builder_impulse_five:
        if np.isnan(impulse_direction):
            impulse_direction = self.impulse_direction

        _ret = builder_impulse_five(impulse_direction,fluent_builder)
        for wave in waves:
            _ret.add(wave)
