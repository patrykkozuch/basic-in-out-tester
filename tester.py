import os
import os.path
import fnmatch
from re import sub
import subprocess

TESTS_FOLDER = ''
TESTS_OUTPUT_FOLDER = ''

tests_folder = TESTS_FOLDER if TESTS_FOLDER != '' else input(
    "Enter tests folder name: ")
tests_output_folder = TESTS_OUTPUT_FOLDER if TESTS_OUTPUT_FOLDER != '' else input(
    "Enter folder name for tests output: ")

if not os.path.isdir(tests_folder):
    print(f"Folder {tests_folder} not found.")
    exit()

if not os.path.isdir(tests_output_folder):
    os.mkdir(tests_output_folder)
else:
    for file in fnmatch.filter(os.listdir(tests_output_folder), '*.out'):
        os.remove(tests_output_folder + "\\" + file)

if not os.path.isfile("main.exe"):
    print("File \"main.exe\" not found. Compile your program and try again.")
    exit()


tests_number = len(fnmatch.filter(os.listdir(tests_folder), '*.in'))
tests_status = [True for i in range(tests_number)]


for i in range(1, tests_number+1):
    print(f"======== TEST {i} ========")

    t_in = open(f"{tests_folder}/{i}.in",)
    t_out = open(f"{tests_folder}/{i}.out")
    u_out = open(f"{tests_output_folder}/{i}.out", 'w')

    subprocess.run(f"main.exe", stdin=t_in, stdout=u_out)

    u_out.close()
    u_out = open(f"{tests_output_folder}/{i}.out")

    t_lines = t_out.readlines()
    u_lines = u_out.readlines()

    lines_number = min(len(t_lines), len(u_lines))

    for number in range(lines_number):

        if t_lines[number] != u_lines[number]:
            tests_status[i-1] = False

            print(f"Tests found incorrect solution (line {number}):")
            print(f"- got: ", repr(u_lines[number]))
            print(f"- expected: ", repr(t_lines[number]))

    if len(u_lines) > len(t_lines):
        tests_status[i-1] = False

        print("Additionally, your program found too much solutions:")

        for number in range(lines_number, len(u_lines)):
            print(f"(line {number}): ", repr(u_lines[number]))

    if len(u_lines) < len(t_lines):
        tests_status[i-1] = False

        print("Unfortunately, your program didn't find these solutions:")

        for number in range(lines_number, len(t_lines)):
            print(f"(line {number}): ", repr(t_lines[number]))

    print()
    print()

print("===== SUMMARY =====")
for i in range(1, tests_number+1):
    print(f"Test {i}: ", "SUCCESS" if tests_status[i-1] else "FAILURE")
