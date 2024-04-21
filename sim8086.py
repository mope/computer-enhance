import argparse
import struct
import sys

instructions = {
    0b100010: 'mov'
}

w_0_registers = {
    0b000: 'al',
    0b001: 'cl',
    0b010: 'dl',
    0b011: 'bl',
    0b100: 'ah',
    0b101: 'ch',
    0b110: 'dh',
    0b111: 'bh'
}

w_1_registers = {
    0b000: 'ax',
    0b001: 'cx',
    0b010: 'dx',
    0b011: 'bx',
    0b100: 'sp',
    0b101: 'bp',
    0b110: 'si',
    0b111: 'di'
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sim8086')
    parser.add_argument('file', type=str, help='File to be executed')
    args = parser.parse_args()
    file_name = args.file

    with open(file_name, mode='rb') as f:
        while (bytes_ := f.read(2)):
            raw_bytes = struct.unpack("BB", bytes_)
            raw_instruction = (raw_bytes[0] >> 2) & 0b111111
            d = raw_bytes[0] & 0b00000010
            w = raw_bytes[0] & 0b00000001

            raw_reg = (raw_bytes[1] >> 3) & 0b00111
            raw_r_m = raw_bytes[1] & 0b00000111

            if w == 0b0:
                registers = w_0_registers
            else:
                registers = w_1_registers

            instruction = instructions[raw_instruction]
            reg = registers[raw_reg]
            r_m = registers[raw_r_m]

            if d == 0b1:
                sys.stdout.write(f"{instruction} {reg}, {r_m}\n")
            else:
                sys.stdout.write(f"{instruction} {r_m}, {reg}\n")
