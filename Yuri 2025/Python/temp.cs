
// C# program to print the IP address of the machine 
using System;   
using System.Text;   
using System.Net; 
  
class GFG{ 
      
static void Main(string[] args)   
{ 
      
    // Get the Name of HOST   
    string hostName = Dns.GetHostName();  
    Console.WriteLine(hostName);   
      
    // Get the IP from GetHostByName method of dns class. 
    string IP = Dns.GetHostByName(hostName).AddressList[0].ToString();   
    Console.WriteLine("IP Address is : " + IP);   
}   
}