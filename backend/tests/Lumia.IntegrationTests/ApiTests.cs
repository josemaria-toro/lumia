using System.Net;
using Microsoft.AspNetCore.Mvc.Testing;

namespace Lumia.IntegrationTests;

[Trait("Category", "Integration")]
public class ApiTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly WebApplicationFactory<Program> _factory;

    public ApiTests(WebApplicationFactory<Program> factory) => _factory = factory;

    [Fact]
    public async Task Health_ReturnsOk()
    {
        var response = await _factory.CreateClient().GetAsync(new Uri("/api/v1/health", UriKind.Relative));

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }

    [Fact]
    public async Task Content_ReturnsOk()
    {
        var response = await _factory.CreateClient().GetAsync(new Uri("/api/v1/content", UriKind.Relative));

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }
}
