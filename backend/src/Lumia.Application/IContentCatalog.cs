using Lumia.Domain;

namespace Lumia.Application;

/// <summary>Outbound port: source of the streaming content catalog.</summary>
public interface IContentCatalog
{
    Task<IReadOnlyList<ContentItem>> ListAsync(CancellationToken cancellationToken);
}
