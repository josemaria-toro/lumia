using Lumia.Infrastructure;
using Lumia.Workers;

var builder = Host.CreateApplicationBuilder(args);
builder.Services.AddLumia(builder.Configuration);
builder.Services.AddHostedService<CatalogRefreshWorker>();

await builder.Build().RunAsync();
