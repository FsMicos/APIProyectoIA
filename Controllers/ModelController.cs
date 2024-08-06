using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;

namespace APIProyecto.Controllers
{
    [ApiController]
    [Route("Modelo")]
    public class ModelController : ControllerBase
    {


        [HttpGet()]
        public async Task<IActionResult> GetModelo(int Hora, string Circuito, string Tipo, string DiaSemana, int Mes)
        {
            Circuito = Circuito.ToUpper();
            // Valida el modelo
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }
            // Construimos el string de argumentos
            string args = $"{Hora} \"{Circuito}\" \"{Tipo}\" {DiaSemana} {Mes}";
            string pythonPath = "python";
            string scriptPath = "./Resources/modelo.py";
            var start = new ProcessStartInfo
            {
                FileName = pythonPath,
                Arguments = $"{scriptPath} {args}",
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true
            };

            string result;
            using (var process = Process.Start(start))
            {
                result = await process.StandardOutput.ReadToEndAsync();
                string error = await process.StandardError.ReadToEndAsync();
                if (!string.IsNullOrEmpty(error))
                {
                    return StatusCode(500, error);
                }
            }
            return Ok(new { Result = result });
        }
    }
}
