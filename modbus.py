#!/usr/bin/env python
# -*- coding: utf_8 -*-

import serial
import argparse
import sys

import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu


connection_config = {
    'port': '/dev/ttyS4',
    'baudrate': 9600,
    'bytesize': 8,
    'parity': 'N',
    'stopbits': 1,
    'xonxoff': 0
}

master_config = {
    'timeout': 1.0,
    'verbose': True
}

parser = argparse.ArgumentParser()
parser.add_argument("address", help='modbus slave address', type=int)
parser.add_argument("operation", help='[r|w] read or write', choices=['r', 'w'], type=str)
parser.add_argument("register", help='register to write, of 1st register to read', type=int)
parser.add_argument("forth", help='for write opertation: value to be written, for read operation: last register to read', type=int)
args = parser.parse_args()

def main(config, slave_addr, operation, register, value=None):
    # Start logger
    logger = modbus_tk.utils.create_logger("console")

    try:
        # Connect to the slave
        master = modbus_rtu.RtuMaster(
            serial.Serial(**config)
        )
        master.set_timeout(master_config['timeout'])
        master.set_verbose(master_config['verbose'])
        logger.info("connected")

        if operation == 'r':
            if isinstance(register, int):
                register = (register, register+1)
            logger.info(master.execute(slave_addr, cst.READ_HOLDING_REGISTERS, *register))
        elif operation == 'w':
            if not value:
                raise ValueError('Value missing for write operation')
            logger.info(master.execute(slave_addr, cst.WRITE_SINGLE_REGISTER, register, output_value=value))
        else:
            raise ValueError('No such operation {0}'.format(operation))

        # send some queries
        # logger.info(master.execute(1, cst.READ_COILS, 0, 10))
        # logger.info(master.execute(1, cst.READ_DISCRETE_INPUTS, 0, 8))
        # logger.info(master.execute(1, cst.READ_INPUT_REGISTERS, 100, 3))
        # logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 100, 12))
        # logger.info(master.execute(1, cst.WRITE_SINGLE_COIL, 7, output_value=1))
        # logger.info(master.execute(1, cst.WRITE_SINGLE_REGISTER, 2, output_value=54))
        # logger.info(master.execute(1, cst.WRITE_MULTIPLE_COILS, 0, output_value=[1, 1, 0, 1, 1, 0, 1, 1]))
        # logger.info(master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 100, output_value=xrange(12)))

    except modbus_tk.modbus.ModbusError as exc:
        logger.error("{0}- Code={1}".format(exc, exc.get_exception_code()))
    except (OSError, ValueError) as exc:
        logger.error(exc)


if __name__ == "__main__":
    if args.operation == 'r':
        main(connection_config, args.address, 'r', (args.register, args.forth))
    elif args.operation == 'w':
        main(connection_config, args.address, 'w', args.register, value=args.forth)
    else:
        parser.print_help()
        sys.exit(1)

