using Lumia.Application;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace Lumia.Infrastructure;

public static class DependencyInjection
{
    public static IServiceCollection AddLumia(this IServiceCollection services, IConfiguration configuration)
    {
        services.Configure<CatalogOptions>(configuration.GetSection(CatalogOptions.SectionName));
        services.AddSingleton<IContentCatalog, InMemoryContentCatalog>();
        services.AddSingleton<ListContent>();
        return services;
    }
}
