using Lumia.Application;
using Lumia.Infrastructure;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddLumia(builder.Configuration);

var app = builder.Build();

app.MapGet("/api/v1/health", () => Results.Ok(new { status = "ok" }));
app.MapGet("/api/v1/content", async (ListContent useCase, CancellationToken ct) =>
    Results.Ok((await useCase.ExecuteAsync(ct)).Select(i => new { i.Id, i.Title })));

app.Run();

public partial class Program;
