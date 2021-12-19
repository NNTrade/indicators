from typing import List, Tuple
from numpy import NaN
import numpy as np

from src.ElliotWaves.direction import direction
from ...rules import rules
from ...wave import wave

class impulse_five:
    def __init__(self, impulse_direction: direction) -> None:
        self.__wave1 = NaN
        self.__wave2 = NaN
        self.__wave3 = NaN
        self.__wave4 = NaN
        self.__wave5 = NaN
        self.__direction = impulse_direction
        pass

    @property
    def direction(self):
        return self.__direction

    def __check_wave1(self, wave1:wave)->Tuple[bool, List[str]]:
        error_list = []

        if not np.isnan(self.__wave1):
            error_list.append("Wave 1 is already setted")

        return (len(error_list)==0), error_list

    def add_wave1(self, wave1:wave):
        return_status, error_list = self.__check_wave1(wave1)
        if return_status:
            self.__wave1 = wave1
        else:
            raise Exception("Wave adding check FAIL: \n" +
                            "\n".join([("- " + err) for err in error_list]))
    
    def try_add_wave1(self, wave1:wave)->Tuple[bool,List[str]]:
        return_status, error_list = self.__check_wave1(wave1)
        if return_status:
            self.__wave1 = wave1
        return return_status, error_list

    def __check_wave2(self,wave2:wave)->Tuple[bool, List[str]]:
        error_list = []
        
        if not np.isnan(self.__wave2):
            raise Exception("Wave 2 is already setted")
        
        if np.isnan(self.__wave1):
            raise Exception("Wave 1 should be setted before wave 2")
                
        if not rules.EW2_gt_SW1(self.__wave1,wave2,self.__direction):
            error_list.append("EW2 > SW1: FAIL")

        return (len(error_list)==0), error_list

    def add_wave2(self, wave2:wave):
        return_status, error_list = self.__check_wave2(wave2)
        if return_status:
            self.__wave2 = wave2
        else:
            raise Exception("Wave adding check FAIL: \n" +
                            "\n".join([("- " + err) for err in error_list]))

    def try_add_wave2(self, wave2:wave)->Tuple[bool,List[str]]:
        return_status, error_list = self.__check_wave2(wave2)
        if return_status:
            self.__wave2 = wave2
        return return_status, error_list

    def __check_wave3(self,wave3:wave)->Tuple[bool, List[str]]:
        error_list = []

        if not np.isnan(self.__wave3):
            raise Exception("Wave 3 is already setted")
        
        if np.isnan(self.__wave2):
            raise Exception("Wave 2 should be setted before wave 3")
        
        if not rules.EW3_gt_EW1(self.__wave1, wave3,self.direction):
            error_list.append("EW3 > EW1: FAIL")

        if not rules.TWx_not_TWy_not_TWz([self.__wave1,self.__wave2,self.__wave3]):
            error_list.append("TWx <> TWy <>TWz: FAIL")

        return (len(error_list)==0), error_list

    def add_wave3(self, wave3:wave):
        return_status, error_list = self.__check_wave3(wave3)
        if return_status:
            self.__wave3 = wave3
        else:
            raise Exception("Wave adding check FAIL: \n" +
                            "\n".join([("- " + err) for err in error_list]))

    def try_add_wave3(self, wave3:wave)->Tuple[bool,List[str]]:
        return_status, error_list = self.__check_wave3(wave3)
        if return_status:
            self.__wave3 = wave3
        return return_status, error_list

    def __check_wave4(self,wave4:wave)->Tuple[bool, List[str]]:
        error_list = []

        if not np.isnan(self.__wave4):
            raise Exception("Wave 4 is already setted")
        
        if np.isnan(self.__wave3):
            raise Exception("Wave 3 should be setted before wave 4")
        
        if not rules.EW4_gt_EW1(self.__wave1, wave4):
            error_list.append("EW4 > EW1: FAIL")
        
        if not rules.W2_dif_W4(self.__wave2, wave4):
            error_list.append("W2 different W4: FAIL")

        if not rules.TWx_not_TWy_not_TWz([self.__wave2,self.__wave3,self.__wave4]):
            error_list.append("TWx <> TWy <>TWz: FAIL")

        return (len(error_list)==0), error_list

    def add_wave4(self, wave4:wave):
        return_status, error_list = self.__check_wave4(wave4)
        if return_status:
            self.__wave4 = wave4
        else:
            raise Exception("Wave adding check FAIL: \n" +
                            "\n".join([("- " + err) for err in error_list]))

    def try_add_wave4(self, wave4:wave)->Tuple[bool,List[str]]:
        return_status, error_list = self.__check_wave4(wave4)
        if return_status:
            self.__wave4 = wave4
        return return_status, error_list

    def __check_wave5(self,wave5:wave)->Tuple[bool, List[str]]:
        error_list = []

        if not np.isnan(self.__wave5):
            raise Exception("Wave 5 is already setted")
        
        if np.isnan(self.__wave4):
            raise Exception("Wave 4 should be setted before wave 5")
        
        if not rules.HW3_gt_HW1_or_HW3_gt_HW5(self.__wave1,self.__wave3, wave5):
            error_list.append("HW3 > HW1 || HW3 > HW5: FAIL")

        if not rules.EW5_gt_EW3(self.__wave3, wave5, self.direction):
            error_list.append("EW5 > EW3: FAIL")

        if not rules.HWx_gt_HWy_and_HWx_gt_HWz(self.__wave1, self.__wave3, self.__wave5):
            error_list.append("HWx >> HWy & HWx >> HWz: FAIL")

        if not rules.TWx_not_TWy_not_TWz([self.__wave3,self.__wave4,self.__wave5]):
            error_list.append("TWx <> TWy <>TWz: FAIL")

        return (len(error_list)==0), error_list

    def add_wave5(self, wave5:wave):
        return_status, error_list = self.__check_wave5(wave5)
        if return_status:
            self.__wave5 = wave5
        else:
            raise Exception("Wave adding check FAIL: \n" +
                            "\n".join([("- " + err) for err in error_list]))

    def try_add_wave5(self, wave5:wave)->Tuple[bool,List[str]]:
        return_status, error_list = self.__check_wave5(wave5)
        if return_status:
            self.__wave5 = wave5
        return return_status, error_list


    