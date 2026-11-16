using Lumia.Application;
using Lumia.Domain;
using Lumia.Infrastructure;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace Lumia.UnitTests;

public class DependencyInjectionTests
{
    [Fact]
    public async Task AddLumia_BindsCatalogOptionsAndResolvesUseCase()
    {
        var configuration = new ConfigurationBuilder()
            .AddInMemoryCollection(new Dictionary<string, string?> { ["Catalog:Titles:0"] = "Movie" })
            .Build();
        using var provider = new ServiceCollection().AddLumia(configuration).BuildServiceProvider();

        var result = await provider.GetRequiredService<ListContent>().ExecuteAsync(CancellationToken.None);

        Assert.Equal("Movie", Assert.Single(result).Title);
    }

    [Fact]
    public void ContentItem_ExposesIdAndTitle()
    {
        var id = Guid.NewGuid();

        var item = new ContentItem(id, "Movie");

        Assert.Equal(id, item.Id);
        Assert.Equal("Movie", item.Title);
    }
}
