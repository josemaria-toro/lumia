namespace Lumia.Domain;

/// <summary>A piece of streaming content available in the catalog.</summary>
public sealed class ContentItem
{
    public ContentItem(Guid id, string title)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(title);
        Id = id;
        Title = title;
    }

    public Guid Id { get; }

    public string Title { get; }
}
