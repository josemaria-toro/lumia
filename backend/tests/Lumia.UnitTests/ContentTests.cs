using Lumia.Application;
using Lumia.Domain;
using Lumia.Infrastructure;
using Microsoft.Extensions.Options;
using Moq;

namespace Lumia.UnitTests;

public class ContentTests
{
    [Fact]
    public void ContentItem_RejectsBlankTitle()
    {
        Assert.Throws<ArgumentException>(() => new ContentItem(Guid.NewGuid(), " "));
    }

    [Fact]
    public async Task ListContent_OrdersByTitle()
    {
        var catalog = new Mock<IContentCatalog>();
        catalog.Setup(c => c.ListAsync(It.IsAny<CancellationToken>()))
            .ReturnsAsync(new[] { new ContentItem(Guid.NewGuid(), "b"), new ContentItem(Guid.NewGuid(), "A") });

        var result = await new ListContent(catalog.Object).ExecuteAsync(CancellationToken.None);

        Assert.Equal(new[] { "A", "b" }, result.Select(i => i.Title));
    }

    [Fact]
    public void ListContent_RequiresCatalog()
    {
        Assert.Throws<ArgumentNullException>(() => new ListContent(null!));
    }

    [Fact]
    public async Task InMemoryCatalog_ReturnsConfiguredTitles()
    {
        var options = new CatalogOptions();
        options.Titles.Add("Movie");

        var result = await new InMemoryContentCatalog(Options.Create(options)).ListAsync(CancellationToken.None);

        Assert.Single(result);
        Assert.Equal("Movie", result[0].Title);
    }

    [Fact]
    public void InMemoryCatalog_RequiresOptions()
    {
        Assert.Throws<ArgumentNullException>(() => new InMemoryContentCatalog(null!));
    }
}
