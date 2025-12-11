use std::net::{TcpStream, TcpListener};
use std::thread;
use std::io::{BufRead, BufReader, Write};
use std::error::Error;

const HOST: &str = "0.0.0.0";
const PORT: u16 = 5001;


fn handle_read(mut stream: TcpStream) {
    //Accept
    let client = stream.peer_addr().unwrap();
    println!("New connection from {}", client);

    let reader = BufReader::new(stream.try_clone().unwrap());

    // Inform client
    writeln!(stream, "Server responded.").unwrap();

    // Read loop
    for line in reader.lines() {
        match line {
            Ok(msg) => {
                println!("[{}] {}", client, msg);
            }
            Err(e) => {
                println!("Error reading from {}: {}", client, e);
                break;
            }
        } 
    }
}

fn main() -> std::result::Result< (), Box<dyn Error>> {
    let listener = TcpListener::bind((HOST, PORT))?;
    println!("Server listening on {}:{}", HOST, PORT);
    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                thread::spawn(move || {
                    handle_read(stream);
                });
            }
            Err(e) => {
                eprintln!("Connection failed: {}", e);
            }
        }
    }
    Err(Box::new(std::io::Error::new(std::io::ErrorKind::Other, "Server error"))) 
}