namespace Lumia.Infrastructure;

/// <summary>Options for <see cref="InMemoryContentCatalog"/> (Options pattern).</summary>
public sealed class CatalogOptions
{
    public const string SectionName = "Catalog";

    public IList<string> Titles { get; } = new List<string>();
}
