using System.Collections;
using System.Collections.Generic;
using System.Net;
using System.Net.Security;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEditor.MemoryProfiler;
using UnityEngine;

public class tcpTest : MonoBehaviour
{
    Thread receiveThread;
    TcpClient client;
    TcpListener listener;
    int port = 5065;
    Vector3 data = Vector3.zero;
    // Start is called before the first frame update
    void Start()
    {
        initTCP();
    }

    void initTCP(){
        receiveThread = new Thread(new ThreadStart(receiveData));
        receiveThread.IsBackground = true; //End Thread if Unity stopped
        receiveThread.Start();
    }

    void receiveData(){
        //Create server
        listener = new TcpListener(IPAddress.Parse("10.13.225.109"), port);
        listener.Start();

        //Create client to receive data
        client = listener.AcceptTcpClient(); //Get the client

        //Start listening
        while(true){
            connection();
        }

    }

    void connection(){
        NetworkStream stream = client.GetStream();
        //create buffer
        byte[] buffer = new byte[client.ReceiveBufferSize];
        int bytesRead = stream.Read(buffer, 0, client.ReceiveBufferSize);

        //Decode the bytes into a String
        string dataReceived = Encoding.UTF8.GetString(buffer, 0, bytesRead);

        //check is the data get empty string
        if(dataReceived != null && dataReceived != ""){
            data = parseData(dataReceived);
            stream.Write(buffer, 0, bytesRead); //response form the server back to the client
        }

    }

     public static Vector3 parseData(string dataString){
        Debug.Log(dataString);
        // Remove the parentheses
        if (dataString.StartsWith("(") && dataString.EndsWith(")"))
        {
            dataString = dataString.Substring(1, dataString.Length - 2);
        }

        // Split the elements into an array
        string[] stringArray = dataString.Split(',');

        // Store as a Vector3
        Vector3 result = new Vector3(
            float.Parse(stringArray[0]),
            float.Parse(stringArray[1]),
            float.Parse(stringArray[2]));

        return result;
    }

    // Update is called once per frame
    void Update()
    {
        // Set this object's position in the scene according to the position received
        transform.position = data;
    }
}
