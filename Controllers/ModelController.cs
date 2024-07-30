using APIProyecto.Modelo;
using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;

namespace APIProyecto.Controllers
{
    [ApiController]
    [Route("Modelo")]
    public class ModelController : ControllerBase
    {


        [HttpGet()]
        public async Task<IActionResult> GetModelo([FromQuery] Entrada entrada)
        {
            // Valida el modelo
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }
            return Ok(new { Message = "Parametros enviados correctamente", entrada });
        }
    }
}
