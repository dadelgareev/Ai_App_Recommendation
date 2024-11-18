using System.IO;
using System.Threading.Tasks;
using Grpc.Core;
using Microsoft.Extensions.Logging;

namespace GrpcFileTransfer
{
    public class FileTransferService : FileTransfer.FileTransferBase
    {
        private readonly ILogger<FileTransferService> _logger;
        public FileTransferService(ILogger<FileTransferService> logger)
        {
            _logger = logger;
        }

        public override async Task<UploadResponse> UploadCSV(UploadRequest request, ServerCallContext context)
        {
            string filePath = Path.Combine("UploadedFiles", request.FileName);

            // ������� �����, ���� � ���
            Directory.CreateDirectory("UploadedFiles");

            // ��������� ���������� ����� ��� CSV ����
            await File.WriteAllBytesAsync(filePath, request.FileContent.ToByteArray());

            _logger.LogInformation($"���� {request.FileName} �������� �� ����: {filePath}");

            return new UploadResponse { Message = $"���� {request.FileName} ������� ��������." };
        }
    }
}
