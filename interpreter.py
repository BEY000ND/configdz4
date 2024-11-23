import json

def interpret(input_file, output_file, memory_size):
    with open(input_file, 'rb') as infile:
        program = list(infile.read())

    memory = [0] * memory_size
    accumulator = 0
    pc = 0  # Program counter
    execution_log = []  # Лог выполнения

    while pc < len(program):
        opcode = program[pc]
        operand = program[pc + 1] | (program[pc + 2] << 8) | (program[pc + 3] << 16)
        pc += 4
        log_entry = {"opcode": opcode, "operand": operand, "pc": pc}

        if opcode == 0:  # LOAD_CONST
            accumulator = operand
        elif opcode == 1:  # READ_MEM
            if operand >= len(memory):
                raise IndexError(f"Memory read out of bounds at address {operand}")
            accumulator = memory[operand]
        elif opcode == 2:  # WRITE_MEM
            if operand >= len(memory):
                raise IndexError(f"Memory write out of bounds at address {operand}")
            memory[operand] = accumulator
        elif opcode == 3:  # BIN_OP_NE
            if operand >= len(memory):
                raise IndexError(f"Memory comparison out of bounds at address {operand}")
            accumulator = int(accumulator != memory[operand])
        else:
            raise ValueError(f"Unknown opcode {opcode}")

        log_entry.update({"accumulator": accumulator, "memory_snapshot": memory[:]})
        execution_log.append(log_entry)

    # Сохраняем результат выполнения в JSON
    with open(output_file, 'w') as outfile:
        json.dump({
            "final_memory": memory,
            "final_accumulator": accumulator,
            "execution_log": execution_log
        }, outfile, indent=4)

    print(f"Execution complete. Log saved to {output_file}.")

if __name__ == '__main__':
    input_file = 'test_program.bin'
    output_file = 'result.json'
    memory_size = 1024  # Увеличили размер памяти для поддержки больших адресов
    interpret(input_file, output_file, memory_size)
