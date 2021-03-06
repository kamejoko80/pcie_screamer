#!/usr/bin/env python
# -*- coding: utf-8 -*-

from migen import *

from litex.build.generic_platform import *
from litex.build.xilinx import XilinxPlatform


_io = [
    ("clk100", 0, Pins("R2"), IOStandard("LVCMOS33")),

    ("user_led", 0, Pins("V17"), IOStandard("LVCMOS33")),
    ("user_led", 1, Pins("U17"), IOStandard("LVCMOS33")),

    ("serial", 0,
        Subsignal("tx", Pins("U4")),
        Subsignal("rx", Pins("V4")),
        IOStandard("LVCMOS33"),
    ),

    ("pcie_x1", 0,
        Subsignal("rst_n", Pins("M1"), IOStandard("LVCMOS33")),
        Subsignal("clk_p", Pins("D6")),
        Subsignal("clk_n", Pins("D5")),
        Subsignal("rx_p", Pins("A4")),
        Subsignal("rx_n", Pins("A3")),
        Subsignal("tx_p", Pins("B2")),
        Subsignal("tx_n", Pins("B1"))
    ),

    ("usb_fifo_clock", 0, Pins("C13"), IOStandard("LVCMOS33")),
    ("usb_fifo", 0,
        Subsignal("rst", Pins("U15")),
        Subsignal("data", Pins("B9 A9 C9 A10 B10 B11 A12 B12 A13 A14 B14 A15 B15 B16 A17 B17",
                               "C17 C18 D18 E17 E18 E16 F18 F17 G17 H18 D13 C14 D14 D15 C16 D16")),
        Subsignal("be", Pins("L18 M17 N18 N17")),
        Subsignal("rxf_n", Pins("R18")),
        Subsignal("txe_n", Pins("P18")),
        Subsignal("rd_n", Pins("R16")),
        Subsignal("wr_n", Pins("T18")),
        Subsignal("oe_n", Pins("T15")),
        Subsignal("siwua", Pins("R17")),
        IOStandard("LVCMOS33"), Misc("SLEW=FAST")
    ),
]


class Platform(XilinxPlatform):
    default_clk_name = "clk100"
    default_clk_period = 10.0

    def __init__(self, toolchain="vivado", programmer="vivado"):
        XilinxPlatform.__init__(self, "xc7a35t-csg325-2", _io,
                                toolchain=toolchain)
        self.toolchain.bitstream_commands = \
            ["set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]",
             "set_property BITSTREAM.CONFIG.CONFIGRATE 40 [current_design]"]
        self.toolchain.additional_commands = \
            ["write_cfgmem -force -format bin -interface spix4 -size 16 "
             "-loadbit \"up 0x0 {build_name}.bit\" -file {build_name}.bin"]
        self.programmer = programmer
        self.add_platform_command("set_property CLOCK_DEDICATED_ROUTE FALSE [get_nets usb_fifo_clock_IBUF]")


    def do_finalize(self, fragment):
        XilinxPlatform.do_finalize(self, fragment)
        from gateware import constraints
        constraints.apply_xilinx_pcie_constraints(self)
