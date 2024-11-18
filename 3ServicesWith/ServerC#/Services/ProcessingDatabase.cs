using System;
using System.IO;
using System.Threading.Tasks;
using Grpc.Core;
using Microsoft.Extensions.Logging;

namespace ProcessingDatabase.Services
{
    public class ProcessingDatabaseService : ProcessingDatabase.ProcessingDatabaseBase
    {
        private readonly ILogger<ProcessingDatabaseService> _logger;

        public ProcessingDatabaseService(ILogger<ProcessingDatabaseService> logger)
        {
            _logger = logger;
        }

        public override async Task<FileExchange.UploadStatus> ImportCSV(
            IAsyncStreamReader<FileExchange.FileData> requestStream,
            ServerCallContext context)
        {
            string tempFilePath = Path.GetTempFileName();
            string? fileName = null;

            try
            {
                using var fileStream = File.Create(tempFilePath);
                int chunkCount = 0;

                while (await requestStream.MoveNext())
                {
                    var chunk = requestStream.Current;

                    fileName ??= chunk.FileName;
                    if (chunk.ChunkData is not null)
                    {
                        await fileStream.WriteAsync(chunk.ChunkData.ToByteArray());
                    }

                    chunkCount++;
                }

                if (string.IsNullOrEmpty(fileName))
                {
                    throw new RpcException(new Status(StatusCode.InvalidArgument, "Filename is missing"));
                }

                // Обработка файла, сохранение в БД или дальнейшая передача
                _logger.LogInformation($"Received {chunkCount} chunks for file {fileName}.");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error during ImportCSV");
                return new FileExchange.UploadStatus
                {
                    Code = FileExchange.UploadStatusCode.Failed,
                    Message = ex.Message
                };
            }
            finally
            {
                if (File.Exists(tempFilePath))
                {
                    File.Delete(tempFilePath);
                }
            }

            return new FileExchange.UploadStatus
            {
                Code = FileExchange.UploadStatusCode.Ok,
                Message = "File uploaded and processed successfully"
            };
        }
    }
}
