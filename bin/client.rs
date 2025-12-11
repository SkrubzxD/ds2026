use std::net::TcpStream;
use std::io::{Read, Write};

const HOST: &str = "0.0.0.0";
const PORT: u16 = 5001;

fn inform_server(mut stream: TcpStream) {
     let msg = "Hello from client";
            match stream.write_all(msg.as_bytes()) {
                Ok(_) => println!("Sent: {}", msg),
                Err(e) => println!("Failed to write: {}", e),
            }
}

fn open_buffer(mut stream: TcpStream) {
    let mut buffer = [0; 512];
    match stream.read(&mut buffer) {
        Ok(size) => {
            let response = String::from_utf8_lossy(&buffer[..size]);
            println!("Received: {}", response);
        }
        Err(e) => println!("Failed to read: {}", e),
    }
}

fn main() -> Result<(), std::io::Error> {
    match TcpStream::connect((HOST, PORT)) {
        Ok(stream) => {
            println!("Successfully connected to server at {}:{}", HOST, PORT);
            inform_server(stream.try_clone().unwrap());
            open_buffer(stream);
            Ok(())
        }
        Err(e) => { eprintln!("Failed to connect: {}", e);
            Err(e)
        }
    }
}



