def parse_line(line):
    line = line.strip()
    if not line or line.startswith(';'):
        return None
    parts = line.split()
    command = parts[0]
    if len(parts) == 2:  # Команда с операндом
        operand = int(parts[1])
        return command, operand
    elif len(parts) == 1 and command == "BIN_OP_NE":  # Команда без операнда
        return command, None
    else:
        raise ValueError(f"Invalid line format: {line}")


def assemble(input_file, output_file):
    instructions = []
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    # Преобразование в байткод
    bytecode = []
    for line in lines:
        parsed = parse_line(line)
        if not parsed:
            continue
        command, operand = parsed
        if command == "LOAD_CONST":
            bytecode.extend([0, operand & 0xFF, (operand >> 8) & 0xFF, (operand >> 16) & 0xFF])
        elif command == "READ_MEM":
            bytecode.extend([1, operand & 0xFF, (operand >> 8) & 0xFF, (operand >> 16) & 0xFF])
        elif command == "WRITE_MEM":
            bytecode.extend([2, operand & 0xFF, (operand >> 8) & 0xFF, (operand >> 16) & 0xFF])
        elif command == "BIN_OP_NE":
            if operand is not None:
                bytecode.extend([3, operand & 0xFF, (operand >> 8) & 0xFF, (operand >> 16) & 0xFF])
            else:
                bytecode.extend([3, 0, 0, 0])  # Если операнд отсутствует, используем 0
        else:
            raise ValueError(f"Unknown command: {command}")

    # Сохранение в файл
    with open(output_file, 'wb') as outfile:
        outfile.write(bytearray(bytecode))

    print(f"Assembling complete. {len(bytecode) // 4} instructions written.")

if __name__ == '__main__':
    input_file = 'test_program.txt'
    output_file = 'test_program.bin'
    assemble(input_file, output_file)
