use std::env;

mod day_01;

fn main() {
    let args: Vec<String> = env::args().collect();

    match args.len() {
        // No arguments
        1 => {
            // TODO - If there are no arguments, run all days.
            println!("Not supported.")
        }
        2 => {
            let number: i32 = match args[1].parse() {
                Ok(n) => n,
                Err(_) => {
                    eprintln!("Error: First argument not an integer");
                    return;
                }
            };

            //println!("{}", _number);
            match number {
                1 => day_01::solve(),
                _ => eprintln!("Invalid argument."),
            }
        }
        _ => {
            eprintln!("Only 1 argument supported.")
        }
    }
}
