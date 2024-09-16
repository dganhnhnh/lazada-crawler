import csv
import os

RATE = 3
PATH = 'data/'

def rm_line(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    output_lines = []
    skip_next_line = False 

    for i, line in enumerate(lines):
        line = line.strip()
        
        if line == '0' or line == '1':
            if output_lines:
                output_lines.pop()
            output_lines.append(line)
        else:
            if not skip_next_line:
                output_lines.append(line)
            skip_next_line = False

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines('\n'.join(output_lines) + '\n')

def parse_file_to_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)

        if os.stat(output_file).st_size == 0:
            csvwriter.writerow(['Rate', 'Review'])

        in_review_section = False
        review_lines = []

        for i, line in enumerate(lines):
            line = line.strip()

            if line.isdigit():
                if in_review_section and review_lines:
                    review = ' '.join(review_lines).strip()
                    csvwriter.writerow([RATE, review])
                    review_lines = []
                in_review_section = False 
                continue

            if "Verified Purchase" in line:
                in_review_section = True
                review_lines = []
            elif in_review_section:
                review_lines.append(line)

        if in_review_section and review_lines:
            review = ' '.join(review_lines).strip()
            csvwriter.writerow([review, RATE])

if __name__ == "__main__":
    input_file = f'{PATH}a.txt'
    input_file2 = f'{PATH}aa.txt'
    output_file = f'{PATH}{RATE}.csv'
    rm_line(input_file, input_file2)
    parse_file_to_csv(input_file2, output_file)