package ec.edu.espe.ms_clientes.controladores;

import ec.edu.espe.ms_clientes.dto.request.PersonaJuridicaRequestDto;
import ec.edu.espe.ms_clientes.dto.request.PersonaNaturalRequestDto;
import ec.edu.espe.ms_clientes.dto.response.PersonaResponseDto;
import ec.edu.espe.ms_clientes.servicios.PersonaServicio;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/v1/personas")
@Validated
@RequiredArgsConstructor
@Slf4j
public class PersonaController {

    private final PersonaServicio personaServicio;

    @PostMapping("/natural")
    public ResponseEntity<PersonaResponseDto> crearPersonaNatural(
            @Valid @RequestBody PersonaNaturalRequestDto dto) {
        log.info("Solicitud para crear persona natural: {}", dto.getIdentificacion());
        PersonaResponseDto response = personaServicio.crearPersonaNatural(dto);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @PutMapping("/natural/{id}")
    public ResponseEntity<PersonaResponseDto> actualizarPersonaNatural(
            @PathVariable UUID id,
            @Valid @RequestBody PersonaNaturalRequestDto dto) {
        log.info("Solicitud para actualizar persona natural: {}", id);
        PersonaResponseDto response = personaServicio.actualizarPersonaNatural(id, dto);
        return ResponseEntity.ok(response);
    }

    @PostMapping("/juridica")
    public ResponseEntity<PersonaResponseDto> crearPersonaJuridica(
            @Valid @RequestBody PersonaJuridicaRequestDto dto) {
        log.info("Solicitud para crear persona jurídica: {}", dto.getIdentificacion());
        PersonaResponseDto response = personaServicio.crearPersonaJuridica(dto);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @PutMapping("/juridica/{id}")
    public ResponseEntity<PersonaResponseDto> actualizarPersonaJuridica(
            @PathVariable UUID id,
            @Valid @RequestBody PersonaJuridicaRequestDto dto) {
        log.info("Solicitud para actualizar persona jurídica: {}", id);
        PersonaResponseDto response = personaServicio.actualizarPersonaJuridica(id, dto);
        return ResponseEntity.ok(response);
    }

    @GetMapping
    public ResponseEntity<List<PersonaResponseDto>> listarTodasPersonas() {
        log.info("Solicitud para listar todas las personas activas");
        List<PersonaResponseDto> response = personaServicio.findAllPersona();
        return ResponseEntity.ok(response);
    }

    @GetMapping("/natural/activas")
    public ResponseEntity<List<PersonaResponseDto>> listarPersonasNaturalesActivas() {
        log.info("Solicitud para listar personas naturales activas");
        List<PersonaResponseDto> response = personaServicio.listarPersonasNaturales();
        return ResponseEntity.ok(response);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> eliminarPersona(@PathVariable UUID id) {
        log.info("Solicitud para eliminar (desactivar) persona: {}", id);
        personaServicio.eliminarPersona(id);
        return ResponseEntity.noContent().build();
    }
}