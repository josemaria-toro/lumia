using Lumia.Domain;

namespace Lumia.Application;

/// <summary>Use case: list the available streaming content ordered by title.</summary>
public sealed class ListContent
{
    private readonly IContentCatalog _catalog;

    public ListContent(IContentCatalog catalog)
    {
        ArgumentNullException.ThrowIfNull(catalog);
        _catalog = catalog;
    }

    public async Task<IReadOnlyList<ContentItem>> ExecuteAsync(CancellationToken cancellationToken)
    {
        var items = await _catalog.ListAsync(cancellationToken).ConfigureAwait(false);
        return items.OrderBy(i => i.Title, StringComparer.OrdinalIgnoreCase).ToList();
    }
}
