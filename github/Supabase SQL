-- SDKP / SDVR
CREATE TABLE IF NOT EXISTS audit_log_sdkp (
  id BIGSERIAL PRIMARY KEY,
  framework TEXT NOT NULL,
  version TEXT NOT NULL,
  author TEXT NOT NULL,
  project TEXT NOT NULL,
  first_invocation TIMESTAMPTZ NOT NULL,
  checksum TEXT NOT NULL,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE (framework, version)
);

-- SD&N
CREATE TABLE IF NOT EXISTS audit_log_sdn (
  id BIGSERIAL PRIMARY KEY,
  framework TEXT NOT NULL,
  version TEXT NOT NULL,
  author TEXT NOT NULL,
  project TEXT NOT NULL,
  first_invocation TIMESTAMPTZ NOT NULL,
  checksum TEXT NOT NULL,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE (framework, version)
);

-- QCC0
CREATE TABLE IF NOT EXISTS audit_log_qcc (
  id BIGSERIAL PRIMARY KEY,
  framework TEXT NOT NULL,
  version TEXT NOT NULL,
  author TEXT NOT NULL,
  project TEXT NOT NULL,
  first_invocation TIMESTAMPTZ NOT NULL,
  checksum TEXT NOT NULL,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE (framework, version)
);
