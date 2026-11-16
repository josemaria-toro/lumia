using Lumia.Application;

namespace Lumia.Workers;

/// <summary>Background worker that periodically reads the catalog.</summary>
public sealed partial class CatalogRefreshWorker : BackgroundService
{
    private readonly ILogger<CatalogRefreshWorker> _logger;
    private readonly ListContent _listContent;

    public CatalogRefreshWorker(ILogger<CatalogRefreshWorker> logger, ListContent listContent)
    {
        _logger = logger;
        _listContent = listContent;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        using var timer = new PeriodicTimer(TimeSpan.FromMinutes(5));
        do
        {
            var items = await _listContent.ExecuteAsync(stoppingToken).ConfigureAwait(false);
            LogCatalogSize(items.Count);
        }
        while (await timer.WaitForNextTickAsync(stoppingToken).ConfigureAwait(false));
    }

    [LoggerMessage(Level = LogLevel.Information, Message = "Catalog contains {Count} items")]
    private partial void LogCatalogSize(int count);
}
