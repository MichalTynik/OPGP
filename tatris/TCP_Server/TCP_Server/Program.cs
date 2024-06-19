using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Text.Json;


class Start
{
    static void Main(string[] args)
    {
        Server server = new Server();
        server.Run();
    }
}

class Hrac{
    string meno;
    int skore;
    public Hrac(string meno, int skore){
        this.meno = meno;
        this.skore = skore;
    }
}

class Client
{
    Server server;
    public Socket socket;
    EndPoint add;
    string name;
    string login = "CHAT LOGIN";
    byte[] recvBuffer = new byte[1024];
    byte[] buffer;

    public Client(Server server, Socket client_socket)
    {
        this.server = server;
        this.socket = client_socket;
        this.add = client_socket.LocalEndPoint;
    }

    public Socket Socket
    {
        get { return socket; }
    }

    public void Close()
    {
        socket.Close();
        server.Remove_client(this);
    }

    public void Recieve_message(string message)
    {
        Console.WriteLine($"\n{name}: {message}");
        server.Send_message(message);
    }

    public void Send_message(string message)
    {
        socket.Send(Encoding.ASCII.GetBytes(message));
    }

    public void Recieved()
    {
        Hrac hrac;
        try
        {
            int data = socket.Receive(recvBuffer);
            if (data <= 0)
            {
                Close();
                return;
            }

            buffer = new byte[data];
            Array.Copy(recvBuffer, buffer, data);
            string encBuffer = Encoding.ASCII.GetString(buffer);
            if (name == null)
            {
                while (encBuffer.Contains("\n"))
                {
                    string[] lines = encBuffer.Split("\n", 2);

                    if (lines[0].StartsWith(login))
                    {
                        name = lines[0].Substring(login.Length + 1);
                        hrac = new Hrac(name, int.Parse(lines[1]));
                        if (name != null)
                        {
                            encBuffer = lines[1];
                    
                            continue;
                        }
                    }
                    Recieve_message(lines[0]);
                    encBuffer = lines[1];
                    

                }
            }
            else
            {
                Recieve_message(encBuffer);
            }


        }
        catch (SocketException e)
        {
            Console.WriteLine($"Client {name} disconnected");
            Close();
        }
    }



}

class Server
{
    Socket serv_socket;
    List<Client> clients;

    public Server()
    {
        this.serv_socket = new Socket(SocketType.Stream, ProtocolType.Tcp);
        this.serv_socket.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.ReuseAddress, 1);
        this.serv_socket.Bind(new IPEndPoint(IPAddress.Any, 20000));
        this.serv_socket.Listen(1);
        this.clients = new List<Client>();
        Console.WriteLine("Server started!");
    }

    public void Remove_client(Client client)
    {
        clients.Remove(client);
    }

    public void Send_message(string message)
    {
        foreach (Client client in clients)
        {
            client.Send_message(message);
        }
    }

    public void Run()
    {
        while (true)
        {
            List<Socket> waitting_sockets = new List<Socket> { serv_socket };
            List<Socket> read_sockets = new List<Socket>();
            Socket client_socket;

            foreach (Client client in clients)
            {
                waitting_sockets.Add(client.socket);
            }

            Socket.Select(waitting_sockets, null, null, 5000);

            foreach (Socket socket in waitting_sockets)
            {
                if (socket.Poll(0, SelectMode.SelectRead))
                    read_sockets.Add(socket);
            }

            if (read_sockets.Contains(serv_socket))
            {
                client_socket = serv_socket.Accept();
                Client client = new Client(this, client_socket);
                clients.Add(client);
            }

            List<Client> clientsCopy = new List<Client>(clients); // Create a copy of clients list
            foreach (var client in clientsCopy)
            {
                if (read_sockets.Contains(client.socket))
                {
                    client.Recieved();
                }
            }
        }
    }

}