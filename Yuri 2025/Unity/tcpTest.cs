using System;
using System.Collections;
using System.Collections.Generic;
using System.Net;
using System.Net.Security;
using System.Net.Sockets;
using System.Text;
using System.Text.Json;
using System.Threading;
using UnityEditor.MemoryProfiler;
using UnityEngine;

[System.Serializable]
public class TTSMessage
{
    public string type;
    public string emotion;
    public string mp3path;
}
public class tcpTest : MonoBehaviour
{
    public ttsPlayer ttsplayer;
    Thread receiveThread;
    TcpClient client;
    TcpListener listener;
    StringBuilder messageBuffer = new StringBuilder();
    int port = 5065;
    Vector3 data = Vector3.zero;
    bool isRunning = true;
    // Start is called before the first frame update
    public bool needCurious = false;
    public bool needHappy = false;
    public bool needCry = false;
    public bool needShame = false;
    public bool needShock = false;
    public bool needTundere = false;
    public bool needTalking = false;
    public float emo_duration;
    string[] stringArray;
    Queue<string> mainThreadQueue = new Queue<string>();
    object queueLock = new object();
    //private Dictionary<TcpListener,ClientState> clients = new Dictionary<TcpListener,ClientState>();
    void Start()
    {
        Debug.Log($"tcpTest instance id = {GetInstanceID()}");
        initTCP();
    }

    void initTCP(){
        receiveThread = new Thread(new ThreadStart(receiveData));
        receiveThread.IsBackground = true; //End Thread if Unity stopped
        receiveThread.Start();
    }

    void receiveData(){
        //Create server
        listener = new TcpListener(IPAddress.Parse("192.168.1.8"), port);
        listener.Start();

        //Create client to receive data
        client = listener.AcceptTcpClient(); //Get the client
        
        //Start listening
        while(isRunning){
            connection();
        }
        //listener.Stop();
    }

    void connection(){
        NetworkStream stream = client.GetStream();
        //create buffer
        /*byte[] buffer = new byte[client.ReceiveBufferSize];
        int bytesRead = stream.Read(buffer, 0, client.ReceiveBufferSize);*/
        byte[] buffer = new byte[1024];
        int bytesRead = stream.Read(buffer, 0, buffer.Length);
        if (bytesRead <= 0) return;

        //Decode the bytes into a String
        string chunk = Encoding.UTF8.GetString(buffer, 0, bytesRead);
        messageBuffer.Append(chunk);

        string all = messageBuffer.ToString();
        string[] messages = all.Split('\n');

        //last chunk maybe incompleted, we need to save it
        messageBuffer.Clear();
        messageBuffer.Append(messages[messages.Length - 1]);

        for (int i = 0; i < messages.Length - 1; i++)
        {
            lock (queueLock)
            {
                mainThreadQueue.Enqueue(messages[i]);
            }
        }


        /*
        //check is the data get empty string
        if(dataReceived != null && dataReceived != ""){
            Debug.Log(dataReceived);
            // Remove the parentheses
            if (dataReceived.StartsWith("(") && dataReceived.EndsWith(")"))
            {
                dataReceived = dataReceived.Substring(1, dataReceived.Length - 2);
            }
        
            // Split the elements into an array
            stringArray = dataReceived.Split(',');
            Debug.Log("我的data吶??: "+ stringArray[0]);
            
            checkCurious(stringArray);
            checkHappy(stringArray);
            checkCry(stringArray);
            checkShame(stringArray);
            checkShock(stringArray);
            checkTundere(stringArray);
            checkTalking(stringArray);

        //checkCurious(stringArray);
        //stream.Write(buffer, 0, bytesRead); //response form the server back to the client
        }*/

    }
    void processMessage(string json)
    {
        Debug.Log($"processMessage from instance id = {GetInstanceID()}");
        try
        {
            TTSMessage msg = JsonUtility.FromJson<TTSMessage>(json);

            if (msg.type == "tts")
            {
                Debug.Log($"動畫: {msg.emotion}, mp3路徑: {msg.mp3path}");
                if (ttsplayer == null)
                {
                    Debug.LogError("ttsplayer 沒有綁 Inspector");
                    return;
                }
                ttsplayer.PlayTTS(msg.emotion, msg.mp3path);
            }
        }
        catch (Exception e)
        {
            Debug.LogError("JSON 解析失敗: " + e.Message);
        }
    }
     /*public static Vector3 parseData(string dataString){
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
    }*/

    public void checkCurious(string emotion, float duration)
    {   
        needCurious = false;
        if (emotion == "Interested")
        {
            needCurious = true;
            emo_duration = duration;
        }
        Debug.Log("after if-->Need Curious: "+ needCurious);
        
    }

    public void checkHappy(string emotion, float duration)
    {   
        needHappy = false;
        if (emotion == "Happy")
        {
            needHappy = true;
            emo_duration = duration;
        }
        Debug.Log("after if-->Need Happy: "+ needHappy);
        
    }

    public void checkCry(string emotion, float duration)
    {   
        needCry = false;
        if (emotion == "Sad")
        {
            needCry = true;
            emo_duration = duration;
        }
        Debug.Log("after if-->Need Cry: "+ needCry);
        
    }

    public void checkShame(string emotion, float duration)
    {   
        needShame = false;
        if (emotion == "Sensitive")
        {
            needShame = true;
            emo_duration = duration;
        }
        Debug.Log("after if-->Need Shame: "+ needShame);
        
    }

    public void checkShock(string emotion, float duration)
    {   
        needShock = false;
        if (emotion == "Surprised")
        {
            needShock = true;
            emo_duration = duration;
        }
        Debug.Log("after if-->Need Shock: "+ needShock);
        
    }

    public void checkTundere(string emotion, float duration)
    {   
        needTundere = false;
        if (emotion == "Bad")
        {
            needTundere = true;
            emo_duration = duration;
        }
        Debug.Log("after if-->Need Tundere: "+ needTundere);
        
    }

    public void checkTalking(string emotion, float duration)
    {   
        needTalking = false;
        if (emotion == "Neutral")
        {
            needTalking = true;
            emo_duration = duration;
        }
        Debug.Log("after if-->Need Talking: "+ needTalking);
        
    }

    public void resetvalues()
    {
        needCurious = false;
        needHappy = false;
        needCry = false;
        needShame = false;
        needShock = false;
        needTundere = false;
        needTalking = false;
        // stringArray = new string[0];
    }
    // Update is called once per frame
    void Update()
    {
        // Set this object's position in the scene according to the position received
        //transform.position = data;
        
        // Debug.Log("string Array --> " + stringArray[0]);
        //checkCurious(stringArray);
        while (true)
        {
            string json = null;

            lock (queueLock)
            {
                if (mainThreadQueue.Count > 0)
                    json = mainThreadQueue.Dequeue();
            }

            if (json == null) break;

            processMessage(json);
        }
    }

    void OnApplicationQuit()
    {
        //if (receiveThread != null)
        isRunning = false;

        client?.Close();
        listener?.Stop();

        if (receiveThread != null && receiveThread.IsAlive)
            receiveThread.Join();

        Debug.Log("我死了");
    }

    void Awake()
    {
        if (ttsplayer == null)
        {
            ttsplayer = FindObjectOfType<ttsPlayer>();
            Debug.Log("[tcpTest] Auto bind ttsPlayer: " + ttsplayer);
        }

        if (ttsplayer == null)
        {
            Debug.LogError("Scene 裡找不到 ttsPlayer");
        }
    }
}
