package ec.edu.espe.ms_clientes.servicios.impl;

import ec.edu.espe.ms_clientes.dto.mapper.PersonaMapper;
import ec.edu.espe.ms_clientes.dto.request.PersonaJuridicaRequestDto;
import ec.edu.espe.ms_clientes.dto.request.PersonaNaturalRequestDto;
import ec.edu.espe.ms_clientes.dto.response.PersonaResponseDto;
import ec.edu.espe.ms_clientes.models.Persona;
import ec.edu.espe.ms_clientes.models.PersonaJuridica;
import ec.edu.espe.ms_clientes.models.PersonaNatural;
import ec.edu.espe.ms_clientes.repostiorios.PersonaRepositorio;
import ec.edu.espe.ms_clientes.servicios.PersonaServicio;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

@Transactional
@Service
@Slf4j
@RequiredArgsConstructor
public class PersonaServicioImpl implements PersonaServicio {

    private final PersonaRepositorio personaRepositorio;
    private final PersonaMapper personaMapper;

    @Override
    public PersonaResponseDto crearPersonaNatural(PersonaNaturalRequestDto dto) {
        validarUnicidad(dto.getIdentificacion(), dto.getEmail(), dto.getTelefono());

        PersonaNatural pn = PersonaMapper.toEntity(dto);
        if (!pn.validarIdentificacion()) {
            throw new RuntimeException("La cédula ingresada no es válida");
        }

        Persona guardada = personaRepositorio.save(pn);
        log.info("Persona natural creada exitosamente: {} - {}", pn.getIdentificacion(), pn.getNombre() + " " + pn.getApellido());
        return personaMapper.toDto(guardada);
    }

    @Override
    public PersonaResponseDto crearPersonaJuridica(PersonaJuridicaRequestDto dto) {
        validarUnicidad(dto.getIdentificacion(), dto.getEmail(), dto.getTelefono());

        PersonaJuridica pj = personaMapper.toEntity(dto);
        if (!pj.validarIdentificacion()) {
            throw new RuntimeException("El RUC ingresado no es válido");
        }

        Persona guardada = personaRepositorio.save(pj);
        log.info("Persona jurídica creada exitosamente: {} - {}", pj.getIdentificacion(), pj.getRazonSocial());
        return personaMapper.toDto(guardada);
    }

    @Override
    @Transactional(readOnly = true)
    public List<PersonaResponseDto> findAllPersona() {
        return personaRepositorio.findAll().stream()
                .filter(Persona::getActivo)
                .map(personaMapper::toDto)
                .collect(Collectors.toList());
    }

    @Override
    public void eliminarPersona(UUID id) {
        Persona persona = personaRepositorio.findById(id)
                .orElseThrow(() -> new RuntimeException("Persona no encontrada con id: " + id));

        persona.setActivo(false);
        personaRepositorio.save(persona);
        log.info("Persona eliminada lógicamente (desactivada): {}", id);
    }

    @Override
    public PersonaResponseDto actualizarPersonaNatural(UUID id, PersonaNaturalRequestDto dto) {
        PersonaNatural existente = (PersonaNatural) personaRepositorio.findById(id)
                .orElseThrow(() -> new RuntimeException("Persona natural no encontrada"));

        // Validar que no se dupliquen email/teléfono con otra persona
        validarUnicidadAlActualizar(id, dto.getEmail(), dto.getTelefono());

        if (!dto.getIdentificacion().equals(existente.getIdentificacion())) {
            throw new RuntimeException("No se permite cambiar la identificación");
        }

        if (!existente.validarIdentificacion()) {
            throw new RuntimeException("La cédula ingresada no es válida");
        }

        // Actualizar campos
        existente.setNombre(dto.getNombre());
        existente.setEmail(dto.getEmail());
        existente.setTelefono(dto.getTelefono());
        existente.setDireccion(dto.getDireccion());
        existente.setApellido(dto.getApellido());
        existente.setFechaNacimiento(dto.getFechaNacimiento());
        existente.setGenero(dto.getGenero());

        Persona actualizada = personaRepositorio.save(existente);
        log.info("Persona natural actualizada: {}", id);
        return personaMapper.toDto(actualizada);
    }

    @Override
    public PersonaResponseDto actualizarPersonaJuridica(UUID id, PersonaJuridicaRequestDto dto) {
        PersonaJuridica existente = (PersonaJuridica) personaRepositorio.findById(id)
                .orElseThrow(() -> new RuntimeException("Persona jurídica no encontrada"));

        validarUnicidadAlActualizar(id, dto.getEmail(), dto.getTelefono());

        if (!dto.getIdentificacion().equals(existente.getIdentificacion())) {
            throw new RuntimeException("No se permite cambiar el RUC");
        }

        if (!existente.validarIdentificacion()) {
            throw new RuntimeException("El RUC ingresado no es válido");
        }

        existente.setNombre(dto.getNombre());
        existente.setEmail(dto.getEmail());
        existente.setTelefono(dto.getTelefono());
        existente.setDireccion(dto.getDireccion());
        existente.setRazonSocial(dto.getRazonSocial());
        existente.setRepresentanteLegal(dto.getRepresentanteLegal());
        existente.setDireccionLegal(dto.getDireccionLegal());

        Persona actualizada = personaRepositorio.save(existente);
        log.info("Persona jurídica actualizada: {}", id);
        return personaMapper.toDto(actualizada);
    }

    @Override
    @Transactional(readOnly = true)
    public List<PersonaResponseDto> listarPersonasNaturales() {
        return personaRepositorio.findPersonaNaturalActivas().stream()
                .map(personaMapper::toDto)
                .collect(Collectors.toList());
    }

    private void validarUnicidad(String identificacion, String email, String telefono) {
        if (personaRepositorio.existsByIdentificacion(identificacion)) {
            throw new RuntimeException("Ya existe una persona con la identificación: " + identificacion);
        }
        if (personaRepositorio.existsByEmail(email)) {
            throw new RuntimeException("El email ya está registrado: " + email);
        }
        if (personaRepositorio.existsByTelefono(telefono)) {
            throw new RuntimeException("El teléfono ya está registrado: " + telefono);
        }
    }

    private void validarUnicidadAlActualizar(UUID id, String email, String telefono) {
        Optional<Persona> porEmail = personaRepositorio.findByEmail(email);
        if (porEmail.isPresent() && !porEmail.get().getId().equals(id)) {
            throw new RuntimeException("El email ya está en uso por otra persona");
        }

        Optional<Persona> porTelefono = personaRepositorio.findByTelefono(telefono);
        if (porTelefono.isPresent() && !porTelefono.get().getId().equals(id)) {
            throw new RuntimeException("El teléfono ya está en uso por otra persona");
        }
    }
}