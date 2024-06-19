using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Data.SQLite;
using System.Data.SqlClient;



class Start
{
    static void Main(string[] args)
    {
        Server server = new Server();
        server.Run();
    }
}

class HracInfo
{
    public string? Meno { get; set; }
    public int Skore { get; set; }

}

class Hrac
{
    string meno;
    int skore;
    private readonly string dbFileName = "user_scores.db";
    private readonly string connectionString;
    public Hrac(string meno, int skore)
    {
        this.meno = meno;
        this.skore = skore;
        this.connectionString = $"Data Source={dbFileName}";

        VytvorDb();
        Zapis();
    }

    void Zapis()
    {
        using (var connection = new SQLiteConnection(connectionString))
        {
            connection.Open();
            using (var command = new SQLiteCommand(connection))
            {
                command.CommandText = "SELECT COUNT(*) FROM HracInfo WHERE meno = @meno";
                command.Parameters.AddWithValue("@meno", this.meno);
                long count = (long)command.ExecuteScalar();

                if (count == 0)
                {
                    command.CommandText = "INSERT INTO HracInfo(meno, skore) VALUES(@meno, skore)";
                    command.Parameters.AddWithValue("@meno", meno);
                    command.Parameters.AddWithValue("@skore", skore);
                    command.ExecuteNonQuery();
                }
                else
                {

                }
            }
        }
        Console.WriteLine("Player added");
    }

    void VytvorDb()
    {
        if (!File.Exists(dbFileName))
        {
            SQLiteConnection.CreateFile(dbFileName);
            Console.WriteLine("DB vytvorena");
        }
        using (var connect = new SQLiteConnection(connectionString))
        {
            connect.Open();
            using (var command = new SQLiteCommand(connect))
            {
                command.CommandText = "CREATE TABLE IF NOT EXISTS HracInfo(Id INTEGER PRIMARY KEY AUTOINCREMENT, meno TEXT, skore INT)";
                command.ExecuteNonQuery();
                Console.WriteLine("Tabulka vytvorena");
            }
        }
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
        this.clients = [];
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
            List<Socket> waitting_sockets = [serv_socket];
            List<Socket> read_sockets = [];
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
                Client client = new(this, client_socket);
                clients.Add(client);
            }

            List<Client> clientsCopy = new(clients); // Create a copy of clients list
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