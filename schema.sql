-- =========================================================
-- TECHFIX INFORMÁTICA
-- Etapa 1 - Banco de dados
-- =========================================================

-- Tabela de clientes
CREATE TABLE clientes (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    celular VARCHAR(20) NOT NULL,

    CONSTRAINT clientes_email_valido
        CHECK (
            email ~* '^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$'
        ),

    CONSTRAINT clientes_celular_valido
        CHECK (
            celular ~ '^\+?[0-9]{10,15}$'
        )
);

-- Tabela de ordens de serviço
CREATE TABLE ordens_servico (
    id BIGSERIAL PRIMARY KEY,
    cliente_id BIGINT NOT NULL,
    descricao TEXT NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'Aberto',
    data_abertura TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT ordens_servico_cliente_fk
        FOREIGN KEY (cliente_id)
        REFERENCES clientes(id)
        ON DELETE RESTRICT,

    CONSTRAINT ordens_servico_status_valido
        CHECK (
            status IN (
                'Aberto',
                'Em análise',
                'Aguardando peça',
                'Concluído',
                'Entregue'
            )
        )
);

-- Índices para facilitar as consultas
CREATE INDEX idx_ordens_servico_status
    ON ordens_servico(status);

CREATE INDEX idx_ordens_servico_cliente
    ON ordens_servico(cliente_id);
