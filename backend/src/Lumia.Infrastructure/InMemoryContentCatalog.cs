using Lumia.Application;
using Lumia.Domain;
using Microsoft.Extensions.Options;

namespace Lumia.Infrastructure;

/// <summary>Outbound adapter that serves a catalog configured through <see cref="CatalogOptions"/>.</summary>
public sealed class InMemoryContentCatalog : IContentCatalog
{
    private readonly CatalogOptions _options;

    public InMemoryContentCatalog(IOptions<CatalogOptions> options)
    {
        ArgumentNullException.ThrowIfNull(options);
        _options = options.Value;
    }

    public Task<IReadOnlyList<ContentItem>> ListAsync(CancellationToken cancellationToken)
    {
        IReadOnlyList<ContentItem> items = _options.Titles
            .Select(t => new ContentItem(Guid.NewGuid(), t))
            .ToList();
        return Task.FromResult(items);
    }
}
