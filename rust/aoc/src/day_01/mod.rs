use std::fs;

pub fn solve() {
    solve_1();
    solve_2();
}

const DIGITS: Vec<String> = Vec.new([
    String::from("zero"),
    String::from("one"),
    String::from("two"),
    String::from("three"),
    String::from("four"),
    String::from("five"),
    String::from("six"),
    String::from("seven"),
    String::from("eight"),
    String::from("nine")
]);



fn solve_1() {
    let file_path = "src/day_01/input.txt";
    let input = fs::read_to_string(file_path).expect("Can't read input file.");

    let mut total = 0;
    for line in input.split("\n") {
        if line == "" {
            continue;
        }
        let (first_integer, last_integer) = get_integers(line);
        total += first_integer.unwrap() * 10 + last_integer.unwrap();
    }
    println!("{:?}", total);
}

fn get_integers(line: &str) -> (Option<u32>, Option<u32>) {
    let mut first_integer = None;
    let mut last_integer = None;

    for char in line.chars() {
        if char.is_digit(10) {
            first_integer = char.to_digit(10);
            break;
        }
    }

    for char in line.chars().rev() {
        if char.is_digit(10) {
            last_integer = char.to_digit(10);
            break;
        }
    }
    return (first_integer, last_integer);
}

fn solve_2() {
    let file_path = "src/day_01/input.txt";
    let input = fs::read_to_string(file_path).expect("Can't read input file.");
    
    let mut total = 0;
    for line in input.split("\n") {
        if line == "" {
            continue;
        }
        let (first_integer, last_integer) = get_integers_part_2(line);
        total += first_integer.unwrap() * 10 + last_integer.unwrap();

    }
    println!("{:?}", total);
}

fn get_integers_part_2(line: &str) -> (Option<u32>, Option<u32>) {
    let digits = vec![
        "zero".to_string(),
        "one".to_string(),
        "two".to_string(),
        "three".to_string(),
        "four".to_string(),
        "five".to_string(),
        "six".to_string(),
        "seven".to_string(),
        "eight".to_string(),
        "nine".to_string()
    ];

}



