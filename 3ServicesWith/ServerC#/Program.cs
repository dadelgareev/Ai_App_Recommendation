using System;
using System.IO;
using System.Threading.Tasks;
using Grpc.Core;
using Microsoft.AspNetCore.Server.Kestrel.Core;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using ProcessingDatabase.Services;

namespace GrpcFileTransfer
{
    public class Program
    {
        public static async Task Main(string[] args)
        {
            // �������� ���� .csv ������ � ����� ������ UploadedFiles ����� �������� �������
            CleanCsvFilesInUploadedFilesDirectories();

            var host = Host.CreateDefaultBuilder(args)
                .ConfigureLogging(logging =>
                {
                    logging.ClearProviders();
                    logging.AddConsole();
                })
                .ConfigureServices(services =>
                {
                    services.AddGrpc();
                })
                .ConfigureWebHostDefaults(webBuilder =>
                {
                    webBuilder.ConfigureKestrel(options =>
                    {
                        options.ListenAnyIP(50051, listenOptions =>
                        {
                            listenOptions.Protocols = HttpProtocols.Http2;
                        });
                    });
                    webBuilder.Configure(app =>
                    {
                        app.UseRouting();
                        app.UseEndpoints(endpoints =>
                        {
                            endpoints.MapGrpcService<ProcessingDatabaseService>();
                        });
                    });
                })
                .Build();

            Console.WriteLine("������ ������� �� ����� 50051...");
            await host.RunAsync();
        }


        private static void CleanCsvFilesInUploadedFilesDirectories()
        {
            // ���� � ����� UploadedFiles ������ �������
            string projectUploadedFilesDir = Path.Combine(Directory.GetCurrentDirectory(), "UploadedFiles");

            // ���� � ����� UploadedFiles �� ���� ������� ���� �������
            string parentUploadedFilesDir = Path.Combine(Directory.GetParent(Directory.GetCurrentDirectory()).FullName, "UploadedFiles");

            // ����� ��� ������� CSV-������ � ��������� �����
            void CleanDirectory(string directoryPath)
            {
                try
                {
                    if (Directory.Exists(directoryPath))
                    {
                        string[] csvFiles = Directory.GetFiles(directoryPath, "*.csv");
                        foreach (var file in csvFiles)
                        {
                            File.Delete(file);
                            Console.WriteLine($"������ ����: {file}");
                        }
                    }
                    else
                    {
                        Console.WriteLine($"����� {directoryPath} �� �������. �������� ����� �����...");
                        Directory.CreateDirectory(directoryPath);
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"������ ��� �������� .csv ������ �� ����� {directoryPath}: {ex.Message}");
                }
            }

            // ������� ����� �����
            CleanDirectory(projectUploadedFilesDir);
            CleanDirectory(parentUploadedFilesDir);
        }
    }
}
