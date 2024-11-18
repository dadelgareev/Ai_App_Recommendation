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
            // Удаление всех .csv файлов в обеих папках UploadedFiles перед запуском сервера
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

            Console.WriteLine("Сервер запущен на порту 50051...");
            await host.RunAsync();
        }


        private static void CleanCsvFilesInUploadedFilesDirectories()
        {
            // Путь к папке UploadedFiles внутри проекта
            string projectUploadedFilesDir = Path.Combine(Directory.GetCurrentDirectory(), "UploadedFiles");

            // Путь к папке UploadedFiles на один уровень выше проекта
            string parentUploadedFilesDir = Path.Combine(Directory.GetParent(Directory.GetCurrentDirectory()).FullName, "UploadedFiles");

            // Метод для очистки CSV-файлов в указанной папке
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
                            Console.WriteLine($"Удален файл: {file}");
                        }
                    }
                    else
                    {
                        Console.WriteLine($"Папка {directoryPath} не найдена. Создание новой папки...");
                        Directory.CreateDirectory(directoryPath);
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Ошибка при удалении .csv файлов из папки {directoryPath}: {ex.Message}");
                }
            }

            // Очистка обеих папок
            CleanDirectory(projectUploadedFilesDir);
            CleanDirectory(parentUploadedFilesDir);
        }
    }
}
