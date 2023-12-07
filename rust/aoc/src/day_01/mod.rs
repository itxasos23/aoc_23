use std::fs;

pub fn solve() {
    solve_1();
    solve_2();
}

fn solve_1() {
    let file_path = "src/day_01/input.txt";
    let input = fs::read_to_string(file_path).expect("Can't read input file.");

    let mut total = 0;
    for line in input.split("\n") {
        if line == "" {
            continue
        }
        let first_integer = get_first_integer(line).unwrap();
        let last_integer = get_last_integer(line).unwrap();
        total += first_integer*10+last_integer;
    }
    println!("{:?}", total);
}

fn get_first_integer(line: &str) -> Option<u32> {
    for char in line.chars() {
        if char.is_digit(10) {
            return char.to_digit(10)
        }
    }
    return None
}

fn get_last_integer(line: &str) -> Option<u32> {
    for char in line.chars().rev() {
        if char.is_digit(10) {
            return char.to_digit(10)
        }
    }
    return None
}

fn solve_2() {
    let file_path = "src/day_01/input.txt";
    let input = fs::read_to_string(file_path).expect("Can't read input file.");
    println!("test 02");
}
