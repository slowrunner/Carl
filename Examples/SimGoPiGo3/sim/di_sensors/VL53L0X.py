# https://www.dexterindustries.com
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/DI_Sensors/blob/master/LICENSE.md
#
# Python drivers for the VL53L0X laser distance sensor

from __future__ import print_function
from __future__ import division

import di_i2c
import time

# Constants
SYSRANGE_START                              = 0x00

SYSTEM_THRESH_HIGH                          = 0x0C
SYSTEM_THRESH_LOW                           = 0x0E

SYSTEM_SEQUENCE_CONFIG                      = 0x01
SYSTEM_RANGE_CONFIG                         = 0x09
SYSTEM_INTERMEASUREMENT_PERIOD              = 0x04

SYSTEM_INTERRUPT_CONFIG_GPIO                = 0x0A

GPIO_HV_MUX_ACTIVE_HIGH                     = 0x84

SYSTEM_INTERRUPT_CLEAR                      = 0x0B

RESULT_INTERRUPT_STATUS                     = 0x13
RESULT_RANGE_STATUS                         = 0x14

RESULT_CORE_AMBIENT_WINDOW_EVENTS_RTN       = 0xBC
RESULT_CORE_RANGING_TOTAL_EVENTS_RTN        = 0xC0
RESULT_CORE_AMBIENT_WINDOW_EVENTS_REF       = 0xD0
RESULT_CORE_RANGING_TOTAL_EVENTS_REF        = 0xD4
RESULT_PEAK_SIGNAL_RATE_REF                 = 0xB6

ALGO_PART_TO_PART_RANGE_OFFSET_MM           = 0x28

I2C_SLAVE_DEVICE_ADDRESS                    = 0x8A

MSRC_CONFIG_CONTROL                         = 0x60

PRE_RANGE_CONFIG_MIN_SNR                    = 0x27
PRE_RANGE_CONFIG_VALID_PHASE_LOW            = 0x56
PRE_RANGE_CONFIG_VALID_PHASE_HIGH           = 0x57
PRE_RANGE_MIN_COUNT_RATE_RTN_LIMIT          = 0x64

FINAL_RANGE_CONFIG_MIN_SNR                  = 0x67
FINAL_RANGE_CONFIG_VALID_PHASE_LOW          = 0x47
FINAL_RANGE_CONFIG_VALID_PHASE_HIGH         = 0x48
FINAL_RANGE_CONFIG_MIN_COUNT_RATE_RTN_LIMIT = 0x44

PRE_RANGE_CONFIG_SIGMA_THRESH_HI            = 0x61
PRE_RANGE_CONFIG_SIGMA_THRESH_LO            = 0x62

PRE_RANGE_CONFIG_VCSEL_PERIOD               = 0x50
PRE_RANGE_CONFIG_TIMEOUT_MACROP_HI          = 0x51
PRE_RANGE_CONFIG_TIMEOUT_MACROP_LO          = 0x52

SYSTEM_HISTOGRAM_BIN                        = 0x81
HISTOGRAM_CONFIG_INITIAL_PHASE_SELECT       = 0x33
HISTOGRAM_CONFIG_READOUT_CTRL               = 0x55

FINAL_RANGE_CONFIG_VCSEL_PERIOD             = 0x70
FINAL_RANGE_CONFIG_TIMEOUT_MACROP_HI        = 0x71
FINAL_RANGE_CONFIG_TIMEOUT_MACROP_LO        = 0x72
CROSSTALK_COMPENSATION_PEAK_RATE_MCPS       = 0x20

MSRC_CONFIG_TIMEOUT_MACROP                  = 0x46

SOFT_RESET_GO2_SOFT_RESET_N                 = 0xBF
IDENTIFICATION_MODEL_ID                     = 0xC0
IDENTIFICATION_REVISION_ID                  = 0xC2

OSC_CALIBRATE_VAL                           = 0xF8

GLOBAL_CONFIG_VCSEL_WIDTH                   = 0x32
GLOBAL_CONFIG_SPAD_ENABLES_REF_0            = 0xB0
GLOBAL_CONFIG_SPAD_ENABLES_REF_1            = 0xB1
GLOBAL_CONFIG_SPAD_ENABLES_REF_2            = 0xB2
GLOBAL_CONFIG_SPAD_ENABLES_REF_3            = 0xB3
GLOBAL_CONFIG_SPAD_ENABLES_REF_4            = 0xB4
GLOBAL_CONFIG_SPAD_ENABLES_REF_5            = 0xB5

GLOBAL_CONFIG_REF_EN_START_SELECT           = 0xB6
DYNAMIC_SPAD_NUM_REQUESTED_REF_SPAD         = 0x4E
DYNAMIC_SPAD_REF_EN_START_OFFSET            = 0x4F
POWER_MANAGEMENT_GO1_POWER_FORCE            = 0x80

VHV_CONFIG_PAD_SCL_SDA__EXTSUP_HV           = 0x89

ALGO_PHASECAL_LIM                           = 0x30
ALGO_PHASECAL_CONFIG_TIMEOUT                = 0x30

ADDRESS_DEFAULT = 0x29


class VL53L0X(object):
    """Drivers for VL53L0X laser distance sensor"""

    VcselPeriodPreRange   = 0
    VcselPeriodFinalRange = 1

    # "global variables"
    io_timeout = 0
    did_timeout = False

    # The I2C address is software programmable (volatile), and defaults to 0x52 >> 1 = 0x29.
    # __init__ changes the address (default to 0x54 >> 1 = 0x2A) to prevent conflicts.
    ADDRESS = ADDRESS_DEFAULT

    def __init__(self, address = 0x2A, timeout = 0.5, bus = "RPI_1SW"):
        self.i2c_bus = di_i2c.DI_I2C(bus = bus, address = address)

        try:
            self.i2c_bus.write_reg_8(SOFT_RESET_GO2_SOFT_RESET_N, 0x00) # try resetting from 0x2A
            time.sleep(0.002)
        except IOError:
            pass

        self.ADDRESS = ADDRESS_DEFAULT
        self.i2c_bus.set_address(self.ADDRESS)
        self.i2c_bus.write_reg_8(SOFT_RESET_GO2_SOFT_RESET_N, 0x00) # reset default 0x29

        time.sleep(0.005)
        # delay added because threaded instantiation would fail,even with mutex in place

        self.i2c_bus.write_reg_8(SOFT_RESET_GO2_SOFT_RESET_N, 0x01) # release reset

        time.sleep(0.005)
       # delay added because threaded instantiation would fail,even with mutex in place

        self.set_address(address)

        self.init()                   # initialize the sensor
        self.set_timeout(timeout)     # set the timeout

    def set_address(self, address):
        address &= 0x7f
        try:
            self.i2c_bus.write_reg_8(I2C_SLAVE_DEVICE_ADDRESS, address)
            self.ADDRESS = address
            self.i2c_bus.set_address(self.ADDRESS)
        except IOError:
            self.i2c_bus.set_address(address)
            self.i2c_bus.write_reg_8(I2C_SLAVE_DEVICE_ADDRESS, address)
            self.ADDRESS = address
            self.i2c_bus.set_address(self.ADDRESS)

    def init(self):
        self.i2c_bus.write_reg_8(VHV_CONFIG_PAD_SCL_SDA__EXTSUP_HV, (self.i2c_bus.read_8(VHV_CONFIG_PAD_SCL_SDA__EXTSUP_HV) | 0x01)) # set bit 0

        # "Set I2C standard mode"
        self.i2c_bus.write_reg_8(0x88, 0x00)

        self.i2c_bus.write_reg_8(0x80, 0x01)
        self.i2c_bus.write_reg_8(0xFF, 0x01)
        self.i2c_bus.write_reg_8(0x00, 0x00)
        self.stop_variable = self.i2c_bus.read_8(0x91)
        self.i2c_bus.write_reg_8(0x00, 0x01)
        self.i2c_bus.write_reg_8(0xFF, 0x00)
        self.i2c_bus.write_reg_8(0x80, 0x00)

        # disable SIGNAL_RATE_MSRC (bit 1) and SIGNAL_RATE_PRE_RANGE (bit 4) limit checks
        self.i2c_bus.write_reg_8(MSRC_CONFIG_CONTROL, (self.i2c_bus.read_8(MSRC_CONFIG_CONTROL) | 0x12))

        # set final range signal rate limit to 0.25 MCPS (million counts per second)
        self.set_signal_rate_limit(0.25)

        self.i2c_bus.write_reg_8(SYSTEM_SEQUENCE_CONFIG, 0xFF)

        # VL53L0X_DataInit() end

        # VL53L0X_StaticInit() begin

        spad_count, spad_type_is_aperture, success = self.get_spad_info()
        if not success:
            return False

        # The SPAD map (RefGoodSpadMap) is read by VL53L0X_get_info_from_device() in
        # the API, but the same data seems to be more easily readable from
        # GLOBAL_CONFIG_SPAD_ENABLES_REF_0 through _6, so read it from there
        ref_spad_map = self.i2c_bus.read_list(GLOBAL_CONFIG_SPAD_ENABLES_REF_0, 6)

        # -- VL53L0X_set_reference_spads() begin (assume NVM values are valid)

        self.i2c_bus.write_reg_8(0xFF, 0x01)
        self.i2c_bus.write_reg_8(DYNAMIC_SPAD_REF_EN_START_OFFSET, 0x00)
        self.i2c_bus.write_reg_8(DYNAMIC_SPAD_NUM_REQUESTED_REF_SPAD, 0x2C)
        self.i2c_bus.write_reg_8(0xFF, 0x00)
        self.i2c_bus.write_reg_8(GLOBAL_CONFIG_REF_EN_START_SELECT, 0xB4)

        if spad_type_is_aperture:
            first_spad_to_enable = 12 # 12 is the first aperture spad
        else:
            first_spad_to_enable = 0

        spads_enabled = 0

        for i in range(48):
            if i < first_spad_to_enable or spads_enabled == spad_count:
                # This bit is lower than the first one that should be enabled, or
                # (reference_spad_count) bits have already been enabled, so zero this bit
                ref_spad_map[int(i / 8)] &= ~(1 << (i % 8))
            elif (ref_spad_map[int(i / 8)] >> (i % 8)) & 0x1:
                spads_enabled += 1

        self.i2c_bus.write_reg_list(GLOBAL_CONFIG_SPAD_ENABLES_REF_0, ref_spad_map)

        # -- VL53L0X_set_reference_spads() end

        # -- VL53L0X_load_tuning_settings() begin
        # DefaultTuningSettings from vl53l0x_tuning.h

        self.i2c_bus.write_reg_8(0xFF, 0x01)
        self.i2c_bus.write_reg_8(0x00, 0x00)

        self.i2c_bus.write_reg_8(0xFF, 0x00)
        self.i2c_bus.write_reg_8(0x09, 0x00)
        self.i2c_bus.write_reg_8(0x10, 0x00)
        self.i2c_bus.write_reg_8(0x11, 0x00)

        self.i2c_bus.write_reg_8(0x24, 0x01)
        self.i2c_bus.write_reg_8(0x25, 0xFF)
        self.i2c_bus.write_reg_8(0x75, 0x00)

        self.i2c_bus.write_reg_8(0xFF, 0x01)
        self.i2c_bus.write_reg_8(0x4E, 0x2C)
        self.i2c_bus.write_reg_8(0x48, 0x00)
        self.i2c_bus.write_reg_8(0x30, 0x20)

        self.i2c_bus.write_reg_8(0xFF, 0x00)
        self.i2c_bus.write_reg_8(0x30, 0x09)
        self.i2c_bus.write_reg_8(0x54, 0x00)
        self.i2c_bus.write_reg_8(0x31, 0x04)
        self.i2c_bus.write_reg_8(0x32, 0x03)
        self.i2c_bus.write_reg_8(0x40, 0x83)
        self.i2c_bus.write_reg_8(0x46, 0x25)
        self.i2c_bus.write_reg_8(0x60, 0x00)
        self.i2c_bus.write_reg_8(0x27, 0x00)
        self.i2c_bus.write_reg_8(0x50, 0x06)
        self.i2c_bus.write_reg_8(0x51, 0x00)
        self.i2c_bus.write_reg_8(0x52, 0x96)
        self.i2c_bus.write_reg_8(0x56, 0x08)
        self.i2c_bus.write_reg_8(0x57, 0x30)
        self.i2c_bus.write_reg_8(0x61, 0x00)
        self.i2c_bus.write_reg_8(0x62, 0x00)
        self.i2c_bus.write_reg_8(0x64, 0x00)
        self.i2c_bus.write_reg_8(0x65, 0x00)
        self.i2c_bus.write_reg_8(0x66, 0xA0)

        self.i2c_bus.write_reg_8(0xFF, 0x01)
        self.i2c_bus.write_reg_8(0x22, 0x32)
        self.i2c_bus.write_reg_8(0x47, 0x14)
        self.i2c_bus.write_reg_8(0x49, 0xFF)
        self.i2c_bus.write_reg_8(0x4A, 0x00)

        self.i2c_bus.write_reg_8(0xFF, 0x00)
        self.i2c_bus.write_reg_8(0x7A, 0x0A)
        self.i2c_bus.write_reg_8(0x7B, 0x00)
        self.i2c_bus.write_reg_8(0x78, 0x21)

        self.i2c_bus.write_reg_8(0xFF, 0x01)
        self.i2c_bus.write_reg_8(0x23, 0x34)
        self.i2c_bus.write_reg_8(0x42, 0x00)
        self.i2c_bus.write_reg_8(0x44, 0xFF)
        self.i2c_bus.write_reg_8(0x45, 0x26)
        self.i2c_bus.write_reg_8(0x46, 0x05)
        self.i2c_bus.write_reg_8(0x40, 0x40)
        self.i2c_bus.write_reg_8(0x0E, 0x06)
        self.i2c_bus.write_reg_8(0x20, 0x1A)
        self.i2c_bus.write_reg_8(0x43, 0x40)

        self.i2c_bus.write_reg_8(0xFF, 0x00)
        self.i2c_bus.write_reg_8(0x34, 0x03)
        self.i2c_bus.write_reg_8(0x35, 0x44)

        self.i2c_bus.write_reg_8(0xFF, 0x01)
        self.i2c_bus.write_reg_8(0x31, 0x04)
        self.i2c_bus.write_reg_8(0x4B, 0x09)
        self.i2c_bus.write_reg_8(0x4C, 0x05)
        self.i2c_bus.write_reg_8(0x4D, 0x04)

        self.i2c_bus.write_reg_8(0xFF, 0x00)
        self.i2c_bus.write_reg_8(0x44, 0x00)
        self.i2c_bus.write_reg_8(0x45, 0x20)
        self.i2c_bus.write_reg_8(0x47, 0x08)
        self.i2c_bus.write_reg_8(0x48, 0x28)
        self.i2c_bus.write_reg_8(0x67, 0x00)
        self.i2c_bus.write_reg_8(0x70, 0x04)
        self.i2c_bus.write_reg_8(0x71, 0x01)
        self.i2c_bus.write_reg_8(0x72, 0xFE)
        self.i2c_bus.write_reg_8(0x76, 0x00)
        self.i2c_bus.write_reg_8(0x77, 0x00)

        self.i2c_bus.write_reg_8(0xFF, 0x01)
        self.i2c_bus.write_reg_8(0x0D, 0x01)

        self.i2c_bus.write_reg_8(0xFF, 0x00)
        self.i2c_bus.write_reg_8(0x80, 0x01)
        self.i2c_bus.write_reg_8(0x01, 0xF8)

        self.i2c_bus.write_reg_8(0xFF, 0x01)
        self.i2c_bus.write_reg_8(0x8E, 0x01)
        self.i2c_bus.write_reg_8(0x00, 0x01)
        self.i2c_bus.write_reg_8(0xFF, 0x00)
        self.i2c_bus.write_reg_8(0x80, 0x00)

        # -- VL53L0X_load_tuning_settings() end

        # "Set interrupt config to new sample ready"
        # -- VL53L0X_SetGpioConfig() begin

        self.i2c_bus.write_reg_8(SYSTEM_INTERRUPT_CONFIG_GPIO, 0x04)
        self.i2c_bus.write_reg_8(GPIO_HV_MUX_ACTIVE_HIGH, self.i2c_bus.read_8(GPIO_HV_MUX_ACTIVE_HIGH) & ~0x10) # active low
        self.i2c_bus.write_reg_8(SYSTEM_INTERRUPT_CLEAR, 0x01)

        # -- VL53L0X_SetGpioConfig() end

        self.measurement_timing_budget_us = self.get_measurement_timing_budget()

        # "Disable MSRC and TCC by default"
        # MSRC = Minimum Signal Rate Check
        # TCC = Target CentreCheck
        # -- VL53L0X_SetSequenceStepEnable() begin

        self.i2c_bus.write_reg_8(SYSTEM_SEQUENCE_CONFIG, 0xE8)

        # -- VL53L0X_SetSequenceStepEnable() end

        # "Recalculate timing budget"
        self.set_measurement_timing_budget(self.measurement_timing_budget_us)

        # VL53L0X_StaticInit() end

        # VL53L0X_PerformRefCalibration() begin (VL53L0X_perform_ref_calibration())

        # -- VL53L0X_perform_vhv_calibration() begin

        self.i2c_bus.write_reg_8(SYSTEM_SEQUENCE_CONFIG, 0x01)
        if not self.perform_single_ref_calibration(0x40):
            return False

        # -- VL53L0X_perform_vhv_calibration() end

        # -- VL53L0X_perform_phase_calibration() begin

        self.i2c_bus.write_reg_8(SYSTEM_SEQUENCE_CONFIG, 0x02)
        if not self.perform_single_ref_calibration(0x00):
            return False

        # -- VL53L0X_perform_phase_calibration() end

        # "restore the previous Sequence Config"
        self.i2c_bus.write_reg_8(SYSTEM_SEQUENCE_CONFIG, 0xE8)

        # VL53L0X_PerformRefCalibration() end

        return True

# duplicate method
    # def set_signal_rate_limit(self, limit_Mcps):
    #     if (limit_Mcps < 0 or limit_Mcps > 511.99):
    #         return False

    #     # Q9.7 fixed point format (9 integer bits, 7 fractional bits)
    #     self.i2c_bus.write_reg_16(FINAL_RANGE_CONFIG_MIN_COUNT_RATE_RTN_LIMIT, int(limit_Mcps * (1 << 7)))
    #     return True

    # Get reference SPAD (single photon avalanche diode) count and type
    # based on VL53L0X_get_info_from_device(),
    # but only gets reference SPAD count and type
    def get_spad_info(self):
        self.i2c_bus.write_reg_8(0x80, 0x01)
        self.i2c_bus.write_reg_8(0xFF, 0x01)
        self.i2c_bus.write_reg_8(0x00, 0x00)

        self.i2c_bus.write_reg_8(0xFF, 0x06)
        self.i2c_bus.write_reg_8(0x83, self.i2c_bus.read_8(0x83) | 0x04)
        self.i2c_bus.write_reg_8(0xFF, 0x07)
        self.i2c_bus.write_reg_8(0x81, 0x01)

        self.i2c_bus.write_reg_8(0x80, 0x01)

        self.i2c_bus.write_reg_8(0x94, 0x6b)
        self.i2c_bus.write_reg_8(0x83, 0x00)
        self.start_timeout()
        while (self.i2c_bus.read_8(0x83) == 0x00):
            if (self.check_timeout_expired()):
                return 0, 0, False

        self.i2c_bus.write_reg_8(0x83, 0x01)
        tmp = self.i2c_bus.read_8(0x92)

        count = tmp & 0x7f
        type_is_aperture = (tmp >> 7) & 0x01

        self.i2c_bus.write_reg_8(0x81, 0x00)
        self.i2c_bus.write_reg_8(0xFF, 0x06)
        self.i2c_bus.write_reg_8(0x83, self.i2c_bus.read_8(0x83) & ~0x04)
        self.i2c_bus.write_reg_8(0xFF, 0x01)
        self.i2c_bus.write_reg_8(0x00, 0x01)

        self.i2c_bus.write_reg_8(0xFF, 0x00)
        self.i2c_bus.write_reg_8(0x80, 0x00)

        return count, type_is_aperture, True

    # Check if timeout is enabled (set to nonzero value) and has expired
    def check_timeout_expired(self):
        if(self.io_timeout > 0 and (time.time() - self.timeout_start) > self.io_timeout):
            return True
        return False

    # Record the current time to check an upcoming timeout against
    def start_timeout(self):
        self.timeout_start = time.time()


    #SequenceStepEnables = {"tcc":0, "msrc":0, "dss":0, "pre_range":0, "final_range":0}
    #SequenceStepTimeouts = {"pre_range_vcsel_period_pclks":0, "final_range_vcsel_period_pclks":0, "msrc_dss_tcc_mclks":0, "pre_range_mclks":0, "final_range_mclks":0, "msrc_dss_tcc_us":0, "pre_range_us":0, "final_range_us":0}



    # Get the measurement timing budget in microseconds
    # based on VL53L0X_get_measurement_timing_budget_micro_seconds()
    # in us
    def get_measurement_timing_budget(self):

        StartOverhead      = 1910 # note that this is different than the value in set_
        EndOverhead        = 960
        MsrcOverhead       = 660
        TccOverhead        = 590
        DssOverhead        = 690
        PreRangeOverhead   = 660
        FinalRangeOverhead = 550

        # "Start and end overhead times always present"
        budget_us = StartOverhead + EndOverhead

        enables = self.get_sequence_step_enables()
        timeouts = self.get_sequence_step_timeouts(enables["pre_range"])

        if (enables["tcc"]):
            budget_us += (timeouts["msrc_dss_tcc_us"] + TccOverhead)

        if (enables["dss"]):
            budget_us += 2 * (timeouts["msrc_dss_tcc_us"] + DssOverhead)
        elif (enables["msrc"]):
            budget_us += (timeouts["msrc_dss_tcc_us"] + MsrcOverhead)

        if (enables["pre_range"]):
            budget_us += (timeouts["pre_range_us"] + PreRangeOverhead)

        if (enables["final_range"]):
            budget_us += (timeouts["final_range_us"] + FinalRangeOverhead)

        self.measurement_timing_budget_us = budget_us # store for internal reuse
        return budget_us

    # Get sequence step enables
    # based on VL53L0X_get_sequence_step_enables()
    def get_sequence_step_enables(self):
        sequence_config = self.i2c_bus.read_8(SYSTEM_SEQUENCE_CONFIG)
        SequenceStepEnables = {"tcc":0, "msrc":0, "dss":0, "pre_range":0, "final_range":0}
        SequenceStepEnables["tcc"]         = (sequence_config >> 4) & 0x1
        SequenceStepEnables["dss"]         = (sequence_config >> 3) & 0x1
        SequenceStepEnables["msrc"]        = (sequence_config >> 2) & 0x1
        SequenceStepEnables["pre_range"]   = (sequence_config >> 6) & 0x1
        SequenceStepEnables["final_range"] = (sequence_config >> 7) & 0x1
        return SequenceStepEnables

    # Get sequence step timeouts
    # based on get_sequence_step_timeout(),
    # but gets all timeouts instead of just the requested one, and also stores
    # intermediate values
    def get_sequence_step_timeouts(self, pre_range):
        SequenceStepTimeouts = {"pre_range_vcsel_period_pclks":0, "final_range_vcsel_period_pclks":0, "msrc_dss_tcc_mclks":0, "pre_range_mclks":0, "final_range_mclks":0, "msrc_dss_tcc_us":0, "pre_range_us":0, "final_range_us":0}
        SequenceStepTimeouts["pre_range_vcsel_period_pclks"] = self.get_vcsel_pulse_period(self.VcselPeriodPreRange)

        SequenceStepTimeouts["msrc_dss_tcc_mclks"] = self.i2c_bus.read_8(MSRC_CONFIG_TIMEOUT_MACROP) + 1
        SequenceStepTimeouts["msrc_dss_tcc_us"] = self.timeout_mclks_to_microseconds(SequenceStepTimeouts["msrc_dss_tcc_mclks"], SequenceStepTimeouts["pre_range_vcsel_period_pclks"])

        SequenceStepTimeouts["pre_range_mclks"] = self.decode_timeout(self.i2c_bus.read_16(PRE_RANGE_CONFIG_TIMEOUT_MACROP_HI))
        SequenceStepTimeouts["pre_range_us"] = self.timeout_mclks_to_microseconds(SequenceStepTimeouts["pre_range_mclks"], SequenceStepTimeouts["pre_range_vcsel_period_pclks"])

        SequenceStepTimeouts["final_range_vcsel_period_pclks"] = self.get_vcsel_pulse_period(self.VcselPeriodFinalRange)

        SequenceStepTimeouts["final_range_mclks"] = self.decode_timeout(self.i2c_bus.read_16(FINAL_RANGE_CONFIG_TIMEOUT_MACROP_HI))

        if (pre_range):
            SequenceStepTimeouts["final_range_mclks"] -= SequenceStepTimeouts["pre_range_mclks"]

        SequenceStepTimeouts["final_range_us"] = self.timeout_mclks_to_microseconds(SequenceStepTimeouts["final_range_mclks"], SequenceStepTimeouts["final_range_vcsel_period_pclks"])

        return SequenceStepTimeouts

    # Decode VCSEL (vertical cavity surface emitting laser) pulse period in PCLKs
    # from register value
    # based on VL53L0X_decode_vcsel_period()
    def decode_vcsel_period(self, reg_val):
        return (((reg_val) + 1) << 1)

    # Get the VCSEL pulse period in PCLKs for the given period type.
    # based on VL53L0X_get_vcsel_pulse_period()
    def get_vcsel_pulse_period(self, type):
        if type == self.VcselPeriodPreRange:
            return self.decode_vcsel_period(self.i2c_bus.read_8(PRE_RANGE_CONFIG_VCSEL_PERIOD))
        elif type == self.VcselPeriodFinalRange:
            return self.decode_vcsel_period(self.i2c_bus.read_8(FINAL_RANGE_CONFIG_VCSEL_PERIOD))
        else:
            return 255

    # Convert sequence step timeout from MCLKs to microseconds with given VCSEL period in PCLKs
    # based on VL53L0X_calc_timeout_us()
    def timeout_mclks_to_microseconds(self, timeout_period_mclks, vcsel_period_pclks):
        macro_period_ns = self.calc_macro_period(vcsel_period_pclks)
        return ((timeout_period_mclks * macro_period_ns) + (macro_period_ns / 2)) / 1000

    # Calculate macro period in *nanoseconds* from VCSEL period in PCLKs
    # based on VL53L0X_calc_macro_period_ps()
    # PLL_period_ps = 1655; macro_period_vclks = 2304
    def calc_macro_period(self, vcsel_period_pclks):
        return (((2304 * vcsel_period_pclks * 1655) + 500) / 1000)

    # Decode sequence step timeout in MCLKs from register value
    # based on VL53L0X_decode_timeout()
    # Note: the original function returned a uint32_t, but the return value is
    #always stored in a uint16_t.
    def decode_timeout(self, reg_val):
        # format: "(LSByte * 2^MSByte) + 1"
        return ((reg_val & 0x00FF) << ((reg_val & 0xFF00) >> 8)) + 1

    # Set the measurement timing budget in microseconds, which is the time allowed
    # for one measurement the ST API and this library take care of splitting the
    # timing budget among the sub-steps in the ranging sequence. A longer timing
    # budget allows for more accurate measurements. Increasing the budget by a
    # factor of N decreases the range measurement standard deviation by a factor of
    # sqrt(N). Defaults to about 33 milliseconds the minimum is 20 ms.
    # based on VL53L0X_set_measurement_timing_budget_micro_seconds()
    def set_measurement_timing_budget(self, budget_us):
        StartOverhead      = 1320 # note that this is different than the value in get_
        EndOverhead        = 960
        MsrcOverhead       = 660
        TccOverhead        = 590
        DssOverhead        = 690
        PreRangeOverhead   = 660
        FinalRangeOverhead = 550

        MinTimingBudget = 20000

        if budget_us < MinTimingBudget:
            return False

        used_budget_us = StartOverhead + EndOverhead

        enables = self.get_sequence_step_enables()
        timeouts = self.get_sequence_step_timeouts(enables["pre_range"])

        if enables["tcc"]:
            used_budget_us += (timeouts["msrc_dss_tcc_us"] + TccOverhead)

        if enables["dss"]:
            used_budget_us += 2 * (timeouts["msrc_dss_tcc_us"] + DssOverhead)
        elif enables["msrc"]:
            used_budget_us += (timeouts["msrc_dss_tcc_us"] + MsrcOverhead)

        if enables["pre_range"]:
            used_budget_us += (timeouts["pre_range_us"] + PreRangeOverhead)

        if enables["final_range"]:
            used_budget_us += FinalRangeOverhead

            # "Note that the final range timeout is determined by the timing
            # budget and the sum of all other timeouts within the sequence.
            # If there is no room for the final range timeout, then an error
            # will be set. Otherwise the remaining time will be applied to
            # the final range."

            if used_budget_us > budget_us:
                # "Requested timeout too big."
                return False

            final_range_timeout_us = budget_us - used_budget_us

            # set_sequence_step_timeout() begin
            # (SequenceStepId == VL53L0X_SEQUENCESTEP_FINAL_RANGE)

            # "For the final range timeout, the pre-range timeout
            #  must be added. To do this both final and pre-range
            #  timeouts must be expressed in macro periods MClks
            #  because they have different vcsel periods."

            final_range_timeout_mclks = self.timeout_microseconds_to_mclks(final_range_timeout_us, timeouts["final_range_vcsel_period_pclks"])

            if enables["pre_range"]:
                final_range_timeout_mclks += timeouts["pre_range_mclks"]

            self.i2c_bus.write_reg_16(FINAL_RANGE_CONFIG_TIMEOUT_MACROP_HI, self.encode_timeout(final_range_timeout_mclks))

            # set_sequence_step_timeout() end

            self.measurement_timing_budget_us = budget_us # store for internal reuse
        return True

    # Encode sequence step timeout register value from timeout in MCLKs
    # based on VL53L0X_encode_timeout()
    # Note: the original function took a uint16_t, but the argument passed to it
    # is always a uint16_t.
    def encode_timeout(self, timeout_mclks):
        # format: "(LSByte * 2^MSByte) + 1"

        ls_byte = 0
        ms_byte = 0

        if timeout_mclks > 0:
            ls_byte = timeout_mclks - 1

            while ((int(ls_byte) & 0xFFFFFF00) > 0):
                ls_byte /= 2 # >>=
                ms_byte += 1

            return ((ms_byte << 8) | (int(ls_byte) & 0xFF))
        else:
            return 0

    # Convert sequence step timeout from microseconds to MCLKs with given VCSEL period in PCLKs
    # based on VL53L0X_calc_timeout_mclks()
    def timeout_microseconds_to_mclks(self, timeout_period_us, vcsel_period_pclks):
        macro_period_ns = self.calc_macro_period(vcsel_period_pclks)
        return (((timeout_period_us * 1000) + (macro_period_ns / 2)) / macro_period_ns)

    # based on VL53L0X_perform_single_ref_calibration()
    def perform_single_ref_calibration(self, vhv_init_byte):
        self.i2c_bus.write_reg_8(SYSRANGE_START, 0x01 | vhv_init_byte) # VL53L0X_REG_SYSRANGE_MODE_START_STOP

        self.start_timeout()
        while ((self.i2c_bus.read_8(RESULT_INTERRUPT_STATUS) & 0x07) == 0):
            if self.check_timeout_expired():
                return False

        self.i2c_bus.write_reg_8(SYSTEM_INTERRUPT_CLEAR, 0x01)

        self.i2c_bus.write_reg_8(SYSRANGE_START, 0x00)

        return True

    def set_timeout(self, timeout):
        self.io_timeout = timeout

    # Start continuous ranging measurements. If period_ms (optional) is 0 or not
    # given, continuous back-to-back mode is used (the sensor takes measurements as
    # often as possible) otherwise, continuous timed mode is used, with the given
    # inter-measurement period in milliseconds determining how often the sensor
    # takes a measurement.
    # based on VL53L0X_StartMeasurement()
    def start_continuous(self, period_ms = 0):
        self.i2c_bus.write_reg_8(0x80, 0x01)
        self.i2c_bus.write_reg_8(0xFF, 0x01)
        self.i2c_bus.write_reg_8(0x00, 0x00)
        self.i2c_bus.write_reg_8(0x91, self.stop_variable)
        self.i2c_bus.write_reg_8(0x00, 0x01)
        self.i2c_bus.write_reg_8(0xFF, 0x00)
        self.i2c_bus.write_reg_8(0x80, 0x00)

        if period_ms != 0:
            # continuous timed mode

            # VL53L0X_SetInterMeasurementPeriodMilliSeconds() begin

            osc_calibrate_val = self.i2c_bus.read_16(OSC_CALIBRATE_VAL)

            if osc_calibrate_val != 0:
                period_ms *= osc_calibrate_val

            self.i2c_bus.write_reg_32(SYSTEM_INTERMEASUREMENT_PERIOD, period_ms)

            # VL53L0X_SetInterMeasurementPeriodMilliSeconds() end

            self.i2c_bus.write_reg_8(SYSRANGE_START, 0x04) # VL53L0X_REG_SYSRANGE_MODE_TIMED
        else:
            # continuous back-to-back mode
            self.i2c_bus.write_reg_8(SYSRANGE_START, 0x02) # VL53L0X_REG_SYSRANGE_MODE_BACKTOBACK

    # Returns a range reading in millimeters when continuous mode is active
    # (read_range_single_millimeters() also calls this function after starting a
    # single-shot range measurement)
    def read_range_continuous_millimeters(self):
        self.start_timeout()
        while ((self.i2c_bus.read_8(RESULT_INTERRUPT_STATUS) & 0x07) == 0):
            if self.check_timeout_expired():
                self.did_timeout = True
                raise IOError("read_range_continuous_millimeters timeout")

        # assumptions: Linearity Corrective Gain is 1000 (default)
        # fractional ranging is not enabled
        range = self.i2c_bus.read_16(RESULT_RANGE_STATUS + 10)

        self.i2c_bus.write_reg_8(SYSTEM_INTERRUPT_CLEAR, 0x01)

        return range

    # Did a timeout occur in one of the read functions since the last call to
    # timeout_occurred()?
    def timeout_occurred(self):
        tmp = self.did_timeout
        self.did_timeout = False
        return tmp

    # Set the VCSEL (vertical cavity surface emitting laser) pulse period for the
    # given period type (pre-range or final range) to the given value in PCLKs.
    # Longer periods seem to increase the potential range of the sensor.
    # Valid values are (even numbers only):
    #  pre:  12 to 18 (initialized default: 14)
    #  final: 8 to 14 (initialized default: 10)
    # based on VL53L0X_setVcselPulsePeriod()
    def set_vcsel_pulse_period(self, type, period_pclks):
        vcsel_period_reg = self.encode_vcsel_period(period_pclks)

        enables = self.get_sequence_step_enables()
        timeouts = self.get_sequence_step_timeouts(enables["pre_range"])

        # "Apply specific settings for the requested clock period"
        # "Re-calculate and apply timeouts, in macro periods"

        # "When the VCSEL period for the pre or final range is changed,
        # the corresponding timeout must be read from the device using
        # the current VCSEL period, then the new VCSEL period can be
        # applied. The timeout then must be written back to the device
        # using the new VCSEL period.
        #
        # For the MSRC timeout, the same applies - this timeout being
        # dependant on the pre-range vcsel period."

        if type == self.VcselPeriodPreRange:
            # "Set phase check limits"
            if period_pclks == 12:
                self.i2c_bus.write_reg_8(PRE_RANGE_CONFIG_VALID_PHASE_HIGH, 0x18)
            elif period_pclks == 14:
                self.i2c_bus.write_reg_8(PRE_RANGE_CONFIG_VALID_PHASE_HIGH, 0x30)
            elif period_pclks == 16:
                self.i2c_bus.write_reg_8(PRE_RANGE_CONFIG_VALID_PHASE_HIGH, 0x40)
            elif period_pclks == 18:
                self.i2c_bus.write_reg_8(PRE_RANGE_CONFIG_VALID_PHASE_HIGH, 0x50)
            else:
                return False

            self.i2c_bus.write_reg_8(PRE_RANGE_CONFIG_VALID_PHASE_LOW, 0x08)

            # apply new VCSEL period
            self.i2c_bus.write_reg_8(PRE_RANGE_CONFIG_VCSEL_PERIOD, vcsel_period_reg)

            # update timeouts

            # set_sequence_step_timeout() begin
            # (SequenceStepId == VL53L0X_SEQUENCESTEP_PRE_RANGE)

            new_pre_range_timeout_mclks = self.timeout_microseconds_to_mclks(timeouts["pre_range_us"], period_pclks)

            self.i2c_bus.write_reg_16(PRE_RANGE_CONFIG_TIMEOUT_MACROP_HI, self.encode_timeout(new_pre_range_timeout_mclks))

            # set_sequence_step_timeout() end

            # set_sequence_step_timeout() begin
            # (SequenceStepId == VL53L0X_SEQUENCESTEP_MSRC)

            new_msrc_timeout_mclks = self.timeout_microseconds_to_mclks(timeouts["msrc_dss_tcc_us"], period_pclks)

            if new_msrc_timeout_mclks > 256:
                self.i2c_bus.write_reg_8(MSRC_CONFIG_TIMEOUT_MACROP, 255)
            else:
                self.i2c_bus.write_reg_8(MSRC_CONFIG_TIMEOUT_MACROP, (new_msrc_timeout_mclks - 1))

            # set_sequence_step_timeout() end
        elif type == self.VcselPeriodFinalRange:
            if period_pclks == 8:
                self.i2c_bus.write_reg_8(FINAL_RANGE_CONFIG_VALID_PHASE_HIGH, 0x10)
                self.i2c_bus.write_reg_8(FINAL_RANGE_CONFIG_VALID_PHASE_LOW,  0x08)
                self.i2c_bus.write_reg_8(GLOBAL_CONFIG_VCSEL_WIDTH, 0x02)
                self.i2c_bus.write_reg_8(ALGO_PHASECAL_CONFIG_TIMEOUT, 0x0C)
                self.i2c_bus.write_reg_8(0xFF, 0x01)
                self.i2c_bus.write_reg_8(ALGO_PHASECAL_LIM, 0x30)
                self.i2c_bus.write_reg_8(0xFF, 0x00)
            elif period_pclks == 10:
                self.i2c_bus.write_reg_8(FINAL_RANGE_CONFIG_VALID_PHASE_HIGH, 0x28)
                self.i2c_bus.write_reg_8(FINAL_RANGE_CONFIG_VALID_PHASE_LOW,  0x08)
                self.i2c_bus.write_reg_8(GLOBAL_CONFIG_VCSEL_WIDTH, 0x03)
                self.i2c_bus.write_reg_8(ALGO_PHASECAL_CONFIG_TIMEOUT, 0x09)
                self.i2c_bus.write_reg_8(0xFF, 0x01)
                self.i2c_bus.write_reg_8(ALGO_PHASECAL_LIM, 0x20)
                self.i2c_bus.write_reg_8(0xFF, 0x00)
            elif period_pclks == 12:
                self.i2c_bus.write_reg_8(FINAL_RANGE_CONFIG_VALID_PHASE_HIGH, 0x38)
                self.i2c_bus.write_reg_8(FINAL_RANGE_CONFIG_VALID_PHASE_LOW,  0x08)
                self.i2c_bus.write_reg_8(GLOBAL_CONFIG_VCSEL_WIDTH, 0x03)
                self.i2c_bus.write_reg_8(ALGO_PHASECAL_CONFIG_TIMEOUT, 0x08)
                self.i2c_bus.write_reg_8(0xFF, 0x01)
                self.i2c_bus.write_reg_8(ALGO_PHASECAL_LIM, 0x20)
                self.i2c_bus.write_reg_8(0xFF, 0x00)
            elif period_pclks == 14:
                self.i2c_bus.write_reg_8(FINAL_RANGE_CONFIG_VALID_PHASE_HIGH, 0x48)
                self.i2c_bus.write_reg_8(FINAL_RANGE_CONFIG_VALID_PHASE_LOW,  0x08)
                self.i2c_bus.write_reg_8(GLOBAL_CONFIG_VCSEL_WIDTH, 0x03)
                self.i2c_bus.write_reg_8(ALGO_PHASECAL_CONFIG_TIMEOUT, 0x07)
                self.i2c_bus.write_reg_8(0xFF, 0x01)
                self.i2c_bus.write_reg_8(ALGO_PHASECAL_LIM, 0x20)
                self.i2c_bus.write_reg_8(0xFF, 0x00)
            else:
                # invalid period
                return False

            # apply new VCSEL period
            self.i2c_bus.write_reg_8(FINAL_RANGE_CONFIG_VCSEL_PERIOD, vcsel_period_reg)

            # update timeouts

            # set_sequence_step_timeout() begin
            # (SequenceStepId == VL53L0X_SEQUENCESTEP_FINAL_RANGE)

            # "For the final range timeout, the pre-range timeout
            #  must be added. To do this both final and pre-range
            #  timeouts must be expressed in macro periods MClks
            #  because they have different vcsel periods."

            new_final_range_timeout_mclks = self.timeout_microseconds_to_mclks(timeouts["final_range_us"], period_pclks)

            if enables["pre_range"]:
                new_final_range_timeout_mclks += timeouts["pre_range_mclks"]

            self.i2c_bus.write_reg_16(FINAL_RANGE_CONFIG_TIMEOUT_MACROP_HI, self.encode_timeout(new_final_range_timeout_mclks))

            # set_sequence_step_timeout end
        else:
            # invalid type
            return False

        # "Finally, the timing budget must be re-applied"

        self.set_measurement_timing_budget(self.measurement_timing_budget_us)

        # "Perform the phase calibration. This is needed after changing on vcsel period."
        # VL53L0X_perform_phase_calibration() begin

        sequence_config = self.i2c_bus.read_8(SYSTEM_SEQUENCE_CONFIG)
        self.i2c_bus.write_reg_8(SYSTEM_SEQUENCE_CONFIG, 0x02)
        self.perform_single_ref_calibration(0x0)
        self.i2c_bus.write_reg_8(SYSTEM_SEQUENCE_CONFIG, sequence_config)

        # VL53L0X_perform_phase_calibration() end

        return True

    # Performs a single-shot range measurement and returns the reading in
    # millimeters
    # based on VL53L0X_PerformSingleRangingMeasurement()
    def read_range_single_millimeters(self):
        self.i2c_bus.write_reg_8(0x80, 0x01)
        self.i2c_bus.write_reg_8(0xFF, 0x01)
        self.i2c_bus.write_reg_8(0x00, 0x00)
        self.i2c_bus.write_reg_8(0x91, self.stop_variable)
        self.i2c_bus.write_reg_8(0x00, 0x01)
        self.i2c_bus.write_reg_8(0xFF, 0x00)
        self.i2c_bus.write_reg_8(0x80, 0x00)

        self.i2c_bus.write_reg_8(SYSRANGE_START, 0x01)

        # "Wait until start bit has been cleared"
        self.start_timeout()
        while (self.i2c_bus.read_8(SYSRANGE_START) & 0x01):
            if self.check_timeout_expired():
                self.did_timeout = True
                raise IOError("read_range_single_millimeters timeout")
        return self.read_range_continuous_millimeters()

    # Set the return signal rate limit check value in units of MCPS (mega counts
    # per second). "This represents the amplitude of the signal reflected from the
    # target and detected by the device"; setting this limit presumably determines
    # the minimum measurement necessary for the sensor to report a valid reading.
    # Setting a lower limit increases the potential range of the sensor but also
    # seems to increase the likelihood of getting an inaccurate reading because of
    # unwanted reflections from objects other than the intended target.
    # Defaults to 0.25 MCPS as initialized by the ST API and this library.
    def set_signal_rate_limit(self, limit_Mcps):
        if limit_Mcps < 0 or limit_Mcps > 511.99:
            raise ValueError("set_signal_rate_limit limit out of range (0 - 511.99)")
        # Q9.7 fixed point format (9 integer bits, 7 fractional bits)
        self.i2c_bus.write_reg_16(FINAL_RANGE_CONFIG_MIN_COUNT_RATE_RTN_LIMIT, (limit_Mcps * (1 << 7)))# writeReg16Bit(FINAL_RANGE_CONFIG_MIN_COUNT_RATE_RTN_LIMIT, limit_Mcps * (1 << 7));

    # Encode VCSEL pulse period register value from period in PCLKs
    # based on VL53L0X_encode_vcsel_period()
    def encode_vcsel_period(self, period_pclks):
        return((period_pclks >> 1) - 1)
