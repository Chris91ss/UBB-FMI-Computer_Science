using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

public class Program
{
    public static void Main(string[] args)
    {
        List<string> urls = new List<string>
        {
            "http://www.google.com/",
            "http://www.microsoft.com/",
            "http://www.amazon.com/",
            "http://www.reddit.com/",
            "http://www.stackoverflow.com/",
        };

        string downloadDirectory = "download";
        Directory.CreateDirectory(downloadDirectory);

        Console.WriteLine("Choose implementation:");
        Console.WriteLine("1. Callbacks");
        Console.WriteLine("2. Tasks with ContinueWith");
        Console.WriteLine("3. Async/Await");
        var choice = Console.ReadLine();

        switch (choice)
        {
            case "1":
                DownloaderCallbacks.Run(urls, downloadDirectory);
                break;
            case "2":
                 DownloaderTasks.Run(urls, downloadDirectory);
                break;
            case "3":
                DownloaderAsyncAwait.Run(urls, downloadDirectory).Wait();
                break;
            default:
                Console.WriteLine("Invalid choice.");
                break;
        }
    }
}

#region Callbacks

public static class DownloaderCallbacks
{
    private static CountdownEvent countdown;

    public static void Run(List<string> urls, string downloadDirectory)
    {
        Console.WriteLine("--- Callback Implementation ---");
        countdown = new CountdownEvent(urls.Count);

        foreach (var url in urls)
        {
            var downloader = new FileDownloader(url, downloadDirectory, () => countdown.Signal());
            downloader.Start();
        }

        countdown.Wait();
        Console.WriteLine($"--- All downloads completed. Files saved to {downloadDirectory}. ---");
    }

    private class FileDownloader
    {
        private readonly Uri url;
        private readonly string host;
        private readonly string path;
        private readonly int port;
        private readonly string filename;
        private readonly string outputPath;
        private readonly Action onCompleted;

        private Socket socket;
        private readonly byte[] buffer = new byte[1024];
        private readonly MemoryStream responseStream = new MemoryStream();
        private bool headersReceived = false;
        private int contentLength = -1;
        private int bodyBytesReceived = 0;
        private FileStream fileStream;

        public FileDownloader(string urlString, string downloadDirectory, Action onCompleted)
        {
            this.url = new Uri(urlString);
            this.host = url.Host;
            this.path = url.AbsolutePath;
            this.port = url.Port == -1 ? 80 : url.Port;
            this.filename = Path.GetFileName(url.AbsolutePath);
            if (string.IsNullOrEmpty(filename))
            {
                this.filename = $"{host.Replace('.', '_')}.html";
            }
            this.outputPath = Path.Combine(downloadDirectory, this.filename);
            this.onCompleted = onCompleted;
        }

        public void Start()
        {
            Dns.BeginGetHostEntry(host, OnHostEntry, null);
        }

        private void OnHostEntry(IAsyncResult ar)
        {
            try
            {
                IPHostEntry hostEntry = Dns.EndGetHostEntry(ar);
                IPAddress ipAddress = hostEntry.AddressList.FirstOrDefault(ip => ip.AddressFamily == AddressFamily.InterNetwork);
                if (ipAddress == null)
                {
                    Console.WriteLine($"Could not resolve IP for {host}");
                    Finish(true);
                    return;
                }

                socket = new Socket(ipAddress.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
                IPEndPoint remoteEP = new IPEndPoint(ipAddress, port);
                socket.BeginConnect(remoteEP, OnConnect, null);
            }
            catch (Exception e)
            {
                Console.WriteLine($"Error on DNS resolution for {host}: {e.Message}");
                Finish(true);
            }
        }

        private void OnConnect(IAsyncResult ar)
        {
            try
            {
                socket.EndConnect(ar);
                Console.WriteLine($"Connected to {host}.");
                string request = $"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: Close\r\n\r\n";
                byte[] requestBytes = Encoding.ASCII.GetBytes(request);
                socket.BeginSend(requestBytes, 0, requestBytes.Length, SocketFlags.None, OnSend, null);
            }
            catch (Exception e)
            {
                Console.WriteLine($"Error connecting to {host}: {e.Message}");
                Finish(true);
            }
        }

        private void OnSend(IAsyncResult ar)
        {
            try
            {
                int bytesSent = socket.EndSend(ar);
                Console.WriteLine($"Sent {bytesSent} bytes to {host}.");
                socket.BeginReceive(buffer, 0, buffer.Length, SocketFlags.None, OnReceive, null);
            }
            catch (Exception e)
            {
                Console.WriteLine($"Error sending to {host}: {e.Message}");
                Finish(true);
            }
        }

        private void OnReceive(IAsyncResult ar)
        {
            try
            {
                int bytesRead = socket.EndReceive(ar);

                if (bytesRead > 0)
                {
                    if (!headersReceived)
                    {
                        responseStream.Write(buffer, 0, bytesRead);
                        ProcessInitialResponse();
                    }
                    else
                    {
                        ProcessBody(buffer, bytesRead);
                    }
                }
                else
                {
                    Finish();
                }
            }
            catch (Exception e)
            {
                Console.WriteLine($"Error receiving from {host}: {e.Message}");
                Finish(true);
            }
        }
        
        private void ProcessInitialResponse()
        {
            byte[] responseBytes = responseStream.ToArray();
            int headerEndIndex = FindHeaderEnd(responseBytes);

            if (headerEndIndex != -1)
            {
                headersReceived = true;
                string headers = Encoding.ASCII.GetString(responseBytes, 0, headerEndIndex);
                ParseHeaders(headers);

                int bodyStartIndex = headerEndIndex + 4;
                int initialBodyLength = responseBytes.Length - bodyStartIndex;

                fileStream = new FileStream(outputPath, FileMode.Create);

                if (initialBodyLength > 0)
                {
                    fileStream.Write(responseBytes, bodyStartIndex, initialBodyLength);
                    bodyBytesReceived += initialBodyLength;
                }

                if (contentLength != -1 && bodyBytesReceived >= contentLength)
                {
                    Finish();
                }
                else
                {
                    socket.BeginReceive(buffer, 0, buffer.Length, SocketFlags.None, OnReceive, null);
                }
            }
            else
            {
                socket.BeginReceive(buffer, 0, buffer.Length, SocketFlags.None, OnReceive, null);
            }
        }
        
        private void ProcessBody(byte[] data, int count)
        {
            fileStream.Write(data, 0, count);
            bodyBytesReceived += count;

            if (contentLength != -1 && bodyBytesReceived >= contentLength)
            {
                Finish();
            }
            else
            {
                socket.BeginReceive(buffer, 0, buffer.Length, SocketFlags.None, OnReceive, null);
            }
        }

        private void ParseHeaders(string headers)
        {
            var lines = headers.Split(new[] { "\r\n" }, StringSplitOptions.None);
            foreach (var line in lines)
            {
                if (line.StartsWith("Content-Length:", StringComparison.OrdinalIgnoreCase))
                {
                    contentLength = int.Parse(line.Substring("Content-Length:".Length).Trim());
                    Console.WriteLine($"Content-Length for {host}: {contentLength}");
                    break;
                }
            }
        }

        private int FindHeaderEnd(byte[] data)
        {
            byte[] sequence = { 13, 10, 13, 10 }; // \r\n\r\n
            for (int i = 0; i <= data.Length - sequence.Length; i++)
            {
                if (data.Skip(i).Take(sequence.Length).SequenceEqual(sequence))
                    return i;
            }
            return -1;
        }

        private void Finish(bool error = false)
        {
            socket?.Close();
            fileStream?.Close();

            if (!error)
            {
                Console.WriteLine($"Finished downloading from {host}. Saved to {outputPath}.");
            }
            else
            {
                Console.WriteLine($"Download from {host} failed.");
                if (File.Exists(outputPath)) File.Delete(outputPath);
            }
            onCompleted();
        }
    }
}
#endregion

#region Tasks
public static class DownloaderTasks
{
    private class DownloadState
    {
        public Uri Url;
        public string Host;
        public string Path;
        public int Port;
        public string Filename;
        public string OutputPath;
        public Socket Socket;
        public readonly byte[] Buffer = new byte[1024];
        public readonly MemoryStream ResponseStream = new MemoryStream();
        public bool HeadersReceived = false;
        public int ContentLength = -1;
        public int BodyBytesReceived = 0;
        public FileStream FileStream;
    }

    public static void Run(List<string> urls, string downloadDirectory)
    {
        Console.WriteLine("--- Tasks with ContinueWith Implementation ---");
        var tasks = new List<Task>();
        foreach(var url in urls)
        {
            tasks.Add(DownloadFile(url, downloadDirectory));
        }
        Task.WhenAll(tasks).Wait();
        Console.WriteLine($"--- All downloads completed. Files saved to {downloadDirectory}. ---");
    }
    
    private static Task DownloadFile(string urlString, string downloadDirectory)
    {
        var state = new DownloadState();
        state.Url = new Uri(urlString);
        state.Host = state.Url.Host;
        state.Path = state.Url.AbsolutePath;
        state.Port = state.Url.Port == -1 ? 80 : state.Url.Port;
        state.Filename = System.IO.Path.GetFileName(state.Url.AbsolutePath);
        if (string.IsNullOrEmpty(state.Filename))
        {
            state.Filename = $"{state.Host.Replace('.', '_')}.html";
        }
        state.OutputPath = Path.Combine(downloadDirectory, state.Filename);
        
        return TaskExtensions.GetHostEntryAsync(state.Host)
            .ContinueWith(t => OnHostEntry(t, state))
            .Unwrap()
            .ContinueWith(t => OnConnect(t, state))
            .Unwrap()
            .ContinueWith((Task<int> t) => OnSend(t, state))
            .Unwrap()
            .ContinueWith(t => OnReceive(t, state))
            .Unwrap();
    }

    private static Task OnHostEntry(Task<IPHostEntry> task, DownloadState state)
    {
        if (task.IsFaulted)
        {
            Console.WriteLine($"Error on DNS resolution for {state.Host}: {task.Exception.InnerException.Message}");
            return Task.CompletedTask;
        }

        IPHostEntry hostEntry = task.Result;
        IPAddress ipAddress = hostEntry.AddressList.FirstOrDefault(ip => ip.AddressFamily == AddressFamily.InterNetwork);
        if (ipAddress == null)
        {
            Console.WriteLine($"Could not resolve IP for {state.Host}");
            return Task.CompletedTask;
        }

        state.Socket = new Socket(ipAddress.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
        IPEndPoint remoteEP = new IPEndPoint(ipAddress, state.Port);
        return state.Socket.ConnectAsync(remoteEP);
    }
    
    private static Task<int> OnConnect(Task task, DownloadState state)
    {
        if (task.IsFaulted)
        {
            Console.WriteLine($"Error connecting to {state.Host}: {task.Exception.InnerException.Message}");
            return Task.FromException<int>(task.Exception);
        }
        Console.WriteLine($"Connected to {state.Host}.");
        string request = $"GET {state.Path} HTTP/1.1\r\nHost: {state.Host}\r\nConnection: Close\r\n\r\n";
        byte[] requestBytes = Encoding.ASCII.GetBytes(request);
        return state.Socket.SendAsync(requestBytes, 0, requestBytes.Length, SocketFlags.None);
    }
    
    private static Task OnSend(Task<int> task, DownloadState state)
    {
        if (task.IsFaulted)
        {
            Console.WriteLine($"Error sending to {state.Host}: {task.Exception.InnerException.Message}");
            return Task.CompletedTask;
        }
        Console.WriteLine($"Sent {task.Result} bytes to {state.Host}.");
        return ReceiveLoop(state);
    }
    
    private static Task OnReceive(Task task, DownloadState state)
    {
        state.Socket?.Close();
        state.FileStream?.Close();

        if (task.IsFaulted)
        {
            Console.WriteLine($"Download from {state.Host} failed: {task.Exception.InnerException.Message}");
            if (File.Exists(state.OutputPath)) File.Delete(state.OutputPath);
        }
        else
        {
            Console.WriteLine($"Finished downloading from {state.Host}. Saved to {state.OutputPath}.");
        }
        return Task.CompletedTask;
    }
    
    private static Task ReceiveLoop(DownloadState state)
    {
        return state.Socket.ReceiveAsync(state.Buffer, 0, state.Buffer.Length, SocketFlags.None)
            .ContinueWith(t =>
            {
                if (t.IsFaulted) return Task.FromException(t.Exception);
                
                int bytesRead = t.Result;
                if (bytesRead > 0)
                {
                    if (!state.HeadersReceived)
                    {
                        state.ResponseStream.Write(state.Buffer, 0, bytesRead);
                        return ProcessInitialResponse(state).ContinueWith(t2 => t2.Result ? ReceiveLoop(state) : Task.CompletedTask).Unwrap();
                    }
                    else
                    {
                        return ProcessBody(state, state.Buffer, bytesRead).ContinueWith(t2 => t2.Result ? ReceiveLoop(state) : Task.CompletedTask).Unwrap();
                    }
                }
                return Task.CompletedTask; // End of stream
            }).Unwrap();
    }

    private static Task<bool> ProcessInitialResponse(DownloadState state)
    {
        byte[] responseBytes = state.ResponseStream.ToArray();
        int headerEndIndex = FindHeaderEnd(responseBytes);
        if (headerEndIndex == -1) return Task.FromResult(true); // Continue receiving

        state.HeadersReceived = true;
        string headers = Encoding.ASCII.GetString(responseBytes, 0, headerEndIndex);
        ParseHeaders(state, headers);

        int bodyStartIndex = headerEndIndex + 4;
        int initialBodyLength = responseBytes.Length - bodyStartIndex;

        state.FileStream = new FileStream(state.OutputPath, FileMode.Create);

        if (initialBodyLength > 0)
        {
            state.FileStream.Write(responseBytes, bodyStartIndex, initialBodyLength);
            state.BodyBytesReceived += initialBodyLength;
        }

        return Task.FromResult(state.ContentLength == -1 || state.BodyBytesReceived < state.ContentLength);
    }

    private static Task<bool> ProcessBody(DownloadState state, byte[] data, int count)
    {
        state.FileStream.Write(data, 0, count);
        state.BodyBytesReceived += count;
        return Task.FromResult(state.ContentLength == -1 || state.BodyBytesReceived < state.ContentLength);
    }
    
    private static void ParseHeaders(DownloadState state, string headers)
    {
        var lines = headers.Split(new[] { "\r\n" }, StringSplitOptions.None);
        foreach (var line in lines)
        {
            if (line.StartsWith("Content-Length:", StringComparison.OrdinalIgnoreCase))
            {
                state.ContentLength = int.Parse(line.Substring("Content-Length:".Length).Trim());
                Console.WriteLine($"Content-Length for {state.Host}: {state.ContentLength}");
                break;
            }
        }
    }

    private static int FindHeaderEnd(byte[] data)
    {
        byte[] sequence = { 13, 10, 13, 10 }; // \r\n\r\n
        for (int i = 0; i <= data.Length - sequence.Length; i++)
        {
            if (data.Skip(i).Take(sequence.Length).SequenceEqual(sequence))
                return i;
        }
        return -1;
    }
}

public static class TaskExtensions
{
    public static Task<IPHostEntry> GetHostEntryAsync(string host)
    {
        var tcs = new TaskCompletionSource<IPHostEntry>();
        Dns.BeginGetHostEntry(host, ar => {
            try { tcs.SetResult(Dns.EndGetHostEntry(ar)); }
            catch (Exception e) { tcs.SetException(e); }
        }, null);
        return tcs.Task;
    }

    public static Task ConnectAsync(this Socket socket, EndPoint remoteEP)
    {
        var tcs = new TaskCompletionSource<bool>();
        socket.BeginConnect(remoteEP, ar => {
            try { socket.EndConnect(ar); tcs.SetResult(true); }
            catch (Exception e) { tcs.SetException(e); }
        }, socket);
        return tcs.Task;
    }

    public static Task<int> SendAsync(this Socket socket, byte[] buffer, int offset, int size, SocketFlags socketFlags)
    {
        var tcs = new TaskCompletionSource<int>();
        socket.BeginSend(buffer, offset, size, socketFlags, ar => {
            try { tcs.SetResult(socket.EndSend(ar)); }
            catch (Exception e) { tcs.SetException(e); }
        }, socket);
        return tcs.Task;
    }

    public static Task<int> ReceiveAsync(this Socket socket, byte[] buffer, int offset, int size, SocketFlags socketFlags)
    {
        var tcs = new TaskCompletionSource<int>();
        socket.BeginReceive(buffer, offset, size, socketFlags, ar => {
            try { tcs.SetResult(socket.EndReceive(ar)); }
            catch (Exception e) { tcs.SetException(e); }
        }, socket);
        return tcs.Task;
    }
}
#endregion

#region AsyncAwait
public static class DownloaderAsyncAwait
{
    public static async Task Run(List<string> urls, string downloadDirectory)
    {
        Console.WriteLine("--- Async/Await Implementation ---");
        var tasks = new List<Task>();
        foreach(var url in urls)
        {
            tasks.Add(DownloadFile(url, downloadDirectory));
        }
        await Task.WhenAll(tasks);
        Console.WriteLine($"--- All downloads completed. Files saved to {downloadDirectory}. ---");
    }

    private static async Task DownloadFile(string urlString, string downloadDirectory)
    {
        var url = new Uri(urlString);
        var host = url.Host;
        var path = url.AbsolutePath;
        var port = url.Port == -1 ? 80 : url.Port;
        var filename = System.IO.Path.GetFileName(url.AbsolutePath);
        if (string.IsNullOrEmpty(filename))
        {
            filename = $"{host.Replace('.', '_')}.html";
        }
        var outputPath = Path.Combine(downloadDirectory, filename);

        Socket socket = null;
        FileStream fileStream = null;

        try
        {
            IPHostEntry hostEntry = await TaskExtensions.GetHostEntryAsync(host);
            IPAddress ipAddress = hostEntry.AddressList.FirstOrDefault(ip => ip.AddressFamily == AddressFamily.InterNetwork);
            if (ipAddress == null)
            {
                Console.WriteLine($"Could not resolve IP for {host}");
                return;
            }

            socket = new Socket(ipAddress.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
            IPEndPoint remoteEP = new IPEndPoint(ipAddress, port);
            await socket.ConnectAsync(remoteEP);
            Console.WriteLine($"Connected to {host}.");

            string request = $"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: Close\r\n\r\n";
            byte[] requestBytes = Encoding.ASCII.GetBytes(request);
            int bytesSent = await socket.SendAsync(requestBytes, 0, requestBytes.Length, SocketFlags.None);
            Console.WriteLine($"Sent {bytesSent} bytes to {host}.");

            var buffer = new byte[1024];
            
            var responseStream = new MemoryStream();
            int headerEndIndex = -1;
            byte[] responseBytes = null;
            
            while (true)
            {
                int bytesRead = await socket.ReceiveAsync(buffer, 0, buffer.Length, SocketFlags.None);
                if (bytesRead == 0) break;

                responseStream.Write(buffer, 0, bytesRead);
                responseBytes = responseStream.ToArray();
                headerEndIndex = FindHeaderEnd(responseBytes);
                if (headerEndIndex != -1) break;
            }

            if (headerEndIndex == -1)
            {
                Console.WriteLine($"Could not find headers for {host}");
                return;
            }

            string headers = Encoding.ASCII.GetString(responseBytes, 0, headerEndIndex);
            int contentLength = ParseHeaders(headers, host);

            int bodyStartIndex = headerEndIndex + 4;
            int initialBodyLength = responseBytes.Length - bodyStartIndex;

            fileStream = new FileStream(outputPath, FileMode.Create);
            int bodyBytesReceived = 0;

            if (initialBodyLength > 0)
            {
                fileStream.Write(responseBytes, bodyStartIndex, initialBodyLength);
                bodyBytesReceived += initialBodyLength;
            }

            while (contentLength == -1 || bodyBytesReceived < contentLength)
            {
                int bytesRead = await socket.ReceiveAsync(buffer, 0, buffer.Length, SocketFlags.None);
                if (bytesRead == 0) break;

                fileStream.Write(buffer, 0, bytesRead);
                bodyBytesReceived += bytesRead;
            }

            Console.WriteLine($"Finished downloading from {host}. Saved to {outputPath}.");
        }
        catch (Exception e)
        {
            Console.WriteLine($"Download from {host} failed: {e.Message}");
            if (File.Exists(outputPath)) File.Delete(outputPath);
        }
        finally
        {
            socket?.Close();
            fileStream?.Close();
        }
    }

    private static int ParseHeaders(string headers, string host)
    {
        int contentLength = -1;
        var lines = headers.Split(new[] { "\r\n" }, StringSplitOptions.None);
        foreach (var line in lines)
        {
            if (line.StartsWith("Content-Length:", StringComparison.OrdinalIgnoreCase))
            {
                contentLength = int.Parse(line.Substring("Content-Length:".Length).Trim());
                Console.WriteLine($"Content-Length for {host}: {contentLength}");
                break;
            }
        }
        return contentLength;
    }

    private static int FindHeaderEnd(byte[] data)
    {
        byte[] sequence = { 13, 10, 13, 10 }; // \r\n\r\n
        for (int i = 0; i <= data.Length - sequence.Length; i++)
        {
            if (data.Skip(i).Take(sequence.Length).SequenceEqual(sequence))
                return i;
        }
        return -1;
    }
}
#endregion
