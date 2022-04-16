package java_client.src.runables;

import java.net.Socket;
import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStreamReader;


public class MessageReceiver implements Runnable{
    private Socket client;

    public MessageReceiver(Socket clientSocket){
        this.client = clientSocket;
    }

    @Override
    public void run() {
        try (
            InputStreamReader iReader = new InputStreamReader(this.client.getInputStream()); 
            BufferedReader bf = new BufferedReader(iReader)
        ){
            String line;
            while ((line=bf.readLine()) != null) {
                System.out.println(line);
            }
            
        } catch (IOException e) {
            e.printStackTrace();
        }
        
    }
    
}
