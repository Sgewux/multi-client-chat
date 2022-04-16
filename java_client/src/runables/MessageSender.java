package java_client.src.runables;

import java.net.Socket;
import java.util.Scanner;
import java.io.IOException;
import java.io.DataOutputStream;

public class MessageSender implements Runnable {
    private Socket client;

    public MessageSender(Socket clientSocket){
        this.client = clientSocket;
    }

    @Override
    public void run() {

        try (
            Scanner sc = new Scanner(System.in);
            DataOutputStream outputStream = new DataOutputStream(this.client.getOutputStream())
        ) {
            while (sc.hasNextLine()) {
                String line = sc.nextLine();
                if (!line.isBlank()) {
                    outputStream.writeUTF(line);
                }
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
        
    }
    
}
