package java_client.src;

import java_client.src.runables.*; //  message sender and reciever

import java.net.Socket;
import java.util.Scanner;
import java.io.IOException;
import java.io.DataOutputStream;

class Client{
    public static void main(String[] args) {
        /* 
        The socket obj defined below int the try-with-resourses statement
        must has as params the ip and port of your server, so letting this
        as it was written by myself wont work.
        */
        try (Socket client = new Socket("192.168.1.11", 8080);
            Scanner sc = new Scanner(System.in);
        ) {
            
            DataOutputStream outputStream = new DataOutputStream(client.getOutputStream());
            System.out.print("Write your username: ");
            outputStream.writeUTF(sc.nextLine());

            MessageSender messageSender = new MessageSender(client);
            MessageReceiver messageReceiver = new MessageReceiver(client);

            Thread messageSenderThread = new Thread(messageSender, "message_sender_thread");
            Thread messageRecieverThread = new Thread(messageReceiver, "message_reciever_thread");

            messageRecieverThread.start();
            messageSenderThread.start();

            // Joining threads to keep the Socket resourse alive
            messageRecieverThread.join();
            messageSenderThread.join();


            
        } catch (IOException | InterruptedException e) {
            System.out.println(e.getMessage());
        } 
        
    }
        
}