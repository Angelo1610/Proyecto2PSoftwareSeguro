package ec.edu.espe.ms_clientes.servicios.impl;

import ec.edu.espe.ms_clientes.dto.mapper.PersonaMapper;
import ec.edu.espe.ms_clientes.dto.request.PersonaJuridicaRequestDto;
import ec.edu.espe.ms_clientes.dto.request.PersonaNaturalRequestDto;
import ec.edu.espe.ms_clientes.dto.response.PersonaResponseDto;
import ec.edu.espe.ms_clientes.models.Persona;
import ec.edu.espe.ms_clientes.models.PersonaNatural;
import ec.edu.espe.ms_clientes.repostiorios.PersonaRepositorio;
import ec.edu.espe.ms_clientes.servicios.PersonaServicio;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

@Transactional
@Service
@Slf4j //log.info - log.error - log.debug
@RequiredArgsConstructor
public class PersonaServicioImpl implements PersonaServicio {

    private final PersonaRepositorio personaRepositorio;
    private final PersonaMapper personaMapper;

    @Override
    @Transactional
    public PersonaResponseDto crearPersonaNatural(PersonaNaturalRequestDto dto) {

        if (personaRepositorio.existsByIdentificacion(dto.getIdentificacion())) {
            log.error("Ya existe una persona con esa identificacion: " + dto.getIdentificacion());
            throw new RuntimeException("Ya existe una persona con esa identificación");
        }

        if (personaRepositorio.existsByEmail(dto.getEmail())) {
            throw new RuntimeException("Ya existe una persona con esa email");
        }

        if (personaRepositorio.existsByTelefono(dto.getTelefono())) {
            throw new RuntimeException("Ya existe una persona con esa telefono");
        }

        PersonaNatural pn = PersonaMapper.toEntity(dto);

        if (!pn.validarIdentificacion()) {
            throw new RuntimeException("La identificacion no es valida");
        }

        Persona p = personaRepositorio.save(pn);

        log.info("Persona creada satisfactoriamente con id = " + p.getId());
        return personaMapper.toDto(p);
    }

    @Override
    public PersonaResponseDto crearPersonaJuridica(PersonaJuridicaRequestDto dto) {
        //completar registro de personaJuridica
        return null;
    }

    @Override
    @Transactional(readOnly = true)
    public List<PersonaResponseDto> findAllPersona() {
        personaRepositorio.findAll()
                .stream()
                .map(personaMapper::toDto)
                .collect(Collectors.toList());
        return List.of();
    }

    @Override
    public void eliminarPersona(UUID id) {
        //completar
    }

    @Override
    public PersonaResponseDto actualizarPersonaNatural(UUID id, PersonaNaturalRequestDto dto) {
        //completar
        return null;
    }

    @Override
    public PersonaResponseDto actualizarPersonaJuridica(UUID id, PersonaJuridicaRequestDto dto) {
        //completar
        return null;
    }

    @Override
    @Transactional(readOnly = true)
    public List<PersonaResponseDto> ListarPersonasNaturales() {


    }

    @Override
    public List<PersonaResponseDto> listarPersonasNaturales() {

        return personaRepositorio.findPersonasNaturalesActivas()
                .stream()
                .map(personaMapper::toDto)
                .collect(Collectors.toList());
    }


}
